#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recalculador del Índice Onomástico (`libro/32_indice_onomastico.md`) sobre un PDF
maquetado de la Segunda Edición.

Por defecto opera en modo vista previa segura: genera `dist/maqueta/onomastico_recalculado.md`
y un reporte comparativo sin modificar `libro/32_indice_onomastico.md`.
Solo escribe sobre `libro/32_indice_onomastico.md` si se pasa explícitamente `--escribir`
en la fase de cierre editorial.
"""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import REPO_ROOT, es_ruta_dentro_de_respaldo  # noqa: E402

PDF_POR_DEFECTO = REPO_ROOT / "dist" / "maqueta" / "Critica_de_la_Razon_Mediatica_2ed_digital.pdf"
ONOMASTICO_ORIG = REPO_ROOT / "libro" / "32_indice_onomastico.md"
SALIDA_PREVIEW = REPO_ROOT / "dist" / "maqueta" / "onomastico_recalculado.md"


def normalizar_busqueda(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    return sin_tildes.lower()


def extraer_paginas_pdf(pdf_path: Path) -> List[str]:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("Se requiere 'pdftotext' (Poppler) para extraer texto por página del PDF.")
    proc = subprocess.run(
        [pdftotext, str(pdf_path), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    # pdftotext separa páginas con salto de formulario (\f)
    paginas = proc.stdout.split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()
    return paginas


def detectar_inicio_onomastico(paginas: List[str]) -> int:
    """Encuentra la página (1-based) donde comienza el propio Índice Onomástico para excluirlo."""
    for idx in range(len(paginas) - 1, -1, -1):
        norm = normalizar_busqueda(paginas[idx][:400])
        if "indice onomastico" in norm and "abad" in normalizar_busqueda(paginas[idx]):
            return idx + 1
    return len(paginas) + 1


def parsear_entradas_onomastico(ruta: Path) -> List[Tuple[str, str, List[str]]]:
    """
    Extrae (linea_original, etiqueta_nombre, terminos_busqueda) desde 32_indice_onomastico.md.
    """
    entradas: List[Tuple[str, str, List[str]]] = []
    for raw in ruta.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s.startswith("- "):
            continue
        cuerpo = s[2:].strip()
        if ":" not in cuerpo:
            continue
        nombre_raw = cuerpo.split(":", 1)[0].strip().strip("*")
        # Extraer apellidos principales (antes de la coma) para búsqueda robusta
        partes_autores = re.split(r"\s+y\s+", nombre_raw)
        terminos: List[str] = []
        for pa in partes_autores:
            apellido = pa.split(",", 1)[0].strip()
            # Quitar partículas iniciales sueltas (ej. "DE SPINOZA" -> "spinoza")
            limpio = re.sub(r"^(DE|DEL|DE LA|VON|VAN)\s+", "", apellido, flags=re.IGNORECASE).strip()
            if len(limpio) >= 3:
                terminos.append(limpio)
        if terminos:
            entradas.append((s, nombre_raw, terminos))
    return entradas


def buscar_paginas_para_entrada(
    terminos: List[str],
    paginas_norm: List[str],
    pag_inicio: int,
    pag_fin_excl: int,
) -> List[int]:
    patrones = [re.compile(r"\b" + re.escape(normalizar_busqueda(t)) + r"\b") for t in terminos]
    encontradas: List[int] = []
    for num_pag in range(pag_inicio, min(pag_fin_excl, len(paginas_norm) + 1)):
        txt = paginas_norm[num_pag - 1]
        if all(p.search(txt) for p in patrones):
            encontradas.append(num_pag)
    return encontradas


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recalcula los números de página del Índice Onomástico usando el PDF maquetado."
    )
    parser.add_argument(
        "--pdf",
        default=str(PDF_POR_DEFECTO),
        help="PDF compilado sobre el cual recalcular páginas (por defecto: dist/maqueta/Critica_de_la_Razon_Mediatica_2ed_digital.pdf)",
    )
    parser.add_argument(
        "--fuente",
        default=str(ONOMASTICO_ORIG),
        help="Archivo base del Índice Onomástico (por defecto: libro/32_indice_onomastico.md)",
    )
    parser.add_argument(
        "--desde-pagina",
        type=int,
        default=1,
        help="Primera página física a considerar en el rastreo (por defecto: 1)",
    )
    parser.add_argument(
        "--hasta-pagina",
        type=int,
        default=None,
        help="Última página física a incluir (por defecto: se detecta automáticamente antes del propio Onomástico)",
    )
    parser.add_argument(
        "--escribir",
        action="store_true",
        help="Sobrescribe libro/32_indice_onomastico.md (usar únicamente en cierre editorial tras revisar la vista previa)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.is_absolute():
        pdf_path = REPO_ROOT / pdf_path
    if not pdf_path.exists():
        print(f"[ERROR] No existe el PDF indicado: {pdf_path}")
        print("        Compila primero la maqueta con: python3 -B scripts/edicion/compilar_maqueta.py")
        return 1

    fuente_path = Path(args.fuente)
    if not fuente_path.is_absolute():
        fuente_path = REPO_ROOT / fuente_path

    destino = fuente_path if args.escribir else SALIDA_PREVIEW
    if es_ruta_dentro_de_respaldo(destino):
        raise PermissionError(f"Escritura bloqueada en respaldo_v1.0/: {destino}")

    paginas = extraer_paginas_pdf(pdf_path)
    paginas_norm = [normalizar_busqueda(p) for p in paginas]
    inicio_ono = args.hasta_pagina + 1 if args.hasta_pagina else detectar_inicio_onomastico(paginas)

    entradas = parsear_entradas_onomastico(fuente_path)
    lineas_out: List[str] = ["# ÍNDICE ONOMÁSTICO", ""]
    con_ocurrencias = 0
    sin_ocurrencias: List[str] = []

    for _, nombre, terminos in entradas:
        pags = buscar_paginas_para_entrada(terminos, paginas_norm, args.desde_pagina, inicio_ono)
        if pags:
            con_ocurrencias += 1
            lista_p = ", ".join(str(p) for p in pags)
            lineas_out.append(f"- {nombre}: *{lista_p}*")
        else:
            sin_ocurrencias.append(nombre)
            lineas_out.append(f"- {nombre}: *[SIN COINCIDENCIAS — REVISAR]*")

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(lineas_out) + "\n", encoding="utf-8")

    print(f"=== Recálculo de Índice Onomástico ===")
    print(f"PDF analizado:       {pdf_path.relative_to(REPO_ROOT) if pdf_path.is_relative_to(REPO_ROOT) else pdf_path} ({len(paginas)} págs.)")
    print(f"Rango escaneado:     págs. {args.desde_pagina} – {inicio_ono - 1}")
    print(f"Entradas procesadas: {len(entradas)} | Con coincidencias: {con_ocurrencias} | Sin coincidencias: {len(sin_ocurrencias)}")
    print(f"Archivo generado:    {destino.relative_to(REPO_ROOT)} ({'ESCRITO EN LIBRO' if args.escribir else 'VISTA PREVIA'})")
    if sin_ocurrencias:
        print("Muestra sin coincidencias (posibles variantes ortográficas/acentos en texto):")
        for nom in sin_ocurrencias[:12]:
            print(f"  - {nom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
