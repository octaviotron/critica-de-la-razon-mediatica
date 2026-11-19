#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador automático del Índice General (`libro/01_indice.md`) a partir del manifiesto
`libro.yaml` y los encabezados reales (`#`, `##`, `###`) de cada archivo Markdown.

Por defecto genera una vista previa en `dist/indice_generado.md` sin modificar `libro/`.
Usa `--escribir` para actualizar directamente el archivo marcado con `tipo: indice`
en el manifiesto (bloqueado por seguridad sobre manifiestos inmutables o `respaldo_v1.0/`).
"""

import argparse
from pathlib import Path
import re
import sys
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    DEFAULT_DIST_DIR,
    REPO_ROOT,
    cargar_manifiesto,
    es_ruta_dentro_de_respaldo,
)


def extraer_encabezados(md_text: str, incluir_h3: bool = False) -> List[Tuple[int, str]]:
    """Extrae encabezados Markdown (#, ##, ###) ignorando el bloque de notas al pie."""
    encabezados: List[Tuple[int, str]] = []
    max_lvl = 3 if incluir_h3 else 2
    for line in md_text.splitlines():
        s = line.strip()
        m = re.match(r"^(#{1,3})\s+(.+)$", s)
        if not m:
            continue
        lvl = len(m.group(1))
        if lvl <= max_lvl:
            titulo = m.group(2).strip()
            encabezados.append((lvl, titulo))
    return encabezados


def construir_indice_markdown(ruta_manifiesto: str | None = None, incluir_h3: bool = False) -> Tuple[str, Path | None, bool]:
    manifiesto = cargar_manifiesto(ruta_manifiesto)
    lineas: List[str] = [
        "# Índice General",
        "",
        f"> **{manifiesto.obra.titulo}** — *{manifiesto.obra.edicion}* (`v{manifiesto.obra.version}`)",
        "",
    ]

    for sec in manifiesto.secciones:
        if not sec.mostrar_en_indice:
            continue
        lineas.append(f"## {sec.titulo}")
        lineas.append("")
        for cap in sec.capitulos:
            if cap.tipo == "indice":
                continue
            lineas.append(f"- **[{cap.titulo}]({cap.archivo})**")

            if cap.tipo in ("preliminares", "bibliografia", "glosario", "onomastico"):
                continue

            if cap.ruta.exists():
                encabezados = extraer_encabezados(cap.ruta.read_text(encoding="utf-8"), incluir_h3=incluir_h3)
                # Mostrar subtítulos internos (## y opcionalmente ###) distintos del título principal
                for lvl, subtitulo in encabezados:
                    if lvl == 1:
                        continue
                    if subtitulo.lower() == cap.titulo.lower():
                        continue
                    sangria = "  " if lvl == 2 else "    "
                    lineas.append(f"{sangria}- {subtitulo}")

        lineas.append("")

    indice_ref = manifiesto.capitulo_indice
    destino_indice = indice_ref.ruta if indice_ref else None
    return "\n".join(lineas).rstrip() + "\n", destino_indice, manifiesto.obra.inmutable


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera el Índice General en Markdown a partir de libro.yaml y los encabezados de cada capítulo."
    )
    parser.add_argument(
        "--manifiesto",
        default=None,
        help="Ruta al manifiesto YAML (por defecto: libro.yaml)",
    )
    parser.add_argument(
        "--incluir-h3",
        action="store_true",
        help="Incluye también encabezados de tercer nivel (###) en el índice",
    )
    parser.add_argument(
        "--salida",
        default=None,
        help="Archivo de salida personalizado (por defecto: dist/indice_generado.md)",
    )
    parser.add_argument(
        "--escribir",
        action="store_true",
        help="Actualiza directamente el archivo marcado como 'tipo: indice' en el manifiesto (ej. libro/01_indice.md)",
    )
    args = parser.parse_args()

    contenido, destino_indice, es_inmutable = construir_indice_markdown(
        ruta_manifiesto=args.manifiesto,
        incluir_h3=args.incluir_h3,
    )

    if args.escribir:
        if es_inmutable:
            raise PermissionError("Operación bloqueada: el manifiesto está marcado como inmutable.")
        if destino_indice is None:
            raise RuntimeError("El manifiesto no declara ningún capítulo con 'tipo: indice'.")
        destino = destino_indice
    elif args.salida:
        destino = Path(args.salida)
        if not destino.is_absolute():
            destino = (REPO_ROOT / destino).resolve()
    else:
        destino = (DEFAULT_DIST_DIR / "indice_generado.md").resolve()

    if es_ruta_dentro_de_respaldo(destino):
        raise PermissionError(f"Operación bloqueada: no se puede escribir dentro de respaldo_v1.0/ ({destino}).")

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")

    try:
        rel = destino.relative_to(REPO_ROOT)
    except ValueError:
        rel = destino
    print(f"[OK] Índice generado en: {rel} ({len(contenido.splitlines())} líneas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
