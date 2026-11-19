#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un reporte comparativo en `dist/` entre el estado actual del libro (`libro.yaml` y `libro/`)
y el respaldo inmutable de la 1.ª edición (`respaldo_v1.0/libro.yaml` y `respaldo_v1.0/md/`),
detectando tanto cambios estructurales (índice, orden, capítulos añadidos/eliminados/movidos)
como cambios textuales por capítulo (diferencia de palabras y líneas).

Soporta comparar un solo capítulo (`--capitulo <id|archivo>`) para facilitar el resumen de
cambios que acompaña cada entrega al autor, o comparar contra cualquier commit de Git (`--desde-git`).
"""

import argparse
from datetime import datetime
import difflib
from pathlib import Path
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    DEFAULT_DIST_DIR,
    DEFAULT_MANIFIESTO,
    REPO_ROOT,
    RESPALDO_MANIFIESTO,
    buscar_capitulo,
    cargar_manifiesto,
    es_ruta_dentro_de_respaldo,
)


def comparar_capitulo_unico(ruta_base: str, ruta_actual: str, selector: str, incluir_diffs: bool) -> str:
    m_base = cargar_manifiesto(ruta_base)
    m_act = cargar_manifiesto(ruta_actual)
    cap_act = buscar_capitulo(m_act, selector)

    base_por_archivo = {c.archivo: c for c in m_base.capitulos}
    cap_base = base_por_archivo.get(cap_act.archivo)

    txt_act = cap_act.ruta.read_text(encoding="utf-8") if cap_act.ruta.exists() else ""
    pal_act = len(txt_act.split())

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    estado_txt = cap_act.estado or "sin estado"

    if cap_base is None:
        return (
            f"# Cambios del Capítulo `{cap_act.archivo}` (Capítulo Nuevo)\n\n"
            f"**Fecha:** {fecha}  \n"
            f"**Título:** {cap_act.titulo}  \n"
            f"**Estado:** `{estado_txt}`  \n"
            f"**Palabras actuales:** {pal_act:,} (no existía en `respaldo_v1.0/`)\n"
        )

    txt_base = cap_base.ruta.read_text(encoding="utf-8") if cap_base.ruta.exists() else ""
    pal_base = len(txt_base.split())
    delta = pal_act - pal_base
    signo = "+" if delta >= 0 else ""

    out = [
        f"# Cambios del Capítulo `{cap_act.archivo}` vs. Primera Edición (2006)",
        "",
        f"**Fecha:** {fecha}  ",
        f"**Título:** {cap_act.titulo}  ",
        f"**Estado:** `{estado_txt}`  ",
        f"**Palabras:** {pal_base:,} → {pal_act:,} ({signo}{delta:,})  ",
        f"**¿Modificado?:** {'No (idéntico a 2006)' if txt_base == txt_act else 'Sí'}",
        "",
    ]

    if txt_base != txt_act and incluir_diffs:
        diff_lines = list(
            difflib.unified_diff(
                txt_base.splitlines(),
                txt_act.splitlines(),
                fromfile=f"respaldo_v1.0/md/{cap_act.archivo}",
                tofile=f"libro/{cap_act.archivo}",
                lineterm="",
                n=2,
            )
        )
        out.append("## Detalle de diferencias (`unified diff`)\n")
        out.append("```diff\n" + "\n".join(diff_lines) + "\n```\n")

    return "\n".join(out)


def comparar_contra_respaldo(ruta_base: str, ruta_actual: str, incluir_diffs: bool) -> str:
    m_base = cargar_manifiesto(ruta_base)
    m_act = cargar_manifiesto(ruta_actual)

    base_por_archivo = {c.archivo: (i, c) for i, c in enumerate(m_base.capitulos)}
    act_por_archivo = {c.archivo: (i, c) for i, c in enumerate(m_act.capitulos)}

    añadidos = [c for c in m_act.capitulos if c.archivo not in base_por_archivo]
    eliminados = [c for c in m_base.capitulos if c.archivo not in act_por_archivo]
    movidos: List[str] = []

    orden_base_comunes = [c.archivo for c in m_base.capitulos if c.archivo in act_por_archivo]
    orden_act_comunes = [c.archivo for c in m_act.capitulos if c.archivo in base_por_archivo]
    orden_cambio = orden_base_comunes != orden_act_comunes

    for archivo, (idx_act, cap_act) in act_por_archivo.items():
        if archivo in base_por_archivo:
            idx_base, cap_base = base_por_archivo[archivo]
            if cap_base.seccion_id != cap_act.seccion_id or idx_base != idx_act:
                movidos.append(
                    f"- `{archivo}`: posición `{idx_base + 1}` (`{cap_base.seccion_titulo}`) "
                    f"→ posición `{idx_act + 1}` (`{cap_act.seccion_titulo}`)"
                )

    filas_texto: List[str] = []
    bloques_diff: List[str] = []
    caps_modificados = 0
    total_pal_base = 0
    total_pal_act = 0

    for cap in m_act.capitulos:
        txt_act = cap.ruta.read_text(encoding="utf-8") if cap.ruta.exists() else ""
        pal_act = len(txt_act.split())
        total_pal_act += pal_act

        if cap.archivo in base_por_archivo:
            _, cap_base = base_por_archivo[cap.archivo]
            txt_base = cap_base.ruta.read_text(encoding="utf-8") if cap_base.ruta.exists() else ""
            pal_base = len(txt_base.split())
            total_pal_base += pal_base

            if txt_base == txt_act:
                estado = "Sin cambios"
            else:
                caps_modificados += 1
                delta = pal_act - pal_base
                signo = "+" if delta >= 0 else ""
                estado = f"**Modificado** ({signo}{delta:,} palabras)"
                if incluir_diffs:
                    diff_lines = list(
                        difflib.unified_diff(
                            txt_base.splitlines(),
                            txt_act.splitlines(),
                            fromfile=f"respaldo_v1.0/md/{cap.archivo}",
                            tofile=f"libro/{cap.archivo}",
                            lineterm="",
                            n=2,
                        )
                    )
                    bloques_diff.append(f"### `{cap.archivo}`\n\n```diff\n" + "\n".join(diff_lines) + "\n```\n")
        else:
            pal_base = 0
            caps_modificados += 1
            estado = f"**Nuevo** (+{pal_act:,} palabras)"

        delta_num = pal_act - pal_base
        signo_num = "+" if delta_num > 0 else ""
        filas_texto.append(
            f"| `{cap.id}` | `{cap.archivo}` | {pal_base:,} | {pal_act:,} | {signo_num}{delta_num:,} | {estado} |"
        )

    for cap_el in eliminados:
        pal_el = len(cap_el.ruta.read_text(encoding="utf-8").split()) if cap_el.ruta.exists() else 0
        total_pal_base += pal_el
        filas_texto.append(
            f"| `{cap_el.id}` | `{cap_el.archivo}` | {pal_el:,} | 0 | -{pal_el:,} | **Eliminado** |"
        )

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    delta_total = total_pal_act - total_pal_base
    signo_total = "+" if delta_total > 0 else ""

    out: List[str] = [
        "# Reporte Comparativo de Cambios Editoriales",
        "",
        f"**Fecha de generación:** {fecha}  ",
        f"**Base de referencia:** `{m_base.ruta_manifiesto.relative_to(REPO_ROOT)}` (`v{m_base.obra.version}`)  ",
        f"**Versión actual:** `{m_act.ruta_manifiesto.relative_to(REPO_ROOT)}` (`v{m_act.obra.version}`)  ",
        "",
        "---",
        "",
        "## 1. Cambios Estructurales y de Índice",
        "",
        f"- **Capítulos en base:** {len(m_base.capitulos)} | **Capítulos actuales:** {len(m_act.capitulos)}",
        f"- **Capítulos añadidos:** {len(añadidos)}",
        f"- **Capítulos eliminados:** {len(eliminados)}",
        f"- **Reordenamiento o cambio de parte:** {'Sí' if (orden_cambio or movidos) else 'No'}",
        "",
    ]

    if añadidos:
        out.append("### Capítulos añadidos")
        for c in añadidos:
            out.append(f"- `{c.archivo}` (`{c.seccion_titulo}` — {c.titulo})")
        out.append("")

    if eliminados:
        out.append("### Capítulos eliminados")
        for c in eliminados:
            out.append(f"- `{c.archivo}` (antes en `{c.seccion_titulo}`)")
        out.append("")

    if movidos:
        out.append("### Capítulos reubicados")
        out.extend(movidos)
        out.append("")

    out.extend(
        [
            "---",
            "",
            "## 2. Resumen Textual por Capítulo",
            "",
            f"- **Capítulos con diferencias textuales:** {caps_modificados}",
            f"- **Palabras totales:** {total_pal_base:,} → {total_pal_act:,} ({signo_total}{delta_total:,})",
            "",
            "| ID | Archivo | Palabras Base | Palabras Actual | Delta | Estado |",
            "| :-: | :--- | ---: | ---: | ---: | :--- |",
            *filas_texto,
            "",
        ]
    )

    if bloques_diff:
        out.extend(["---", "", "## 3. Detalle de Diferencias (`unified diff`)", "", *bloques_diff])

    return "\n".join(out)


def comparar_desde_git(ref_git: str) -> str:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    stat_cmd = ["git", "diff", "--stat", f"{ref_git}..HEAD", "--", "libro/", "libro.yaml"]
    word_cmd = ["git", "diff", "--word-diff=plain", f"{ref_git}..HEAD", "--", "libro/", "libro.yaml"]

    stat_out = subprocess.check_output(stat_cmd, cwd=REPO_ROOT, text=True)
    word_out = subprocess.check_output(word_cmd, cwd=REPO_ROOT, text=True)

    return (
        f"# Reporte de Cambios vía Git (`{ref_git}..HEAD`)\n\n"
        f"**Fecha de generación:** {fecha}\n\n"
        "## Resumen (`git diff --stat`)\n\n"
        "```text\n"
        f"{stat_out.strip() or '(Sin diferencias registradas en libro/ ni libro.yaml)'}\n"
        "```\n\n"
        "## Diferencias por palabra (`git diff --word-diff=plain`)\n\n"
        "```diff\n"
        f"{word_out.strip() or '(Sin diferencias)'}\n"
        "```\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera un reporte comparativo de cambios estructurales y textuales en dist/."
    )
    parser.add_argument(
        "--base",
        default=str(RESPALDO_MANIFIESTO),
        help="Manifiesto base de referencia (por defecto: respaldo_v1.0/libro.yaml)",
    )
    parser.add_argument(
        "--actual",
        default=str(DEFAULT_MANIFIESTO),
        help="Manifiesto actual a comparar (por defecto: libro.yaml)",
    )
    parser.add_argument(
        "--capitulo",
        default=None,
        help="Compara únicamente un capítulo por id o nombre de archivo (ej. 19 o 19_parte4_ensayo_3.md)",
    )
    parser.add_argument(
        "--desde-git",
        default=None,
        help="Opcional: genera el reporte usando git diff --word-diff desde un commit o referencia de Git",
    )
    parser.add_argument(
        "--incluir-diffs",
        action="store_true",
        help="Incluye el bloque unified diff completo de los capítulos modificados",
    )
    parser.add_argument(
        "--salida",
        default=None,
        help="Ruta del archivo de salida (por defecto: dist/reporte_cambios.md o dist/cambios_cap_<archivo>.md)",
    )
    args = parser.parse_args()

    if args.desde_git:
        contenido = comparar_desde_git(args.desde_git)
        default_name = "reporte_cambios_git.md"
    elif args.capitulo:
        contenido = comparar_capitulo_unico(
            args.base, args.actual, args.capitulo, incluir_diffs=args.incluir_diffs
        )
        cap_ref = buscar_capitulo(cargar_manifiesto(args.actual), args.capitulo)
        default_name = f"cambios_cap_{Path(cap_ref.archivo).stem}.md"
    else:
        contenido = comparar_contra_respaldo(args.base, args.actual, incluir_diffs=args.incluir_diffs)
        default_name = "reporte_cambios.md"

    if args.salida:
        destino = Path(args.salida)
        if not destino.is_absolute():
            destino = (REPO_ROOT / destino).resolve()
    else:
        destino = (DEFAULT_DIST_DIR / default_name).resolve()

    if es_ruta_dentro_de_respaldo(destino):
        raise PermissionError(f"Operación bloqueada: no se puede escribir dentro de respaldo_v1.0/ ({destino}).")

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")

    try:
        rel = destino.relative_to(REPO_ROOT)
    except ValueError:
        rel = destino
    print(f"[OK] Reporte comparativo generado en: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
