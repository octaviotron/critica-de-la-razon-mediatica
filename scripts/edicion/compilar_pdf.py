#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador de PDF de lectura desde un manifiesto YAML (`libro.yaml` o `respaldo_v1.0/libro.yaml`).

Genera un PDF limpio de alta legibilidad en `dist/` siguiendo exactamente el orden de secciones
y capítulos definido en el manifiesto. No depende del pipeline histórico de extracción ni de un
número fijo de capítulos: si reordenas, añades o quitas capítulos en `libro.yaml`, el PDF refleja
automáticamente la nueva estructura.

Ejemplos:
  # Compilar la versión actual (Segunda Edición en proceso) desde libro.yaml:
  python3 scripts/edicion/compilar_pdf.py

  # Compilar la Primera Edición intacta desde el respaldo inmutable:
  python3 scripts/edicion/compilar_pdf.py --manifiesto respaldo_v1.0/libro.yaml

  # Compilar en modo revisión con etiquetas de párrafo [ID.PPP]:
  python3 scripts/edicion/compilar_pdf.py --etiquetar-parrafos
"""

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys
from typing import List, Tuple

import cairo
import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    CapituloRef,
    DEFAULT_DIST_DIR,
    LibroManifiesto,
    REPO_ROOT,
    cargar_manifiesto,
    es_ruta_dentro_de_respaldo,
)

# Dimensiones de página (Tamaño Carta / Letter en puntos: 612 x 792 pt)
PAGE_WIDTH = 612.0
PAGE_HEIGHT = 792.0
MARGIN_LEFT = 54.0
MARGIN_RIGHT = 54.0
MARGIN_TOP = 58.0
MARGIN_BOTTOM = 54.0
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


def escape_pango(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_inline_to_pango(text: str) -> str:
    """
    Convierte formato inline Markdown (***negrita cursiva***, **negrita**, *cursiva*,
    enlaces [texto](url), llamadas a notas [^n]) a Pango Markup seguro.
    """
    # Convertir enlaces Markdown [etiqueta](destino) en su etiqueta visible
    clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    esc = escape_pango(clean)

    # Llamadas a notas al pie [^12] -> superíndice azul
    esc = re.sub(
        r"\[\^([^\]]+)\]",
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


def parse_md_blocks(md_text: str, cap_id: str, etiquetar: bool = False) -> List[Tuple[str, str, str]]:
    """
    Parsea el contenido de un archivo Markdown de capítulo y devuelve una lista de tuplas:
    (block_type, tag_label, text_content)
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
        m_fn = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", line)
        if m_fn:
            fn_id = m_fn.group(1)
            fn_body = m_fn.group(2).strip()
            i += 1
            while i < n and lines[i].strip() and not re.match(r"^\[\^[^\]]+\]:", lines[i]) and not lines[i].startswith("#"):
                fn_body += " " + lines[i].strip()
                i += 1
            raw_blocks.append((f"fn:{fn_id}", fn_body))
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

        # Párrafo normal
        p_lines = [line.strip()]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt or nxt == "---" or nxt.startswith(("#", ">", "- ")) or re.match(r"^\[\^[^\]]+\]:", nxt):
                break
            p_lines.append(nxt)
            i += 1
        raw_blocks.append(("p", " ".join(p_lines)))

    labeled_blocks: List[Tuple[str, str, str]] = []
    para_counter = 0

    for btype, btext in raw_blocks:
        if btype in ("h1", "h2", "h3", "hr", "epigraph_author"):
            labeled_blocks.append((btype, "", btext))
        elif btype.startswith("fn:"):
            fn_id = btype.split(":", 1)[1]
            if etiquetar:
                tag = f"[{cap_id}.N{fn_id.zfill(2)}]" if fn_id.isdigit() else f"[{cap_id}.N{fn_id}]"
            else:
                tag = f"[{fn_id}]"
            labeled_blocks.append(("fn", tag, btext))
        else:
            para_counter += 1
            tag = f"[{cap_id}.{para_counter:03d}]" if etiquetar else ""
            labeled_blocks.append((btype, tag, btext))

    return labeled_blocks


class BookPDFBuilder:
    def __init__(
        self,
        out_pdf_path: Path,
        manifiesto: LibroManifiesto,
        version_str: str,
        etiquetar: bool = False,
    ) -> None:
        self.out_pdf_path = out_pdf_path
        self.manifiesto = manifiesto
        self.version_str = version_str
        self.etiquetar = etiquetar
        self.surface = cairo.PDFSurface(str(out_pdf_path), PAGE_WIDTH, PAGE_HEIGHT)
        self.ctx = cairo.Context(self.surface)
        self.page_num = 0
        self.y = MARGIN_TOP
        self.current_chapter_header = ""
        self.total_paragraphs = 0
        self.total_footnotes = 0

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
        layout.set_font_description(Pango.FontDescription("Sans 7.5"))
        layout.set_width(int(CONTENT_WIDTH * Pango.SCALE))
        titulo_esc = escape_pango(self.manifiesto.obra.titulo)
        header_esc = escape_pango(self.current_chapter_header)
        markup = f'<span foreground="#666666">{titulo_esc} ({escape_pango(self.version_str)}) | {header_esc}</span>'
        layout.set_markup(markup, -1)
        self.ctx.move_to(MARGIN_LEFT, 28.0)
        PangoCairo.show_layout(self.ctx, layout)

        self.ctx.set_source_rgb(0.8, 0.8, 0.8)
        self.ctx.set_line_width(0.5)
        self.ctx.move_to(MARGIN_LEFT, 44.0)
        self.ctx.line_to(PAGE_WIDTH - MARGIN_RIGHT, 44.0)
        self.ctx.stroke()
        self.ctx.restore()

    def draw_footer(self) -> None:
        self.ctx.save()
        footer_y = PAGE_HEIGHT - 38.0
        self.ctx.set_source_rgb(0.8, 0.8, 0.8)
        self.ctx.set_line_width(0.5)
        self.ctx.move_to(MARGIN_LEFT, footer_y - 6.0)
        self.ctx.line_to(PAGE_WIDTH - MARGIN_RIGHT, footer_y - 6.0)
        self.ctx.stroke()

        layout = PangoCairo.create_layout(self.ctx)
        layout.set_font_description(Pango.FontDescription("Sans 8.5"))
        layout.set_width(int(CONTENT_WIDTH * Pango.SCALE))
        layout.set_alignment(Pango.Alignment.CENTER)
        edicion_esc = escape_pango(self.manifiesto.obra.edicion)
        if self.etiquetar:
            footer_text = f'<span foreground="#555555">Página <b>{self.page_num}</b>  —  {edicion_esc} (Modo revisión etiquetado)</span>'
        else:
            footer_text = f'<span foreground="#555555">Página <b>{self.page_num}</b>  —  {edicion_esc}</span>'
        layout.set_markup(footer_text, -1)
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
            plain = escape_pango(re.sub(r"<[^>]+>", "", markup))
            layout.set_markup(plain, -1)

        line_count = layout.get_line_count()
        _, logical_rect = layout.get_pixel_extents()
        total_h = float(logical_rect.height)

        max_y = PAGE_HEIGHT - MARGIN_BOTTOM
        if self.y + space_before > max_y - 20:
            self.start_new_page()

        self.y += space_before

        if self.y + total_h <= max_y:
            if keep_with_next and (self.y + total_h + 32.0 > max_y):
                self.start_new_page()
            self.ctx.move_to(MARGIN_LEFT + indent_left, self.y)
            PangoCairo.show_layout(self.ctx, layout)
            self.y += total_h + space_after
            return

        for idx in range(line_count):
            layout_line = layout.get_line_readonly(idx)
            _, line_ext = layout_line.get_pixel_extents()
            lh = max(float(line_ext.height), 13.0) * line_spacing
            if self.y + lh > max_y:
                self.start_new_page()
            baseline_y = self.y + (float(line_ext.height) * 0.82)
            self.ctx.move_to(MARGIN_LEFT + indent_left + float(line_ext.x), baseline_y)
            PangoCairo.show_layout_line(self.ctx, layout_line)
            self.y += lh

        self.y += space_after

    def draw_cover(self) -> None:
        self.start_new_page(is_cover=True)
        self.y = 140.0

        obra = self.manifiesto.obra
        self.render_layout_block(
            f'<span foreground="#555555" weight="bold">{escape_pango(obra.edicion.upper())} — {escape_pango(self.version_str)}</span>',
            font_str="Sans Bold 10",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=18.0,
        )
        self.render_layout_block(
            f"<b>{escape_pango(obra.titulo)}</b>",
            font_str="Serif Bold 24",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=10.0,
        )
        if obra.subtitulo:
            self.render_layout_block(
                f"<i>{escape_pango(obra.subtitulo)}</i>",
                font_str="Serif Italic 12",
                indent_left=24.0,
                indent_right=24.0,
                justify=False,
                align=Pango.Alignment.CENTER,
                space_after=28.0,
            )
        if obra.autor:
            self.render_layout_block(
                f"<b>{escape_pango(obra.autor)}</b>",
                font_str="Serif Bold 14",
                justify=False,
                align=Pango.Alignment.CENTER,
                space_after=40.0,
            )

        # Línea decorativa
        self.ctx.save()
        self.ctx.set_source_rgb(0.6, 0.6, 0.6)
        self.ctx.set_line_width(0.8)
        self.ctx.move_to(MARGIN_LEFT + 90, self.y)
        self.ctx.line_to(PAGE_WIDTH - MARGIN_RIGHT - 90, self.y)
        self.ctx.stroke()
        self.ctx.restore()
        self.y += 28.0

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        manifiesto_rel = self.manifiesto.ruta_manifiesto.relative_to(REPO_ROOT)
        modo_txt = "Lectura con etiquetas [ID.PPP]" if self.etiquetar else "Lectura editorial limpia"
        self.render_layout_block(
            f'<span foreground="#555555">Compilado el {fecha_actual}\n'
            f"Manifiesto: <b>{escape_pango(str(manifiesto_rel))}</b>  |  "
            f"Capítulos: <b>{len(self.manifiesto.capitulos)}</b>  |  Modo: <b>{modo_txt}</b></span>",
            font_str="Sans 8.5",
            justify=False,
            align=Pango.Alignment.CENTER,
            space_after=8.0,
        )

    def render_chapter(self, cap: CapituloRef, md_text: str) -> None:
        header_titulo = cap.titulo if len(cap.titulo) <= 78 else cap.titulo[:75] + "…"
        self.current_chapter_header = header_titulo
        self.start_new_page()

        if self.etiquetar:
            folios_info = f" | Folios 2006: {cap.folios_2006}" if cap.folios_2006 else ""
            banner_markup = (
                f'<span foreground="#ffffff" background="#880000" weight="bold">  ID {escape_pango(cap.id)}  </span> '
                f'<span foreground="#333333" weight="bold"> {escape_pango(cap.archivo)}{escape_pango(folios_info)}</span>'
            )
            self.render_layout_block(
                banner_markup,
                font_str="Sans 9",
                justify=False,
                space_before=2.0,
                space_after=12.0,
                keep_with_next=True,
            )

        blocks = parse_md_blocks(md_text, cap.id, etiquetar=self.etiquetar)
        for btype, tag, btext in blocks:
            pango_txt = md_inline_to_pango(btext)
            tag_span = f'<span font_desc="Monospace Bold 8.5" foreground="#880000">{escape_pango(tag)}</span> ' if tag else ""

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
                self.total_paragraphs += 1
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
                self.total_paragraphs += 1
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
                self.total_paragraphs += 1
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
                self.total_footnotes += 1
                fn_tag_span = f'<span font_desc="Monospace Bold 8.5" foreground="#004488">{escape_pango(tag)}</span> '
                self.render_layout_block(
                    f"{fn_tag_span}{pango_txt}",
                    font_str="Serif 9",
                    indent_left=8.0,
                    justify=True,
                    space_before=1.0,
                    space_after=4.0,
                )
            else:
                self.total_paragraphs += 1
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


def compilar_pdf(
    ruta_manifiesto: str | None = None,
    version_override: str | None = None,
    salida_dir: str | None = None,
    etiquetar_parrafos: bool = False,
) -> Path:
    manifiesto = cargar_manifiesto(ruta_manifiesto)
    raw_ver = version_override or manifiesto.obra.version
    clean_ver = raw_ver if raw_ver.startswith("v") else f"v{raw_ver}"

    out_dir = Path(salida_dir) if salida_dir else DEFAULT_DIST_DIR
    if not out_dir.is_absolute():
        out_dir = (REPO_ROOT / out_dir).resolve()

    if es_ruta_dentro_de_respaldo(out_dir):
        raise PermissionError(f"Operación bloqueada: no se puede compilar dentro de respaldo_v1.0/ ({out_dir}).")

    out_dir.mkdir(parents=True, exist_ok=True)
    sufijo = "_revision" if etiquetar_parrafos else ""
    out_pdf_path = out_dir / f"Critica_de_la_Razon_Mediatica_{clean_ver}{sufijo}.pdf"

    builder = BookPDFBuilder(
        out_pdf_path=out_pdf_path,
        manifiesto=manifiesto,
        version_str=clean_ver,
        etiquetar=etiquetar_parrafos,
    )
    builder.draw_cover()

    for cap in manifiesto.capitulos:
        if not cap.ruta.exists():
            raise FileNotFoundError(f"No se encontró el archivo de capítulo declarado en el manifiesto: {cap.ruta}")
        md_text = cap.ruta.read_text(encoding="utf-8")
        builder.render_chapter(cap, md_text)

    total_pages = builder.finish()
    size_mb = out_pdf_path.stat().st_size / (1024 * 1024)
    try:
        rel_out = out_pdf_path.relative_to(REPO_ROOT)
    except ValueError:
        rel_out = out_pdf_path

    print(
        f"[OK] PDF compilado: {rel_out} "
        f"({total_pages} páginas, {len(manifiesto.capitulos)} capítulos, "
        f"{builder.total_paragraphs:,} bloques, {builder.total_footnotes} notas al pie, {size_mb:.2f} MB)"
    )
    return out_pdf_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compila el libro en PDF desde un manifiesto YAML (libro.yaml o respaldo_v1.0/libro.yaml)."
    )
    parser.add_argument(
        "--manifiesto",
        default=None,
        help="Ruta al manifiesto YAML (por defecto: libro.yaml; usar respaldo_v1.0/libro.yaml para la 1.ª edición)",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Sobrescribe la etiqueta de versión en portada y nombre de archivo (por defecto toma obra.version del YAML)",
    )
    parser.add_argument(
        "--salida",
        default=None,
        help="Directorio de salida del PDF (por defecto: dist/)",
    )
    parser.add_argument(
        "--etiquetar-parrafos",
        action="store_true",
        help="Modo revisión opcional: antepone etiquetas [ID.PPP] a cada párrafo y [ID.NXX] a cada nota",
    )
    args = parser.parse_args()

    compilar_pdf(
        ruta_manifiesto=args.manifiesto,
        version_override=args.version,
        salida_dir=args.salida,
        etiquetar_parrafos=args.etiquetar_parrafos,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
