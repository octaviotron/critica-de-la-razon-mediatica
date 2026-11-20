# Bitácora Editorial de Cambios (`CHANGELOG.md`)

Registro editorial de alto nivel por capítulo aprobado e hitos de ***Crítica de la Razón Mediática*** (Juan Barreto Cipriani).  
El estado de cada capítulo (`pendiente` | `en_revision` | `aprobado`) se consulta en [`libro.yaml`](libro.yaml), y el detalle exacto de cambios contra 2006 puede consultarse en cualquier momento frente al respaldo inmutable [`respaldo_v1.0/`](respaldo_v1.0/).

---

## Segunda Edición — En proceso (`libro/`)

### Capítulos aprobados por el autor
* *(Ninguno aún — todos los capítulos en [`libro/`](libro/) se encuentran en su estado base de 2006, `estado: pendiente` en [`libro.yaml`](libro.yaml). Los pendientes de Glosario, Bibliografía, autores e índice se centralizan en [`notas/NOTAS.md`](notas/NOTAS.md).)*

### Arquitectura editorial
* Creación de la carpeta escalable [`notas/`](notas/) con [`notas/NOTAS.md`](notas/NOTAS.md) (ideas globales y autores por incorporar) y 33 fichas personalizadas en [`notas/capitulos/`](notas/capitulos/) con sugerencias basadas en el contenido de cada capítulo.
* Definición del flujo simplificado capítulo por capítulo: edición directa de cada `.md` en `libro/` con IA → revisión e iteración con el autor (entrega por capítulo en PDF o Word `.docx`) → aprobación en `libro.yaml` (`estado: aprobado`) → commit y push simple en `main`.
* Incorporación de [`SSOT/guia_estilo_editorial.md`](SSOT/guia_estilo_editorial.md) con las reglas de voz filosófica, vocabulario protegido y protocolo operativo por capítulo.
* Incorporación del manifiesto declarativo [`libro.yaml`](libro.yaml) (**Opción A**: nombres de archivo estables, orden flexible del índice y seguimiento de `estado` por capítulo).
* Creación del respaldo inmutable [`respaldo_v1.0/`](respaldo_v1.0/) con copia testigo de los 33 capítulos originales, manifiesto congelado (`respaldo_v1.0/libro.yaml`), huellas SHA-256 (`respaldo_v1.0/manifiesto_v1.0.md`) y guía propia (`respaldo_v1.0/README.md`).
* Separación de scripts en `scripts/extraccion_v1/` (pipeline histórico congelado de 2006, protegido contra sobrescritura) y `scripts/edicion/` (herramientas internas ejecutadas por la IA bajo demanda, con soporte por capítulo en PDF/DOCX).
* Exclusión de artefactos compilados en `dist/` mediante [`.gitignore`](.gitignore).

---

## Primera Edición (2006) — Base Digital Íntegra (`respaldo_v1.0/`)

### Extracción y verificación
* Extracción determinista desde `fuente/Libro Crítica de La Razon Mediatica.pdf` (666 páginas físicas) a 33 archivos Markdown en `libro/` y copia inmutable en `respaldo_v1.0/md/`.
* Depuración única de artefactos técnicos de conversión (sin cambios de contenido): corrección de formato/cortes de párrafo en 6 archivos (`09`, `10`, `11`, `13`, `20` y `28`) y recuperación de 27 enlaces/definiciones de notas al pie (`07`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `18` y `19`), sincronizada en `respaldo_v1.0/md/` con regeneración de huellas SHA-256 antes de iniciar ediciones de la 2.ª edición.
* Auditoría contable matemática al **100.000%**: `1,008,962 / 1,008,962` caracteres alfanuméricos, `197,690` palabras, `535` notas al pie enlazadas (`0` pérdidas, `0` mezclas entre capítulos).
