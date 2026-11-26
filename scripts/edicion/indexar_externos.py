#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indexador incremental y determinista de bibliografía externa ubicada en `externos/`.

Funciones principales:
1. Escanea `externos/` soportando PDF, HTML/HTM, TXT, MD, DOCX y EPUB.
2. Extrae texto limpio conservando el número de página (PDF) o sección (HTML/TXT/DOCX/EPUB),
   además de metadatos y tabla de contenidos (TOC/bookmarks) cuando existan.
3. Mantiene un índice local de búsqueda de texto completo SQLite FTS5 en
   `dist/indice_externos/corpus.db` y copias paginadas en `dist/indice_externos/txt/`.
4. Sincroniza el manifiesto bibliográfico `notas/fuentes/catalogo.yaml` sin sobrescribir
   campos curados manualmente (citas europeas, postura de diálogo, capítulos destino, estado).
"""

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple
import unicodedata

from bs4 import BeautifulSoup
import yaml

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None  # type: ignore

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    DEFAULT_DIST_DIR,
    REPO_ROOT,
    es_ruta_dentro_de_respaldo,
)

EXTERNOS_DIR = REPO_ROOT / "externos"
FUENTES_NOTAS_DIR = REPO_ROOT / "notas" / "fuentes"
CATALOGO_PATH = FUENTES_NOTAS_DIR / "catalogo.yaml"
INDICE_DIR = DEFAULT_DIST_DIR / "indice_externos"
CORPUS_DB_PATH = INDICE_DIR / "corpus.db"
TXT_DIR = INDICE_DIR / "txt"

EXTENSIONES_SOPORTADAS = {".pdf", ".html", ".htm", ".txt", ".md", ".docx", ".epub"}
ARCHIVOS_IGNORADOS = {"readme.md", ".ds_store", "thumbs.db"}
CHUNK_CHARS = 3500


def norm_nfc(texto: str) -> str:
    return unicodedata.normalize("NFC", texto)


def calcular_sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def generar_slug(nombre_archivo: str, usados: set[str]) -> str:
    base = Path(norm_nfc(nombre_archivo)).stem
    # Limpiar sufijos frecuentes de descarga
    base = re.sub(r"\s*[-_]\s*libgen\.li\b", "", base, flags=re.IGNORECASE)
    base = re.sub(r"\s*[-_]\s*z-?lib\b", "", base, flags=re.IGNORECASE)
    ascii_txt = (
        unicodedata.normalize("NFKD", base)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_txt).strip("_")
    slug = re.sub(r"_+", "_", slug)[:52].strip("_") or "fuente"
    candidato = slug
    n = 2
    while candidato in usados:
        sufijo = f"_{n}"
        candidato = f"{slug[: 52 - len(sufijo)]}{sufijo}"
        n += 1
    usados.add(candidato)
    return candidato


def detectar_idioma(texto_muestra: str) -> str:
    palabras = re.findall(r"[a-zA-Záéíóúüñçàâêîôûèéëïüœ]+", texto_muestra[:15000].lower())
    if not palabras:
        return "desconocido"
    marcas = {
        "es": {"de", "la", "que", "el", "en", "los", "del", "las", "por", "para", "una", "como", "más", "también", "sobre"},
        "fr": {"le", "la", "les", "des", "une", "dans", "pour", "avec", "nous", "vous", "être", "cette", "mais", "qui", "sont"},
        "en": {"the", "and", "that", "with", "for", "this", "from", "are", "was", "have", "not", "their", "which", "they"},
    }
    conteos = {lang: sum(1 for p in palabras if p in vocab) for lang, vocab in marcas.items()}
    mejor = max(conteos, key=lambda k: conteos[k])
    return mejor if conteos[mejor] >= 5 else "es"


def dividir_en_secciones(texto: str, max_chars: int = CHUNK_CHARS) -> List[Tuple[int, str, str]]:
    """Divide texto continuo en secciones numeradas respetando párrafos."""
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", texto) if p.strip()]
    if not parrafos:
        return [(1, "Sección 1", "")]

    secciones: List[Tuple[int, str, str]] = []
    actual: List[str] = []
    largo = 0
    sec_num = 1
    for p in parrafos:
        if actual and largo + len(p) + 2 > max_chars:
            secciones.append((sec_num, f"Sección {sec_num}", "\n\n".join(actual)))
            sec_num += 1
            actual = [p]
            largo = len(p)
        else:
            actual.append(p)
            largo += len(p) + 2
    if actual:
        secciones.append((sec_num, f"Sección {sec_num}", "\n\n".join(actual)))
    return secciones


def _extraer_toc_pypdf(reader: Any, max_items: int = 120) -> List[Dict[str, Any]]:
    toc: List[Dict[str, Any]] = []
    try:
        outline = reader.outline
    except Exception:
        return toc

    def recorrer(nodos: Any, nivel: int) -> None:
        if len(toc) >= max_items:
            return
        for item in nodos:
            if len(toc) >= max_items:
                break
            if isinstance(item, list):
                recorrer(item, nivel + 1)
            else:
                titulo = str(getattr(item, "title", "") or "").strip()
                pag = None
                try:
                    pag = reader.get_destination_page_number(item) + 1
                except Exception:
                    pag = None
                if titulo:
                    toc.append({"nivel": nivel, "titulo": titulo, "pagina": pag})

    if isinstance(outline, list):
        recorrer(outline, 1)
    return toc


def extraer_pdf(ruta: Path) -> Tuple[List[Tuple[int, str, str]], Dict[str, Any]]:
    meta: Dict[str, Any] = {"titulo": "", "autor": "", "url": "", "fecha": "", "toc": []}
    paginas_texto: List[str] = []

    pdftotext_bin = shutil.which("pdftotext")
    if pdftotext_bin:
        proc = subprocess.run(
            [pdftotext_bin, str(ruta), "-"],
            capture_output=True,
            check=False,
        )
        if proc.returncode == 0:
            raw = proc.stdout.decode("utf-8", errors="replace")
            partes = raw.split("\f")
            if partes and not partes[-1].strip():
                partes = partes[:-1]
            paginas_texto = partes

    if PdfReader is not None:
        try:
            reader = PdfReader(str(ruta))
            md = reader.metadata or {}
            meta["titulo"] = str(md.get("/Title") or "").strip()
            meta["autor"] = str(md.get("/Author") or "").strip()
            meta["fecha"] = str(md.get("/CreationDate") or "").strip()
            meta["toc"] = _extraer_toc_pypdf(reader)
            if not paginas_texto:
                paginas_texto = [(p.extract_text() or "") for p in reader.pages]
        except Exception:
            pass

    if not paginas_texto:
        paginas_texto = [""]

    paginas: List[Tuple[int, str, str]] = []
    for idx, txt in enumerate(paginas_texto, start=1):
        limpio = re.sub(r"[ \t]+\n", "\n", txt.replace("\r\n", "\n").replace("\r", "\n"))
        limpio = re.sub(r"\n{3,}", "\n\n", limpio).strip()
        paginas.append((idx, f"Pág. PDF {idx}", limpio))

    return paginas, meta


def extraer_html(ruta: Path) -> Tuple[List[Tuple[int, str, str]], Dict[str, Any]]:
    raw = ruta.read_bytes()
    try:
        html_str = raw.decode("utf-8")
    except UnicodeDecodeError:
        html_str = raw.decode("latin-1", errors="replace")

    soup = BeautifulSoup(html_str, "html.parser")
    meta: Dict[str, Any] = {"titulo": "", "autor": "", "url": "", "fecha": "", "toc": []}

    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        meta["titulo"] = str(og_title["content"]).strip()
    elif soup.title and soup.title.string:
        meta["titulo"] = soup.title.string.strip()

    for attr_key, attr_val in [("name", "author"), ("property", "article:author"), ("name", "byl")]:
        tag = soup.find("meta", attrs={attr_key: attr_val})
        if tag and tag.get("content"):
            meta["autor"] = str(tag["content"]).strip()
            break

    canon = soup.find("link", attrs={"rel": "canonical"})
    og_url = soup.find("meta", attrs={"property": "og:url"})
    if canon and canon.get("href"):
        meta["url"] = str(canon["href"]).strip()
    elif og_url and og_url.get("content"):
        meta["url"] = str(og_url["content"]).strip()

    for prop in ("article:published_time", "og:published_time", "datePublished"):
        t = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if t and t.get("content"):
            meta["fecha"] = str(t["content"]).strip()
            break
    if not meta["fecha"]:
        time_tag = soup.find("time")
        if time_tag:
            meta["fecha"] = str(time_tag.get("datetime") or time_tag.get_text(strip=True)).strip()

    # Seleccionar contenedor principal evitando falsos positivos de tarjetas <article> pequeñas
    body = soup.body or soup
    body_len = len(body.get_text(" ", strip=True))
    candidatos = soup.find_all(["article", "main"])
    mejor_cand = max(candidatos, key=lambda c: len(c.get_text(" ", strip=True)), default=None)
    if mejor_cand is not None:
        cand_len = len(mejor_cand.get_text(" ", strip=True))
        contenedor = mejor_cand if (cand_len >= 1500 and cand_len >= body_len * 0.25) else body
    else:
        contenedor = body

    tags_ruido = ["script", "style", "noscript", "svg", "nav", "footer", "aside", "form", "button"]
    if contenedor is body:
        tags_ruido.append("header")
    for tag in contenedor.find_all(tags_ruido):
        tag.decompose()

    bloques: List[str] = []
    toc: List[Dict[str, Any]] = []
    for elem in contenedor.find_all(["h1", "h2", "h3", "p", "blockquote", "li"]):
        txt = re.sub(r"\s+", " ", elem.get_text(" ", strip=True)).strip()
        if not txt or len(txt) < 3:
            continue
        if elem.name in ("h1", "h2", "h3"):
            nivel = int(elem.name[1])
            toc.append({"nivel": nivel, "titulo": txt, "pagina": None})
            bloques.append(f"{'#' * nivel} {txt}")
        else:
            bloques.append(txt)

    # Deduplicar bloques idénticos consecutivos
    filtrados: List[str] = []
    for b in bloques:
        if not filtrados or filtrados[-1] != b:
            filtrados.append(b)

    texto_completo = "\n\n".join(filtrados)
    meta["toc"] = toc[:80]
    return dividir_en_secciones(texto_completo), meta


def extraer_texto_plano(ruta: Path) -> Tuple[List[Tuple[int, str, str]], Dict[str, Any]]:
    raw = ruta.read_bytes()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("latin-1", errors="replace")
    txt = txt.replace("\r\n", "\n").replace("\r", "\n").strip()
    primera = next((l.strip("# ").strip() for l in txt.splitlines() if l.strip()), "")
    meta: Dict[str, Any] = {"titulo": primera[:140], "autor": "", "url": "", "fecha": "", "toc": []}
    return dividir_en_secciones(txt), meta


def extraer_con_pandoc(ruta: Path) -> Tuple[List[Tuple[int, str, str]], Dict[str, Any]]:
    pandoc_bin = shutil.which("pandoc")
    if not pandoc_bin:
        raise RuntimeError(f"Se requiere 'pandoc' para indexar {ruta.name}.")
    proc = subprocess.run(
        [pandoc_bin, str(ruta), "-t", "plain", "--wrap=none"],
        capture_output=True,
        check=True,
    )
    txt = proc.stdout.decode("utf-8", errors="replace").strip()
    primera = next((l.strip() for l in txt.splitlines() if l.strip()), "")
    meta: Dict[str, Any] = {"titulo": primera[:140], "autor": "", "url": "", "fecha": "", "toc": []}
    return dividir_en_secciones(txt), meta


def extraer_documento(ruta: Path) -> Tuple[List[Tuple[int, str, str]], Dict[str, Any]]:
    ext = ruta.suffix.lower()
    if ext == ".pdf":
        return extraer_pdf(ruta)
    if ext in (".html", ".htm"):
        return extraer_html(ruta)
    if ext in (".txt", ".md"):
        return extraer_texto_plano(ruta)
    if ext in (".docx", ".epub"):
        return extraer_con_pandoc(ruta)
    raise ValueError(f"Extensión no soportada: {ext}")


def listar_archivos_externos() -> List[Path]:
    if not EXTERNOS_DIR.is_dir():
        return []
    archivos: List[Path] = []
    for p in sorted(EXTERNOS_DIR.rglob("*")):
        if not p.is_file():
            continue
        if any(part.startswith(".") for part in p.relative_to(EXTERNOS_DIR).parts):
            continue
        if p.name.lower() in ARCHIVOS_IGNORADOS:
            continue
        if p.suffix.lower() not in EXTENSIONES_SOPORTADAS:
            continue
        archivos.append(p)
    return archivos


def inicializar_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS fuentes (
            slug TEXT PRIMARY KEY,
            archivo TEXT NOT NULL,
            ruta_rel TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            formato TEXT NOT NULL,
            paginas INTEGER NOT NULL,
            caracteres INTEGER NOT NULL,
            idioma TEXT NOT NULL,
            requiere_ocr INTEGER NOT NULL,
            titulo_meta TEXT,
            autor_meta TEXT,
            url_meta TEXT,
            fecha_meta TEXT,
            toc_json TEXT,
            mtime REAL NOT NULL,
            size_bytes INTEGER NOT NULL,
            indexado_en TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS paginas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL,
            num_pagina INTEGER NOT NULL,
            etiqueta TEXT NOT NULL,
            texto TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_paginas_slug_num ON paginas(slug, num_pagina);

        CREATE VIRTUAL TABLE IF NOT EXISTS paginas_fts USING fts5(
            slug UNINDEXED,
            num_pagina UNINDEXED,
            etiqueta UNINDEXED,
            texto,
            content='paginas',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 2'
        );
        """
    )


def eliminar_fuente_en_db(conn: sqlite3.Connection, slug: str) -> None:
    rows = conn.execute("SELECT id, slug, num_pagina, etiqueta, texto FROM paginas WHERE slug = ?", (slug,)).fetchall()
    for row_id, r_slug, r_num, r_etq, r_txt in rows:
        conn.execute(
            "INSERT INTO paginas_fts(paginas_fts, rowid, slug, num_pagina, etiqueta, texto) VALUES ('delete', ?, ?, ?, ?, ?)",
            (row_id, r_slug, r_num, r_etq, r_txt),
        )
    conn.execute("DELETE FROM paginas WHERE slug = ?", (slug,))
    conn.execute("DELETE FROM fuentes WHERE slug = ?", (slug,))


def guardar_fuente_en_db(
    conn: sqlite3.Connection,
    slug: str,
    archivo_nfc: str,
    ruta_rel_nfc: str,
    sha256: str,
    formato: str,
    paginas: List[Tuple[int, str, str]],
    caracteres: int,
    idioma: str,
    requiere_ocr: bool,
    meta: Dict[str, Any],
    mtime: float,
    size_bytes: int,
) -> None:
    eliminar_fuente_en_db(conn, slug)
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """
        INSERT INTO fuentes (
            slug, archivo, ruta_rel, sha256, formato, paginas, caracteres,
            idioma, requiere_ocr, titulo_meta, autor_meta, url_meta, fecha_meta,
            toc_json, mtime, size_bytes, indexado_en
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            slug,
            archivo_nfc,
            ruta_rel_nfc,
            sha256,
            formato,
            len(paginas),
            caracteres,
            idioma,
            1 if requiere_ocr else 0,
            meta.get("titulo", ""),
            meta.get("autor", ""),
            meta.get("url", ""),
            meta.get("fecha", ""),
            json.dumps(meta.get("toc", []), ensure_ascii=False),
            mtime,
            size_bytes,
            ahora,
        ),
    )
    for num_pag, etiqueta, texto in paginas:
        cur = conn.execute(
            "INSERT INTO paginas (slug, num_pagina, etiqueta, texto) VALUES (?, ?, ?, ?)",
            (slug, num_pag, etiqueta, texto),
        )
        row_id = cur.lastrowid
        conn.execute(
            "INSERT INTO paginas_fts (rowid, slug, num_pagina, etiqueta, texto) VALUES (?, ?, ?, ?, ?)",
            (row_id, slug, num_pag, etiqueta, texto),
        )


def escribir_txt_paginado(slug: str, archivo_nfc: str, paginas: List[Tuple[int, str, str]]) -> None:
    TXT_DIR.mkdir(parents=True, exist_ok=True)
    destino = TXT_DIR / f"{slug}.txt"
    if es_ruta_dentro_de_respaldo(destino):
        raise PermissionError(f"Operación bloqueada sobre respaldo_v1.0/: {destino}")
    partes = [f"# Fuente: {archivo_nfc} (slug: {slug})\n"]
    for num_pag, etiqueta, texto in paginas:
        partes.append(f"\n=== [{num_pag}] {etiqueta} ===\n{texto}\n")
    destino.write_text("".join(partes), encoding="utf-8")


def cargar_catalogo() -> Dict[str, Any]:
    if not CATALOGO_PATH.exists():
        return {
            "carpeta_externos": "externos",
            "indice_local": "dist/indice_externos/corpus.db",
            "fuentes": [],
        }
    data = yaml.safe_load(CATALOGO_PATH.read_text(encoding="utf-8")) or {}
    if "fuentes" not in data or not isinstance(data["fuentes"], list):
        data["fuentes"] = []
    return data


def guardar_catalogo(data: Dict[str, Any]) -> None:
    if es_ruta_dentro_de_respaldo(CATALOGO_PATH):
        raise PermissionError(f"Operación bloqueada sobre respaldo_v1.0/: {CATALOGO_PATH}")
    CATALOGO_PATH.parent.mkdir(parents=True, exist_ok=True)
    encabezado = (
        "# Catálogo Maestro de Bibliografía Externa (`notas/fuentes/catalogo.yaml`)\n"
        "#\n"
        "# Espejo bibliográfico de los archivos depositados en `externos/`.\n"
        "# Los campos técnicos (`archivo`, `sha256`, `paginas`, `caracteres`, `requiere_ocr`)\n"
        "# se sincronizan automáticamente mediante `scripts/edicion/indexar_externos.py`,\n"
        "# preservando siempre los campos editoriales curados (`cita_europea`, `postura_dialogo`,\n"
        "# `temas`, `capitulos_destino`, `estado`, `notas`).\n\n"
    )
    cuerpo = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110)
    CATALOGO_PATH.write_text(encabezado + cuerpo, encoding="utf-8")


def necesita_sincronizacion() -> bool:
    """Comprobación rápida (por ruta relativa, tamaño y mtime) para auto-indexación silenciosa."""
    archivos = listar_archivos_externos()
    if not archivos:
        return False
    if not CORPUS_DB_PATH.exists():
        return True
    try:
        conn = sqlite3.connect(str(CORPUS_DB_PATH))
        try:
            en_db = {
                row[0]: (row[1], row[2])
                for row in conn.execute("SELECT ruta_rel, size_bytes, mtime FROM fuentes").fetchall()
            }
        finally:
            conn.close()
    except sqlite3.Error:
        return True

    en_disco: Dict[str, Tuple[int, float]] = {}
    for p in archivos:
        rel_nfc = norm_nfc(p.relative_to(EXTERNOS_DIR).as_posix())
        st = p.stat()
        en_disco[rel_nfc] = (st.st_size, st.st_mtime)

    if set(en_disco.keys()) != set(en_db.keys()):
        return True
    for rel_nfc, (sz, mt) in en_disco.items():
        db_sz, db_mt = en_db[rel_nfc]
        if sz != db_sz or abs(mt - db_mt) > 1.0:
            return True
    return False


def sincronizar_externos(forzar: bool = False, silencioso: bool = False) -> Dict[str, Any]:
    INDICE_DIR.mkdir(parents=True, exist_ok=True)
    FUENTES_NOTAS_DIR.mkdir(parents=True, exist_ok=True)

    catalogo = cargar_catalogo()
    entradas_existentes: List[Dict[str, Any]] = catalogo.get("fuentes", [])
    por_ruta: Dict[str, Dict[str, Any]] = {}
    por_sha: Dict[str, Dict[str, Any]] = {}
    slugs_usados: set[str] = set()

    for e in entradas_existentes:
        slug = str(e.get("id", "")).strip()
        if slug:
            slugs_usados.add(slug)
        if e.get("archivo"):
            por_ruta[norm_nfc(str(e["archivo"]))] = e
        if e.get("sha256"):
            por_sha[str(e["sha256"])] = e

    conn = sqlite3.connect(str(CORPUS_DB_PATH))
    inicializar_db(conn)
    db_por_slug = {
        row[0]: (row[1], row[2], row[3])
        for row in conn.execute("SELECT slug, sha256, size_bytes, mtime FROM fuentes").fetchall()
    }

    archivos = listar_archivos_externos()
    nuevos: List[str] = []
    actualizados: List[str] = []
    sin_cambios: List[str] = []
    slugs_activos: set[str] = set()

    for ruta in archivos:
        rel_nfc = norm_nfc(ruta.relative_to(EXTERNOS_DIR).as_posix())
        st = ruta.stat()
        sha = calcular_sha256(ruta)

        entrada = por_ruta.get(rel_nfc) or por_sha.get(sha)
        es_nueva_en_catalogo = entrada is None
        if entrada is None:
            slug = generar_slug(rel_nfc, slugs_usados)
            entrada = {
                "id": slug,
                "archivo": rel_nfc,
                "formato": ruta.suffix.lower().lstrip("."),
                "sha256": sha,
                "titulo": "",
                "autor": "",
                "anio": "",
                "editorial": "",
                "ciudad": "",
                "url": "",
                "idioma": "",
                "tipo": "articulo" if ruta.suffix.lower() in (".html", ".htm") else ("nota_personal" if ruta.suffix.lower() in (".txt", ".md") else "libro"),
                "postura_dialogo": "por_definir",
                "cita_europea": "",
                "paginas": 0,
                "caracteres": 0,
                "requiere_ocr": False,
                "temas": [],
                "capitulos_destino": [],
                "estado": "pendiente_ficha",
                "ficha": f"notas/fuentes/{slug}.md",
                "notas": "",
            }
            entradas_existentes.append(entrada)
            por_ruta[rel_nfc] = entrada
            por_sha[sha] = entrada
        else:
            slug = str(entrada["id"])
            entrada["archivo"] = rel_nfc
            entrada.pop("ausente_en_disco", None)

        slugs_activos.add(slug)

        db_info = db_por_slug.get(slug)
        ya_indexado = (
            not forzar
            and db_info is not None
            and db_info[0] == sha
            and (TXT_DIR / f"{slug}.txt").exists()
        )

        if ya_indexado:
            # Actualizar mtime/size en DB si cambió solo timestamp
            if db_info[1] != st.st_size or abs(db_info[2] - st.st_mtime) > 1.0:
                conn.execute(
                    "UPDATE fuentes SET mtime = ?, size_bytes = ?, archivo = ?, ruta_rel = ? WHERE slug = ?",
                    (st.st_mtime, st.st_size, norm_nfc(ruta.name), rel_nfc, slug),
                )
            sin_cambios.append(slug)
            continue

        paginas, meta = extraer_documento(ruta)
        texto_total = "\n".join(p[2] for p in paginas)
        n_chars = len(texto_total)
        n_pags = len(paginas)
        idioma = detectar_idioma(texto_total)
        requiere_ocr = ruta.suffix.lower() == ".pdf" and (n_chars / max(n_pags, 1)) < 100

        guardar_fuente_en_db(
            conn=conn,
            slug=slug,
            archivo_nfc=norm_nfc(ruta.name),
            ruta_rel_nfc=rel_nfc,
            sha256=sha,
            formato=ruta.suffix.lower().lstrip("."),
            paginas=paginas,
            caracteres=n_chars,
            idioma=idioma,
            requiere_ocr=requiere_ocr,
            meta=meta,
            mtime=st.st_mtime,
            size_bytes=st.st_size,
        )
        escribir_txt_paginado(slug, norm_nfc(ruta.name), paginas)

        # Actualizar campos técnicos y completar vacíos sin pisar curación manual
        entrada["sha256"] = sha
        entrada["formato"] = ruta.suffix.lower().lstrip(".")
        entrada["paginas"] = n_pags
        entrada["caracteres"] = n_chars
        entrada["requiere_ocr"] = requiere_ocr
        if not entrada.get("idioma"):
            entrada["idioma"] = idioma
        if not entrada.get("titulo") and meta.get("titulo"):
            entrada["titulo"] = meta["titulo"]
        if not entrada.get("autor") and meta.get("autor"):
            entrada["autor"] = meta["autor"]
        if not entrada.get("url") and meta.get("url"):
            entrada["url"] = meta["url"]
        if not entrada.get("ficha"):
            entrada["ficha"] = f"notas/fuentes/{slug}.md"

        if es_nueva_en_catalogo:
            nuevos.append(slug)
        else:
            actualizados.append(slug)

    # Limpiar de SQLite fuentes removidas de externos/, pero conservarlas marcadas en catalogo.yaml
    ausentes: List[str] = []
    for slug_db in list(db_por_slug.keys()):
        if slug_db not in slugs_activos:
            eliminar_fuente_en_db(conn, slug_db)
            txt_file = TXT_DIR / f"{slug_db}.txt"
            txt_file.unlink(missing_ok=True)
            ausentes.append(slug_db)

    for e in entradas_existentes:
        if e.get("id") not in slugs_activos:
            e["ausente_en_disco"] = True

    conn.commit()
    conn.close()

    catalogo["fuentes"] = entradas_existentes
    guardar_catalogo(catalogo)

    resumen = {
        "total_disco": len(archivos),
        "nuevos": nuevos,
        "actualizados": actualizados,
        "sin_cambios": sin_cambios,
        "ausentes": ausentes,
    }

    if not silencioso:
        print("=== Indexación de Bibliografía Externa (`externos/`) ===")
        print(f"Índice local:  {CORPUS_DB_PATH.relative_to(REPO_ROOT)}")
        print(f"Catálogo:      {CATALOGO_PATH.relative_to(REPO_ROOT)}")
        print(
            f"Archivos:      {len(archivos)} en disco | Nuevos: {len(nuevos)} | "
            f"Reindexados: {len(actualizados)} | Sin cambios: {len(sin_cambios)} | Ausentes: {len(ausentes)}"
        )
        if nuevos:
            print(f"  + Nuevos:      {', '.join(nuevos)}")
        if actualizados:
            print(f"  ~ Reindexados: {', '.join(actualizados)}")
        if ausentes:
            print(f"  - Ausentes:    {', '.join(ausentes)}")

    return resumen


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Indexa incrementalmente los archivos de `externos/` en SQLite FTS5 y sincroniza `notas/fuentes/catalogo.yaml`."
    )
    parser.add_argument(
        "--forzar",
        action="store_true",
        help="Reindexa todos los archivos de `externos/` ignorando la caché SHA-256.",
    )
    args = parser.parse_args()
    sincronizar_externos(forzar=args.forzar, silencioso=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
