# SSOT: Guía de Estilo y Reglas Operativas para Edición con IA

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Uso:** Lectura obligatoria para la IA al iniciar cada sesión de edición de un capítulo en [`libro/`](../libro/).

---

## 1. Reglas de Fidelidad Textual y Estilo

1. **Conservar la voz filosófica y académica del autor:** No aplanar, simplificar ni vulgarizar el registro ensayístico del profesor Juan Barreto Cipriani.
2. **Nunca resumir ni recortar argumentos** salvo instrucción explícita del usuario o del autor.
3. **Vocabulario conceptual protegido (no reemplazar por sinónimos ni eliminar guiones conceptuales):**
   * `massmediática`, `mass-media`, `biopolítica`, `biopoder`, `agenciamiento`, `significante-signo`, `cuerpo-potencia`, `rostro-proceso`, `hecha-en-común`, `trabajo-valor`, `ético-política`, `post-scriptum`, `rizoma`, `pliegue`, `líneas de fuga`, `subjetividad`, `performativo`, `habitus`, `multitud`, `dispositivo`, `aura`.
4. **Convenciones Markdown y límites técnicos de compilación (`compilar_pdf.py`):**
   * **Sintaxis soportada en `libro/*.md`:**
     * Encabezados: `#` título principal del capítulo, `##` subtítulos internos, `###` sub-subtítulos. *(Nota: [`libro/31_glosario.md`](../libro/31_glosario.md) usa actualmente el formato `· Término:` en sus 93 entradas; no reformatear a `###` sin decisión expresa al cierre.)*
     * Epígrafes: `> *Texto del epígrafe*` seguido de `> — Autor`.
     * Citas extensas a bando: bloque `> ...` conservando cursivas originales.
     * Listas con viñetas (`- `) y **listas numeradas extensas (`1.`, `2.`, …)**: dejar siempre **una línea en blanco entre cada ítem numerado** (como en `libro/13_parte2_ensayo_3.md` y `libro/20_parte4_ensayo_4.md`) para que `compilar_pdf.py` renderice cada punto como bloque independiente y no los agrupe en un solo párrafo.
     * Formato inline: `***negrita cursiva***`, `**negrita**`, `*cursiva*` (nunca dejar asteriscos impares ni cruzar saltos de línea).
     * Notas al pie: llamadas `[^id]` en el cuerpo y definiciones `[^id]: texto` al final del archivo tras `---` en un solo párrafo por nota. Las llamadas inline seguidas de dos puntos (ej. `cultura de masas[^41]:`) son sintaxis válida reconocida por `validar_libro.py` y `compilar_pdf.py`.
   * **Sintaxis a EVITAR en `libro/*.md`** *(el motor PangoCairo de `compilar_pdf.py` no la renderiza y la imprimiría en crudo)*: encabezados de 4.º nivel (`####`), tablas Markdown (`|...|`), bloques de código (` ``` `), imágenes incrustadas (`![...]`) y notas al pie divididas en múltiples párrafos con línea en blanco.
5. **Estándar editorial de citas, comillas y política anti-alucinación bibliográfica:**
   * **Sistema de citas:** Usar notas al pie de tradición clásica europea (no formato APA en el cuerpo): `Inicial. Apellido, *Título del libro*, Editorial, Ciudad, Año, p. X.` (con *Ibíd.*, *Op. cit.* y punto final).
   * **Comillas:** Preferir comillas latinas (`«»`) para citas textuales, comillas dobles (`""`) para énfasis o citas internas y evitar comillas angulares simples (`‹›`).
   * **Prohibición estricta de inventar citas o páginas:** Al incorporar nuevos autores (Varoufakis, Han, Fisher, Harari, Dennis, Žižek u otros), **nunca inventar citas textuales entrecomilladas ni números de página**. Si no se dispone de la fuente literal verificada, redactar en paráfrasis analítica rigurosa o anotar `[VERIFICAR CITA/PÁG.]` en `notas/capitulos/<archivo>.md`.
6. **Notas al pie sin renumeración manual y omisiones conocidas de 2006:**
   * Nunca borres ni desconectes una llamada `[^n]` ni su definición `[^n]:` existente sin autorización expresa.
   * Si agregas una nota nueva en medio de un capítulo que ya tiene numeración de 2006, **no renumeres manualmente** las notas posteriores: usa un identificador temporal claro (por ejemplo `[^14b]` o `[^algoritmo]`). La renumeración secuencial se realiza solo al cierre editorial.
   * **Omisiones confirmadas del libro impreso de 2006 (NO son errores de conversión):** Todos los artefactos mecánicos de conversión (saltos de línea, listas partidas y 27 notas al pie) ya fueron depurados y sellados en `libro/` y `respaldo_v1.0/`. Las únicas **6 advertencias residuales** que reporta `validar_libro.py` corresponden a omisiones reales de la edición impresa original de 2006 y deben consultarse con el autor al editar cada capítulo afectado:
     * `11_parte2_ensayo_1.md`: definiciones `[^15]:` y `[^19]:` sin llamada en el impreso (y salto del número `17`).
     * `17_parte4_ensayo_1.md`: definición `[^28]:` sin llamada en el impreso.
     * `20_parte4_ensayo_4.md`: llamada `[^3]` (punto 34) cuya definición nunca se imprimió en el folio 377.
     * `24_parte5_ensayo_4.md`: llamada `[^4]` cuya definición nunca se imprimió en el folio 467, y definición `[^2]:` sin llamada en el impreso.
     * `27_parte6_ensayo_3.md`: definición `[^3]:` sin llamada en el impreso.

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
4. **Al recibir la aprobación explícita del autor (confirmada por el usuario):**
   * Marcar como completadas (`- [x]`) las tareas incorporadas en `notas/capitulos/<archivo>.md` y en [`notas/NOTAS.md`](../notas/NOTAS.md).
   * Anotar cualquier término nuevo de Glosario o referencia nueva para Bibliografía en [`notas/NOTAS.md`](../notas/NOTAS.md) (no en `CHANGELOG.md`).
   * Cambiar `estado: "aprobado"` en [`libro.yaml`](../libro.yaml).
   * Registrar el capítulo aprobado en [`CHANGELOG.md`](../CHANGELOG.md).
   * Dejar los cambios listos para que el usuario haga su `commit` + `push` (o ejecutarlo solo si el usuario lo pide expresamente).

---

## 3. Reglas de Seguridad Inviolables

* **Directorios intocables:** Nunca modificar, renombrar ni escribir dentro de [`respaldo_v1.0/`](../respaldo_v1.0/), [`fuente/`](../fuente/) ni [`scripts/extraccion_v1/`](../scripts/extraccion_v1/).
* **Textos de autores invitados protegidos (NO reescribir contenido sin orden expresa del usuario/autor):**
  * [`libro/03_liminar.md`](../libro/03_liminar.md) — Michel Maffesoli.
  * [`libro/04_prologo_1_rigoberto_lanz.md`](../libro/04_prologo_1_rigoberto_lanz.md) — Rigoberto Lanz.
  * [`libro/05_prologo_2_nelson_guzman.md`](../libro/05_prologo_2_nelson_guzman.md) — Nelson Guzmán.
  * [`libro/06_prologo_3_magaldy_tellez.md`](../libro/06_prologo_3_magaldy_tellez.md) — Magaldy Téllez.
  * [`libro/29_post_scriptum.md`](../libro/29_post_scriptum.md) — *Tercer movimiento: Entre dinosaurios y unicornios* (Javier Biardeau).
* **Regla sobre todos los `README.md` públicos:** Prohibido mencionar explícitamente «IA» o «Inteligencia Artificial» en cualquier archivo `README.md` del repositorio (`README.md`, `libro/README.md`, `notas/README.md`, `respaldo_v1.0/README.md`, `SSOT/README.md`). Emplear siempre términos como *edición asistida* o *ejecución asistida de scripts*.
* **Límites en Git y estado `aprobado`:** Trabajar siempre en `main`; **no crear ramas ni tags**; **no ejecutar `git commit` ni `git push` sin instrucción explícita del usuario**; y **nunca marcar `estado: "aprobado"` en `libro.yaml`** por iniciativa propia (solo cuando el usuario confirme la aprobación del autor).
* **Separación estricta `notas/NOTAS.md` vs. `CHANGELOG.md`:** Todo lo *pendiente* (autores, glosario, bibliografía futura, cambios de índice) va en [`notas/NOTAS.md`](../notas/NOTAS.md); [`CHANGELOG.md`](../CHANGELOG.md) registra únicamente lo *ya aprobado o completado*.
* **Índices y carpeta `dist/`:** No editar `libro/01_indice.md` manualmente ni actualizar `libro/32_indice_onomastico.md` hasta el cierre editorial. La carpeta `dist/` es de salidas temporales para entregas (PDF por defecto salvo que se pida Word `.docx`) y puede limpiarse libremente.
