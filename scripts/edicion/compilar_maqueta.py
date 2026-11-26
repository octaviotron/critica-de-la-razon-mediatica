#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador editorial LuaLaTeX para la maqueta de la Segunda Edición
de *Crítica de la Razón Mediática* (Juan Barreto Cipriani).

Lee en solo lectura:
  - `libro.yaml` (o `--manifiesto`) vía `manifiesto.py`
  - `libro/*.md`
  - `maquetacion/diseno_2ed.yaml` y `maquetacion/plantilla/*.tex`
  - `fuente/FUENTES/` y `fuente/RAZON/images/` (y `maquetacion/activos/` si existen)

Escribe todos los artefactos temporales y el PDF final exclusivamente en `dist/maqueta/`
(ignorado por Git). Nunca modifica `libro/`, `respaldo_v1.0/`, `fuente/` ni `externos/`.
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (  # noqa: E402
    CapituloRef,
    LibroManifiesto,
    REPO_ROOT,
    buscar_capitulo,
    cargar_manifiesto,
    es_ruta_dentro_de_respaldo,
)

DISENO_POR_DEFECTO = REPO_ROOT / "maquetacion" / "diseno_2ed.yaml"
PLANTILLA_DIR = REPO_ROOT / "maquetacion" / "plantilla"
DIST_MAQUETA_DIR = REPO_ROOT / "dist" / "maqueta"
RUTAS_PROHIBIDAS_ESCRITURA = (
    REPO_ROOT / "respaldo_v1.0",
    REPO_ROOT / "fuente",
    REPO_ROOT / "externos",
    REPO_ROOT / "scripts" / "extraccion_v1",
)


def verificar_ruta_escritura_segura(ruta: Path) -> None:
    """Impide cualquier escritura en carpetas protegidas/inmutables."""
    resuelta = ruta.resolve()
    if es_ruta_dentro_de_respaldo(resuelta):
        raise PermissionError(f"Escritura bloqueada en respaldo_v1.0/: {resuelta}")
    for prohibida in RUTAS_PROHIBIDAS_ESCRITURA:
        try:
            resuelta.relative_to(prohibida.resolve())
            raise PermissionError(f"Escritura bloqueada en ruta protegida ({prohibida.name}/): {resuelta}")
        except ValueError:
            continue


def cargar_diseno(ruta_diseno: Path) -> Dict[str, Any]:
    if not ruta_diseno.exists():
        raise FileNotFoundError(f"No se encontró la configuración de diseño: {ruta_diseno}")
    with ruta_diseno.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def comando_salto(valor: str) -> str:
    val = (valor or "clearpage").strip().lower()
    if val == "cleardoublepage":
        return r"\cleardoublepage"
    if val in ("none", "ninguno", ""):
        return ""
    return r"\clearpage"


def escapar_latex(texto: str) -> str:
    reemplazos = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    out = texto
    for k, v in reemplazos:
        out = out.replace(k, v)
    return out


def sanitizar_para_amiga(texto: str, mapa_sanitizacion: Dict[str, str]) -> str:
    """Reemplaza caracteres ausentes en amiga4ever pro2.ttf para evitar glifos en blanco."""
    out = texto
    for k, v in mapa_sanitizacion.items():
        out = out.replace(k, v)
    return out


def resolver_imagen_origen(nombre: str, diseno: Dict[str, Any]) -> Optional[Path]:
    """Busca primero en maquetacion/activos/ (nuevos 2.ª ed.) y luego en fuente/RAZON/images/."""
    activos_dir = REPO_ROOT / diseno["portadillas"].get("carpeta_activos_2ed", "maquetacion/activos")
    origen_dir = REPO_ROOT / diseno["portadillas"].get("carpeta_origen", "fuente/RAZON/images")
    for carpeta in (activos_dir, origen_dir):
        cand = carpeta / nombre
        if cand.exists():
            return cand
    return None


def preparar_imagenes(
    diseno: Dict[str, Any],
    modo: str,
    img_dir: Path,
    hallazgos: List[str],
    requeridas: Optional[set] = None,
) -> Dict[str, Path]:
    verificar_ruta_escritura_segura(img_dir)
    img_dir.mkdir(parents=True, exist_ok=True)
    magick = shutil.which("magick") or shutil.which("convert")

    port_cfg = diseno["portadillas"]
    formato_tif = (
        port_cfg.get("formato_imprenta", "png")
        if modo == "imprenta"
        else port_cfg.get("formato_digital", "jpg")
    ).lower()
    calidad_jpg = str(port_cfg.get("calidad_jpg", 92))

    if requeridas is None:
        requeridas = (
            set(port_cfg.get("por_seccion", {}).values())
            | set(port_cfg.get("por_capitulo", {}).values())
            | {port_cfg.get("imagen_hoyo", "hoyo.jpg")}
        )
    else:
        requeridas = set(requeridas) | {port_cfg.get("imagen_hoyo", "hoyo.jpg")}

    mapa: Dict[str, Path] = {}
    for nombre in sorted(requeridas):
        if not nombre:
            continue
        src = resolver_imagen_origen(nombre, diseno)
        if src is None:
            hallazgos.append(f"[IMG FALTANTE] No se encontró activo gráfico: '{nombre}'")
            continue

        stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", src.stem).strip("_").lower()
        if src.suffix.lower() in (".tif", ".tiff"):
            if not magick:
                raise RuntimeError("Se requiere ImageMagick ('magick' o 'convert') para convertir portadillas .tif.")
            dst = img_dir / f"{stem}_{modo}.{formato_tif}"
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                cmd = [magick, str(src)]
                if modo == "imprenta":
                    cmd += ["-colorspace", "Gray", "-density", "300", str(dst)]
                else:
                    cmd += ["-colorspace", "sRGB", "-quality", calidad_jpg, str(dst)]
                subprocess.run(cmd, check=True, capture_output=True)
        else:
            dst = img_dir / f"{stem}{src.suffix.lower()}"
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                shutil.copy2(src, dst)
        mapa[nombre] = dst
    return mapa


def convertir_inline_latex(
    texto: str,
    notas_map: Dict[str, str],
    cap_id: str,
    hallazgos: List[str],
    permitir_notas: bool = True,
) -> str:
    """Convierte inline Markdown (enlaces, código `...`, énfasis y notas [^id]) a LaTeX seguro."""
    # Quitar enlaces Markdown [etiqueta](url) dejando solo etiqueta
    txt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)

    # Extraer llamadas a notas [^id] antes de escapar
    marcadores_notas: Dict[str, str] = {}

    def _reemp_nota(m: re.Match) -> str:
        fn_id = m.group(1)
        token = f"@@FN{len(marcadores_notas)}@@"
        if not permitir_notas:
            marcadores_notas[token] = ""
            return token
        cuerpo_nota = notas_map.get(fn_id)
        if cuerpo_nota is None:
            hallazgos.append(f"[{cap_id}] Llamada a nota sin definición: [^{fn_id}] (marca visible en PDF)")
            marcadores_notas[token] = rf"\textsuperscript{{[{escapar_latex(fn_id)}?]}}"
        else:
            nota_tex = convertir_inline_latex(cuerpo_nota, {}, cap_id, hallazgos, permitir_notas=False)
            marcadores_notas[token] = rf"\footnote{{{nota_tex}}}"
        return token

    txt = re.sub(r"\[\^([^\]]+)\]", _reemp_nota, txt)

    # Extraer backticks inline (`...`) antes de escapar (Bug E: evita que TeX los vuelva comillas ‘...‘)
    marcadores_code: Dict[str, str] = {}

    def _reemp_code(m: re.Match) -> str:
        token = f"@@CD{len(marcadores_code)}@@"
        contenido = escapar_latex(m.group(1))
        marcadores_code[token] = rf"\textup{{{contenido}}}"
        return token

    txt = re.sub(r"`([^`]+)`", _reemp_code, txt)
    # Limpiar cualquier backtick huérfano residual
    txt = txt.replace("`", "'")

    if txt.count("*") % 2 == 1:
        hallazgos.append(f"[{cap_id}] Asterisco impar detectado en bloque: {texto[:70]!r}...")

    esc = escapar_latex(txt)
    esc = re.sub(r"\*\*\*([^\*]+?)\*\*\*", r"\\textbf{\\textit{\1}}", esc)
    esc = re.sub(r"\*\*([^\*]+?)\*\*", r"\\textbf{\1}", esc)
    esc = re.sub(r"\*([^\*]+?)\*", r"\\textit{\1}", esc)
    esc = esc.replace("*", "")

    for token, rep in marcadores_code.items():
        esc = esc.replace(token, rep)
    for token, rep in marcadores_notas.items():
        esc = esc.replace(token, rep)

    return esc


def aplicar_capitular(parrafo_tex: str, diseno: Dict[str, Any]) -> str:
    """Aplica \\lettrine a la primera letra y resto de la primera palabra (Bug F resuelto)."""
    cap_cfg = diseno.get("capitular", {})
    if not cap_cfg.get("activa", True):
        return parrafo_tex

    s = parrafo_tex.lstrip()
    m = re.match(r"^([A-ZÁÉÍÓÚÜÑ])([a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]*)(.*)$", s, re.S)
    if not m:
        return parrafo_tex

    inicial = m.group(1)
    resto_pal = m.group(2)
    resto = m.group(3)

    fuente_key = str(cap_cfg.get("fuente", "amiga")).lower()
    fuente_cmd = {
        "amiga": r"\amigafont",
        "swis": r"\swisfont",
        "bauhaus": r"\bauhausfont",
    }.get(fuente_key, r"\amigafont")

    lineas = cap_cfg.get("lineas", 3)
    lhang = cap_cfg.get("lhang", 0.05)
    findent = cap_cfg.get("findent_pt", 1.5)
    nindent = cap_cfg.get("nindent_pt", 0.0)

    return (
        rf"\lettrine[lines={lineas},lhang={lhang},findent={findent}pt,nindent={nindent}pt]"
        rf"{{{fuente_cmd} {inicial}}}{{{resto_pal}}}{resto}"
    )


def separar_notas_y_cuerpo(md_text: str) -> Tuple[List[str], Dict[str, str]]:
    """Separa líneas del cuerpo principal y diccionario de definiciones [^id]: texto."""
    lines = md_text.splitlines()
    cuerpo: List[str] = []
    notas: Dict[str, str] = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m_fn = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", line.strip())
        if m_fn:
            fn_id = m_fn.group(1)
            fn_body = m_fn.group(2).strip()
            i += 1
            while (
                i < n
                and lines[i].strip()
                and not re.match(r"^\[\^[^\]]+\]:", lines[i].strip())
                and not lines[i].strip().startswith("#")
            ):
                fn_body += " " + lines[i].strip()
                i += 1
            notas[fn_id] = fn_body
            continue
        cuerpo.append(line)
        i += 1
    while cuerpo and not cuerpo[-1].strip():
        cuerpo.pop()
    if cuerpo and cuerpo[-1].strip() == "---":
        cuerpo.pop()
    return cuerpo, notas


def render_titulo_dual(
    titulo: str,
    mapa_sanitizacion: Dict[str, str],
    subtitulo_linea2: Optional[str] = None,
) -> str:
    """Replica el estilo dual de 2006: línea superior Bauhaus 93 + inferior Amiga Forever Pro2."""
    t1 = escapar_latex(sanitizar_para_amiga(titulo.upper(), mapa_sanitizacion))
    if subtitulo_linea2:
        t2 = escapar_latex(sanitizar_para_amiga(subtitulo_linea2.upper(), mapa_sanitizacion))
        return (
            r"\begin{center}" + "\n"
            r"{\bauhausfont\fontsize{17}{20}\selectfont " + t1 + r"\par}\vspace{3pt}" + "\n"
            r"{\amigafont\fontsize{10.5}{14}\selectfont " + t2 + r"\par}" + "\n"
            r"\end{center}\vspace{8pt}"
        )
    palabras = titulo.strip().split()
    if len(palabras) >= 4:
        mitad = max(2, len(palabras) // 2)
        p1 = escapar_latex(sanitizar_para_amiga(" ".join(palabras[:mitad]).upper(), mapa_sanitizacion))
        p2 = escapar_latex(sanitizar_para_amiga(" ".join(palabras[mitad:]).upper(), mapa_sanitizacion))
        return (
            r"\begin{center}" + "\n"
            r"{\bauhausfont\fontsize{15.5}{19}\selectfont " + p1 + r"\par}\vspace{3pt}" + "\n"
            r"{\amigafont\fontsize{9.5}{13}\selectfont " + p2 + r"\par}" + "\n"
            r"\end{center}\vspace{8pt}"
        )
    return (
        r"\begin{center}" + "\n"
        r"{\bauhausfont\fontsize{16.5}{20}\selectfont " + t1 + r"\par}" + "\n"
        r"\end{center}\vspace{8pt}"
    )


def consumir_bloque_cita(lines: List[str], i: int) -> Tuple[List[str], int]:
    """
    Consume un bloque `> ...` completo y fusiona un bloque `> — Autor` inmediatamente
    posterior separado por líneas en blanco (Bug D: evita firmas huérfanas en página siguiente).
    """
    n = len(lines)
    q_lines: List[str] = []
    while i < n and lines[i].strip().startswith(">"):
        q_clean = re.sub(r"^>\s?", "", lines[i].strip())
        if q_clean:
            q_lines.append(q_clean)
        i += 1

    # Mirar hacia adelante por si la atribución (> — Autor) viene tras líneas en blanco
    j = i
    while j < n and not lines[j].strip():
        j += 1
    if j < n and lines[j].strip().startswith(">"):
        cand = re.sub(r"^>\s?", "", lines[j].strip())
        if cand.startswith(("—", "-", "–")):
            i = j
            while i < n and lines[i].strip().startswith(">"):
                q_clean = re.sub(r"^>\s?", "", lines[i].strip())
                if q_clean:
                    q_lines.append(q_clean)
                i += 1
    return q_lines, i


def render_bloque_cita_latex(
    q_lines: List[str],
    notas_map: Dict[str, str],
    cap_id: str,
    hallazgos: List[str],
    forzar_epigrafe: bool = False,
) -> str:
    es_epigrafe = (
        forzar_epigrafe
        or any(ql.startswith("—") for ql in q_lines)
        or (len(q_lines) <= 3 and all(ql.startswith("*") and ql.endswith("*") for ql in q_lines))
    )
    out: List[str] = []
    if es_epigrafe:
        out.append(r"\begin{epigrafe2006}")
        for ql in q_lines:
            if ql.startswith("—"):
                autor_ep = convertir_inline_latex(ql.lstrip("— "), notas_map, cap_id, hallazgos)
                out.append(rf"\vspace{{3pt}}\textbf{{{autor_ep}}}\par")
            else:
                txt_ep = convertir_inline_latex(ql, notas_map, cap_id, hallazgos)
                out.append(txt_ep + r"\par")
        out.append(r"\end{epigrafe2006}")
    else:
        out.append(r"\begin{citabando2006}")
        for ql in q_lines:
            out.append(convertir_inline_latex(ql, notas_map, cap_id, hallazgos) + r"\par")
        out.append(r"\end{citabando2006}")
    return "\n".join(out)


def extraer_apertura_parte(
    cuerpo_lines: List[str],
    es_primero_de_parte: bool,
) -> Tuple[List[str], List[str]]:
    """
    Para archivos de apertura de Parte (`08`, `11`, `14`, `17`, `21`, `25`), extrae el
    encabezado `# <N-ésima> Parte ...` y su epígrafe de Parte para colocarlos en la
    página titular de la Parte, devolviendo (epigrafe_parte_lines, resto_del_ensayo).
    Resuelve Bug C (títulos duplicados y mezcla de epígrafes Parte/Ensayo I).
    """
    if not es_primero_de_parte or not cuerpo_lines:
        return [], cuerpo_lines

    i = 0
    n = len(cuerpo_lines)
    while i < n and not cuerpo_lines[i].strip():
        i += 1
    if i >= n:
        return [], cuerpo_lines

    primera = cuerpo_lines[i].strip()
    if not re.match(r"^#\s+(Primera|Segunda|Tercera|Cuarta|Quinta|Sexta)\s+Parte\b", primera, re.IGNORECASE):
        return [], cuerpo_lines

    # Saltar la línea `# <N> Parte ...` (y cualquier continuación inmediata `#`/`##` de ese título)
    i += 1
    while i < n and (not cuerpo_lines[i].strip() or (cuerpo_lines[i].strip().startswith(("## ", "# ")) and not re.match(r"^#\s+[IVX]+\b", cuerpo_lines[i].strip()))):
        if cuerpo_lines[i].strip().startswith(">"):
            break
        i += 1

    # Consumir el epígrafe de la Parte si está presente
    epigrafe_parte: List[str] = []
    if i < n and cuerpo_lines[i].strip().startswith(">"):
        epigrafe_parte, i = consumir_bloque_cita(cuerpo_lines, i)

    return epigrafe_parte, cuerpo_lines[i:]


def saltar_encabezado_apertura_ensayo(lines: List[str], cap: CapituloRef) -> int:
    """
    Salta los encabezados iniciales de apertura del capítulo (`#`, `##`, o `###` en mayúsculas
    que formen parte de un título partido de QuarkXPress), ya que el título limpio del capítulo
    se imprime desde `libro.yaml`. Preserva `00_preliminares.md` completo.
    """
    if cap.tipo == "preliminares":
        return 0

    i = 0
    n = len(lines)
    visto_titulo = False
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith(("# ", "## ")):
            visto_titulo = True
            i += 1
            continue
        # En algunos ensayos (ej. 08: `### INFORMACIÓN-COMUNICACIÓN`), la 3.ª línea del título partido es ### TODO MAYÚSCULAS
        if visto_titulo and s.startswith("### "):
            t = s[4:].strip()
            letras = [ch for ch in t if ch.isalpha()]
            if letras and sum(1 for ch in letras if ch.isupper()) / len(letras) >= 0.85:
                i += 1
                continue
        break
    return i


def convertir_capitulo_a_latex(
    cap: CapituloRef,
    diseno: Dict[str, Any],
    hallazgos: List[str],
    cabecera_seccion: str,
    es_primero_de_parte: bool,
    cuerpo_lines: Optional[List[str]] = None,
    notas_map: Optional[Dict[str, str]] = None,
) -> str:
    if cuerpo_lines is None or notas_map is None:
        md_text = cap.ruta.read_text(encoding="utf-8")
        cuerpo_lines, notas_map = separar_notas_y_cuerpo(md_text)

    saltos_cfg = diseno.get("paginacion_saltos", {})
    mapa_amiga = diseno.get("tipografia", {}).get("sanitizacion_amiga", {})
    incluir_sub_toc = bool(diseno.get("indice_general", {}).get("incluir_subsecciones", False))
    excluir_cap = set(diseno.get("capitular", {}).get("excluir_tipos", []))

    out: List[str] = []

    # Salto configurable por tipo de capítulo (clave para controlar páginas vacías)
    if cap.tipo == "preliminares":
        salto = comando_salto(saltos_cfg.get("salto_preliminares", "clearpage"))
    elif cap.tipo == "anexo":
        salto = comando_salto(saltos_cfg.get("salto_anexo", "clearpage"))
    elif cap.tipo in ("epilogo", "post_scriptum", "bibliografia", "glosario", "onomastico"):
        salto = comando_salto(saltos_cfg.get("salto_capitulos_cierre", "clearpage"))
    elif es_primero_de_parte:
        salto = comando_salto(saltos_cfg.get("salto_primero_de_parte", "clearpage"))
    else:
        salto = comando_salto(saltos_cfg.get("salto_entre_ensayos", "clearpage"))

    if salto:
        out.append(salto)

    # Configurar cabecera corrida y reiniciar notas al pie si aplica
    cab_sec_tex = escapar_latex(cabecera_seccion)
    titulo_corto = cap.titulo.split("—")[0].split(":")[0].strip()
    if len(titulo_corto) > 42:
        titulo_corto = titulo_corto[:39] + "…"
    cab_cap_tex = escapar_latex(titulo_corto)

    if diseno.get("notas_al_pie", {}).get("reiniciar_por_capitulo", True):
        out.append(r"\setcounter{footnote}{0}")
    out.append(rf"\renewcommand{{\runningpart}}{{{cab_sec_tex}}}")
    out.append(rf"\renewcommand{{\runningessay}}{{{cab_cap_tex}}}")

    if cap.tipo != "preliminares":
        toc_title = escapar_latex(cap.titulo)
        out.append(rf"\phantomsection\addcontentsline{{toc}}{{chapter}}{{{toc_title}}}")

    if cap.tipo == "preliminares":
        out.append(r"\thispagestyle{empty}")
    else:
        out.append(r"\thispagestyle{plain2006}")
        out.append(r"\vspace*{6mm}")
        out.append(render_titulo_dual(cap.titulo, mapa_amiga))

    i = saltar_encabezado_apertura_ensayo(cuerpo_lines, cap)
    n = len(cuerpo_lines)

    capitular_aplicada = cap.tipo in excluir_cap or not diseno.get("capitular", {}).get("activa", True)
    en_lista = False

    def cerrar_lista() -> None:
        nonlocal en_lista
        if en_lista:
            out.append(r"\end{itemize}")
            en_lista = False

    while i < n:
        line = cuerpo_lines[i].rstrip()
        s = line.strip()
        if not s:
            i += 1
            continue

        if s == "---":
            cerrar_lista()
            out.append(r"\separadorInterno")
            i += 1
            continue

        if s.startswith("# "):
            cerrar_lista()
            t = s[2:].strip()
            if re.match(r"^[-–—]+$", t):
                hallazgos.append(f"[{cap.id}] Encabezado guion suelto ignorado en maqueta: {s!r}")
            else:
                out.append(r"\vspace{8pt}" + render_titulo_dual(t, mapa_amiga))
            i += 1
            continue

        if s.startswith("## "):
            cerrar_lista()
            t = s[3:].strip()
            if re.match(r"^[-–—]+$", t):
                hallazgos.append(f"[{cap.id}] Encabezado guion suelto ignorado en maqueta: {s!r}")
            else:
                t_tex = escapar_latex(sanitizar_para_amiga(t, mapa_amiga))
                out.append(
                    r"\needspace{4\baselineskip}\vspace{10pt}"
                    rf"\noindent{{\amigafont\fontsize{{8.5}}{{12}}\selectfont {t_tex}}}\par\nopagebreak\vspace{{5pt}}"
                )
                if incluir_sub_toc:
                    out.append(rf"\addcontentsline{{toc}}{{section}}{{{escapar_latex(t)}}}")
            i += 1
            continue

        if s.startswith("### "):
            cerrar_lista()
            t = s[4:].strip()
            if re.match(r"^[-–—]+$", t):
                hallazgos.append(f"[{cap.id}] Sub-encabezado guion suelto ignorado en maqueta: {s!r}")
            else:
                t_tex = escapar_latex(t)
                out.append(
                    r"\needspace{3\baselineskip}\vspace{8pt}"
                    rf"\noindent\textbf{{\large {t_tex}}}\par\nopagebreak\vspace{{4pt}}"
                )
            i += 1
            continue

        if s.startswith(">"):
            cerrar_lista()
            q_lines, i = consumir_bloque_cita(cuerpo_lines, i)
            if q_lines:
                out.append(render_bloque_cita_latex(q_lines, notas_map, cap.id, hallazgos))
            continue

        m_li = re.match(r"^(\s*)-\s+(.*)$", line)
        if m_li:
            item_tex = convertir_inline_latex(m_li.group(2).strip(), notas_map, cap.id, hallazgos)
            if cap.tipo in ("bibliografia", "onomastico"):
                out.append(rf"\noindent\hangindent=6mm\hangafter=1 {item_tex}\par\vspace{{2pt}}")
            else:
                if not en_lista:
                    out.append(r"\begin{itemize}")
                    en_lista = True
                out.append(rf"\item {item_tex}")
            i += 1
            continue

        # Párrafo normal
        cerrar_lista()
        p_lines = [s]
        i += 1
        while i < n:
            nxt = cuerpo_lines[i].strip()
            if not nxt or nxt == "---" or nxt.startswith(("#", ">", "- ")):
                break
            p_lines.append(nxt)
            i += 1
        raw_p = " ".join(p_lines)

        if cap.tipo == "glosario" and raw_p.startswith("·"):
            m_g = re.match(r"^·\s*([^:\n]+?):\s*(.*)$", raw_p)
            if m_g:
                term = escapar_latex(m_g.group(1).strip().strip("*"))
                body = convertir_inline_latex(m_g.group(2).strip(), notas_map, cap.id, hallazgos)
                out.append(rf"\noindent\textbf{{· {term}:}} {body}\par\vspace{{4pt}}")
            else:
                out.append(
                    r"\noindent "
                    + convertir_inline_latex(raw_p, notas_map, cap.id, hallazgos)
                    + r"\par\vspace{4pt}"
                )
            continue

        p_tex = convertir_inline_latex(raw_p, notas_map, cap.id, hallazgos)
        if not capitular_aplicada:
            p_tex = aplicar_capitular(p_tex, diseno)
            capitular_aplicada = True
            out.append(r"\noindent " + p_tex + "\n")
        else:
            out.append(p_tex + "\n")

    cerrar_lista()
    return "\n".join(out)


def construir_bloque_marco_externo(diseno: Dict[str, Any], hoyo_path: str) -> str:
    mc = diseno.get("marco_externo", {})
    if not mc.get("activo", True):
        return r"\newcommand{\dibujarMarcoExterno}{}"

    x_off = mc.get("x_offset_mm", 8.5)
    l_sup = mc.get("linea_superior_largo_mm", 16.5)
    f_y = mc.get("folio_y_mm", 17.2)
    f_pt = mc.get("folio_pt", 9.0)
    l_inf = mc.get("linea_inferior_alto_mm", 42.0)
    h_y = mc.get("hoyo_y_mm", 41.5)
    h_w = mc.get("hoyo_ancho_mm", 5.5)
    r_y = mc.get("rotulo_y_mm", 10.0)
    txt_b = escapar_latex(mc.get("texto_superior_bauhaus", "Crítica de la "))
    txt_a = escapar_latex(mc.get("texto_superior_amiga", "Razón Mediática"))
    firma = escapar_latex(mc.get("firma_autor", "Juan Barreto"))
    x_rot_ext = round(x_off + 1.1, 2)
    x_rot_int = round(x_off - 1.1, 2)

    nodo_hoyo_impar = (
        rf"\node[anchor=south,inner sep=0pt] at ([xshift=-{x_off}mm,yshift={h_y}mm]current page.south east) "
        rf"{{\includegraphics[width={h_w}mm]{{{hoyo_path}}}}};"
        if hoyo_path
        else ""
    )
    nodo_hoyo_par = (
        rf"\node[anchor=south,inner sep=0pt] at ([xshift={x_off}mm,yshift={h_y}mm]current page.south west) "
        rf"{{\includegraphics[width={h_w}mm]{{{hoyo_path}}}}};"
        if hoyo_path
        else ""
    )

    return rf"""\newcommand{{\dibujarMarcoExterno}}{{%
  \begin{{tikzpicture}}[remember picture,overlay]
    \ifodd\value{{page}}
      \draw[line width=0.45pt,black] ([xshift=-{x_off}mm]current page.north east) -- ([xshift=-{x_off}mm,yshift=-{l_sup}mm]current page.north east);
      \node[anchor=north,inner sep=1pt] at ([xshift=-{x_off}mm,yshift=-{f_y}mm]current page.north east) {{\bauhausfont\fontsize{{{f_pt}}}{{{f_pt + 1}}}\selectfont\thepage}};
      \draw[line width=0.45pt,black] ([xshift=-{x_off}mm]current page.south east) -- ([xshift=-{x_off}mm,yshift={l_inf}mm]current page.south east);
      {nodo_hoyo_impar}
      \node[rotate=90,anchor=south west,inner sep=0pt] at ([xshift=-{x_rot_ext}mm,yshift={r_y}mm]current page.south east) {{\bauhausfont\fontsize{{5.2}}{{6}}\selectfont {txt_b}\amigafont\fontsize{{4.2}}{{5}}\selectfont {txt_a}}};
      \node[rotate=90,anchor=north west,inner sep=0pt] at ([xshift=-{x_rot_int}mm,yshift={r_y}mm]current page.south east) {{\swisfont\fontsize{{4.8}}{{5.5}}\selectfont {firma}}};
    \else
      \draw[line width=0.45pt,black] ([xshift={x_off}mm]current page.north west) -- ([xshift={x_off}mm,yshift=-{l_sup}mm]current page.north west);
      \node[anchor=north,inner sep=1pt] at ([xshift={x_off}mm,yshift=-{f_y}mm]current page.north west) {{\bauhausfont\fontsize{{{f_pt}}}{{{f_pt + 1}}}\selectfont\thepage}};
      \draw[line width=0.45pt,black] ([xshift={x_off}mm]current page.south west) -- ([xshift={x_off}mm,yshift={l_inf}mm]current page.south west);
      {nodo_hoyo_par}
      \node[rotate=90,anchor=south west,inner sep=0pt] at ([xshift={x_rot_int}mm,yshift={r_y}mm]current page.south west) {{\bauhausfont\fontsize{{5.2}}{{6}}\selectfont {txt_b}\amigafont\fontsize{{4.2}}{{5}}\selectfont {txt_a}}};
      \node[rotate=90,anchor=north west,inner sep=0pt] at ([xshift={x_rot_ext}mm,yshift={r_y}mm]current page.south west) {{\swisfont\fontsize{{4.8}}{{5.5}}\selectfont {firma}}};
    \fi
  \end{{tikzpicture}}%
}}"""


def ensamblar_tex(
    manifiesto: LibroManifiesto,
    diseno: Dict[str, Any],
    imgs: Dict[str, Path],
    modo: str,
    hallazgos: List[str],
    capitulo_unico: Optional[CapituloRef] = None,
) -> str:
    tpl_maestra = (PLANTILLA_DIR / "libro_2ed.tex").read_text(encoding="utf-8")
    tpl_especiales = (PLANTILLA_DIR / "estilos_especiales.tex").read_text(encoding="utf-8")

    pag = diseno["pagina"]
    tip = diseno["tipografia"]
    cab = diseno["cabecera"]
    ind = diseno["indice_general"]
    not_cfg = diseno["notas_al_pie"]
    port_cfg = diseno["portadillas"]
    saltos = diseno["paginacion_saltos"]
    ed = diseno["edicion"]
    mapa_amiga = tip.get("sanitizacion_amiga", {})

    fuentes_dir_tex = (REPO_ROOT / tip["carpeta_fuentes"]).resolve().as_posix() + "/"
    hoyo_key = port_cfg.get("imagen_hoyo", "hoyo.jpg")
    hoyo_path = imgs[hoyo_key].resolve().as_posix() if hoyo_key in imgs else ""

    # Modo imprenta: marcas de corte y sangrado (si crop.sty existe o con geometry ampliado)
    paquete_crop = ""
    if modo == "imprenta":
        bleed = float(pag.get("sangrado_mm", 3.0))
        w_imp = round(float(pag["ancho_mm"]) + 2 * bleed + 14.0, 2)
        h_imp = round(float(pag["alto_mm"]) + 2 * bleed + 14.0, 2)
        paquete_crop = (
            rf"\IfFileExists{{crop.sty}}{{\usepackage[cam,center,width={w_imp}mm,height={h_imp}mm]{{crop}}}}{{}}"
        )

    # Bloque de cabecera corrida
    if cab.get("activa", True):
        cab_pt = cab.get("tamano_pt", 7.8)
        ratio_fil = cab.get("ancho_filete_ratio", 0.42)
        grosor_fil = cab.get("grosor_filete_pt", 0.35)
        bloque_cab = (
            r"\parbox[b]{\textwidth}{%" + "\n"
            rf"      \fontsize{{{cab_pt}}}{{{round(cab_pt + 1.2, 1)}}}\selectfont"
            r"\textcolor{headergray}{\runningpart\ /\ }\runningessay\\[-1pt]" + "\n"
            rf"      \textcolor{{rulegray}}{{\rule{{{ratio_fil}\textwidth}}{{{grosor_fil}pt}}}}" + "\n"
            r"    }%"
        )
    else:
        bloque_cab = ""

    # Páginas blancas limpias tras \cleardoublepage
    limpiar_blancas = ""
    if saltos.get("limpiar_paginas_blancas", True):
        limpiar_blancas = (
            r"\makeatletter" + "\n"
            r"\def\cleardoublepage{\clearpage\if@twoside\ifodd\c@page\else"
            r"\hbox{}\thispagestyle{empty}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}" + "\n"
            r"\makeatother"
        )

    # Capitular: texto normal vs versalitas
    cfg_cap_txt = (
        r"\renewcommand{\LettrineTextFont}{\normalfont}"
        if diseno.get("capitular", {}).get("texto_normal", True)
        else ""
    )

    # Notas al pie estilo 2006 (número plano colgante) vs superíndice
    if not_cfg.get("estilo", "plano_2006") == "plano_2006":
        sangria_fn = not_cfg.get("sangria_colgante_em", 1.4)
        estilo_notas = (
            r"\makeatletter" + "\n"
            r"\renewcommand\@makefntext[1]{%" + "\n"
            rf"  \noindent\hangindent={sangria_fn}em\hangafter=1%" + "\n"
            rf"  \makebox[{sangria_fn}em][l]{{\@thefnmark}}#1%" + "\n"
            r"}" + "\n"
            r"\makeatother"
        )
    else:
        estilo_notas = ""

    # Relleno con puntos guía en TOC
    toc_relleno = (
        r"\leaders\hbox{$\m@th\mkern \@dotsep mu\hbox{.}\mkern \@dotsep mu$}\hfill"
        if ind.get("puntos_guia", True)
        else r"\hfill"
    )

    # Rellenar estilos_especiales.tex
    reemp_esp = {
        "%%CONFIG_CAPITULAR_TEXTO%%": cfg_cap_txt,
        "%%ANCHO_FILETE_NOTA%%": str(not_cfg.get("ancho_filete_ratio", 0.36)),
        "%%NOTA_PT%%": str(not_cfg.get("tamano_pt", 8.2)),
        "%%NOTA_INTERLINEADO_PT%%": str(not_cfg.get("interlineado_pt", 10.0)),
        "%%ESTILO_NOTAS_AL_PIE%%": estilo_notas,
        "%%SALTO_PORTADILLA_GRAFICA%%": comando_salto(saltos.get("portadillas_graficas", "cleardoublepage")),
        "%%SALTO_PORTADILLA_TIPOGRAFICA%%": comando_salto(saltos.get("portadillas_tipograficas", "cleardoublepage")),
        "%%PORTADILLA_ANCHO_MM%%": str(port_cfg.get("ancho_mm", 125.0)),
        "%%PORTADILLA_ALTO_MM%%": str(port_cfg.get("alto_mm", 185.0)),
        "%%TOC_DEPTH%%": str(ind.get("profundidad_toc", 0)),
        "%%TOC_ESPACIO_PARTE_PT%%": str(ind.get("espacio_antes_parte_pt", 8.0)),
        "%%TOC_PARTE_PT%%": str(ind.get("tamano_parte_pt", 9.5)),
        "%%TOC_ESPACIO_CAP_PT%%": str(ind.get("espacio_antes_capitulo_pt", 2.5)),
        "%%TOC_CAP_PT%%": str(ind.get("tamano_capitulo_pt", 7.5)),
        "%%TOC_SEC_PT%%": str(ind.get("tamano_seccion_pt", 7.0)),
        "%%TOC_INTERLINEADO_PT%%": str(ind.get("interlineado_pt", 9.2)),
        "%%TOC_RELLENO_CAP%%": toc_relleno,
        "%%SALTO_INDICE_GENERAL%%": comando_salto(saltos.get("salto_indice_general", "cleardoublepage")),
        "%%SUBTITULO_INDICE%%": escapar_latex(ed.get("subtitulo_indice", "Segunda Edición")),
        "%%TITULO_INDICE%%": escapar_latex(ind.get("titulo", "ÍNDICE GENERAL")),
    }
    estilos_render = tpl_especiales
    for k, v in reemp_esp.items():
        estilos_render = estilos_render.replace(k, v)

    # Construir cuerpo del libro (o de un único capítulo)
    cuerpo: List[str] = []
    usa_romana = pag.get("numeracion", "arabiga_continua") == "romana_preliminares"
    inicio_num = r"\frontmatter" if (usa_romana and capitulo_unico is None) else r"\pagenumbering{arabic}"
    mainmatter_iniciado = not usa_romana

    if capitulo_unico is None and ed.get("mostrar_portada_interior", True):
        salto_portada = comando_salto(saltos.get("salto_tras_portada_interior", "cleardoublepage"))
        cuerpo.append(
            "\n".join(
                [
                    r"\thispagestyle{empty}",
                    r"\vspace*{28mm}",
                    r"\begin{center}",
                    rf"  {{\bauhausfont\fontsize{{22}}{{26}}\selectfont {escapar_latex(ed.get('titulo_linea_1', 'CRÍTICA DE LA RAZÓN'))}\par}}\vspace{{4pt}}",
                    rf"  {{\amigafont\fontsize{{14}}{{18}}\selectfont {escapar_latex(ed.get('titulo_linea_2', 'MEDIÁTICA'))}\par}}\vspace{{10mm}}",
                    rf"  {{\itshape\fontsize{{11}}{{14}}\selectfont {ed.get('subtitulo_obra', '')}\par}}\vspace{{18mm}}",
                    rf"  {{\bauhausfont\fontsize{{14}}{{18}}\selectfont {escapar_latex(ed.get('autor_portada', 'JUAN BARRETO CIPRIANI'))}\par}}\vspace{{22mm}}",
                    rf"  {{\fontsize{{9.5}}{{12}}\selectfont {escapar_latex(ed.get('etiqueta_portada', 'SEGUNDA EDICIÓN'))}\par}}",
                    r"\end{center}",
                    salto_portada,
                ]
            )
        )

    por_seccion = port_cfg.get("por_seccion", {})
    por_capitulo = port_cfg.get("por_capitulo", {})
    tipograficas_tipo = port_cfg.get("tipograficas_por_tipo", {})
    pagina_parte_sep = bool(saltos.get("pagina_titular_parte_separada", True))

    for sec in manifiesto.secciones:
        caps_sec = (
            [c for c in sec.capitulos if c.id == capitulo_unico.id]
            if capitulo_unico is not None
            else sec.capitulos
        )
        if not caps_sec:
            continue

        # Portadilla de sección (en libro completo, o si el capítulo único es el primero de su sección)
        es_inicio_seccion = capitulo_unico is None or sec.capitulos[0].id == capitulo_unico.id
        img_sec = por_seccion.get(sec.id) if es_inicio_seccion else None

        # Pre-extraer epígrafe de Parte del primer capítulo si corresponde (Bug C)
        epigrafe_parte_lines: List[str] = []
        pre_cuerpo_primero: Optional[Tuple[List[str], Dict[str, str]]] = None
        if sec.id.startswith("parte_") and es_inicio_seccion and caps_sec:
            primer_cap = caps_sec[0]
            md_txt = primer_cap.ruta.read_text(encoding="utf-8")
            c_lines, n_map = separar_notas_y_cuerpo(md_txt)
            epigrafe_parte_lines, resto_lines = extraer_apertura_parte(c_lines, True)
            pre_cuerpo_primero = (resto_lines, n_map)

        if img_sec and img_sec in imgs:
            if not mainmatter_iniciado and sec.id in ("apertura", "parte_1"):
                cuerpo.append(r"\mainmatter")
                mainmatter_iniciado = True
            cuerpo.append(rf"\portadillaGrafica{{{imgs[img_sec].resolve().as_posix()}}}")
            if sec.id.startswith("parte_") and pagina_parte_sep:
                partes_t = sec.titulo.split(":", 1)
                p_num = escapar_latex(partes_t[0].strip())
                p_nom = partes_t[1].strip() if len(partes_t) > 1 else sec.titulo
                cuerpo.append(r"\thispagestyle{plain2006}\vspace*{20mm}")
                cuerpo.append(
                    rf"\begin{{center}}{{\fontsize{{13}}{{16}}\selectfont {p_num}\par}}\vspace{{10mm}}\end{{center}}"
                )
                cuerpo.append(render_titulo_dual(p_nom, mapa_amiga))
                if epigrafe_parte_lines:
                    cuerpo.append(r"\vspace{8mm}")
                    cuerpo.append(
                        render_bloque_cita_latex(
                            epigrafe_parte_lines,
                            pre_cuerpo_primero[1] if pre_cuerpo_primero else {},
                            caps_sec[0].id,
                            hallazgos,
                            forzar_epigrafe=True,
                        )
                    )
                if capitulo_unico is None:
                    cuerpo.append(rf"\phantomsection\addcontentsline{{toc}}{{part}}{{{escapar_latex(sec.titulo)}}}")
                cuerpo.append(r"\clearpage")
            elif capitulo_unico is None:
                cuerpo.append(rf"\phantomsection\addcontentsline{{toc}}{{part}}{{{escapar_latex(sec.titulo)}}}")

        for idx_cap, cap in enumerate(caps_sec):
            if cap.tipo == "indice":
                if capitulo_unico is None:
                    cuerpo.append(r"\tableofcontents")
                continue

            if not mainmatter_iniciado and sec.id == "apertura":
                cuerpo.append(r"\mainmatter")
                mainmatter_iniciado = True

            img_cap = por_capitulo.get(cap.id)
            if img_cap and img_cap in imgs:
                cuerpo.append(rf"\portadillaGrafica{{{imgs[img_cap].resolve().as_posix()}}}")
            elif cap.tipo in tipograficas_tipo:
                t_cfg = tipograficas_tipo[cap.tipo]
                cuerpo.append(
                    rf"\portadillaTipografica{{{escapar_latex(t_cfg.get('antetitulo', ''))}}}"
                    rf"{{{escapar_latex(t_cfg.get('titulo', cap.titulo.upper()))}}}"
                )

            cab_sec = sec.titulo.split(":")[0].strip()
            es_primero = (idx_cap == 0) and (sec.capitulos[0].id == cap.id)
            c_override = pre_cuerpo_primero[0] if (es_primero and pre_cuerpo_primero) else None
            n_override = pre_cuerpo_primero[1] if (es_primero and pre_cuerpo_primero) else None

            cuerpo.append(
                convertir_capitulo_a_latex(
                    cap=cap,
                    diseno=diseno,
                    hallazgos=hallazgos,
                    cabecera_seccion=cab_sec,
                    es_primero_de_parte=es_primero,
                    cuerpo_lines=c_override,
                    notas_map=n_override,
                )
            )

    # Sustituir placeholders en plantilla maestra
    reemp_maestra = {
        "%%CUERPO_PT%%": str(int(tip.get("cuerpo_pt", 10))),
        "%%ANCHO_MM%%": str(pag["ancho_mm"]),
        "%%ALTO_MM%%": str(pag["alto_mm"]),
        "%%MARGEN_SUP_MM%%": str(pag["margen_superior_mm"]),
        "%%MARGEN_INF_MM%%": str(pag["margen_inferior_mm"]),
        "%%MARGEN_INT_MM%%": str(pag["margen_interior_mm"]),
        "%%MARGEN_EXT_MM%%": str(pag["margen_exterior_mm"]),
        "%%HEADHEIGHT_PT%%": str(pag["headheight_pt"]),
        "%%HEADSEP_MM%%": str(pag["headsep_mm"]),
        "%%FOOTSKIP_MM%%": str(pag["footskip_mm"]),
        "%%PAQUETE_CROP_IMPRENTA%%": paquete_crop,
        "%%FUENTES_DIR%%": fuentes_dir_tex,
        "%%FONT_REGULAR%%": tip["principal"]["regular"],
        "%%FONT_NEGRITA%%": tip["principal"]["negrita"],
        "%%FONT_CURSIVA%%": tip["principal"]["cursiva"],
        "%%FONT_NEGRITA_CURSIVA%%": tip["principal"]["negrita_cursiva"],
        "%%FONT_FAMILIA%%": tip["principal"]["familia"],
        "%%FONT_AMIGA%%": tip["amiga"],
        "%%FONT_BAUHAUS%%": tip["bauhaus"],
        "%%FONT_SWIS%%": tip["swis"],
        "%%COLOR_GRIS_CABECERA%%": str(cab.get("color_gris", "0.55")),
        "%%COLOR_FILETE_CABECERA%%": str(cab.get("color_filete", "0.45")),
        "%%INTERLINEADO_FACTOR%%": str(tip.get("interlineado_factor", 1.14)),
        "%%SANGRIA_MM%%": str(tip.get("sangria_mm", 7.0)),
        "%%ESPACIO_PARRAFOS_PT%%": str(tip.get("espacio_parrafos_pt", 0.0)),
        "%%EMERGENCYSTRETCH_EM%%": str(tip.get("emergencystretch_em", 1.5)),
        "%%WIDOWPENALTY%%": str(tip.get("widowpenalty", 10000)),
        "%%CLUBPENALTY%%": str(tip.get("clubpenalty", 10000)),
        "%%BLOQUE_MARCO_EXTERNO%%": construir_bloque_marco_externo(diseno, hoyo_path),
        "%%BLOQUE_CABECERA_CORRIDA%%": bloque_cab,
        "%%GROSOR_FILETE_PT%%": str(cab.get("grosor_filete_pt", 0.35)),
        "%%LIMPIAR_PAGINAS_BLANCAS%%": limpiar_blancas,
        "%%ESTILOS_ESPECIALES%%": estilos_render,
        "%%INICIO_NUMERACION%%": inicio_num,
        "%%CUERPO_DOCUMENTO%%": "\n".join(cuerpo),
    }

    tex_final = tpl_maestra
    for k, v in reemp_maestra.items():
        tex_final = tex_final.replace(k, v)
    return tex_final


def ejecutar_lualatex(tex_path: Path, build_dir: Path, max_pasadas: int) -> Tuple[int, int, str]:
    """Ejecuta LuaLaTeX con caché local (Bug A) hasta estabilizar referencias cruzadas (Bug G)."""
    lualatex = shutil.which("lualatex")
    if not lualatex:
        raise RuntimeError("No se encontró 'lualatex' en el PATH del sistema.")

    texmf_var = build_dir / "texmf-var"
    texmf_var.mkdir(parents=True, exist_ok=True)
    env_tex = os.environ.copy()
    env_tex["TEXMFVAR"] = str(texmf_var)
    env_tex["TEXMFCACHE"] = str(texmf_var)
    env_tex["XDG_CACHE_HOME"] = str(texmf_var)

    pasadas_hechas = 0
    ultimo_log = ""
    for paso in range(1, max_pasadas + 1):
        pasadas_hechas = paso
        t_p = time.time()
        proc = subprocess.run(
            [
                lualatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(build_dir),
                str(tex_path),
            ],
            capture_output=True,
            text=True,
            env=env_tex,
            check=False,
        )
        dt = time.time() - t_p
        print(f"      Pasada {paso}/{max_pasadas} finalizada en {dt:.1f}s (código {proc.returncode})")
        if proc.returncode != 0:
            tail = "\n".join(proc.stdout.splitlines()[-40:])
            return proc.returncode, pasadas_hechas, tail

        log_path = build_dir / f"{tex_path.stem}.log"
        ultimo_log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""

        necesita_otra = bool(
            re.search(r"Label\(s\) may have changed|Rerun to get (cross-references|outlines|the TOC)", ultimo_log)
        )
        # Si es libro completo y acabamos de completar la pasada 1, siempre requerir al menos 2 pasadas
        if paso >= 2 and not necesita_otra:
            break

    return 0, pasadas_hechas, ultimo_log


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compila la maqueta editorial LuaLaTeX de la Segunda Edición en dist/maqueta/."
    )
    parser.add_argument(
        "--manifiesto",
        default=None,
        help="Ruta al manifiesto YAML (por defecto: libro.yaml)",
    )
    parser.add_argument(
        "--diseno",
        default=str(DISENO_POR_DEFECTO),
        help="Ruta a la configuración YAML de maquetación (por defecto: maquetacion/diseno_2ed.yaml)",
    )
    parser.add_argument(
        "--capitulo",
        default=None,
        help="Compila únicamente un capítulo específico por id o nombre de archivo (ej. 08 o A1)",
    )
    parser.add_argument(
        "--modo",
        choices=("digital", "imprenta"),
        default="digital",
        help="Modo de compilación: 'digital' (por defecto) o 'imprenta' (sangrado, marcas de corte y PNG 300 DPI)",
    )
    parser.add_argument(
        "--pasadas",
        type=int,
        default=None,
        help="Número máximo de pasadas de LuaLaTeX (por defecto: 4 para libro completo, 2 para un capítulo)",
    )
    parser.add_argument(
        "--solo-tex",
        action="store_true",
        help="Genera únicamente el archivo .tex en dist/maqueta/build/ sin invocar LuaLaTeX",
    )
    parser.add_argument(
        "--salida",
        default=None,
        help="Ruta de salida del PDF final (por defecto en dist/maqueta/)",
    )
    args = parser.parse_args()

    t0 = time.time()
    manifiesto = cargar_manifiesto(args.manifiesto)
    diseno = cargar_diseno(Path(args.diseno))
    cap_unico = buscar_capitulo(manifiesto, args.capitulo) if args.capitulo else None

    build_dir = DIST_MAQUETA_DIR / "build"
    img_dir = DIST_MAQUETA_DIR / "img"
    verificar_ruta_escritura_segura(build_dir)
    verificar_ruta_escritura_segura(img_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    # Determinar imágenes estrictamente necesarias
    port_cfg = diseno["portadillas"]
    req_imgs: Optional[set] = None
    if cap_unico is not None:
        req_imgs = set()
        for sec in manifiesto.secciones:
            if any(c.id == cap_unico.id for c in sec.capitulos):
                if sec.capitulos[0].id == cap_unico.id and sec.id in port_cfg.get("por_seccion", {}):
                    req_imgs.add(port_cfg["por_seccion"][sec.id])
                break
        if cap_unico.id in port_cfg.get("por_capitulo", {}):
            req_imgs.add(port_cfg["por_capitulo"][cap_unico.id])

    hallazgos: List[str] = []
    print(f"[1/4] Preparando activos gráficos ({args.modo}) en dist/maqueta/img/...")
    imgs = preparar_imagenes(diseno, args.modo, img_dir, hallazgos, requeridas=req_imgs)
    print(f"      Imágenes listas: {len(imgs)}")

    etiqueta = f"cap_{cap_unico.id}_{args.modo}" if cap_unico else f"libro_2ed_{args.modo}"
    tex_path = build_dir / f"{etiqueta}.tex"
    print(
        f"[2/4] Ensamblando LaTeX ({'capítulo ' + cap_unico.id if cap_unico else str(len(manifiesto.capitulos)) + ' capítulos'})..."
    )
    tex_str = ensamblar_tex(manifiesto, diseno, imgs, args.modo, hallazgos, capitulo_unico=cap_unico)
    tex_path.write_text(tex_str, encoding="utf-8")
    print(f"      .tex generado: {tex_path.relative_to(REPO_ROOT)} ({tex_path.stat().st_size:,} bytes)")

    if args.solo_tex:
        print("[OK] Modo --solo-tex completado.")
        return 0

    max_pasadas = args.pasadas or (2 if cap_unico else 4)
    print(f"[3/4] Compilando con LuaLaTeX (hasta {max_pasadas} pasadas automáticas)...")
    rc, pasadas_hechas, log_o_err = ejecutar_lualatex(tex_path, build_dir, max_pasadas)
    if rc != 0:
        print("[ERROR] Falló la compilación LuaLaTeX (últimas líneas):")
        print(log_o_err)
        return 1

    if args.salida:
        pdf_out = Path(args.salida)
        if not pdf_out.is_absolute():
            pdf_out = REPO_ROOT / pdf_out
    else:
        nombre_pdf = (
            f"Critica_de_la_Razon_Mediatica_cap_{cap_unico.id}_{args.modo}.pdf"
            if cap_unico
            else f"Critica_de_la_Razon_Mediatica_2ed_{args.modo}.pdf"
        )
        pdf_out = DIST_MAQUETA_DIR / nombre_pdf

    verificar_ruta_escritura_segura(pdf_out)
    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(build_dir / f"{etiqueta}.pdf", pdf_out)

    # Auditar log y contar páginas
    overfull = re.findall(r"Overfull \\hbox.*", log_o_err)
    underfull = re.findall(r"Underfull \\hbox.*", log_o_err)
    missing_chars = re.findall(r"Missing character:.*", log_o_err)
    latex_warns = re.findall(r"LaTeX Warning:.*", log_o_err)

    total_pags = 0
    if shutil.which("pdfinfo"):
        pinfo = subprocess.run(["pdfinfo", str(pdf_out)], capture_output=True, text=True, check=False).stdout
        m_pags = re.search(r"Pages:\s+(\d+)", pinfo)
        if m_pags:
            total_pags = int(m_pags.group(1))

    reporte = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "modo": args.modo,
        "alcance": f"capitulo:{cap_unico.id}" if cap_unico else "libro_completo",
        "pdf": str(pdf_out.relative_to(REPO_ROOT)) if pdf_out.is_relative_to(REPO_ROOT) else str(pdf_out),
        "paginas_pdf": total_pags,
        "tamano_mb": round(pdf_out.stat().st_size / (1024 * 1024), 2),
        "pasadas_lualatex": pasadas_hechas,
        "duracion_seg": round(time.time() - t0, 1),
        "missing_characters": len(missing_chars),
        "missing_characters_muestra": sorted(set(missing_chars))[:15],
        "overfull_hbox": len(overfull),
        "overfull_hbox_muestra": overfull[:15],
        "underfull_hbox": len(underfull),
        "latex_warnings": len(latex_warns),
        "latex_warnings_muestra": sorted(set(latex_warns))[:15],
        "hallazgos_precompilacion": hallazgos,
    }
    reporte_path = DIST_MAQUETA_DIR / f"reporte_{etiqueta}.json"
    reporte_path.write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")

    print("[4/4] Resumen de compilación:")
    print(f"      PDF final:      {reporte['pdf']} ({total_pags} páginas, {reporte['tamano_mb']} MB)")
    print(f"      Tiempo/Pasadas: {reporte['duracion_seg']}s ({pasadas_hechas} pasadas)")
    print(
        f"      Calidad TeX:    missing_chars={len(missing_chars)} | overfull={len(overfull)} "
        f"| underfull={len(underfull)} | warnings={len(latex_warns)}"
    )
    print(f"      Reporte JSON:   {reporte_path.relative_to(REPO_ROOT)}")
    if hallazgos:
        print(f"      Hallazgos ({len(hallazgos)}):")
        for h in hallazgos[:10]:
            print(f"        - {h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
