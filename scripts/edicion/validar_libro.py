#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador editorial para la Segunda Edición (y verificador del respaldo inmutable v1.0).

Comprueba:
1. Existencia de todos los archivos declarados en `libro.yaml` y detección de archivos `.md` huérfanos.
2. Unicidad de IDs y rutas en el manifiesto.
3. Integridad de notas al pie por capítulo (`[^n]` en texto <-> `[^n]:` en definiciones).
4. Enlaces Markdown relativos rotos entre capítulos.
5. (Opcional `--verificar-respaldo`) Verificación criptográfica SHA-256 de `respaldo_v1.0/md/`
   contra `respaldo_v1.0/manifiesto_v1.0.md`.
"""

import argparse
import hashlib
from pathlib import Path
import re
import sys
from typing import Dict, List, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    ESTADOS_VALIDOS,
    REPO_ROOT,
    buscar_capitulo,
    cargar_manifiesto,
)


def analizar_notas_al_pie(md_text: str) -> Tuple[Set[str], Set[str], List[str]]:
    """Devuelve (llamadas_en_cuerpo, definiciones, notas_invalidas)."""
    definiciones: Set[str] = set()
    llamadas: Set[str] = set()
    invalidas: List[str] = []

    for line in md_text.splitlines():
        if re.match(r"^\[\^nota\]:", line):
            invalidas.append("Definición huérfana '[^nota]:'")
            continue
        m_def = re.match(r"^\[\^([^\]]+)\]:\s*", line)
        if m_def:
            definiciones.add(m_def.group(1))
            resto = line[m_def.end() :]
            for ref in re.findall(r"\[\^([^\]]+)\](?!:)", resto):
                llamadas.add(ref)
        else:
            for ref in re.findall(r"\[\^([^\]]+)\](?!:)", line):
                llamadas.add(ref)

    return llamadas, definiciones, invalidas


def verificar_enlaces_locales(md_text: str, archivo_actual: Path) -> List[str]:
    rotos: List[str] = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md_text):
        tgt = target.strip().strip("<>")
        if not tgt or tgt.startswith(("http://", "https://", "mailto:", "#")):
            continue
        ruta_sin_ancla = tgt.split("#", 1)[0]
        if not ruta_sin_ancla:
            continue
        destino = (archivo_actual.parent / ruta_sin_ancla).resolve()
        if not destino.exists():
            rotos.append(tgt)
    return rotos


def verificar_respaldo_sha256() -> Tuple[int, List[str]]:
    respaldo_dir = REPO_ROOT / "respaldo_v1.0"
    manifiesto_sha = respaldo_dir / "manifiesto_v1.0.md"
    md_dir = respaldo_dir / "md"
    errores: List[str] = []

    if not manifiesto_sha.exists():
        return 0, [f"Falta el manifiesto criptográfico: {manifiesto_sha}"]

    esperados: Dict[str, Tuple[int, str]] = {}
    patron = re.compile(r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*([\d,]+)\s*\|\s*`([0-9a-f]{64})`\s*\|$")
    for line in manifiesto_sha.read_text(encoding="utf-8").splitlines():
        m = patron.match(line.strip())
        if m:
            fname = m.group(1)
            nbytes = int(m.group(2).replace(",", ""))
            sha = m.group(3)
            esperados[fname] = (nbytes, sha)

    if not esperados:
        return 0, [f"No se pudieron leer huellas SHA-256 desde {manifiesto_sha}"]

    for fname, (exp_bytes, exp_sha) in sorted(esperados.items()):
        fpath = md_dir / fname
        if not fpath.exists():
            errores.append(f"Archivo faltante en respaldo_v1.0/md/: {fname}")
            continue
        data = fpath.read_bytes()
        real_sha = hashlib.sha256(data).hexdigest()
        if len(data) != exp_bytes or real_sha != exp_sha:
            errores.append(
                f"Integridad alterada en respaldo_v1.0/md/{fname}: "
                f"esperado ({exp_bytes} B, {exp_sha[:12]}…), real ({len(data)} B, {real_sha[:12]}…)"
            )

    extra_files = sorted(
        p.name for p in md_dir.glob("*.md") if p.name not in esperados
    )
    for extra in extra_files:
        errores.append(f"Archivo no registrado dentro de respaldo_v1.0/md/: {extra}")

    return len(esperados), errores


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida la estructura, notas al pie, enlaces e integridad editorial del libro."
    )
    parser.add_argument(
        "--manifiesto",
        default=None,
        help="Ruta al manifiesto YAML (por defecto: libro.yaml)",
    )
    parser.add_argument(
        "--capitulo",
        default=None,
        help="Valida únicamente un capítulo específico por id o nombre de archivo (ej. 19 o 19_parte4_ensayo_3.md)",
    )
    parser.add_argument(
        "--verificar-respaldo",
        action="store_true",
        help="Verifica también las huellas SHA-256 de respaldo_v1.0/md/ contra respaldo_v1.0/manifiesto_v1.0.md",
    )
    parser.add_argument(
        "--estricto",
        action="store_true",
        help="Trata las advertencias (ej. archivos huérfanos o notas desparejadas) como errores",
    )
    args = parser.parse_args()

    manifiesto = cargar_manifiesto(args.manifiesto)
    errores: List[str] = []
    advertencias: List[str] = []

    ids_vistos: Set[str] = set()
    rutas_vistas: Set[Path] = set()

    total_palabras = 0
    total_notas = 0
    total_bloques = 0
    conteo_estados: Dict[str, int] = {e: 0 for e in ESTADOS_VALIDOS}
    usa_estados = False

    if args.capitulo:
        capitulos_a_validar = [buscar_capitulo(manifiesto, args.capitulo)]
    else:
        capitulos_a_validar = manifiesto.capitulos

    print(f"=== Validación Editorial: {manifiesto.obra.titulo} ({manifiesto.obra.version}) ===")
    print(f"Manifiesto:   {manifiesto.ruta_manifiesto.relative_to(REPO_ROOT)}")
    print(f"Carpeta base: {manifiesto.carpeta_base.relative_to(REPO_ROOT)}")
    if args.capitulo:
        c0 = capitulos_a_validar[0]
        estado_str = f" | Estado: {c0.estado}" if c0.estado else ""
        print(f"Capítulo:     [{c0.id}] {c0.archivo}{estado_str}\n")
    else:
        print(f"Secciones:    {len(manifiesto.secciones)} | Capítulos declarados: {len(manifiesto.capitulos)}\n")

    for cap in capitulos_a_validar:
        if cap.id in ids_vistos:
            errores.append(f"ID de capítulo duplicado en manifiesto: '{cap.id}'")
        ids_vistos.add(cap.id)

        if cap.ruta in rutas_vistas:
            errores.append(f"Archivo declarado dos veces en manifiesto: '{cap.archivo}'")
        rutas_vistas.add(cap.ruta)

        if cap.estado is not None:
            usa_estados = True
            if cap.estado not in ESTADOS_VALIDOS:
                errores.append(
                    f"[{cap.id}] Estado inválido '{cap.estado}' en manifiesto (válidos: {', '.join(ESTADOS_VALIDOS)})"
                )
            else:
                conteo_estados[cap.estado] += 1

        if not cap.ruta.exists():
            errores.append(f"[{cap.id}] Archivo inexistente: {cap.archivo}")
            continue

        md_text = cap.ruta.read_text(encoding="utf-8")
        if not md_text.strip():
            errores.append(f"[{cap.id}] Archivo vacío: {cap.archivo}")
            continue

        palabras = len(md_text.split())
        bloques = len([b for b in md_text.split("\n\n") if b.strip() and b.strip() != "---"])
        llamadas, definiciones, invalidas = analizar_notas_al_pie(md_text)

        total_palabras += palabras
        total_bloques += bloques
        total_notas += len(definiciones)

        for inv in invalidas:
            errores.append(f"[{cap.id}] {cap.archivo}: {inv}")

        sin_def = sorted(llamadas - definiciones)
        sin_llamada = sorted(definiciones - llamadas)
        if sin_def:
            advertencias.append(f"[{cap.id}] {cap.archivo}: llamadas a notas sin definición (revisar en 2.ª ed.): {sin_def}")
        if sin_llamada:
            advertencias.append(f"[{cap.id}] {cap.archivo}: definiciones de notas sin llamada en texto (revisar en 2.ª ed.): {sin_llamada}")

        enlaces_rotos = verificar_enlaces_locales(md_text, cap.ruta)
        for roto in enlaces_rotos:
            errores.append(f"[{cap.id}] {cap.archivo}: enlace local roto -> '{roto}'")

    # Detectar archivos .md huérfanos solo cuando se valida el libro completo
    if not args.capitulo and manifiesto.carpeta_base.is_dir():
        en_disco = sorted(p.resolve() for p in manifiesto.carpeta_base.rglob("*.md"))
        for p in en_disco:
            if p not in rutas_vistas:
                rel = p.relative_to(manifiesto.carpeta_base)
                advertencias.append(f"Archivo .md no registrado en manifiesto: '{rel}'")

    if args.verificar_respaldo:
        n_sha, err_sha = verificar_respaldo_sha256()
        if err_sha:
            errores.extend(err_sha)
        else:
            print(f"[OK] Respaldo inmutable verificado por SHA-256: {n_sha}/{n_sha} archivos íntegros en respaldo_v1.0/md/.")

    print(
        f"[RESUMEN] Capítulos: {len(capitulos_a_validar)} | Palabras: {total_palabras:,} | "
        f"Bloques: {total_bloques:,} | Notas al pie: {total_notas}"
    )
    if usa_estados and not args.capitulo:
        total_caps = len(capitulos_a_validar)
        pct = (conteo_estados["aprobado"] / total_caps * 100.0) if total_caps else 0.0
        print(
            f"[AVANCE]  Aprobados: {conteo_estados['aprobado']}/{total_caps} ({pct:.1f}%) | "
            f"En revisión: {conteo_estados['en_revision']} | Pendientes: {conteo_estados['pendiente']}"
        )

    if advertencias:
        print(f"\n[ADVERTENCIAS] ({len(advertencias)}):")
        for adv in advertencias:
            print(f"  - {adv}")

    if errores:
        print(f"\n[ERRORES] ({len(errores)}):")
        for err in errores:
            print(f"  - {err}")
        return 1

    if args.estricto and advertencias:
        print("\n[ERROR] Modo estricto activado: existen advertencias pendientes.")
        return 1

    print("\n[OK] Validación editorial superada sin errores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
