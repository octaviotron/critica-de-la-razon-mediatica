# Maquetación Editorial — Segunda Edición (`maquetacion/`)

Subsistema declarativo y modular para compilar la **maqueta editorial de imprenta y lectura digital** de ***Crítica de la Razón Mediática*** (2.ª Edición) con `LuaLaTeX`, preservando la identidad gráfica de la Primera Edición (2006) desde [`libro/`](../libro/), [`libro.yaml`](../libro.yaml) y los activos originales en solo lectura de [`fuente/`](../fuente/).

---

## Estructura del Directorio

| Ruta | Responsabilidad |
| :--- | :--- |
| [`diseno_2ed.yaml`](diseno_2ed.yaml) | Parámetros ajustables: trim (`126.4 × 191.1 mm`), márgenes, saltos de página (control de páginas en blanco), fuentes, capitulares, sello lateral, cabeceras, Índice General, notas al pie y mapeo de portadillas. |
| [`plantilla/libro_2ed.tex`](plantilla/libro_2ed.tex) | Plantilla maestra `LuaLaTeX` (geometría, tipografías, estilos de página `libro2006` / `plain2006` y marco lateral). |
| [`plantilla/estilos_especiales.tex`](plantilla/estilos_especiales.tex) | Estilos de epígrafes indivisibles, citas a bando, notas al pie, portadillas gráficas/tipográficas y diseño del Índice General. |
| [`activos/`](activos/README.md) | Carpeta reservada para nuevos activos gráficos exclusivos de la 2.ª edición (p. ej., nuevas portadillas para el *Prefacio* o el *Anexo editorial*). |
| [`cubierta/`](cubierta/especificaciones_lomo.md) | Especificaciones separadas de portada, lomo, contraportada y solapas (cálculo de lomo según conteo final de páginas y papel). |

---

## Cómo Compilar y Ajustar la Maqueta

Todo el trabajo temporal (`.tex`, `.log`, imágenes convertidas y PDFs compilados) se escribe exclusivamente en `dist/maqueta/` (ignorado por Git).

```bash
# Compilar la maqueta completa (modo digital, con 3 pasadas automáticas)
python3 -B scripts/edicion/compilar_maqueta.py

# Prueba rápida de un solo capítulo (ideal para iterar diseño en ~4-5 s)
python3 -B scripts/edicion/compilar_maqueta.py --capitulo 08

# Compilar versión de imprenta (sangrado 3 mm + marcas de corte + portadillas PNG)
python3 -B scripts/edicion/compilar_maqueta.py --modo imprenta

# Previsualizar recálculo del Índice Onomástico sobre el PDF compilado
python3 -B scripts/edicion/recalcular_onomastico.py
```

### Dónde ajustar los cambios más frecuentes
* **Eliminar o controlar páginas en blanco:** bloque `paginacion_saltos:` en [`diseno_2ed.yaml`](diseno_2ed.yaml).
* **Cambiar márgenes, tamaño de letra, sello lateral o cabeceras:** bloques `pagina:`, `tipografia:`, `marco_externo:` y `cabecera:` en [`diseno_2ed.yaml`](diseno_2ed.yaml) y [`plantilla/libro_2ed.tex`](plantilla/libro_2ed.tex).
* **Rediseñar el Índice General:** bloque `indice_general:` en [`diseno_2ed.yaml`](diseno_2ed.yaml) y macros `\l@part`, `\l@chapter`, `\l@section`, `\tableofcontents` en [`plantilla/estilos_especiales.tex`](plantilla/estilos_especiales.tex).
* **Especificación técnica completa y checklist pre-imprenta:** [`SSOT/guia_maquetacion_segunda_edicion.md`](../SSOT/guia_maquetacion_segunda_edicion.md).
