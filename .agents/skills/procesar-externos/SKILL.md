---
name: procesar-externos
description: >-
  Usar cuando el usuario indique que añadió, modificó o eliminó archivos de bibliografía
  en `externos/`, o solicite indexar, fichar o mapear nuevas fuentes externas hacia
  `notas/fuentes/` y los capítulos del libro.
---

# Procedimiento: Incorporación y Fichado de Bibliografía Externa (`externos/`)

El directorio `externos/` es de **solo lectura** (nunca editar, renombrar ni mover archivos allí). Toda la curación vive en `notas/fuentes/` y el índice local reconstruible en `dist/indice_externos/`.

---

## Paso 1 — Indexación Incremental

Ejecutar silenciosamente el indexador:
```bash
python3 -B scripts/edicion/indexar_externos.py
```
Esto detecta únicamente archivos nuevos, modificados o ausentes por SHA-256 (soportando PDF, HTML/HTM, TXT, MD, DOCX y EPUB), actualiza `dist/indice_externos/corpus.db` (SQLite FTS5) + `dist/indice_externos/txt/`, y da de alta las fuentes nuevas en `notas/fuentes/catalogo.yaml` con `estado: "pendiente_ficha"` sin sobrescribir campos curados.

Listar el estado actual y comprobar calidad de extracción:
```bash
python3 -B scripts/edicion/buscar_externos.py --listar
```
* **Control de calidad inmediato:**
  * Si algún PDF aparece con `[OCR!]` (`requiere_ocr: true`), advertirlo al usuario porque no tiene capa de texto usable sin OCR previo.
  * Si un archivo `.html`/`.htm` extrajo menos de `1,000` caracteres pese a ser un artículo extenso, inspeccionar su estructura HTML (posible falso positivo de una tarjeta `<article>` lateral) y ajustar `extraer_html()` en `indexar_externos.py` si hace falta.

---

## Paso 2 — Inspección Quirúrgica de Cada Fuente Nueva

**Nunca volcar libros o PDFs completos al contexto.** Para cada `<slug>` nuevo (`estado: pendiente_ficha`):
1. Inspeccionar metadatos, TOC y estadísticas:
   ```bash
   python3 -B scripts/edicion/buscar_externos.py --sin-auto-indexar --info <slug>
   ```
2. Leer únicamente portada, hoja de créditos/colofón, índice y apertura (páginas `1–6`, y últimas páginas si los créditos están al final):
   ```bash
   python3 -B scripts/edicion/buscar_externos.py --sin-auto-indexar --leer <slug> --paginas 1-6 --max-chars 3500
   ```
   * Si algún dato editorial (ciudad, editorial, año o medio) no aparece en el documento, **nunca inventarlo**: marcar `[VERIFICAR EDITORIAL/AÑO]` o `[VERIFICAR MEDIO Y FECHA]`.
   * Si el PDF proviene de OCR con erratas menores o está en otro idioma (p. ej. francés), anotar la advertencia explícita en la ficha.

---

## Paso 3 — Curado del Catálogo (`notas/fuentes/catalogo.yaml`)

Preservando intactos los campos técnicos (`id`, `archivo`, `sha256`, `paginas`, `caracteres`, `requiere_ocr`), completar:
* `titulo`, `autor`, `anio`, `editorial`, `ciudad`, `url`, `idioma`, `tipo` (`libro` | `articulo` | `informe` | `nota_personal`).
* `postura_dialogo`: `afin` | `dialogo_critico` | `critica` | `insumo_empirico`.
* `cita_europea`: formato clásico europeo listo para notas al pie.
* `temas`: lista corta de etiquetas temáticas.
* `capitulos_destino`: lista de IDs de capítulos de `libro.yaml` (ej. `['07', '19', '21']`).
* `estado: "fichado"` y `notas` breves.

---

## Paso 4 — Ficha Curada y Cruce Editorial

1. Crear o actualizar `notas/fuentes/<slug>.md` con:
   * Metadatos, postura de diálogo y cita europea verificada (más nota de idioma/OCR si aplica).
   * Tesis central y mapa de capítulos/apartados relevantes del documento.
   * Ejes concretos de diálogo con *Crítica de la Razón Mediática*.
   * Comando listo de consulta (`buscar_externos.py --fuente <slug>`).
   * Checklist `- [ ]` de integración hacia los capítulos en `../capitulos/<archivo>.md`.
2. Enlazar las obras nuevas relevantes en `notas/NOTAS.md` (Sección 1) y, si amplían el mapa por capítulo, actualizar `notas/mapa_obra.md`.

---

## Paso 5 — Verificación y Resumen al Usuario

1. Verificar idempotencia del indexador (debe reportar `0` nuevos / `0` reindexados sin pisar campos curados):
   ```bash
   python3 -B scripts/edicion/indexar_externos.py
   ```
2. Verificar que los enlaces relativos de `notas/fuentes/<slug>.md` y `notas/NOTAS.md` existen y ejecutar `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo`.
3. Entregar al usuario un resumen breve con las fuentes incorporadas, su cita europea, postura de diálogo y capítulos sugeridos (sin ejecutar `git commit` ni `git push`).
