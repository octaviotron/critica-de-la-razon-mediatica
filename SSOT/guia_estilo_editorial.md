# SSOT: Guía de Estilo y Reglas Operativas para Edición con IA

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Uso:** Lectura obligatoria para la IA al iniciar cada sesión de edición de un capítulo en [`libro/`](../libro/).

---

## 1. Reglas de Fidelidad Textual y Estilo

1. **Conservar la voz filosófica y académica del autor:** No aplanar, simplificar ni vulgarizar el registro ensayístico del profesor Juan Barreto Cipriani. Consultar siempre [`SSOT/perfil_voz_autor.md`](perfil_voz_autor.md) (párrafos modelo, anti-patrones de prosa sintética prohibidos e inventario de los 92 términos del Glosario).
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
   * **Prohibición estricta de inventar citas o páginas:** Al incorporar nuevos autores (Varoufakis, Han, Fisher, Harari, Dennis, Žižek, Sadin, Cortina, Bostrom, Reyes u otros), **nunca inventar citas textuales entrecomilladas ni números de página**. Si la obra existe en [`externos/`](../externos/), verificar el fragmento literal y la página exacta mediante `python3 -B scripts/edicion/buscar_externos.py` (y su ficha en `notas/fuentes/`). Si la fuente está en otro idioma (p. ej. francés en `La vie spectrale.pdf`), indicar `[trad. propia]` o contrastar con edición publicada en castellano. Si no se dispone de la fuente literal verificada, redactar en paráfrasis analítica rigurosa o anotar `[VERIFICAR CITA/PÁG.]` en `notas/capitulos/<archivo>.md`.
6. **Notas al pie sin renumeración manual y omisiones conocidas de 2006:**
   * Nunca borres ni desconectes una llamada `[^n]` ni su definición `[^n]:` existente sin autorización expresa.
   * Si agregas una nota nueva en medio de un capítulo que ya tiene numeración de 2006, **no renumeres manualmente** las notas posteriores: usa un identificador temporal claro (por ejemplo `[^14b]` o `[^algoritmo]`). La renumeración secuencial se realiza solo al cierre editorial.
   * **Omisiones confirmadas del libro impreso de 2006 (NO son errores de conversión):** Todos los artefactos mecánicos de conversión (saltos de línea, listas partidas y 27 notas al pie) ya fueron depurados y sellados en `libro/` y `respaldo_v1.0/`. Las únicas **6 advertencias residuales** que reporta `validar_libro.py` corresponden a omisiones reales de la edición impresa original de 2006 y deben consultarse con el autor al editar cada capítulo afectado:
     * `11_parte2_ensayo_1.md`: definiciones `[^15]:` y `[^19]:` sin llamada en el impreso (y salto del número `17`).
     * `17_parte4_ensayo_1.md`: definición `[^28]:` sin llamada en el impreso.
     * `20_parte4_ensayo_4.md`: llamada `[^3]` (punto 34) cuya definición nunca se imprimió en el folio 377.
     * `24_parte5_ensayo_4.md`: llamada `[^4]` cuya definición nunca se imprimió en el folio 467, y definición `[^2]:` sin llamada en el impreso.
     * `27_parte6_ensayo_3.md`: definición `[^3]:` sin llamada en el impreso.

### 1.1. Decisiones Editoriales Confirmadas para la Segunda Edición
Estas 6 pautas ya fueron definidas con el proyecto y rigen por defecto en todas las sesiones (sin necesidad de volver a preguntarlas):
1. **Inserción de actualizaciones (2006 → actualidad):** *Integración híbrida* — tejer orgánicamente los desarrollos nuevos dentro del flujo del ensayo (sin borrar argumentos de 2006) cuando amplían una tesis ya presente, y abrir subapartados nuevos al cierre de secciones clave cuando se introduce un giro histórico mayor (ej. paso de la TV a plataformas/algoritmos/IA).
2. **Anclaje temporal de cifras y ejemplos de 2006:** *Contextualización histórica + puente al presente* — conservar las referencias de 2006 como hito genealógico (*«hace dos décadas…»*) y contrastarlas de inmediato con el escenario contemporáneo verificado.
3. **Citas de fuentes en otro idioma (ej. francés en `La vie spectrale.pdf`):** *Traducción directa al español + nota de edición original* — insertar las citas traducidas en el cuerpo e indicar en la nota al pie europea la edición original seguida de `[trad. propia]` (sustituible si luego ingresa edición publicada en castellano).
4. **Textos de autores invitados de 2006 (`03`–`06` en `prologos_2006` y Biardeau en `29` desde `L101`):** *Conservación íntegra* como memoria histórica de la 1.ª edición (explicada en el futuro *Prefacio a la Segunda Edición*). En [`libro.yaml`](../libro.yaml), `03_liminar.md` (Michel Maffesoli, intercalado como «Liminar» sin foliar en 2006) queda integrado como **Pro(Logos) I** junto a `04`–`06` (`Pro(Logos)` II–IV) sin renombrar el archivo; solo se unificarían sus encabezados partidos al cierre si el autor lo confirma.
5. **Formato de entrega por defecto para rondas de revisión del autor:** *PDF limpio de lectura* (`compilar_pdf.py --capitulo <id>` en `dist/`) acompañado de resumen breve de 5–10 viñetas. Word `.docx` (`--formato docx`) y PDF etiquetado (`--etiquetar-parrafos`) quedan disponibles solo bajo pedido puntual.
6. **Uniformidad tipográfica y de aparato crítico (aplicación progresiva por capítulo):** Comillas latinas `«»` para citas textuales, `""` para énfasis/citas internas y sustitución de las 40 comillas `‹›`; notas al pie estandarizadas con `Ibíd.`, `Op. cit.` y punto final; corrección automática al paso de `Masmediática` → `Massmediática`, `S. i ek` → `S. Žižek`, `Gumis` → `Gomis`, `Foweler` → `Fowler`, `Lippman` → `Lippmann` y unificación de encabezados partidos; conservar `· Término:` en `31_glosario.md` y decidir recién al cierre si pasa a `### Término`.

---

## 2. Protocolo Operativo de la IA por Capítulo

Para ahorrar tokens y evitar mezclas, **se trabaja un solo archivo `.md` por sesión** (sin leer el resto de `libro/` ni `respaldo_v1.0/md/` salvo para comparar el mismo capítulo contra 2006).

1. **Al recibir instrucciones de edición sobre un capítulo (`libro/<archivo>.md`):**
   * Ejecutar `python3 -B scripts/edicion/contexto_capitulo.py --capitulo <id>` para obtener en un solo paso el briefing completo (estado en `libro.yaml`, alerta de autoría protegida, diagnóstico técnico en vivo, ficha de `notas/capitulos/`, fuentes externas asignadas y menciones en `notas/NOTAS.md`), y consultar [`notas/mapa_obra.md`](../notas/mapa_obra.md) y [`SSOT/perfil_voz_autor.md`](perfil_voz_autor.md).
   * Para verificar citas o conceptos dentro del propio libro o del Glosario sin cargar otros capítulos, usar `python3 -B scripts/edicion/buscar_libro.py`; para citas literales de `externos/`, usar `python3 -B scripts/edicion/buscar_externos.py`.
   * Aplicar las modificaciones solicitadas directamente en `libro/<archivo>.md`.
   * Actualizar su `estado` a `"en_revision"` en [`libro.yaml`](../libro.yaml) si estaba en `"pendiente"`.
   * Ejecutar silenciosamente la validación del capítulo:
     `python3 -B scripts/edicion/validar_libro.py --capitulo <id>`
2. **Al avisar el usuario que añadió o actualizó archivos en `externos/`:**
   * Ejecutar silenciosamente `python3 -B scripts/edicion/indexar_externos.py` (indexación incremental en `dist/indice_externos/corpus.db` y alta en `notas/fuentes/catalogo.yaml`).
   * Inspeccionar metadatos, colofón y TOC de las fuentes nuevas mediante `buscar_externos.py --info` y `--leer <slug> --paginas 1-6` (más créditos finales si hace falta).
   * Completar los campos editoriales en `notas/fuentes/catalogo.yaml` (cita europea, postura de diálogo, temas, capítulos destino, `estado: "fichado"`), redactar `notas/fuentes/<slug>.md`, enlazar en `notas/NOTAS.md` y entregar un resumen breve al usuario.
3. **Al preparar una entrega para revisión del autor:**
   * Generar el archivo limpio **solo de ese capítulo** en `dist/` (PDF por defecto o Word `.docx` si el autor revisa en Word/Google Docs):
     * PDF: `python3 -B scripts/edicion/compilar_pdf.py --capitulo <id>`
     * Word: `python3 -B scripts/edicion/compilar_pdf.py --capitulo <id> --formato docx`
   * Comparar ese capítulo contra 2006 (`python3 -B scripts/edicion/reporte_cambios.py --capitulo <id>`) y entregar al usuario un **resumen breve (5–10 viñetas)** de qué se actualizó para acompañar el envío al autor.
4. **Al recibir observaciones del autor:**
   * Registrar las observaciones en `notas/capitulos/<archivo>.md`, aplicar las correcciones indicadas sobre el mismo `libro/<archivo>.md`, volver a validar el capítulo y generar un nuevo PDF/DOCX de revisión si hace falta.
5. **Al recibir la aprobación explícita del autor (confirmada por el usuario):**
   * Marcar como completadas (`- [x]`) las tareas incorporadas en `notas/capitulos/<archivo>.md`, en `notas/fuentes/<slug>.md` (si se integraron fuentes externas) y en [`notas/NOTAS.md`](../notas/NOTAS.md).
   * Actualizar el resumen de 2.ª edición y el registro de autores/conceptos ya introducidos en [`notas/mapa_obra.md`](../notas/mapa_obra.md).
   * Anotar cualquier término nuevo de Glosario o referencia nueva para Bibliografía en [`notas/NOTAS.md`](../notas/NOTAS.md) (no en `CHANGELOG.md`).
   * Cambiar `estado: "aprobado"` en [`libro.yaml`](../libro.yaml).
   * Registrar el capítulo aprobado en [`CHANGELOG.md`](../CHANGELOG.md).
   * Dejar los cambios listos para que el usuario haga su `commit` + `push` (o ejecutarlo solo si el usuario lo pide expresamente).

---

## 3. Reglas de Seguridad Inviolables

* **Directorios intocables / solo lectura:** Nunca modificar, renombrar ni escribir dentro de [`respaldo_v1.0/`](../respaldo_v1.0/), [`fuente/`](../fuente/), [`scripts/extraccion_v1/`](../scripts/extraccion_v1/) ni [`externos/`](../externos/).
* **Textos de autores invitados protegidos (NO reescribir contenido sin orden expresa del usuario/autor; verificados automáticamente por `validar_libro.py`):**
  * [`libro/03_liminar.md`](../libro/03_liminar.md) — **Pro(Logos) I:** Michel Maffesoli (íntegro; publicado como *Liminar* en 2006).
  * [`libro/04_prologo_1_rigoberto_lanz.md`](../libro/04_prologo_1_rigoberto_lanz.md) — **Pro(Logos) II:** Rigoberto Lanz (íntegro).
  * [`libro/05_prologo_2_nelson_guzman.md`](../libro/05_prologo_2_nelson_guzman.md) — **Pro(Logos) III:** Nelson Guzmán (íntegro).
  * [`libro/06_prologo_3_magaldy_tellez.md`](../libro/06_prologo_3_magaldy_tellez.md) — **Pro(Logos) IV:** Magaldy Téllez (íntegro).
  * [`libro/29_post_scriptum.md`](../libro/29_post_scriptum.md) — **Frontera exacta:** líneas `1–100` (*Primer* y *Segundo movimiento*) son de Juan Barreto (editables); desde la **línea `101`** (`### Tercer movimiento: Entre dinosaurios y unicornios`) es ensayo invitado de Javier Biardeau (protegido).
* **Regla sobre todos los `README.md` públicos:** Prohibido mencionar explícitamente «IA» o «Inteligencia Artificial» en cualquier archivo `README.md` del repositorio (`README.md`, `libro/README.md`, `notas/README.md`, `respaldo_v1.0/README.md`, `scripts/README.md`, `SSOT/README.md`). Emplear siempre términos como *edición asistida* o *ejecución asistida de scripts*.
* **Límites en Git y estado `aprobado`:** Trabajar siempre en `main`; **no crear ramas ni tags**; **no ejecutar `git commit` ni `git push` sin instrucción explícita del usuario**; y **nunca marcar `estado: "aprobado"` en `libro.yaml`** por iniciativa propia (solo cuando el usuario confirme la aprobación del autor).
* **Separación estricta `notas/NOTAS.md` vs. `CHANGELOG.md`:** Todo lo *pendiente* (autores, glosario, bibliografía futura, cambios de índice) va en [`notas/NOTAS.md`](../notas/NOTAS.md); [`CHANGELOG.md`](../CHANGELOG.md) registra únicamente lo *ya aprobado o completado*.
* **Índices y carpeta `dist/`:** No editar `libro/01_indice.md` manualmente ni actualizar `libro/32_indice_onomastico.md` hasta el cierre editorial. La carpeta `dist/` es de salidas temporales para entregas (PDF por defecto salvo que se pida Word `.docx`) y puede limpiarse libremente.
