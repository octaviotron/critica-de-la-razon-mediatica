#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 2: Conversión Estructural Determinista de PDF (vía XML de Poppler) a Markdown por Capítulos (Método 1).
Procesa las 666 páginas del PDF según el Mapa Maestro del SSOT y genera los 33 archivos .md en libro/.
"""

import html
import importlib.util
import os
import re
from typing import Dict, List, Optional, Set, Tuple

# Importar definiciones y parser del Paso 1 (01_extraer_xml.py)
_spec = importlib.util.spec_from_file_location("step1", os.path.join(os.path.dirname(__file__), "01_extraer_xml.py"))
step1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(step1)

CHAPTERS = step1.CHAPTERS
PageData = step1.PageData
TextNode = step1.TextNode
parse_all_pages = step1.parse_all_pages

OUT_DIR = "libro"
os.makedirs(OUT_DIR, exist_ok=True)

COMPOUND_PREFIXES = {
    "auto", "anti", "pre", "post", "co", "no", "sin", "con", "sub", "ex",
    "meta", "micro", "macro", "multi", "neo", "contra", "entre", "super", "sobre", "ultra", "vice", "cuasi",
}


def build_lexicons(pages: Dict[int, PageData]) -> Tuple[Set[str], Set[str]]:
    """
    Construye a partir de todo el libro:
    1. all_words: conjunto de palabras simples completas (sin guion) presentes en la obra.
    2. inline_compounds: conjunto de palabras compuestas con guion explícito en medio de línea.
    """
    all_words: Set[str] = set()
    inline_compounds: Set[str] = set()

    for p in pages.values():
        for n in p.nodes:
            txt = n.clean_text.strip()
            txt_no_end_hyphen = re.sub(r"-\s*$", "", txt)
            for w in re.findall(r"\b[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]{2,}\b", txt_no_end_hyphen):
                all_words.add(w.lower())
            for c in re.findall(r"\b[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]{2,}-[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]{2,}\b", txt_no_end_hyphen):
                inline_compounds.add(c.lower())

    return all_words, inline_compounds


def has_written_accent(word: str) -> bool:
    return bool(re.search(r"[áéíóúÁÉÍÓÚ]", word))


def join_hyphenated(line1: str, line2: str, all_words: Set[str], inline_compounds: Set[str]) -> str:
    """
    Une dos líneas consecutivas cuando la primera termina en guion de corte de línea.
    Determina si debe conservarse el guion (palabra compuesta legítima) o eliminarse (corte silábico).
    """
    m1 = re.search(r"([a-záéíóúñüA-ZÁÉÍÓÚÑÜ]+)-\s*([\*]*)$", line1)
    m2 = re.match(r"^([\*]*)([a-záéíóúñüA-ZÁÉÍÓÚÑÜ]+)(.*)$", line2)
    if not m1 or not m2:
        return line1.rstrip() + " " + line2.lstrip()

    w1, trail_stars = m1.group(1), m1.group(2)
    lead_stars, w2, rest2 = m2.group(1), m2.group(2), m2.group(3)
    prefix_line1 = line1[: m1.start(1)]

    combined_plain = (w1 + w2).lower()
    compound_plain = f"{w1}-{w2}".lower()

    keep_hyphen = False
    if compound_plain in inline_compounds and combined_plain not in all_words:
        keep_hyphen = True
    elif w2[0].isupper():
        keep_hyphen = True
    elif has_written_accent(w1) and has_written_accent(w2):
        keep_hyphen = True
    elif w1.lower() in COMPOUND_PREFIXES and combined_plain not in all_words:
        keep_hyphen = True

    if trail_stars and trail_stars == lead_stars:
        sep = "-" if keep_hyphen else ""
        return f"{prefix_line1}{w1}{sep}{w2}{rest2}"
    else:
        sep = "-" if keep_hyphen else ""
        return f"{prefix_line1}{w1}{trail_stars}{sep}{lead_stars}{w2}{rest2}"


def format_node_markdown(node: TextNode, is_superscript: bool = False) -> str:
    """Convierte las etiquetas HTML internas (<i>, <b>) de un nodo TextNode a Markdown."""
    raw = node.raw_inner
    if is_superscript:
        clean_num = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        return f"[^{clean_num}]"

    s = re.sub(r"<b>\s*<i>(.*?)</i>\s*</b>", lambda m: f"***{m.group(1)}***", raw, flags=re.S)
    s = re.sub(r"<i>\s*<b>(.*?)</b>\s*</i>", lambda m: f"***{m.group(1)}***", s, flags=re.S)
    s = re.sub(r"<b>(\s*)(.*?)(\s*)</b>", lambda m: f"{m.group(1)}**{m.group(2)}**{m.group(3)}", s, flags=re.S)
    s = re.sub(r"<i>(\s*)(.*?)(\s*)</i>", lambda m: f"{m.group(1)}*{m.group(2)}*{m.group(3)}", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return s


def group_nodes_into_lines(nodes: List[TextNode]) -> List[List[TextNode]]:
    """Agrupa nodos de texto en líneas horizontales con tolerancia vertical de ±4 px."""
    if not nodes:
        return []
    sorted_nodes = sorted(nodes, key=lambda n: (n.top, n.left))
    lines: List[List[TextNode]] = []
    for n in sorted_nodes:
        placed = False
        for ln in reversed(lines[-3:]):
            base_tops = [x.top for x in ln if not (x.family == "Garamond" and x.size in (14, 15) and x.clean_text.strip().isdigit())]
            ref_top = sum(base_tops) / len(base_tops) if base_tops else ln[0].top
            is_sup_candidate = (
                n.family == "Garamond"
                and n.size in (14, 15)
                and n.clean_text.strip().isdigit()
                and any(x.family == "Garamond" and x.size == 18 for x in ln)
            )
            tol = 6 if is_sup_candidate else 4
            if abs(n.top - ref_top) <= tol:
                ln.append(n)
                placed = True
                break
        if not placed:
            lines.append([n])

    for ln in lines:
        ln.sort(key=lambda x: x.left)
    lines.sort(key=lambda ln: min(x.top for x in ln))
    return lines


def assemble_line_text(ln: List[TextNode], mark_superscripts: bool = True) -> str:
    """Ensambla los nodos de una línea horizontal en un string Markdown."""
    has_g18 = any(x.family == "Garamond" and x.size == 18 for x in ln)
    parts: List[str] = []
    prev_right = None

    for n in ln:
        txt_clean = n.clean_text.strip()
        is_sup = (
            mark_superscripts
            and has_g18
            and n.family == "Garamond"
            and n.size in (14, 15)
            and txt_clean.isdigit()
        )
        piece = format_node_markdown(n, is_superscript=is_sup)
        if prev_right is not None:
            gap = n.left - prev_right
            if gap > 2 and not parts[-1].endswith(" ") and not piece.startswith(" ") and not is_sup:
                if not re.match(r"^[,.;:!?)\]}»”]", piece.lstrip("*")):
                    parts.append(" ")
        parts.append(piece)
        prev_right = n.left + n.width

    joined = "".join(parts)
    joined = re.sub(r"\*\s+\*", " ", joined)
    joined = re.sub(r"[ \t]{2,}", " ", joined).strip()
    if mark_superscripts:
        joined = re.sub(r"([.»”\"’'])\s*(\d{1,2})$", r"\1[^\2]", joined)
    return joined


def normalize_amiga_heading(text: str) -> str:
    """Normaliza palabras con mezcla de mayúsculas/minúsculas de la fuente AmigaForeverPro2."""
    def fix_word(m: re.Match) -> str:
        w = m.group(0)
        if any(c.isupper() for c in w[1:]):
            return w.upper()
        return w

    return re.sub(r"[A-Za-záéíóúñüÁÉÍÓÚÑÜ]{2,}", fix_word, text)


def convert_preliminares(pages: Dict[int, PageData], start_p: int, end_p: int, all_words: Set[str], inline_compounds: Set[str]) -> str:
    """Convierte las páginas preliminares (PDF 2–4: Créditos, Portadilla y Epígrafe general)."""
    out_lines: List[str] = []

    # Página 2: Créditos
    p2_lines = group_nodes_into_lines(pages[2].nodes)
    for ln in p2_lines:
        out_lines.append(assemble_line_text(ln, mark_superscripts=False) + "  ")
    out_lines.append("\n---\n")

    # Página 3: Portadilla
    p3_lines = group_nodes_into_lines(pages[3].nodes)
    title_words: List[str] = []
    other_lines: List[str] = []
    for ln in p3_lines:
        txt = assemble_line_text(ln, mark_superscripts=False).strip()
        if any(x.size >= 50 for x in ln):
            title_words.append(txt)
        else:
            other_lines.append(txt)

    if other_lines:
        out_lines.append(f"**{other_lines[0]}**\n")
    if title_words:
        out_lines.append(f"# {' '.join(title_words)}\n")
    for l in other_lines[1:]:
        out_lines.append(f"**{l}**  ")
    out_lines.append("\n---\n")

    # Página 4: Epígrafe de Deleuze y Guattari
    p4_lines = group_nodes_into_lines(pages[4].nodes)
    ep_lines: List[str] = []
    author_line = ""
    for ln in p4_lines:
        txt = assemble_line_text(ln, mark_superscripts=False)
        if "Deleuze" in txt:
            author_line = txt
        else:
            ep_lines.append(txt)

    merged_ep = ""
    for l in ep_lines:
        if not merged_ep:
            merged_ep = l
        elif re.search(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]-\s*\*?$", merged_ep):
            merged_ep = join_hyphenated(merged_ep, l, all_words, inline_compounds)
        else:
            merged_ep += " " + l
    merged_ep = re.sub(r"\*\s*\*", " ", merged_ep)
    merged_ep = re.sub(r"[ \t]{2,}", " ", merged_ep).strip()
    out_lines.append(f"> {merged_ep}\n>\n> — {author_line}\n")
    return "\n".join(out_lines)


def convert_indice(pages: Dict[int, PageData], start_p: int, end_p: int) -> str:
    """Convierte el Índice (PDF 5–8 / Folios 7–10) uniendo líneas de títulos largos."""
    items: List[Tuple[str, str]] = []  # (kind, text)
    for pnum in range(start_p, end_p + 1):
        lines = group_nodes_into_lines(pages[pnum].nodes)
        for ln in lines:
            left = min(x.left for x in ln)
            raw_txt = assemble_line_text(ln, mark_superscripts=False)
            clean_dots = re.sub(r"\.{2,}\s*(\d+)", r" — \1", raw_txt)
            clean_dots = re.sub(r"\.{2,}", " ", clean_dots)
            clean_dots = re.sub(r"\*\*\s+", "** ", clean_dots)
            clean_dots = re.sub(r"[ \t]{2,}", " ", clean_dots).strip()

            if clean_dots.lower() == "índice":
                items.append(("h1", clean_dots))
            elif re.match(r"^(Primera|Segunda|Tercera|Cuarta|Quinta|Sexta)\s+Parte$", clean_dots, re.I):
                items.append(("h2", clean_dots))
            else:
                if left <= 135:
                    level = "L1"
                elif left <= 165:
                    level = "L2"
                else:
                    level = "L3"
                # Si el ítem anterior es del mismo nivel (o L2->L3 en continuación de título) y NO termina en número de página, unirlo
                if items and items[-1][0] in ("L1", "L2", "L3") and not re.search(r"\d+$", items[-1][1]):
                    prev_lvl, prev_txt = items[-1]
                    merged = re.sub(r"\*\*\s+\*\*", " ", prev_txt + " " + clean_dots)
                    items[-1] = (prev_lvl, merged)
                else:
                    items.append((level, clean_dots))

    out_lines: List[str] = []
    for kind, txt in items:
        if kind == "h1":
            out_lines.append(f"# {txt}\n")
        elif kind == "h2":
            out_lines.append(f"\n## {txt}\n")
        elif kind == "L1":
            out_lines.append(f"- {txt}")
        elif kind == "L2":
            out_lines.append(f"  - {txt}")
        else:
            out_lines.append(f"    - {txt}")

    return "\n".join(out_lines) + "\n"


def convert_bibliografia(pages: Dict[int, PageData], start_p: int, end_p: int, all_words: Set[str], inline_compounds: Set[str]) -> str:
    """Convierte la Bibliografía (PDF 590–609) agrupando cada entrada bibliográfica como ítem de lista."""
    out_lines: List[str] = []
    entries: List[str] = []

    for pnum in range(start_p, end_p + 1):
        lines = group_nodes_into_lines(pages[pnum].nodes)
        for ln in lines:
            if any(x.family in ("AmigaForeverPro2", "Bauhaus93") and x.size >= 18 for x in ln):
                title_txt = assemble_line_text(ln, mark_superscripts=False)
                out_lines.append(f"# {normalize_amiga_heading(title_txt)}\n")
                continue

            txt = assemble_line_text(ln, mark_superscripts=False)
            plain_start = re.sub(r"^[\*\s]+", "", txt)
            is_new_entry = bool(
                re.match(r"^_{3,}", plain_start)
                or re.match(r"^[A-ZÁÉÍÓÚÑÜ]{2,}", plain_start)
            )
            if is_new_entry or not entries:
                entries.append(txt)
            else:
                if re.search(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]-\s*\*?$", entries[-1]):
                    entries[-1] = join_hyphenated(entries[-1], txt, all_words, inline_compounds)
                else:
                    entries[-1] = entries[-1] + " " + txt

    for ent in entries:
        ent_clean = re.sub(r"\*\s*\*", " ", ent)
        ent_clean = re.sub(r"[ \t]{2,}", " ", ent_clean).strip()
        out_lines.append(f"- {ent_clean}")

    return "\n".join(out_lines) + "\n"


def convert_glosario(pages: Dict[int, PageData], start_p: int, end_p: int, all_words: Set[str], inline_compounds: Set[str]) -> str:
    """Convierte el Glosario (PDF 611–655) preservando cada entrada y su definición."""
    out_lines: List[str] = []
    paragraphs: List[str] = []

    for pnum in range(start_p, end_p + 1):
        lines = group_nodes_into_lines(pages[pnum].nodes)
        for ln in lines:
            if any(x.family in ("AmigaForeverPro2", "Bauhaus93") and x.size >= 20 for x in ln):
                title_txt = assemble_line_text(ln, mark_superscripts=False)
                out_lines.append(f"# {normalize_amiga_heading(title_txt)}\n")
                continue

            left = min(x.left for x in ln)
            txt = assemble_line_text(ln, mark_superscripts=False)
            plain = re.sub(r"[\*]", "", txt).strip()

            is_new_term = plain.startswith("·") or left >= 165
            if is_new_term or not paragraphs:
                paragraphs.append(txt)
            else:
                if re.search(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]-\s*\*?$", paragraphs[-1]):
                    paragraphs[-1] = join_hyphenated(paragraphs[-1], txt, all_words, inline_compounds)
                else:
                    paragraphs[-1] = paragraphs[-1] + " " + txt

    for p_txt in paragraphs:
        p_clean = re.sub(r"\*\s*\*", " ", p_txt)
        p_clean = re.sub(r"[ \t]{2,}", " ", p_clean).strip()
        out_lines.append(p_clean + "\n")

    return "\n".join(out_lines)


def convert_onomastico(pages: Dict[int, PageData], start_p: int, end_p: int, all_words: Set[str], inline_compounds: Set[str]) -> str:
    """Convierte el Índice Onomástico (PDF 657–665) agrupando cada autor y sus páginas."""
    out_lines: List[str] = []
    entries: List[str] = []
    heading_parts: List[str] = []

    for pnum in range(start_p, end_p + 1):
        lines = group_nodes_into_lines(pages[pnum].nodes)
        for ln in lines:
            if any(x.family in ("AmigaForeverPro2", "Bauhaus93") and x.size >= 18 for x in ln):
                heading_parts.append(normalize_amiga_heading(assemble_line_text(ln, mark_superscripts=False)))
                continue

            txt = assemble_line_text(ln, mark_superscripts=False)
            plain = re.sub(r"[\*]", "", txt).strip()
            is_new_author = bool(re.match(r"^[A-ZÁÉÍÓÚÑÜ]", plain))
            if is_new_author or not entries:
                entries.append(txt)
            else:
                entries[-1] = entries[-1] + " " + txt

    if heading_parts:
        out_lines.append(f"# {' '.join(heading_parts)}\n")

    for ent in entries:
        ent_clean = re.sub(r"\*\s*\*", " ", ent)
        ent_clean = re.sub(r"[ \t]{2,}", " ", ent_clean).strip()
        out_lines.append(f"- {ent_clean}")

    return "\n".join(out_lines) + "\n"


def convert_body_chapter(
    pages: Dict[int, PageData],
    start_p: int,
    end_p: int,
    all_words: Set[str],
    inline_compounds: Set[str],
) -> str:
    """Convierte un capítulo de cuerpo principal a Markdown preservando estructura, citas y notas al pie."""
    blocks: List[Tuple[str, str]] = []
    footnotes: List[str] = []

    for pnum in range(start_p, end_p + 1):
        pdata = pages[pnum]
        if not pdata.nodes:
            continue

        # 1. Separar letras capitulares (Drop Caps: AmigaForeverPro2 size >= 28 de 1 carácter)
        drop_caps: List[TextNode] = []
        regular_nodes: List[TextNode] = []
        for n in pdata.nodes:
            if n.family == "AmigaForeverPro2" and n.size >= 28 and len(n.clean_text.strip()) == 1:
                drop_caps.append(n)
            else:
                regular_nodes.append(n)

        lines = group_nodes_into_lines(regular_nodes)
        drop_cap_Zones: List[Tuple[int, int]] = []  # rangos verticales (top_min, top_max) que envuelven una capitular

        # 2. Adherir cada Drop Cap a la línea de cuerpo adyacente
        for dc in drop_caps:
            dc_char = dc.clean_text.strip()
            best_ln = None
            best_dist = 999
            for ln in lines:
                ln_top = min(x.top for x in ln)
                dist = abs(ln_top - dc.top)
                if dist <= 18 and dist < best_dist:
                    best_dist = dist
                    best_ln = ln
            if best_ln is not None:
                dc_first = best_ln[0]
                if dc_first.clean_text.lstrip().startswith(".-"):
                    dc_mod = TextNode(
                        page=dc.page,
                        top=dc_first.top,
                        left=dc_first.left - 5,
                        width=5,
                        height=dc.height,
                        family="Garamond",
                        size=18,
                        color=dc.color,
                        raw_inner=f"<b>{dc_char}</b>",
                        clean_text=dc_char,
                    )
                else:
                    up_char = dc_char.upper()
                    dc_mod = TextNode(
                        page=dc.page,
                        top=dc_first.top,
                        left=dc_first.left - 5,
                        width=5,
                        height=dc.height,
                        family="Garamond",
                        size=18,
                        color=dc.color,
                        raw_inner=up_char,
                        clean_text=up_char,
                    )
                    # Las 2 primeras líneas junto a la capitular están sangradas por la caja de la capitular
                    drop_cap_Zones.append((dc.top - 8, dc.top + 35))
                best_ln.insert(0, dc_mod)
            else:
                lines.append([dc])
                lines.sort(key=lambda ln: min(x.top for x in ln))

        # 3. Determinar margen izquierdo base (base_left) y último renglón de cuerpo Garamond 18 (max_g18)
        g18_lines = [ln for ln in lines if any(x.family == "Garamond" and x.size == 18 for x in ln)]
        if g18_lines:
            base_left = min(min(x.left for x in ln) for ln in g18_lines)
            max_g18 = max(min(x.top for x in ln) for ln in g18_lines)
        else:
            base_left = 86 if pdata.width == 616 else 126
            max_g18 = 9999

        # 4. Clasificar cada línea de la página en body_lines vs footnote_lines
        in_footnote_zone = False
        page_fn_lines: List[Tuple[int, int, str]] = []

        for ln in lines:
            ln_top = min(x.top for x in ln)
            ln_left = min(x.left for x in ln)

            if g18_lines and ln_top > max_g18 + 8:
                is_small_garamond = all(x.family == "Garamond" and x.size in (14, 15) for x in ln)
                if is_small_garamond:
                    if not in_footnote_zone and abs(ln_left - base_left) <= 25:
                        in_footnote_zone = True
                    if in_footnote_zone:
                        fn_txt = assemble_line_text(ln, mark_superscripts=False)
                        page_fn_lines.append((ln_top, ln_left, fn_txt))
                        continue

            is_heading = any(
                x.family in ("Bauhaus93", "AmigaForeverPro2", "Arial-Black", "FranklinGothic-DemiCond")
                or (x.family == "Garamond" and x.size >= 21)
                for x in ln
            )
            if is_heading:
                h_txt = assemble_line_text(ln, mark_superscripts=False)
                h_txt = re.sub(r"\*+", "", h_txt).strip()
                if any(x.family == "AmigaForeverPro2" for x in ln):
                    h_txt = normalize_amiga_heading(h_txt)
                max_sz = max(x.size for x in ln)
                h_level = "h1" if max_sz >= 24 else ("h2" if max_sz >= 18 else "h3")
                if blocks and blocks[-1][0] == h_level:
                    blocks[-1] = (h_level, blocks[-1][1] + " " + h_txt)
                else:
                    blocks.append((h_level, h_txt))
                continue

            is_small_quote = all(x.family == "Garamond" and x.size in (14, 15) for x in ln)
            if is_small_quote:
                q_txt = assemble_line_text(ln, mark_superscripts=True)
                prev_type = blocks[-1][0] if blocks else "h1"
                if ln_left >= base_left + 85 or prev_type in ("h1", "h2", "h3", "epigraph"):
                    btype = "epigraph"
                else:
                    btype = "bq"

                is_bold_author = q_txt.startswith("**") and q_txt.endswith("**") and len(q_txt) < 60
                if is_bold_author:
                    blocks.append(("epigraph_author", q_txt))
                elif blocks and blocks[-1][0] == btype:
                    if re.search(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]-\s*\*?$", blocks[-1][1]):
                        blocks[-1] = (btype, join_hyphenated(blocks[-1][1], q_txt, all_words, inline_compounds))
                    else:
                        blocks[-1] = (btype, blocks[-1][1] + " " + q_txt)
                else:
                    blocks.append((btype, q_txt))
                continue

            body_txt = assemble_line_text(ln, mark_superscripts=True)
            in_dropcap_wrap = any(t0 <= ln_top <= t1 for (t0, t1) in drop_cap_Zones)
            is_indented_new_para = ((ln_left >= base_left + 28) and not in_dropcap_wrap) or body_txt.startswith("**")

            if not blocks or blocks[-1][0] != "p" or is_indented_new_para:
                blocks.append(("p", body_txt))
            else:
                if re.search(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]-\s*\*?$", blocks[-1][1]):
                    blocks[-1] = ("p", join_hyphenated(blocks[-1][1], body_txt, all_words, inline_compounds))
                else:
                    blocks[-1] = ("p", blocks[-1][1] + " " + body_txt)

        # 5. Procesar las líneas de notas al pie de la página
        prev_fn_top = None
        for idx_fn, (fn_top, fn_left, fn_txt) in enumerate(page_fn_lines):
            m_fn_num = re.match(r"^(\*?)*(\d{1,2})(\*?)*\s+(.*)$", fn_txt)
            is_new_fn = False
            if m_fn_num:
                if idx_fn == 0:
                    is_new_fn = True
                elif prev_fn_top is not None and (fn_top - prev_fn_top) >= 17:
                    is_new_fn = True

            if is_new_fn and m_fn_num:
                fn_num = m_fn_num.group(2)
                fn_rest = m_fn_num.group(4).strip()
                lead_star = m_fn_num.group(1) or ""
                trail_star = m_fn_num.group(3) or ""
                prefix_star = "*" if (lead_star != trail_star) else ""
                footnotes.append(f"[^{fn_num}]: {prefix_star}{fn_rest}")
            else:
                if footnotes:
                    if re.search(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]-\s*\*?$", footnotes[-1]):
                        footnotes[-1] = join_hyphenated(footnotes[-1], fn_txt, all_words, inline_compounds)
                    else:
                        footnotes[-1] = footnotes[-1] + " " + fn_txt
                else:
                    footnotes.append(f"[^nota]: {fn_txt}")
            prev_fn_top = fn_top

    # 6. Ensamblar los bloques y las notas al pie en el documento Markdown final
    out_parts: List[str] = []
    for btype, btxt in blocks:
        btxt_clean = re.sub(r"\*\s*\*", " ", btxt)
        btxt_clean = re.sub(r"[ \t]{2,}", " ", btxt_clean).strip()
        if btype == "h1":
            out_parts.append(f"# {btxt_clean}\n")
        elif btype == "h2":
            out_parts.append(f"## {btxt_clean}\n")
        elif btype == "h3":
            out_parts.append(f"### {btxt_clean}\n")
        elif btype == "epigraph":
            out_parts.append(f"> *{btxt_clean.strip('*')}*\n")
        elif btype == "epigraph_author":
            out_parts.append(f"> — {btxt_clean}\n")
        elif btype == "bq":
            out_parts.append(f"> {btxt_clean}\n")
        else:
            out_parts.append(f"{btxt_clean}\n")

    if footnotes:
        out_parts.append("---\n")
        for fn in footnotes:
            fn_clean = re.sub(r"\*\s*\*", " ", fn)
            fn_clean = re.sub(r"[ \t]{2,}", " ", fn_clean).strip()
            out_parts.append(f"{fn_clean}\n")

    return "\n".join(out_parts)


def main() -> None:
    pages = parse_all_pages()
    all_words, inline_compounds = build_lexicons(pages)
    print(f"[INFO] Diccionario interno cargado: {len(all_words):,} palabras simples y {len(inline_compounds):,} compuestos con guion.")

    for cid, fname, title, folio_range, p_start, p_end, mode in CHAPTERS:
        if mode == "prelim":
            md_content = convert_preliminares(pages, p_start, p_end, all_words, inline_compounds)
        elif mode == "index":
            md_content = convert_indice(pages, p_start, p_end)
        elif mode == "biblio":
            md_content = convert_bibliografia(pages, p_start, p_end, all_words, inline_compounds)
        elif mode == "glossary":
            md_content = convert_glosario(pages, p_start, p_end, all_words, inline_compounds)
        elif mode == "onomastico":
            md_content = convert_onomastico(pages, p_start, p_end, all_words, inline_compounds)
        else:
            md_content = convert_body_chapter(pages, p_start, p_end, all_words, inline_compounds)

        out_path = os.path.join(OUT_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        words_count = len(md_content.split())
        print(f"  [{cid:02d}] {fname:<34s} | PDF {p_start:3d}–{p_end:3d} (Folios {folio_range:<8s}) | {words_count:6,d} palabras")

    print(f"\n[OK] Conversión completada: {len(CHAPTERS)} archivos Markdown generados en '{OUT_DIR}/'.")


if __name__ == "__main__":
    main()
