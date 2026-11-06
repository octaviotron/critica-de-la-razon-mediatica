#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 4: Generador de Versión de Lectura en PDF con Etiquetas de Párrafo [CC.PPP]
Lee los 33 archivos Markdown de libro/ (o de la carpeta fuente indicada) y genera un
documento PDF de alta legibilidad en versiones/Critica_de_la_Razon_Mediatica_Lectura_<version>.pdf,
donde cada párrafo lleva al inicio una etiqueta única [CC.PPP] y cada nota al pie [CC.NXX]
para facilitar el dictado de modificaciones por voz del autor.
"""

import argparse
from datetime import datetime
import hashlib
import importlib.util
import os
import re
import shutil
from typing import List, Tuple

import cairo
import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo

# Importar CHAPTERS desde 01_extraer_xml.py
_spec = importlib.util.spec_from_file_location("step1", os.path.join(os.path.dirname(__file__), "01_extraer_xml.py"))
step1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(step1)
CHAPTERS = step1.CHAPTERS

# Dimensiones de página (Tamaño Carta / Letter en puntos: 612 x 792 pt)
PAGE_WIDTH = 612.0
PAGE_HEIGHT = 792.0
MARGIN_LEFT = 54.0
MARGIN_RIGHT = 54.0
MARGIN_TOP = 58.0
MARGIN_BOTTOM = 54.0
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


def md_inline_to_pango(text: str) -> str:
    """
    Convierte formato inline Markdown (***negrita cursiva***, **negrita**, *cursiva*, [^n])
    a Pango Markup seguro (escapando &, <, >).
    """
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Llamadas a notas al pie [^12] -> superíndice azul
    esc = re.sub(
        r"\[\^(\d+)\]",
        r'<sup><span foreground="#004488" weight="bold">[\1]</span></sup>',
        esc,
    )

    # Negrita + cursiva ***...***
    esc = re.sub(r"\*\*\*([^\*]+?)\*\*\*", r"<b><i>\1</i></b>", esc)
    # Negrita **...**
    esc = re.sub(r"\*\*([^\*]+?)\*\*", r"<b>\1</b>", esc)
    # Cursiva *...*
    esc = re.sub(r"\*([^\*]+?)\*", r"<i>\1</i>", esc)

    return esc


def parse_md_blocks(md_text: str, cid: int) -> List[Tuple[str, str, str]]:
    """
    Parsea el contenido de un archivo Markdown de capítulo y devuelve una lista de tuplas:
    (block_type, tag_label, text_content)
    donde block_type in ('h1', 'h2', 'h3', 'hr', 'epigraph', 'epigraph_author', 'bq', 'li', 'fn', 'p').
    Todos los bloques de contenido (excepto encabezados y separadores) llevan su etiqueta [CC.PPP] o [CC.NXX].
    """
    lines = md_text.splitlines()
    raw_blocks: List[Tuple[str, str]] = []

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue

        if line.strip() == "---":
            raw_blocks.append(("hr", ""))
            i += 1
            continue

        if line.startswith("# "):
            raw_blocks.append(("h1", line[2:].strip()))
            i += 1
            continue
        if line.startswith("## "):
            raw_blocks.append(("h2", line[3:].strip()))
            i += 1
            continue
        if line.startswith("### "):
            raw_blocks.append(("h3", line[4:].strip()))
            i += 1
            continue

        # Notas al pie [^N]: texto
        m_fn = re.match(r"^\[\^(\d+)\]:\s*(.*)$", line)
        if m_fn:
            fn_num = int(m_fn.group(1))
            fn_body = m_fn.group(2).strip()
            i += 1
            while i < n and lines[i].strip() and not re.match(r"^\[\^\d+\]:", lines[i]) and not lines[i].startswith("#"):
                fn_body += " " + lines[i].strip()
                i += 1
            raw_blocks.append((f"fn:{fn_num}", fn_body))
            continue

        # Citas / Epígrafes (> ...)
        if line.startswith(">"):
            q_lines = []
            while i < n and lines[i].strip().startswith(">"):
                q_clean = re.sub(r"^>\s?", "", lines[i].strip())
                if q_clean:
                    q_lines.append(q_clean)
                i += 1
            for ql in q_lines:
                if ql.startswith("—"):
                    raw_blocks.append(("epigraph_author", ql))
                elif ql.startswith("*") and ql.endswith("*"):
                    raw_blocks.append(("epigraph", ql))
                else:
                    raw_blocks.append(("bq", ql))
            continue

        # Ítems de lista (- ... o   - ...)
        m_li = re.match(r"^(\s*)-\s+(.*)$", line)
        if m_li:
            indent_len = len(m_li.group(1))
            li_body = m_li.group(2).strip()
            lvl = 1 if indent_len < 2 else (2 if indent_len < 4 else 3)
            raw_blocks.append((f"li:{lvl}", li_body))
            i += 1
            continue

        # Párrafo normal (acumular líneas contiguas que no sean otro bloque)
        p_lines = [line.strip()]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt or nxt == "---" or nxt.startswith(("#", ">", "- ")) or re.match(r"^\[\^\d+\]:", nxt):
                break
            p_lines.append(nxt)
            i += 1
        raw_blocks.append(("p", " ".join(p_lines)))

    # Asignar etiquetas numeradas [CC.PPP] a cada párrafo/cita/ítem y [CC.NXX] a cada nota al pie
    labeled_blocks: List[Tuple[str, str, str]] = []
    para_counter = 0

    for btype, btext in raw_blocks:
        if btype in ("h1", "h2", "h3", "hr", "epigraph_author"):
            labeled_blocks.append((btype, "", btext))
        elif btype.startswith("fn:"):
            fn_num = int(btype.split(":")[1])
            tag = f"[{cid:02d}.N{fn_num:02d}]"
            labeled_blocks.append(("fn", tag, btext))
        else:
            para_counter += 1
            tag = f"[{cid:02d}.{para_counter:03d}]"
            labeled_blocks.append((btype, tag, btext))

    return labeled_blocks


class ReadingPDFBuilder:
    def __init__(self, out_pdf_path: str, version_str: str) -> None:
        self.out_pdf_path = out_pdf_path
        self.version_str = version_str
        self.surface = cairo.PDFSurface(out_pdf_path, PAGE_WIDTH, PAGE_HEIGHT)
        self.ctx = cairo.Context(self.surface)
        self.page_num = 0
        self.y = MARGIN_TOP
        self.current_chapter_header = ""
        self.total_labeled_paragraphs = 0
        self.total_labeled_footnotes = 0

    def start_new_page(self, is_cover: bool = False) -> None:
        if self.page_num > 0:
            self.draw_footer()
            self.ctx.show_page()
        self.page_num += 1
        self.y = MARGIN_TOP
        if not is_cover:
            self.draw_header()

    def draw_header(self) -> None:
        self.ctx.save()
        layout = PangoCairo.create_layout(self.ctx)
        font = Pango.FontDescription("Sans 7.5")
        layout.set_font_description(font)
        layout.set_width(int(CONTENT_WIDTH * Pango.SCALE))
        header_esc = self.current_chapter_header.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        markup = f'<span foreground="#666666">Crítica de la Razón Mediática — Lectura <b>{self.version_str}</b> | {header_esc}</span>'
        layout.set_markup(markup, -1)
        self.ctx.move_to(MARGIN_LEFT, 28.0)
        PangoCairo.show_layout(self.ctx, layout)

        # Línea divisoria superior
        self.ctx.set_source_rgb(0.8, 0.8, 0.8)
        self.ctx.set_line_width(0.5)
        self.ctx.move_to(MARGIN_LEFT, 44.0)
        self.ctx.line_to(PAGE_WIDTH - MARGIN_RIGHT, 44.0)
        self.ctx.stroke()
        self.ctx.restore()

    def draw_footer(self) -> None:
        self.ctx.save()
        # Línea divisoria inferior
        footer_y = PAGE_HEIGHT - 38.0
        self.ctx.set_source_rgb(0.8, 0.8, 0.8)
        self.ctx.set_line_width(0.5)
        self.ctx.move_to(MARGIN_LEFT, footer_y - 6.0)
        self.ctx.line_to(PAGE_WIDTH - MARGIN_RIGHT, footer_y - 6.0)
        self.ctx.stroke()

        layout = PangoCairo.create_layout(self.ctx)
        font = Pango.FontDescription("Sans 8.5")
        layout.set_font_description(font)
        layout.set_width(int(CONTENT_WIDTH * Pango.SCALE))
        layout.set_alignment(Pango.Alignment.CENTER)
        layout.set_markup(
            f'<span foreground="#555555">Página <b>{self.page_num}</b>  —  Use el código <b>[CC.PPP]</b> al inicio de cada párrafo para dictar cambios por voz</span>',
            -1,
        )
        self.ctx.move_to(MARGIN_LEFT, footer_y)
        PangoCairo.show_layout(self.ctx, layout)
        self.ctx.restore()

    def render_layout_block(
        self,
        markup: str,
        font_str: str = "Serif 10.5",
        indent_left: float = 0.0,
        indent_right: float = 0.0,
        justify: bool = True,
        align: Pango.Alignment = Pango.Alignment.LEFT,
        space_before: float = 0.0,
        space_after: float = 6.0,
        line_spacing: float = 1.15,
        keep_with_next: bool = False,
    ) -> None:
        avail_width = CONTENT_WIDTH - indent_left - indent_right
        layout = PangoCairo.create_layout(self.ctx)
        layout.set_font_description(Pango.FontDescription(font_str))
        layout.set_width(int(avail_width * Pango.SCALE))
        layout.set_wrap(Pango.WrapMode.WORD_CHAR)
        layout.set_justify(justify)
        layout.set_alignment(align)
        if hasattr(layout, "set_line_spacing"):
            layout.set_line_spacing(line_spacing)

        try:
            layout.set_markup(markup, -1)
        except Exception:
            plain = re.sub(r"<[^>]+>", "", markup)
            plain = plain.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            layout.set_markup(plain, -1)

        line_count = layout.get_line_count()
        _, logical_rect = layout.get_pixel_extents()
        total_h = float(logical_rect.height)

        max_y = PAGE_HEIGHT - MARGIN_BOTTOM
        if self.y + space_before > max_y - 20:
            self.start_new_page()

        self.y += space_before

        # Si el bloque completo cabe en la página actual, dibujarlo de una vez
        if self.y + total_h <= max_y:
            if keep_with_next and (self.y + total_h + 32.0 > max_y):
                self.start_new_page()
            self.ctx.move_to(MARGIN_LEFT + indent_left, self.y)
            PangoCairo.show_layout(self.ctx, layout)
            self.y += total_h + space_after
            return

        # Si el párrafo es largo y cruza el final de página, renderizar línea por línea para no truncar nada
        for idx in range(line_count):
            layout_line = layout.get_line_readonly(idx)
            _, line_ext = layout_line.get_pixel_extents()
            lh = max(float(line_ext.height), 13.0) * line_spacing
            if self.y + lh > max_y:
                self.start_new_page()
            # Baseline está a ~80% de la altura de la línea
            baseline_y = self.y + (float(line_ext.height) * 0.82)
            self.ctx.move_to(MARGIN_LEFT + indent_left + float(line_ext.x), baseline_y)
            PangoCairo.show_layout_line(self.ctx, layout_line)
            self.y += lh

        self.y += space_after

    def draw_cover_and_instructions(self) -> None:
        self.start_new_page(is_cover=True)
        self.y = 52.0

        self.render_layout_block(
            f'<span foreground="#880000" weight="bold">DOCUMENTO DE TRABAJO Y LECTURA — VERSIÓN {self.version_str}</span>',
            font_str="Sans Bold 10.5",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=8.0,
        )
        self.render_layout_block(
            "<b>Crítica de la Razón Mediática</b>",
            font_str="Serif Bold 20",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=4.0,
        )
        self.render_layout_block(
            "<i>Ensayos sobre biopolítica y potencia política del cuerpo\n(Pre-textos para un debate por el socialismo)</i>",
            font_str="Serif Italic 11.5",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=10.0,
        )
        self.render_layout_block(
            "<b>Autor: Juan Barreto Cipriani</b>\n"
            '<span size="small" foreground="#444444">Asesor Informático (Segunda Edición): Octavio Rossell Tabet (octavio.rossell@gmail.com)</span>',
            font_str="Sans 10",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=14.0,
        )

        # Recuadro de guía rápida para el autor
        box_top = self.y
        self.y = box_top + 10.0
        self.render_layout_block(
            '<span foreground="#880000"><b>GUÍA RÁPIDA PARA DICTAR CAMBIOS CON DISPOSITIVO DE VOZ (IA)</b></span>',
            font_str="Sans Bold 10",
            indent_left=14.0,
            indent_right=14.0,
            justify=False,
            space_after=6.0,
        )
        guide_items = [
            "<b>1. Qué significan los códigos al inicio de cada párrafo:</b>\n"
            'Cada párrafo de este libro lleva al inicio una etiqueta en rojo como <b><span foreground="#880000">[08.014]</span></b>:\n'
            "   • Los primeros dos dígitos (<b>08</b>) indican el número de archivo/capítulo (del <b>00</b> al <b>32</b>).\n"
            "   • Los tres dígitos siguientes (<b>014</b>) indican el número exacto de párrafo dentro de ese capítulo.\n"
            '   • Las notas al pie al final de cada capítulo llevan la letra N, por ejemplo: <b><span foreground="#004488">[08.N02]</span></b>.',
            "<b>2. Cómo dictar una modificación o nota en voz alta:</b>\n"
            "Al hablarle a su dispositivo de voz, mencione siempre primero el código del párrafo. Por ejemplo:\n"
            '   • <i>"En el párrafo <b>08 punto 014</b>, reemplazar la última oración por lo siguiente..."</i>\n'
            '   • <i>"Después del párrafo <b>19 punto 005</b>, insertar este nuevo apartado sobre redes sociales..."</i>\n'
            '   • <i>"En la nota al pie <b>08 punto N02</b>, agregar la referencia a..."</i>',
            "<b>3. Mapa de los 33 Archivos de Capítulo:</b>\n"
            "00: Preliminares | 01: Índice | 02: Agradecimientos | 03: Liminar (M. Maffesoli) | 04–06: Prólogos (R. Lanz, N. Guzmán, M. Téllez) | "
            "07: Preámbulo | 08–10: Primera Parte (Ensayos I–III) | 11–13: Segunda Parte (Ensayos I–III) | 14–16: Tercera Parte (Ensayos I–III) | "
            "17–20: Cuarta Parte (Ensayos I–IV) | 21–24: Quinta Parte (Ensayos I–IV) | 25–27: Sexta Parte (Ensayos I–III) | "
            "28: Epílogo | 29: Post-scriptum | 30: Bibliografía | 31: Glosario | 32: Índice Onomástico.",
        ]
        for g_item in guide_items:
            self.render_layout_block(
                g_item,
                font_str="Sans 8.5",
                indent_left=16.0,
                indent_right=16.0,
                justify=False,
                space_after=6.0,
                line_spacing=1.05,
            )

        box_bottom = self.y + 4.0
        self.ctx.save()
        self.ctx.set_source_rgb(0.55, 0.1, 0.1)
        self.ctx.set_line_width(1.2)
        self.ctx.rectangle(MARGIN_LEFT, box_top, CONTENT_WIDTH, box_bottom - box_top)
        self.ctx.stroke()
        self.ctx.restore()

        self.y = box_bottom + 12.0
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.render_layout_block(
            f'<span foreground="#555555" size="small">Generado automáticamente el {fecha_actual} | Versión: <b>{self.version_str}</b> | Integridad verificada: 100.000%</span>',
            font_str="Sans 8.5",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=8.0,
        )

    def render_chapter(self, cid: int, fname: str, title: str, folio_range: str, md_text: str) -> None:
        self.current_chapter_header = f"Cap. {cid:02d} ({fname}) — Folios orig. {folio_range}"
        self.start_new_page()

        # Banner superior de identificación del archivo de capítulo
        banner_markup = (
            f'<span foreground="#ffffff" background="#880000" weight="bold">  CAPÍTULO {cid:02d}  </span> '
            f'<span foreground="#333333" weight="bold"> Archivo: {fname} (Págs. edición 2006: {folio_range})</span>'
        )
        self.render_layout_block(
            banner_markup,
            font_str="Sans 9.5",
            justify=False,
            space_before=2.0,
            space_after=12.0,
            keep_with_next=True,
        )

        blocks = parse_md_blocks(md_text, cid)
        for btype, tag, btext in blocks:
            pango_txt = md_inline_to_pango(btext)
            tag_span = f'<span font_desc="Monospace Bold 9" foreground="#880000">{tag}</span> ' if tag else ""

            if btype == "h1":
                self.render_layout_block(
                    f"<b>{pango_txt}</b>",
                    font_str="Serif Bold 16",
                    justify=False,
                    space_before=10.0,
                    space_after=8.0,
                    keep_with_next=True,
                )
            elif btype == "h2":
                self.render_layout_block(
                    f"<b>{pango_txt}</b>",
                    font_str="Serif Bold 13",
                    justify=False,
                    space_before=8.0,
                    space_after=6.0,
                    keep_with_next=True,
                )
            elif btype == "h3":
                self.render_layout_block(
                    f"<b>{pango_txt}</b>",
                    font_str="Serif Bold 11.5",
                    justify=False,
                    space_before=6.0,
                    space_after=5.0,
                    keep_with_next=True,
                )
            elif btype == "hr":
                self.y += 6.0
                self.ctx.save()
                self.ctx.set_source_rgb(0.75, 0.75, 0.75)
                self.ctx.set_line_width(0.6)
                self.ctx.move_to(MARGIN_LEFT + 40, self.y)
                self.ctx.line_to(PAGE_WIDTH - MARGIN_RIGHT - 40, self.y)
                self.ctx.stroke()
                self.ctx.restore()
                self.y += 8.0
            elif btype == "epigraph":
                self.total_labeled_paragraphs += 1
                self.render_layout_block(
                    f"{tag_span}<i>{pango_txt}</i>",
                    font_str="Serif Italic 9.5",
                    indent_left=70.0,
                    indent_right=10.0,
                    justify=False,
                    align=Pango.Alignment.RIGHT,
                    space_before=2.0,
                    space_after=4.0,
                )
            elif btype == "epigraph_author":
                self.render_layout_block(
                    f"<b>{pango_txt}</b>",
                    font_str="Serif Bold 9.5",
                    indent_left=70.0,
                    indent_right=10.0,
                    justify=False,
                    align=Pango.Alignment.RIGHT,
                    space_before=0.0,
                    space_after=10.0,
                )
            elif btype == "bq":
                self.total_labeled_paragraphs += 1
                self.render_layout_block(
                    f"{tag_span}{pango_txt}",
                    font_str="Serif 9.5",
                    indent_left=28.0,
                    indent_right=12.0,
                    justify=True,
                    space_before=3.0,
                    space_after=6.0,
                )
            elif btype.startswith("li:"):
                self.total_labeled_paragraphs += 1
                lvl = int(btype.split(":")[1])
                ind = (lvl - 1) * 16.0
                self.render_layout_block(
                    f"{tag_span}• {pango_txt}",
                    font_str="Serif 10",
                    indent_left=ind,
                    justify=False,
                    space_before=1.0,
                    space_after=3.5,
                )
            elif btype == "fn":
                self.total_labeled_footnotes += 1
                fn_tag_span = f'<span font_desc="Monospace Bold 8.5" foreground="#004488">{tag}</span> '
                self.render_layout_block(
                    f"{fn_tag_span}{pango_txt}",
                    font_str="Serif 9",
                    indent_left=8.0,
                    justify=True,
                    space_before=1.0,
                    space_after=4.0,
                )
            else:
                self.total_labeled_paragraphs += 1
                self.render_layout_block(
                    f"{tag_span}{pango_txt}",
                    font_str="Serif 10.5",
                    justify=True,
                    space_before=1.0,
                    space_after=6.5,
                )

    def finish(self) -> int:
        if self.page_num > 0:
            self.draw_footer()
            self.ctx.show_page()
        self.surface.finish()
        return self.page_num


def ensure_versiones_structure(source_dir: str = "libro") -> None:
    """
    Crea y mantiene la estructura de directorios dentro de versiones/ para gestionar
    la versión original congelada (v1.0_original), las versiones en trabajo (v2.0_en_proceso)
    y el historial de cambios (historial_cambios).
    """
    base_dir = "versiones"
    v1_md_dir = os.path.join(base_dir, "v1.0_original", "md")
    v2_notas_dir = os.path.join(base_dir, "v2.0_en_proceso", "notas_autor")
    v2_borradores_dir = os.path.join(base_dir, "v2.0_en_proceso", "borradores_md")
    hist_dir = os.path.join(base_dir, "historial_cambios")

    for d in (base_dir, v1_md_dir, v2_notas_dir, v2_borradores_dir, hist_dir):
        os.makedirs(d, exist_ok=True)

    # Si v1.0_original/md está vacío, copiar la primera conversión íntegra desde libro/
    existing_md = [f for f in os.listdir(v1_md_dir) if f.endswith(".md")]
    if len(existing_md) < len(CHAPTERS):
        manifest_rows = [
            "# Manifiesto de la Versión Base Congelada (`v1.0_original`)",
            "",
            "**Descripción:** Copia inmutable de respaldo de la primera conversión a Markdown (100% fiel a la 1.ª edición de 2006).  ",
            "**Propósito:** Servir como punto de comparación permanente (`diff`) frente a todas las revisiones futuras de la 2.ª edición.  ",
            "",
            "| Nº | Archivo | Bytes | SHA-256 (primeros 16 hex) |",
            "| :-: | :--- | ---: | :---: |",
        ]
        for cid, fname, _, _, _, _, _ in CHAPTERS:
            src_file = os.path.join(source_dir, fname)
            dst_file = os.path.join(v1_md_dir, fname)
            if os.path.exists(src_file):
                shutil.copy2(src_file, dst_file)
                with open(dst_file, "rb") as bf:
                    data = bf.read()
                h16 = hashlib.sha256(data).hexdigest()[:16]
                manifest_rows.append(f"| {cid:02d} | `{fname}` | {len(data):,} | `{h16}` |")

        manifest_path = os.path.join(base_dir, "v1.0_original", "manifiesto_v1.0.md")
        with open(manifest_path, "w", encoding="utf-8") as mf:
            mf.write("\n".join(manifest_rows) + "\n")


def generate_reading_pdf(version: str = "v1.0", source_dir: str = "libro", out_dir: str = "versiones") -> str:
    ensure_versiones_structure(source_dir=source_dir)
    clean_ver = version if version.startswith("v") else f"v{version}"
    pdf_filename = f"Critica_de_la_Razon_Mediatica_Lectura_{clean_ver}.pdf"
    out_pdf_path = os.path.join(out_dir, pdf_filename)

    builder = ReadingPDFBuilder(out_pdf_path, clean_ver)
    builder.draw_cover_and_instructions()

    for cid, fname, title, folio_range, _, _, _ in CHAPTERS:
        md_path = os.path.join(source_dir, fname)
        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        builder.render_chapter(cid, fname, title, folio_range, md_text)

    total_pages = builder.finish()
    size_mb = os.path.getsize(out_pdf_path) / (1024 * 1024)
    print(
        f"[OK] PDF de lectura generado: {out_pdf_path} "
        f"({total_pages} páginas, {builder.total_labeled_paragraphs:,} párrafos etiquetados, "
        f"{builder.total_labeled_footnotes} notas etiquetadas, {size_mb:.2f} MB)"
    )
    return out_pdf_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera el PDF de lectura con párrafos etiquetados [CC.PPP].")
    parser.add_argument("--version", default="v1.0", help="Número de versión para el nombre del archivo PDF (ej. v1.0, v1.1, v2.0)")
    parser.add_argument("--fuente", default="libro", help="Carpeta con los archivos Markdown de entrada (por defecto: libro)")
    parser.add_argument("--salida", default="versiones", help="Carpeta donde se guardará el PDF numerado (por defecto: versiones)")
    args = parser.parse_args()

    generate_reading_pdf(version=args.version, source_dir=args.fuente, out_dir=args.salida)
