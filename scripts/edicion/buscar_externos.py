#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herramienta de consulta quirúrgica sobre la bibliografía externa indexada (`externos/`).

Auto-sincroniza el índice SQLite FTS5 (`dist/indice_externos/corpus.db`) de forma transparente
si detecta archivos nuevos o modificados en `externos/`, evitando que el usuario tenga que
ejecutar scripts manualmente.

Modos de uso (invocados por el agente bajo demanda):
  # Listar todas las fuentes indexadas y su estado editorial:
  python3 -B scripts/edicion/buscar_externos.py --listar

  # Ver metadatos e índice (TOC) de una fuente:
  python3 -B scripts/edicion/buscar_externos.py --info <slug>

  # Buscar términos o frases exactas con página literal (ranking BM25):
  python3 -B scripts/edicion/buscar_externos.py "capitalismo vigilancia" --limite 10
  python3 -B scripts/edicion/buscar_externos.py '"gran Otro"' --fuente <slug>

  # Leer un rango exacto de páginas o secciones para verificar una cita literal:
  python3 -B scripts/edicion/buscar_externos.py --leer <slug> --paginas 1-5

  # Listar fuentes asignadas a un capítulo del libro según notas/fuentes/catalogo.yaml:
  python3 -B scripts/edicion/buscar_externos.py --para-capitulo 19
"""

import argparse
import json
from pathlib import Path
import re
import sqlite3
import sys
from typing import Dict, List, Optional, Set

sys.path.insert(0, str(Path(__file__).resolve().parent))
from indexar_externos import (  # noqa: E402
    CATALOGO_PATH,
    CORPUS_DB_PATH,
    cargar_catalogo,
    necesita_sincronizacion,
    sincronizar_externos,
)


def parsear_rango_paginas(spec: str) -> List[int]:
    resultado: List[int] = []
    for parte in spec.split(","):
        p = parte.strip()
        if not p:
            continue
        if "-" in p:
            a_str, b_str = p.split("-", 1)
            a, b = int(a_str.strip()), int(b_str.strip())
            if a <= b:
                resultado.extend(range(a, b + 1))
            else:
                resultado.extend(range(a, b - 1, -1))
        else:
            resultado.append(int(p))
    # Mantener orden sin duplicados
    vistos: Set[int] = set()
    unicos: List[int] = []
    for n in resultado:
        if n not in vistos:
            vistos.add(n)
            unicos.append(n)
    return unicos


def resolver_slug(conn: sqlite3.Connection, selector: str) -> str:
    sel = selector.strip().lower()
    rows = conn.execute("SELECT slug, archivo FROM fuentes ORDER BY slug").fetchall()
    for slug, archivo in rows:
        if sel == slug.lower() or sel == archivo.lower():
            return slug
    parciales = [slug for slug, archivo in rows if sel in slug.lower() or sel in archivo.lower()]
    if len(parciales) == 1:
        return parciales[0]
    if len(parciales) > 1:
        raise LookupError(f"Selector ambiguo '{selector}'. Coincidencias: {', '.join(parciales)}")
    raise LookupError(f"No se encontró ninguna fuente externa que coincida con '{selector}'.")


def cmd_listar(conn: sqlite3.Connection) -> int:
    catalogo = cargar_catalogo()
    cat_por_id: Dict[str, dict] = {str(e.get("id")): e for e in catalogo.get("fuentes", [])}
    rows = conn.execute(
        "SELECT slug, formato, paginas, caracteres, idioma, requiere_ocr, archivo FROM fuentes ORDER BY slug"
    ).fetchall()
    if not rows:
        print("No hay fuentes indexadas en `externos/`.")
        return 0

    print(f"=== Fuentes Externas Indexadas ({len(rows)}) ===")
    for slug, fmt, pags, chars, lang, ocr, archivo in rows:
        e = cat_por_id.get(slug, {})
        estado = e.get("estado", "pendiente_ficha")
        postura = e.get("postura_dialogo", "por_definir")
        caps = ",".join(str(c) for c in (e.get("capitulos_destino") or [])) or "—"
        ocr_flag = " [OCR!]" if ocr else ""
        print(
            f"- {slug:<46} | {fmt.upper():<4} | {pags:>4} págs | {chars:>8,} chars | "
            f"{lang} | {estado:<15} | {postura:<15} | caps: {caps}{ocr_flag}"
        )
    return 0


def cmd_info(conn: sqlite3.Connection, selector: str) -> int:
    slug = resolver_slug(conn, selector)
    row = conn.execute(
        """
        SELECT slug, archivo, formato, paginas, caracteres, idioma, requiere_ocr,
               titulo_meta, autor_meta, url_meta, fecha_meta, toc_json
        FROM fuentes WHERE slug = ?
        """,
        (slug,),
    ).fetchone()
    if not row:
        raise LookupError(f"Fuente no encontrada: {slug}")

    (
        slug,
        archivo,
        fmt,
        pags,
        chars,
        lang,
        ocr,
        t_meta,
        a_meta,
        u_meta,
        f_meta,
        toc_json,
    ) = row
    catalogo = cargar_catalogo()
    entrada = next((e for e in catalogo.get("fuentes", []) if e.get("id") == slug), {})

    print(f"=== Información de Fuente: {slug} ===")
    print(f"Archivo:        externos/{archivo}")
    print(f"Formato/Págs:   {fmt.upper()} | {pags} págs/secciones | {chars:,} chars | Idioma: {lang} | OCR: {'Sí' if ocr else 'No'}")
    print(f"Meta PDF/HTML:  Título='{t_meta}' | Autor='{a_meta}' | Fecha='{f_meta}'")
    if u_meta:
        print(f"URL detectada:  {u_meta}")
    if entrada:
        print(f"Catálogo:       estado={entrada.get('estado')} | postura={entrada.get('postura_dialogo')} | ficha={entrada.get('ficha')}")
        if entrada.get("cita_europea"):
            print(f"Cita europea:   {entrada.get('cita_europea')}")
        if entrada.get("capitulos_destino"):
            print(f"Caps destino:   {', '.join(str(c) for c in entrada['capitulos_destino'])}")

    toc = json.loads(toc_json or "[]")
    if toc:
        print(f"\nÍndice / TOC ({len(toc)} entradas):")
        for item in toc[:60]:
            sangria = "  " * max(int(item.get("nivel", 1)) - 1, 0)
            pag = f" (p. {item['pagina']})" if item.get("pagina") else ""
            print(f"  {sangria}- {item['titulo']}{pag}")
    else:
        print("\nÍndice / TOC: (no incrustado en el documento)")
    return 0


def cmd_leer(conn: sqlite3.Connection, selector: str, paginas_spec: str, max_chars: int) -> int:
    slug = resolver_slug(conn, selector)
    nums = parsear_rango_paginas(paginas_spec)
    if not nums:
        print("Especifica al menos una página o sección (ej. --paginas 1-3).")
        return 1

    print(f"=== Lectura de `{slug}` (páginas/secciones: {paginas_spec}) ===")
    total_impresos = 0
    for n in nums:
        row = conn.execute(
            "SELECT etiqueta, texto FROM paginas WHERE slug = ? AND num_pagina = ?",
            (slug, n),
        ).fetchone()
        if not row:
            print(f"\n--- [{n}] (no existe en {slug}) ---")
            continue
        etiqueta, texto = row
        print(f"\n--- [{n}] {etiqueta} ---")
        restante = max_chars - total_impresos
        if restante <= 0:
            print("[... truncado por --max-chars; pide un rango menor o aumenta --max-chars ...]")
            break
        if len(texto) > restante:
            print(texto[:restante] + "\n[... truncado por --max-chars ...]")
            total_impresos = max_chars
            break
        print(texto)
        total_impresos += len(texto)
    return 0


def preparar_consulta_fts(consulta: str) -> str:
    """Si la consulta ya usa comillas u operadores FTS5, la respeta; si no, une palabras limpias."""
    q = consulta.strip()
    if any(op in q for op in ('"', " AND ", " OR ", " NOT ", " NEAR", "*")):
        return q
    tokens = re.findall(r"[^\s\-/.,;:¡!¿?()\[\]{}]+", q)
    if not tokens:
        return q
    return " ".join(tokens)


def cmd_buscar(conn: sqlite3.Connection, consulta: str, fuente: Optional[str], limite: int) -> int:
    fts_q = preparar_consulta_fts(consulta)
    slug_filtro = resolver_slug(conn, fuente) if fuente else None

    if slug_filtro:
        sql = """
            SELECT f.slug, f.archivo, p.num_pagina, p.etiqueta,
                   snippet(paginas_fts, 3, '«', '»', ' … ', 28) AS frag,
                   bm25(paginas_fts) AS score
            FROM paginas_fts
            JOIN paginas p ON p.id = paginas_fts.rowid
            JOIN fuentes f ON f.slug = p.slug
            WHERE paginas_fts MATCH ? AND p.slug = ?
            ORDER BY score
            LIMIT ?
        """
        params = (fts_q, slug_filtro, limite)
    else:
        sql = """
            SELECT f.slug, f.archivo, p.num_pagina, p.etiqueta,
                   snippet(paginas_fts, 3, '«', '»', ' … ', 28) AS frag,
                   bm25(paginas_fts) AS score
            FROM paginas_fts
            JOIN paginas p ON p.id = paginas_fts.rowid
            JOIN fuentes f ON f.slug = p.slug
            WHERE paginas_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """
        params = (fts_q, limite)

    rows = conn.execute(sql, params).fetchall()
    print(f"=== Búsqueda en `externos/`: {consulta!r} ({len(rows)} resultado(s)) ===")
    if not rows:
        print("Sin coincidencias.")
        return 0

    for idx, (slug, archivo, num_pag, etiqueta, frag, _score) in enumerate(rows, start=1):
        frag_limpio = re.sub(r"\s+", " ", frag or "").strip()
        print(f"\n[{idx}] {slug} — {etiqueta} ({archivo})")
        print(f"    {frag_limpio}")
    return 0


def cmd_para_capitulo(capitulo: str) -> int:
    objetivo = capitulo.strip()
    objetivo_norm = objetivo.lstrip("0") or "0"
    catalogo = cargar_catalogo()
    coincidencias = []

    for e in catalogo.get("fuentes", []):
        destinos = [str(c).strip() for c in (e.get("capitulos_destino") or [])]
        for d in destinos:
            d_norm = d.lstrip("0") or "0"
            if d == objetivo or (d.isdigit() and objetivo.isdigit() and d_norm == objetivo_norm):
                coincidencias.append(e)
                break

    print(f"=== Fuentes Externas Sugeridas para Capítulo `{objetivo}` ({len(coincidencias)}) ===")
    if not coincidencias:
        print("Ninguna fuente asignada todavía a este capítulo en `notas/fuentes/catalogo.yaml`.")
        return 0

    for e in coincidencias:
        print(f"\n- [{e.get('id')}] ({e.get('postura_dialogo')} | {e.get('estado')})")
        if e.get("cita_europea"):
            print(f"  Cita:  {e['cita_europea']}")
        else:
            print(f"  Obra:  {e.get('autor') or 'Autor por definir'} — {e.get('titulo') or e.get('archivo')}")
        print(f"  Ficha: {e.get('ficha')}")
        if e.get("temas"):
            print(f"  Temas: {', '.join(e['temas'])}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Busca pasajes verificados, lee páginas exactas y consulta el catálogo de `externos/`."
    )
    parser.add_argument("consulta", nargs="?", default=None, help="Términos o frase a buscar (FTS5)")
    parser.add_argument("--fuente", default=None, help="Filtra la búsqueda a un slug o nombre de archivo")
    parser.add_argument("--limite", type=int, default=10, help="Máximo de resultados a devolver (por defecto: 10)")
    parser.add_argument("--listar", action="store_true", help="Lista todas las fuentes indexadas y su estado")
    parser.add_argument("--info", default=None, help="Muestra metadatos e índice (TOC) de una fuente")
    parser.add_argument("--leer", default=None, help="Lee páginas/secciones exactas de una fuente")
    parser.add_argument("--paginas", default="1-3", help="Rango de páginas/secciones para --leer (ej. 1-5 o 12,15-17)")
    parser.add_argument("--max-chars", type=int, default=14000, help="Límite de caracteres en --leer")
    parser.add_argument("--para-capitulo", default=None, help="Muestra las fuentes mapeadas a un capítulo (ej. 19)")
    parser.add_argument("--sin-auto-indexar", action="store_true", help="No reindexa automáticamente antes de consultar")
    args = parser.parse_args()

    if not args.sin_auto_indexar and necesita_sincronizacion():
        sincronizar_externos(forzar=False, silencioso=True)

    if args.para_capitulo:
        return cmd_para_capitulo(args.para_capitulo)

    if not CORPUS_DB_PATH.exists():
        print("El índice local aún no existe y no se encontraron archivos en `externos/`.")
        return 1

    conn = sqlite3.connect(str(CORPUS_DB_PATH))
    try:
        if args.listar:
            return cmd_listar(conn)
        if args.info:
            return cmd_info(conn, args.info)
        if args.leer:
            return cmd_leer(conn, args.leer, args.paginas, args.max_chars)
        if args.consulta:
            return cmd_buscar(conn, args.consulta, args.fuente, args.limite)
        return cmd_listar(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
