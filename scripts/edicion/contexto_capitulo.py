#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de briefing editorial en un solo paso para un capítulo (`--capitulo <id|archivo>`).

Reúne en una sola salida compacta todo el contexto que un agente necesita antes de editar
un capítulo de `libro/`:
1. Metadatos de `libro.yaml`, conteos y estado frente a `respaldo_v1.0/md/`.
2. Aviso explícito si el capítulo (o una sección suya, como `29_post_scriptum.md` desde L101)
   pertenece a un autor invitado protegido.
3. Diagnóstico técnico en vivo (notas al pie, sintaxis PangoCairo, asteriscos, `‹›`, encabezados partidos).
4. Ficha espejo completa de `notas/capitulos/<archivo>.md`.
5. Fuentes externas asignadas en `notas/fuentes/catalogo.yaml` (con auto-sync si aplica).
6. Referencias al capítulo encontradas en `notas/NOTAS.md`.
"""

import argparse
from pathlib import Path
import re
import sys
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from indexar_externos import cargar_catalogo  # noqa: E402
from manifiesto import (  # noqa: E402
    REPO_ROOT,
    buscar_capitulo,
    cargar_manifiesto,
)
from validar_libro import (  # noqa: E402
    INVITADOS_INTEGROS,
    POST_SCRIPTUM_ARCHIVO,
    POST_SCRIPTUM_MARCA_INVITADO,
    analizar_notas_al_pie,
    analizar_sintaxis_editorial,
    verificar_enlaces_locales,
    verificar_texto_invitado,
)


def detectar_encabezados_partidos(md_text: str) -> List[str]:
    lines = md_text.splitlines()
    h = [(i + 1, l.strip()) for i, l in enumerate(lines) if l.strip().startswith("#")]
    alertas: List[str] = []
    if len(h) >= 2 and (h[1][0] - h[0][0] <= 2):
        alertas.append(f"Posible encabezado de apertura partido: L{h[0][0]} `{h[0][1]}` / L{h[1][0]} `{h[1][1]}`")
    for ln, txt in h:
        if re.match(r"^#+\s*[-–—]\s*$", txt):
            alertas.append(f"Encabezado con guion suelto en L{ln}: `{txt}`")
    return alertas


def referencias_en_notas_globales(archivo: str) -> List[str]:
    notas_path = REPO_ROOT / "notas" / "NOTAS.md"
    if not notas_path.exists():
        return []
    lines = notas_path.read_text(encoding="utf-8").splitlines()
    hallazgos: List[str] = []
    bloque_actual = ""
    for line in lines:
        if line.startswith("- ["):
            bloque_actual = line.strip()
        if archivo in line:
            resumen = bloque_actual if bloque_actual and archivo not in bloque_actual else line.strip()
            if resumen not in hallazgos:
                hallazgos.append(resumen)
    return hallazgos


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Muestra el briefing editorial completo de un capítulo antes de editarlo."
    )
    parser.add_argument(
        "--capitulo",
        required=True,
        help="ID o nombre de archivo del capítulo (ej. 19 o 19_parte4_ensayo_3.md)",
    )
    parser.add_argument(
        "--manifiesto",
        default=None,
        help="Ruta al manifiesto YAML (por defecto: libro.yaml)",
    )
    args = parser.parse_args()

    manifiesto = cargar_manifiesto(args.manifiesto)
    cap = buscar_capitulo(manifiesto, args.capitulo)
    md_text = cap.ruta.read_text(encoding="utf-8") if cap.ruta.exists() else ""
    palabras = len(md_text.split())
    llamadas, definiciones, invalidas = analizar_notas_al_pie(md_text)

    respaldo_path = REPO_ROOT / "respaldo_v1.0" / "md" / cap.archivo
    if respaldo_path.exists():
        modificado = respaldo_path.read_text(encoding="utf-8") != md_text
        estado_2006 = "Modificado respecto a 2006" if modificado else "Idéntico a respaldo_v1.0 (2006)"
    else:
        estado_2006 = "Capítulo nuevo (no existía en 2006)"

    print(f"=== BRIEFING EDITORIAL: [{cap.id}] {cap.archivo} ===")
    print(f"Título:        {cap.titulo}")
    print(f"Sección:       {cap.seccion_titulo}")
    print(f"Estado YAML:   {cap.estado or 'sin estado'} | Folios 2006: {cap.folios_2006 or '—'}")
    print(f"Métricas:      {palabras:,} palabras | {len(definiciones)} notas al pie | {estado_2006}")

    # 1. Alerta de autoría invitada
    if cap.archivo in INVITADOS_INTEGROS:
        print(
            f"\n[🔒 PROTEGIDO — AUTOR INVITADO]: Este archivo pertenece íntegramente a "
            f"{INVITADOS_INTEGROS[cap.archivo]}. NO reescribir contenido sin orden expresa del usuario/autor."
        )
    elif cap.archivo == POST_SCRIPTUM_ARCHIVO:
        lin_biardeau = next(
            (i for i, l in enumerate(md_text.splitlines(), 1) if l.strip().startswith(POST_SCRIPTUM_MARCA_INVITADO)),
            None,
        )
        print(
            f"\n[🔒 PROTECCIÓN PARCIAL]: Líneas 1–{(lin_biardeau - 1) if lin_biardeau else 100} son de Juan Barreto (editables). "
            f"Desde la línea {lin_biardeau or 101} (`{POST_SCRIPTUM_MARCA_INVITADO}`) es ensayo invitado de Javier Biardeau (NO editar sin orden expresa)."
        )

    # 2. Diagnóstico técnico en vivo
    print("\n--- 1. Diagnóstico técnico del capítulo ---")
    alertas_diag: List[str] = []
    for inv in invalidas:
        alertas_diag.append(f"[ERROR] {inv}")
    sin_def = sorted(llamadas - definiciones)
    sin_llamada = sorted(definiciones - llamadas)
    if sin_def:
        alertas_diag.append(f"[NOTA] Llamadas sin definición: {sin_def}")
    if sin_llamada:
        alertas_diag.append(f"[NOTA] Definiciones sin llamada: {sin_llamada}")
    for roto in verificar_enlaces_locales(md_text, cap.ruta):
        alertas_diag.append(f"[ERROR] Enlace local roto: {roto}")
    err_s, adv_s = analizar_sintaxis_editorial(md_text, estado=cap.estado)
    for e in err_s:
        alertas_diag.append(f"[ERROR SINTAXIS] {e}")
    for a in adv_s:
        alertas_diag.append(f"[ADVERTENCIA] {a}")
    alerta_inv = verificar_texto_invitado(cap.archivo, md_text)
    if alerta_inv:
        alertas_diag.append(f"[PROTEGIDO] {alerta_inv}")
    for hp in detectar_encabezados_partidos(md_text):
        alertas_diag.append(f"[FORMATO] {hp}")
    n_ang = len(re.findall(r"[‹›]", md_text))
    if n_ang:
        alertas_diag.append(f"[COMILLAS] {n_ang} comilla(s) angular(es) simple(s) ‹› presentes")

    if alertas_diag:
        for item in alertas_diag:
            print(f"  - {item}")
    else:
        print("  - Sin alertas técnicas detectadas.")

    # 3. Fuentes externas asignadas
    print("\n--- 2. Fuentes externas mapeadas (`notas/fuentes/catalogo.yaml`) ---")
    catalogo = cargar_catalogo()
    cap_norm = cap.id.lstrip("0") or "0"
    fuentes_cap = []
    for e in catalogo.get("fuentes", []):
        for d in e.get("capitulos_destino") or []:
            d_str = str(d).strip()
            if d_str == cap.id or (d_str.isdigit() and cap.id.isdigit() and (d_str.lstrip("0") or "0") == cap_norm):
                fuentes_cap.append(e)
                break
    if fuentes_cap:
        for e in fuentes_cap:
            print(f"  - [{e.get('id')}] ({e.get('postura_dialogo')} | {e.get('idioma')}) -> {e.get('ficha')}")
            if e.get("cita_europea"):
                print(f"    Cita: {e['cita_europea']}")
    else:
        print("  - Ninguna fuente externa asignada todavía a este capítulo.")

    # 4. Referencias en notas/NOTAS.md
    print("\n--- 3. Referencias transversales en `notas/NOTAS.md` ---")
    refs_glob = referencias_en_notas_globales(cap.archivo)
    if refs_glob:
        for r in refs_glob:
            print(f"  - {r[:180]}")
    else:
        print("  - Sin menciones directas en `notas/NOTAS.md`.")

    # 5. Ficha espejo del capítulo
    ficha_path = REPO_ROOT / "notas" / "capitulos" / cap.archivo
    print(f"\n--- 4. Ficha espejo (`notas/capitulos/{cap.archivo}`) ---")
    if ficha_path.exists():
        print(ficha_path.read_text(encoding="utf-8").strip())
    else:
        print(f"  (No existe ficha todavía en `notas/capitulos/{cap.archivo}`.)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
