#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscador interno rápido (insensible a tildes y mayúsculas) sobre el manuscrito vivo (`libro/`),
el Glosario (`libro/31_glosario.md`) y la Bibliografía (`libro/30_bibliografia.md`).

Elimina el «efecto túnel» al editar un capítulo a la vez: permite verificar en qué capítulos
aparece un concepto o autor, consultar definiciones exactas del Glosario de Juan Barreto y
comprobar si una obra ya figura en la Bibliografía de 2006.

Ejemplos (ejecutados internamente por el agente bajo demanda):
  # Buscar dónde aparece un autor o concepto en todo el libro (con conteo por capítulo):
  python3 -B scripts/edicion/buscar_libro.py "Baudrillard" --limite 10
  python3 -B scripts/edicion/buscar_libro.py "biopolitica" --solo-conteo

  # Consultar la definición exacta de un término en el Glosario (o listar los 92 términos):
  python3 -B scripts/edicion/buscar_libro.py --glosario "cuerpo"
  python3 -B scripts/edicion/buscar_libro.py --glosario

  # Buscar entradas existentes en la Bibliografía de 2006:
  python3 -B scripts/edicion/buscar_libro.py --bibliografia "Foucault"
"""

import argparse
from pathlib import Path
import re
import sys
from typing import List, Optional, Tuple
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    CapituloRef,
    buscar_capitulo,
    cargar_manifiesto,
)


def normalizar(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sin_tildes.lower()


def recortar_fragmento(linea: str, patron_norm: str, ventana: int = 120) -> str:
    l_norm = normalizar(linea)
    pos = l_norm.find(patron_norm)
    if pos == -1:
        return linea[: ventana * 2]
    ini = max(0, pos - ventana)
    fin = min(len(linea), pos + len(patron_norm) + ventana)
    pref = "… " if ini > 0 else ""
    suf = " …" if fin < len(linea) else ""
    return f"{pref}{linea[ini:fin].strip()}{suf}"


def extraer_entradas_glosario(glosario_path: Path) -> List[Tuple[str, str]]:
    """Devuelve lista de (termino, bloque_completo) de `libro/31_glosario.md`."""
    if not glosario_path.exists():
        return []
    txt = glosario_path.read_text(encoding="utf-8")
    entradas: List[Tuple[str, str]] = []
    termino_actual: Optional[str] = None
    buffer: List[str] = []

    for line in txt.splitlines():
        s = line.strip()
        m = re.match(r"^·\s*\*?\*?([^:\n]+?)\*?\*?:\s*(.*)$", s)
        if not m and s.startswith("· "):
            # Caso heredado de 2006 sin dos puntos (ej. "· Habitus Es la concreción...")
            m_sin_dp = re.match(r"^·\s+([A-ZÁÉÍÓÚÜÑ][^\s]+)\s+(.*)$", s)
            if m_sin_dp:
                m = m_sin_dp
        if m:
            if termino_actual is not None:
                entradas.append((termino_actual, "\n".join(buffer).strip()))
            termino_actual = m.group(1).strip().strip("*")
            buffer = [s]
        elif termino_actual is not None:
            if s.startswith("#"):
                continue
            buffer.append(line)

    if termino_actual is not None:
        entradas.append((termino_actual, "\n".join(buffer).strip()))
    return entradas


def cmd_glosario(manifiesto_path: Optional[str], consulta: Optional[str]) -> int:
    manifiesto = cargar_manifiesto(manifiesto_path)
    cap_gl = next((c for c in manifiesto.capitulos if c.tipo == "glosario"), None)
    if cap_gl is None or not cap_gl.ruta.exists():
        print("No se encontró el archivo de Glosario en el manifiesto.")
        return 1

    entradas = extraer_entradas_glosario(cap_gl.ruta)
    if not consulta:
        print(f"=== Glosario de la Obra ({len(entradas)} términos en `{cap_gl.archivo}`) ===")
        print(", ".join(t for t, _ in entradas))
        return 0

    q_norm = normalizar(consulta.strip())
    exactas = [(t, b) for t, b in entradas if normalizar(t) == q_norm]
    parciales = [(t, b) for t, b in entradas if q_norm in normalizar(t) and normalizar(t) != q_norm]
    en_cuerpo = [(t, b) for t, b in entradas if q_norm not in normalizar(t) and q_norm in normalizar(b)]

    coincidencias = exactas + parciales
    if not coincidencias:
        coincidencias = en_cuerpo[:5]

    print(f"=== Glosario (`{cap_gl.archivo}`): {consulta!r} ({len(coincidencias)} coincidencia(s)) ===")
    if not coincidencias:
        print("Sin coincidencias en el Glosario.")
        return 0

    for termino, bloque in coincidencias[:8]:
        print(f"\n--- {termino} ---")
        print(bloque)
    return 0


def cmd_bibliografia(manifiesto_path: Optional[str], consulta: str) -> int:
    manifiesto = cargar_manifiesto(manifiesto_path)
    cap_bib = next((c for c in manifiesto.capitulos if c.tipo == "bibliografia"), None)
    if cap_bib is None or not cap_bib.ruta.exists():
        print("No se encontró el archivo de Bibliografía en el manifiesto.")
        return 1

    q_norm = normalizar(consulta.strip())
    hits: List[Tuple[int, str]] = []
    for idx, line in enumerate(cap_bib.ruta.read_text(encoding="utf-8").splitlines(), start=1):
        s = line.strip()
        if s and q_norm in normalizar(s):
            hits.append((idx, s))

    print(f"=== Bibliografía (`{cap_bib.archivo}`): {consulta!r} ({len(hits)} entrada(s)) ===")
    if not hits:
        print("Sin coincidencias en la Bibliografía actual.")
        return 0
    for ln, txt in hits[:40]:
        print(f"  L{ln:>3}: {txt}")
    return 0


def cmd_buscar_libro(
    manifiesto_path: Optional[str],
    consulta: str,
    capitulo: Optional[str],
    limite: int,
    solo_conteo: bool,
) -> int:
    manifiesto = cargar_manifiesto(manifiesto_path)
    if capitulo:
        caps: List[CapituloRef] = [buscar_capitulo(manifiesto, capitulo)]
    else:
        caps = [c for c in manifiesto.capitulos if c.tipo not in ("indice", "onomastico")]

    q_norm = normalizar(consulta.strip())
    conteos: List[Tuple[str, str, int]] = []
    fragmentos: List[Tuple[str, str, int, str]] = []
    total_ocurrencias = 0

    for cap in caps:
        if not cap.ruta.exists():
            continue
        lines = cap.ruta.read_text(encoding="utf-8").splitlines()
        n_cap = 0
        for idx, line in enumerate(lines, start=1):
            l_norm = normalizar(line)
            c_line = l_norm.count(q_norm)
            if c_line > 0:
                n_cap += c_line
                if len(fragmentos) < limite:
                    fragmentos.append((cap.id, cap.archivo, idx, recortar_fragmento(line, q_norm)))
        if n_cap > 0:
            total_ocurrencias += n_cap
            conteos.append((cap.id, cap.archivo, n_cap))

    print(
        f"=== Búsqueda en el Libro (`libro/`): {consulta!r} "
        f"({total_ocurrencias} ocurrencia(s) en {len(conteos)} capítulo(s)) ==="
    )
    if not conteos:
        print("Sin coincidencias.")
        return 0

    print("Distribución por capítulo:")
    for cid, archivo, cnt in conteos:
        print(f"  - [{cid}] {archivo}: {cnt}")

    if not solo_conteo:
        print(f"\nPrimeros {len(fragmentos)} fragmento(s):")
        for cid, archivo, ln, frag in fragmentos:
            print(f"  [{cid}] {archivo}:L{ln} -> {frag}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Busca conceptos, autores, definiciones del Glosario y entradas de Bibliografía en `libro/`."
    )
    parser.add_argument("consulta", nargs="?", default=None, help="Texto, concepto o autor a buscar en el libro")
    parser.add_argument("--manifiesto", default=None, help="Ruta al manifiesto YAML (por defecto: libro.yaml)")
    parser.add_argument("--capitulo", default=None, help="Restringe la búsqueda a un solo capítulo (ej. 19)")
    parser.add_argument("--limite", type=int, default=15, help="Máximo de fragmentos a mostrar (por defecto: 15)")
    parser.add_argument("--solo-conteo", action="store_true", help="Muestra solo la distribución de menciones por capítulo")
    parser.add_argument("--glosario", nargs="?", const="", default=None, help="Consulta un término del Glosario (o lista todos si va vacío)")
    parser.add_argument("--bibliografia", default=None, help="Busca entradas en `libro/30_bibliografia.md`")
    args = parser.parse_args()

    if args.glosario is not None:
        return cmd_glosario(args.manifiesto, args.glosario or None)
    if args.bibliografia:
        return cmd_bibliografia(args.manifiesto, args.bibliografia)
    if args.consulta:
        return cmd_buscar_libro(args.manifiesto, args.consulta, args.capitulo, args.limite, args.solo_conteo)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
