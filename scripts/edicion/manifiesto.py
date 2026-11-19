#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo compartido para cargar y resolver el manifiesto estructural del libro (`libro.yaml`
o `respaldo_v1.0/libro.yaml`). Desacopla el orden de lectura, las partes y los metadatos
de los nombres de archivo en `libro/`.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFIESTO = REPO_ROOT / "libro.yaml"
RESPALDO_MANIFIESTO = REPO_ROOT / "respaldo_v1.0" / "libro.yaml"
DEFAULT_DIST_DIR = REPO_ROOT / "dist"


@dataclass(frozen=True)
class ObraMeta:
    titulo: str
    subtitulo: str
    autor: str
    edicion: str
    version: str
    inmutable: bool


@dataclass(frozen=True)
class CapituloRef:
    id: str
    archivo: str
    titulo: str
    tipo: str
    folios_2006: Optional[str]
    seccion_id: str
    seccion_titulo: str
    ruta: Path


@dataclass(frozen=True)
class SeccionLibro:
    id: str
    titulo: str
    mostrar_en_indice: bool
    capitulos: List[CapituloRef]


@dataclass(frozen=True)
class LibroManifiesto:
    ruta_manifiesto: Path
    obra: ObraMeta
    carpeta_base: Path
    secciones: List[SeccionLibro]

    @property
    def capitulos(self) -> List[CapituloRef]:
        todos: List[CapituloRef] = []
        for sec in self.secciones:
            todos.extend(sec.capitulos)
        return todos

    @property
    def capitulo_indice(self) -> Optional[CapituloRef]:
        for cap in self.capitulos:
            if cap.tipo == "indice":
                return cap
        return None


def resolver_ruta_manifiesto(ruta: Optional[str]) -> Path:
    if not ruta:
        return DEFAULT_MANIFIESTO
    p = Path(ruta)
    if p.exists():
        return p.resolve()
    candidato = REPO_ROOT / p
    if candidato.exists():
        return candidato.resolve()
    raise FileNotFoundError(f"No se encontró el manifiesto YAML: {ruta}")


def cargar_manifiesto(ruta: Optional[str] = None) -> LibroManifiesto:
    ruta_abs = resolver_ruta_manifiesto(ruta)
    with ruta_abs.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"El manifiesto '{ruta_abs}' no tiene un objeto YAML válido en la raíz.")

    obra_raw = data.get("obra", {})
    obra = ObraMeta(
        titulo=str(obra_raw.get("titulo", "Sin título")),
        subtitulo=str(obra_raw.get("subtitulo", "")),
        autor=str(obra_raw.get("autor", "")),
        edicion=str(obra_raw.get("edicion", "")),
        version=str(obra_raw.get("version", "0.0.0")),
        inmutable=bool(obra_raw.get("inmutable", False)),
    )

    carpeta_base_raw = data.get("carpeta_base", "libro")
    carpeta_base = (ruta_abs.parent / carpeta_base_raw).resolve()

    secciones: List[SeccionLibro] = []
    for sec_raw in data.get("secciones", []):
        sec_id = str(sec_raw.get("id", ""))
        sec_titulo = str(sec_raw.get("titulo", ""))
        mostrar = bool(sec_raw.get("mostrar_en_indice", True))
        caps: List[CapituloRef] = []
        for cap_raw in sec_raw.get("capitulos", []):
            archivo = str(cap_raw["archivo"])
            cap_ruta = (carpeta_base / archivo).resolve()
            caps.append(
                CapituloRef(
                    id=str(cap_raw["id"]),
                    archivo=archivo,
                    titulo=str(cap_raw.get("titulo", archivo)),
                    tipo=str(cap_raw.get("tipo", "cuerpo")),
                    folios_2006=str(cap_raw["folios_2006"]) if cap_raw.get("folios_2006") else None,
                    seccion_id=sec_id,
                    seccion_titulo=sec_titulo,
                    ruta=cap_ruta,
                )
            )
        secciones.append(
            SeccionLibro(
                id=sec_id,
                titulo=sec_titulo,
                mostrar_en_indice=mostrar,
                capitulos=caps,
            )
        )

    return LibroManifiesto(
        ruta_manifiesto=ruta_abs,
        obra=obra,
        carpeta_base=carpeta_base,
        secciones=secciones,
    )


def es_ruta_dentro_de_respaldo(ruta: Path) -> bool:
    respaldo_root = (REPO_ROOT / "respaldo_v1.0").resolve()
    target = ruta.resolve()
    return target == respaldo_root or respaldo_root in target.parents
