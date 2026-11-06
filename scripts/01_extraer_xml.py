#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 1: Extracción de la capa vectorial XML del PDF fuente mediante Poppler (pdftohtml -xml -i)
y definición del Mapa Maestro de Capítulos (SSOT) y filtrado determinista de ruido de imprenta.
"""

import html
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

PDF_PATH = os.path.join("fuente", "Libro Crítica de La Razon Mediatica.pdf")
XML_CACHE_PATH = "/tmp/libro_razon_mediatica.xml"

# Las 16 páginas exclusivamente gráficas (Portada, 14 portadillas ilustradas, Contraportada)
GRAPHIC_ONLY_PAGES = {1, 11, 15, 39, 82, 170, 221, 284, 360, 448, 532, 556, 589, 610, 656, 666}

# Mapa Maestro de los 33 archivos Markdown (SSOT Sección 3)
# (id_num, filename, title, folio_range_str, pdf_start, pdf_end, mode)
CHAPTERS = [
    (0, "00_preliminares.md", "Preliminares (Créditos, Portadilla y Epígrafe)", "2–5", 2, 4, "prelim"),
    (1, "01_indice.md", "Índice", "7–10", 5, 8, "index"),
    (2, "02_agradecimientos.md", "Agradecimientos", "11–12", 9, 10, "body"),
    (3, "03_liminar.md", "Liminar: La belleza con agudeza y rigor (Michel Maffesoli)", "s/n 1–5", 12, 14, "body"),
    (4, "04_prologo_1_rigoberto_lanz.md", "Pro(Logos) — Comunicación: El clímax de la era posmoderna (Rigoberto Lanz)", "15–23", 16, 23, "body"),
    (5, "05_prologo_2_nelson_guzman.md", "Pro(Logos) — Los nuevos mundos simbólicos (Nelson Guzmán)", "25–31", 24, 30, "body"),
    (6, "06_prologo_3_magaldy_tellez.md", "Pro(Logos) — Trayectos claves para pensar el socialismo como pasión (Magaldy Téllez)", "33–41", 31, 38, "body"),
    (7, "07_preambulo.md", "Un intento para hacerse cargo de la massmediática. A modo de preámbulo", "43–84", 40, 81, "body"),
    (8, "08_parte1_ensayo_1.md", "Primera Parte: Aproximación a una caja de herramientas — Ensayo I: Crisis de la teoría del valor y nuevo dispositivo información-comunicación", "87–109", 83, 105, "body"),
    (9, "09_parte1_ensayo_2.md", "Primera Parte — Ensayo II: Un ejercicio sobre materia oscura y agujeros negros, virus y ADN", "111–121", 106, 117, "body"),
    (10, "10_parte1_ensayo_3.md", "Primera Parte — Ensayo III: Un acercamiento crítico a las tradiciones teóricas en el campo de la comunicación", "123–174", 118, 169, "body"),
    (11, "11_parte2_ensayo_1.md", "Segunda Parte: Cultura(s), campos y massmediática — Ensayo I: Campos híbridos y lecturas transversales", "177–193", 171, 186, "body"),
    (12, "12_parte2_ensayo_2.md", "Segunda Parte — Ensayo II: ¿Una teoría lingüística del valor?", "195–209", 187, 201, "body"),
    (13, "13_parte2_ensayo_3.md", "Segunda Parte — Ensayo III: Una incursión en la estética", "211–229", 202, 220, "body"),
    (14, "14_parte3_ensayo_1.md", "Tercera Parte: Una visión del significante-signo y del lenguaje — Ensayo I: Caminos de la semiótica", "233–258", 222, 246, "body"),
    (15, "15_parte3_ensayo_2.md", "Tercera Parte — Ensayo II: Los fantasmas del sentido: en el giro hermenéutico de la semiótica", "259–278", 247, 266, "body"),
    (16, "16_parte3_ensayo_3.md", "Tercera Parte — Ensayo III: El mito: pasaje narrativo del significante-signo al símbolo", "279–295", 267, 283, "body"),
    (17, "17_parte4_ensayo_1.md", "Cuarta Parte: Subjetividad, dispositivos y mass-media — Ensayo I: Massmediática y construcción de subjetividad", "299–321", 285, 306, "body"),
    (18, "18_parte4_ensayo_2.md", "Cuarta Parte — Ensayo II: La subjetividad massmediática", "323–341", 307, 325, "body"),
    (19, "19_parte4_ensayo_3.md", "Cuarta Parte — Ensayo III: TV: ¿Dispositivo o aparato?", "343–371", 326, 354, "body"),
    (20, "20_parte4_ensayo_4.md", "Cuarta Parte — Ensayo IV: Entonces lo mediático: Manual para ver TV", "373–377", 355, 359, "body"),
    (21, "21_parte5_ensayo_1.md", "Quinta Parte: De la opinión pública a las democracias mass-mediáticas — Ensayo I: La mediática en la hegemonía de la producción inmaterial", "381–405", 361, 384, "body"),
    (22, "22_parte5_ensayo_2.md", "Quinta Parte — Ensayo II: La sociedad mediática", "407–424", 385, 402, "body"),
    (23, "23_parte5_ensayo_3.md", "Quinta Parte — Ensayo III: La massmediatización de la política: su devenir hoy", "425–454", 403, 432, "body"),
    (24, "24_parte5_ensayo_4.md", "Quinta Parte — Ensayo IV: La mediática en su ocurrencia política", "455–469", 433, 447, "body"),
    (25, "25_parte6_ensayo_1.md", "Sexta Parte: La apuesta por la distopía de las multitudes — Ensayo I: Subjetividad y política: del consenso a la voluntad política de la multitud", "473–495", 449, 470, "body"),
    (26, "26_parte6_ensayo_2.md", "Sexta Parte — Ensayo II: De la revuelta a la reinvención del pueblo", "497–526", 471, 500, "body"),
    (27, "27_parte6_ensayo_3.md", "Sexta Parte — Ensayo III: El final de la mosca: la tela arácnida al hilo del cuerpo-potencia", "527–559", 501, 531, "body"),
    (28, "28_epilogo.md", "Epílogo: ¿Se pueden cartografiar los mass-media?", "561–584", 533, 555, "body"),
    (29, "29_post_scriptum.md", "Post-scriptum: Por el socialismo (Con un ensayo de Javier Biardeau)", "587–618", 557, 588, "body"),
    (30, "30_bibliografia.md", "Bibliografía", "621–641", 590, 609, "biblio"),
    (31, "31_glosario.md", "Glosario", "643–687", 611, 655, "glossary"),
    (32, "32_indice_onomastico.md", "Índice Onomástico", "691–699", 657, 665, "onomastico"),
]


@dataclass
class TextNode:
    page: int
    top: int
    left: int
    width: int
    height: int
    family: str
    size: int
    color: str
    raw_inner: str
    clean_text: str


@dataclass
class PageData:
    number: int
    width: int
    height: int
    folio: Optional[int]
    qxp_slug: Optional[str]
    running_header: Optional[str]
    nodes: List[TextNode]


def resolve_pdf_path(pdf_path: str = PDF_PATH) -> str:
    if os.path.exists(pdf_path):
        return pdf_path
    for fname in os.listdir("fuente"):
        if fname.endswith(".pdf") and "Razon" in fname:
            return os.path.join("fuente", fname)
    raise FileNotFoundError(f"No se encontró el PDF en {pdf_path}")


def extract_xml(pdf_path: str = PDF_PATH, out_xml: str = XML_CACHE_PATH) -> str:
    real_pdf = resolve_pdf_path(pdf_path)
    cmd = ["pdftohtml", "-xml", "-i", "-stdout", real_pdf]
    raw_bytes = subprocess.check_output(cmd)
    xml_text = raw_bytes.decode("utf-8", errors="replace")

    pages = re.findall(r'<page number="(\d+)"', xml_text)
    if len(pages) != 666:
        raise RuntimeError(f"Error de integridad: se esperaban 666 páginas y se encontraron {len(pages)}")

    with open(out_xml, "w", encoding="utf-8") as f:
        f.write(xml_text)

    print(f"[OK] XML extraído exitosamente: {len(pages)} páginas verificadas ({len(xml_text):,} bytes) -> {out_xml}")
    return xml_text


def load_or_extract_xml(out_xml: str = XML_CACHE_PATH) -> str:
    if os.path.exists(out_xml) and os.path.getsize(out_xml) > 1_000_000:
        with open(out_xml, "r", encoding="utf-8") as f:
            return f.read()
    return extract_xml(out_xml=out_xml)


def parse_all_pages(xml_text: Optional[str] = None) -> Dict[int, PageData]:
    """
    Parsea las 666 páginas del XML acumulando las definiciones globales <fontspec>
    y separando determinísticamente el ruido de imprenta (sombras, marcas QXP,
    sellos verticales rotados, cabeceras corridas y folios marginales) de los nodos de contenido.
    """
    if xml_text is None:
        xml_text = load_or_extract_xml()

    raw_pages = re.findall(
        r'<page number="(\d+)" position="[^"]*" top="\d+" left="\d+" height="(\d+)" width="(\d+)">(.*?)</page>',
        xml_text,
        re.S,
    )
    if len(raw_pages) != 666:
        raise RuntimeError(f"Se esperaban 666 páginas en XML y se hallaron {len(raw_pages)}")

    fspecs: Dict[str, Tuple[str, int, str]] = {}
    pages_dict: Dict[int, PageData] = {}

    for pnum_str, h_str, w_str, content in raw_pages:
        pnum = int(pnum_str)
        h = int(h_str)
        w = int(w_str)

        # Actualizar tabla acumulativa de fuentes
        for fid, fsize, ffam, fcol in re.findall(
            r'<fontspec id="(\d+)" size="(\d+)" family="([^"]+)" color="([^"]+)"/>', content
        ):
            clean_fam = ffam.split("+")[-1]
            fspecs[fid] = (clean_fam, int(fsize), fcol.lower())

        qxp_slug = None
        folio = None
        running_parts = []
        content_nodes: List[TextNode] = []

        for top_s, left_s, tw_s, th_s, fid, inner in re.findall(
            r'<text top="(-?\d+)" left="(-?\d+)" width="(-?\d+)" height="(-?\d+)" font="(\d+)">(.*?)</text>',
            content,
        ):
            top = int(top_s)
            left = int(left_s)
            tw = int(tw_s)
            th = int(th_s)
            fam, sz, col = fspecs[fid]

            plain = html.unescape(re.sub(r"<[^>]+>", "", inner))

            # 1. Descartar sombras duplicadas de QuarkXPress
            if col in ("#cccccc", "#bdbbbc", "#918f8f"):
                continue

            # 2. Descartar sello editorial vertical rotado (width == 0)
            if tw == 0:
                continue

            # 3. Descartar línea de registro de QuarkXPress (ej. INICIAL.qxp_iniciales 7/25/14 10:42 AM Page 2)
            if fam == "Helvetica" and sz == 12 and top < 25:
                m_qxp = re.search(r"Page\s+(\d+)", plain)
                if m_qxp:
                    qxp_slug = plain.strip()
                    if folio is None:
                        folio = int(m_qxp.group(1))
                    continue

            # 4. Descartar folio impreso en margen exterior superior (Bauhaus93 size 14)
            if fam == "Bauhaus93" and sz == 14 and top < 145 and re.match(r"^\d+$", plain.strip()):
                folio = int(plain.strip())
                continue

            # 5. Descartar cabecera corrida superior (Garamond size 12/14 en el borde superior de páginas de cuerpo)
            header_top_limit = 65 if w == 616 else 105
            if pnum > 4 and fam == "Garamond" and sz in (12, 14) and top < header_top_limit:
                running_parts.append(plain.strip())
                continue

            # Ignorar nodos completamente vacíos
            if not plain.strip():
                continue

            content_nodes.append(
                TextNode(
                    page=pnum,
                    top=top,
                    left=left,
                    width=tw,
                    height=th,
                    family=fam,
                    size=sz,
                    color=col,
                    raw_inner=inner,
                    clean_text=plain,
                )
            )

        pages_dict[pnum] = PageData(
            number=pnum,
            width=w,
            height=h,
            folio=folio,
            qxp_slug=qxp_slug,
            running_header=" ".join(running_parts) if running_parts else None,
            nodes=content_nodes,
        )

    return pages_dict


if __name__ == "__main__":
    xml_data = extract_xml()
    parsed = parse_all_pages(xml_data)
    non_empty = sum(1 for p in parsed.values() if p.nodes)
    empty_pages = sorted(p.number for p in parsed.values() if not p.nodes)
    print(f"[OK] Páginas con texto útil: {non_empty} | Páginas sólo gráficas ({len(empty_pages)}): {empty_pages}")
    assert set(empty_pages) == GRAPHIC_ONLY_PAGES, f"Diferencia en páginas gráficas: {set(empty_pages) ^ GRAPHIC_ONLY_PAGES}"
