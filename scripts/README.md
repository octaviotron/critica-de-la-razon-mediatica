# Herramientas Técnicas y Scripts (`scripts/`)

Documentación técnica de las herramientas internas de validación, compilación, búsqueda e indexación del repositorio ***Crítica de la Razón Mediática*** (Juan Barreto Cipriani).

> Estas herramientas están diseñadas para **ejecución asistida de scripts bajo demanda** durante el flujo editorial capítulo por capítulo, aunque también pueden invocarse manualmente desde la raíz del repositorio usando `python3 -B` (para evitar archivos caché `__pycache__`).

---

## 1. Herramientas Activas de Edición (`scripts/edicion/`)

| Script | Propósito |
| :--- | :--- |
| [`manifiesto.py`](edicion/manifiesto.py) | Módulo compartido que carga [`libro.yaml`](../libro.yaml) o [`respaldo_v1.0/libro.yaml`](../respaldo_v1.0/libro.yaml), resuelve capítulos por `id`/archivo y bloquea cualquier escritura sobre `respaldo_v1.0/`. |
| [`contexto_capitulo.py`](edicion/contexto_capitulo.py) | Consolida en una sola salida el briefing editorial de un capítulo (metadatos, alerta de textos invitados protegidos, diagnóstico técnico en vivo, ficha espejo en `notas/capitulos/`, fuentes externas mapeadas y menciones en `notas/NOTAS.md`). |
| [`validar_libro.py`](edicion/validar_libro.py) | Valida un capítulo (`--capitulo`) o el libro completo: archivos, notas al pie, enlaces locales, sintaxis compatible con PangoCairo, asteriscos impares, marcadores `[VERIFICAR]`, protección de textos invitados (`03`–`06` y `29` desde L101), higiene de los 6 `README.md`, tamaño de `AGENTS.md`, fichas espejo en `notas/capitulos/` y huellas SHA-256 de `respaldo_v1.0/md/` (`--verificar-respaldo`). |
| [`compilar_pdf.py`](edicion/compilar_pdf.py) | Compila un capítulo (`--capitulo`) o el libro completo en `dist/` en formato **PDF** (por defecto, o con etiquetas `[ID.PPP]` mediante `--etiquetar-parrafos`) o **Word (`.docx`)** (`--formato docx`, con prefijado automático de notas por capítulo). También compila la 1.ª edición intacta desde `--manifiesto respaldo_v1.0/libro.yaml`. |
| [`reporte_cambios.py`](edicion/reporte_cambios.py) | Genera en `dist/` un reporte comparativo estructural y textual de un capítulo (`--capitulo`) o del libro completo contra `respaldo_v1.0/` (o contra cualquier referencia de Git mediante `--desde-git`). |
| [`generar_indice.py`](edicion/generar_indice.py) | Regenera el Índice General desde `libro.yaml` y los encabezados reales (`#`, `##`). Por defecto previsualiza en `dist/indice_generado.md`; con `--escribir` actualiza `libro/01_indice.md` (usar solo tras sanear encabezados partidos). |
| [`indexar_externos.py`](edicion/indexar_externos.py) | Indexa incrementalmente (por SHA-256) los archivos de [`externos/`](../externos/) (PDF, HTML, TXT, MD, DOCX, EPUB) en SQLite FTS5 (`dist/indice_externos/corpus.db`) y sincroniza [`notas/fuentes/catalogo.yaml`](../notas/fuentes/catalogo.yaml) preservando campos curados. |
| [`buscar_externos.py`](edicion/buscar_externos.py) | Consulta quirúrgica sobre `externos/` con auto-sincronización silenciosa: búsqueda FTS5 BM25, lectura por rango exacto de páginas (`--leer`), inspección de metadatos/TOC (`--info`) y fuentes asignadas por capítulo (`--para-capitulo`). |
| [`buscar_libro.py`](edicion/buscar_libro.py) | Búsqueda interna insensible a tildes sobre [`libro/`](../libro/), el Glosario (`--glosario`) y la Bibliografía (`--bibliografia`) con distribución de ocurrencias por capítulo. |

---

## 2. Comandos de Referencia Rápida

### Edición y validación de la Segunda Edición (`libro/`)
```bash
# Obtener briefing completo antes de editar un capítulo
python3 -B scripts/edicion/contexto_capitulo.py --capitulo 19

# Validar un capítulo recién editado o todo el libro junto al respaldo SHA-256
python3 -B scripts/edicion/validar_libro.py --capitulo 19
python3 -B scripts/edicion/validar_libro.py --verificar-respaldo

# Compilar un solo capítulo para revisión del autor en dist/ (PDF limpio por defecto, PDF etiquetado o Word)
python3 -B scripts/edicion/compilar_pdf.py --capitulo 19
python3 -B scripts/edicion/compilar_pdf.py --capitulo 19 --etiquetar-parrafos
python3 -B scripts/edicion/compilar_pdf.py --capitulo 19 --formato docx

# Generar reporte comparativo de un capítulo o del libro completo contra 2006 (respaldo_v1.0/)
python3 -B scripts/edicion/reporte_cambios.py --capitulo 19 --incluir-diffs
python3 -B scripts/edicion/reporte_cambios.py

# Compilar el libro completo actual o regenerar el Índice General desde libro.yaml
python3 -B scripts/edicion/compilar_pdf.py
python3 -B scripts/edicion/generar_indice.py --escribir
```

### Búsqueda interna en el libro y en bibliografía externa (`externos/`)
```bash
# Buscar conceptos en el libro, consultar el Glosario o revisar la Bibliografía de 2006
python3 -B scripts/edicion/buscar_libro.py "biopolitica" --solo-conteo
python3 -B scripts/edicion/buscar_libro.py --glosario "cuerpo"
python3 -B scripts/edicion/buscar_libro.py --bibliografia "Foucault"

# Indexar novedades en externos/ y consultar citas verificadas con página exacta
python3 -B scripts/edicion/indexar_externos.py
python3 -B scripts/edicion/buscar_externos.py --para-capitulo 19
python3 -B scripts/edicion/buscar_externos.py "regimen de verdad" --limite 8
python3 -B scripts/edicion/buscar_externos.py --leer la_vie_spectrale --paginas 58-61
```

### Compilar y auditar siempre la Primera Edición (`respaldo_v1.0/`)
```bash
# Compilar el PDF completo de la 1.ª edición (v1.0.0) en dist/
python3 -B scripts/edicion/compilar_pdf.py --manifiesto respaldo_v1.0/libro.yaml

# Auditar al 100.000% respaldo_v1.0/md/ contra el PDF maestro de 2006
python3 -B scripts/extraccion_v1/03_auditar_integridad.py
```

---

## 3. Pipeline Histórico Congelado (`scripts/extraccion_v1/`)

> **⚠️ SOLO LECTURA — CONGELADO:** Estos tres scripts corresponden a la extracción original del PDF maestro de 2006 (Método 1). Nunca deben modificarse ni re-ejecutarse sobre `libro/`.

* **[`01_extraer_xml.py`](extraccion_v1/01_extraer_xml.py):** Extrae la capa vectorial XML de las 666 páginas del PDF mediante `pdftohtml -xml -i` y filtra determinísticamente el ruido de QuarkXPress.
* **[`02_convertir_a_md.py`](extraccion_v1/02_convertir_a_md.py):** Reconstruye los 33 archivos Markdown (protegido: escribe por defecto en `dist/extraccion_v1_md/` y bloquea sobrescrituras accidentales sobre `respaldo_v1.0/` o `libro/`).
* **[`03_auditar_integridad.py`](extraccion_v1/03_auditar_integridad.py):** Ejecuta la auditoría contable al `100.000%` contra el PDF original (por defecto sobre `respaldo_v1.0/md/`).

## 4. Requisitos del Entorno Local

Para ejecutar los scripts en un equipo nuevo (entorno Linux / Python 3):
* **Herramientas de sistema:** `python3`, Poppler (`pdftotext` y `pdftohtml`) y `pandoc` (exportación a Word `.docx` y lectura de `.docx`/`.epub` en `externos/`).
* **Librerías Python:** `PyYAML`, `pycairo` y `PyGObject` (`Pango` / `PangoCairo` para generación de PDF), `pypdf` y `beautifulsoup4` (indexación de `externos/`). `sqlite3` con FTS5 viene incluido en la biblioteca estándar de Python.

Para el flujo editorial completo, véanse [`SSOT/README.md`](../SSOT/README.md) y [`SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md).
