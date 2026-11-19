# Bitácora Editorial de Cambios (`CHANGELOG.md`)

Registro editorial de alto nivel por versión/hito de ***Crítica de la Razón Mediática*** (Juan Barreto Cipriani).  
El detalle línea por línea de cada intervención se gestiona nativamente con Git (`git log`, `git diff`) y puede compararse en cualquier momento contra el respaldo inmutable `respaldo_v1.0/` mediante `python3 scripts/edicion/reporte_cambios.py`.

---

## `[2.0.0-dev]` — En proceso (Preparación de la Segunda Edición)

### Arquitectura y flujo editorial
* Adopción de versionamiento nativo en Git y retiro de la carpeta redundante `versiones/` y del flujo de dictado por voz.
* Incorporación del manifiesto declarativo [`libro.yaml`](libro.yaml) (**Opción A**: los nombres de archivo en `libro/` actúan como IDs estables y el orden/agrupación del índice se controla desde `libro.yaml`).
* Creación del respaldo inmutable [`respaldo_v1.0/`](respaldo_v1.0/) con copia testigo de los 33 capítulos originales, manifiesto estructural congelado (`respaldo_v1.0/libro.yaml`), huellas SHA-256 (`respaldo_v1.0/manifiesto_v1.0.md`) y guía propia (`respaldo_v1.0/README.md`).
* Separación de scripts en `scripts/extraccion_v1/` (pipeline histórico congelado de 2006, protegido contra sobrescritura) y `scripts/edicion/` (`validar_libro.py`, `generar_indice.py`, `compilar_pdf.py`, `reporte_cambios.py`).
* Exclusión de artefactos compilados en `dist/` mediante `.gitignore`.
* Actualización de la documentación en `README.md` y `SSOT/` (sustituyendo la guía de voz por `SSOT/flujo_editorial_segunda_edicion.md`).

### Contenido textual (`libro/`)
* *(Pendiente: los 33 archivos en `libro/` aún se encuentran idénticos a `v1.0.0`.)*

---

## `[1.0.0]` — Primera Edición (2006) — Conversión Digital Íntegra

### Extracción y verificación
* Extracción determinista desde `fuente/Libro Crítica de La Razon Mediatica.pdf` (666 páginas físicas) a 33 archivos Markdown en `libro/` y copia inmutable en `respaldo_v1.0/md/`.
* Auditoría contable matemática al **100.000%**: `1,008,962 / 1,008,962` caracteres alfanuméricos, `197,741` palabras, `513` notas al pie enlazadas (`0` pérdidas, `0` mezclas entre capítulos).
