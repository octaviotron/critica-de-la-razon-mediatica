# SSOT: Guía de Estilo y Reglas Operativas para Edición con IA

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Uso:** Lectura obligatoria para la IA al iniciar cada sesión de edición de un capítulo en [`libro/`](../libro/).

---

## 1. Reglas de Fidelidad Textual y Estilo

1. **Conservar la voz filosófica y académica del autor:** No aplanar, simplificar ni vulgarizar el registro ensayístico del profesor Juan Barreto Cipriani.
2. **Nunca resumir ni recortar argumentos** salvo instrucción explícita del usuario o del autor.
3. **Vocabulario conceptual protegido (no reemplazar por sinónimos ni eliminar guiones conceptuales):**
   * `massmediática`, `mass-media`, `biopolítica`, `biopoder`, `agenciamiento`, `significante-signo`, `cuerpo-potencia`, `rostro-proceso`, `hecha-en-común`, `trabajo-valor`, `ético-política`, `post-scriptum`, `rizoma`, `pliegue`, `líneas de fuga`, `subjetividad`, `performativo`, `habitus`, `multitud`, `dispositivo`, `aura`.
4. **Convenciones Markdown del libro:**
   * Encabezados: `#` título principal del capítulo, `##` subtítulos internos, `###` sub-subtítulos (o entradas de Glosario).
   * Epígrafes: `> *Texto del epígrafe*` seguido de `> — Autor`.
   * Citas extensas a bando: bloque `> ...` conservando cursivas originales.
   * Notas al pie: llamadas `[^id]` en el cuerpo y definiciones `[^id]: texto` al final del archivo tras `---`.
5. **Notas al pie sin renumeración manual:**
   * Nunca borres ni desconectes una llamada `[^n]` ni su definición `[^n]:` existente sin autorización expresa.
   * Si agregas una nota nueva en medio de un capítulo que ya tiene numeración de 2006, **no renumeres manualmente** las notas posteriores: usa un identificador temporal claro (por ejemplo `[^14b]` o `[^algoritmo]`). La renumeración secuencial se realiza solo al cierre editorial.

---

## 2. Protocolo Operativo de la IA por Capítulo

Para ahorrar tokens y evitar mezclas, **se trabaja un solo archivo `.md` por sesión** (sin leer el resto de `libro/` ni `respaldo_v1.0/md/` salvo para comparar el mismo capítulo contra 2006).

1. **Al recibir instrucciones de edición sobre un capítulo (`libro/<archivo>.md`):**
   * Leer únicamente el archivo `.md` objetivo, su ficha espejo en [`notas/capitulos/`](../notas/capitulos/) (`notas/capitulos/<archivo>.md`), las referencias pertinentes de [`notas/NOTAS.md`](../notas/NOTAS.md) y esta guía.
   * Aplicar las modificaciones solicitadas directamente en `libro/<archivo>.md`.
   * Actualizar su `estado` a `"en_revision"` en [`libro.yaml`](../libro.yaml) si estaba en `"pendiente"`.
   * Ejecutar silenciosamente la validación del capítulo:
     `python3 -B scripts/edicion/validar_libro.py --capitulo <id>`
2. **Al preparar una entrega para revisión del autor:**
   * Generar el archivo limpio **solo de ese capítulo** en `dist/` (PDF por defecto o Word `.docx` si el autor revisa en Word/Google Docs):
     * PDF: `python3 -B scripts/edicion/compilar_pdf.py --capitulo <id>`
     * Word: `python3 -B scripts/edicion/compilar_pdf.py --capitulo <id> --formato docx`
   * Comparar ese capítulo contra 2006 (`python3 -B scripts/edicion/reporte_cambios.py --capitulo <id>`) y entregar al usuario un **resumen breve (5–10 viñetas)** de qué se actualizó para acompañar el envío al autor.
3. **Al recibir observaciones del autor:**
   * Registrar las observaciones en `notas/capitulos/<archivo>.md`, aplicar las correcciones indicadas sobre el mismo `libro/<archivo>.md`, volver a validar el capítulo y generar un nuevo PDF/DOCX de revisión si hace falta.
4. **Al recibir la aprobación del autor:**
   * Marcar como completadas (`- [x]`) las tareas incorporadas en `notas/capitulos/<archivo>.md` y en [`notas/NOTAS.md`](../notas/NOTAS.md).
   * Cambiar `estado: "aprobado"` en [`libro.yaml`](../libro.yaml).
   * Registrar el capítulo aprobado (y cualquier término nuevo para Glosario o referencia nueva para Bibliografía) en [`CHANGELOG.md`](../CHANGELOG.md).
   * Dejar el archivo listo para un único `commit` + `push`.

---

## 3. Reglas de Seguridad Inviolables

* **Nunca modificar, renombrar ni escribir** dentro de [`respaldo_v1.0/`](../respaldo_v1.0/) ni dentro de [`fuente/`](../fuente/).
* **No editar `libro/01_indice.md` manualmente** durante la revisión de capítulos individuales; el índice se regenera automáticamente desde [`libro.yaml`](../libro.yaml) cuando se añadan capítulos, cambie el orden o se cierre la edición.
* **No actualizar `libro/32_indice_onomastico.md`** hasta el cierre definitivo del manuscrito.
