# Reglas Universales del Workspace — *Crítica de la Razón Mediática* (2.ª Edición)

Este archivo proporciona el contexto completo, las reglas inviolables, los flujos de trabajo y el protocolo de mantenimiento del repositorio para cualquier agente de IA que opere en este proyecto.

---

## 1. Identidad y Objetivo del Proyecto

* **Obra:** *Crítica de la Razón Mediática. Ensayos sobre biopolítica y potencia política del cuerpo (Pre-textos para un debate por el socialismo)*
* **Autor:** Juan Barreto Cipriani (1.ª edición: UCV / CIPOST, Caracas, 2006; ISBN `980-12-1936-X`)
* **Asesoría informática:** Octavio Rossell Tabet (`octavio.rossell@gmail.com`)
* **Objetivo activo:** Preparar la **Segunda Edición** revisada y actualizada, trabajando **un capítulo `.md` a la vez** en `libro/`, con mínima fricción técnica para el usuario (el usuario opera en lenguaje natural y el agente ejecuta silenciosamente los scripts internos bajo demanda).
* **Base digital verificada:** 33 archivos Markdown (`197,690` palabras, `2,685` bloques, `535` notas al pie, `1,008,962 / 1,008,962` caracteres alfanuméricos, exactitud `100.000%` frente al PDF de 2006).

---

## 2. Jerarquía de Verdad (Prevención de Contradicciones)

Para evitar reglas duplicadas o contradictorias, rige esta precedencia estricta:
1. **`AGENTS.md` (este archivo):** Punto de entrada universal, mapa completo del repositorio, límites de seguridad y protocolo de sincronización ante cambios estructurales.
2. **`SSOT/guia_estilo_editorial.md` y `SSOT/flujo_editorial_segunda_edicion.md`:** Fuente única de verdad operativa para estilo, citas, sintaxis y flujo editorial.
3. **`libro.yaml`:** Manifiesto maestro del orden de partes/capítulos y tablero de `estado` (`pendiente` | `en_revision` | `aprobado`).
4. **`notas/` (`NOTAS.md`, `capitulos/`, `fuentes/`):** Único espacio para todo lo pendiente, observaciones del autor y fichas de bibliografía externa.
5. **`CHANGELOG.md`:** Único registro de hechos cerrados (capítulos ya aprobados e hitos completados).

> Si detectas una contradicción entre `AGENTS.md`, `SSOT/`, un `README.md` o un script en `scripts/edicion/`, **detente, repórtala al usuario** y aplica el Protocolo de Mantenimiento (Sección 9) antes de continuar editando capítulos.

---

## 3. Mapa Completo del Repositorio (Responsabilidades sin Solapamientos)

| Ruta | Naturaleza | Responsabilidad exacta |
| :--- | :--- | :--- |
| `AGENTS.md` | Editable (mantener sincronizado) | Regla universal del workspace para agentes de IA. |
| `libro/` | **Única copia viva** | Capítulos publicables en Markdown (sin notas internas ni borradores). Los 33 nombres originales actúan como IDs estables (**Opción A**). |
| `libro.yaml` | Editable (manifiesto maestro) | Orden del índice, agrupación en 8 secciones y `estado` de cada capítulo. |
| `notas/NOTAS.md` | Editable | Bandeja global de pendientes: autores por incluir, ideas transversales, candidatos al Glosario, nuevos capítulos/índice y hallazgos técnicos. |
| `notas/capitulos/` | Editable | Ficha espejo por capítulo (`<mismo_nombre>.md` que en `libro/`, más planificación de capítulos futuros como `prefacio_segunda_edicion.md`). |
| `notas/fuentes/` | Editable | Catálogo maestro (`catalogo.yaml`) y fichas de lectura curadas (`<slug>.md`) de la bibliografía depositada en `externos/`. |
| `externos/` | **Solo lectura (versionado en Git)** | Biblioteca de bibliografía externa (PDF, HTML, TXT, MD, DOCX, EPUB). Nunca editar ni renombrar archivos aquí. |
| `CHANGELOG.md` | Editable (solo hechos cerrados) | Registro exclusivo de capítulos ya aprobados por el autor e hitos completados. |
| `scripts/edicion/` | Editable (herramientas internas) | Scripts Python ejecutados por el agente bajo demanda (validación, compilación PDF/DOCX, diffs, índice e indexación/búsqueda en `externos/`). |
| `SSOT/` | Editable (documentación rectora) | `README.md`, `flujo_editorial_segunda_edicion.md`, `guia_estilo_editorial.md` (activos); `proceso_conversion_pdf_a_md.md` y `detalle_ejecucion_y_auditoria_conversion.md` (solo consulta histórica). |
| `fuente/` | **INTOCABLE (solo lectura)** | PDF maestro de 2006, maquetación QuarkXPress (`.qxp`), tipografías (`FUENTES/`), portadas (`PORTADA/`) y portadillas (`RAZON/images/`). |
| `respaldo_v1.0/` | **INTOCABLE (solo lectura)** | Copia congelada e inmutable de los 33 `.md` de 2006, `libro.yaml` de v1.0 y huellas SHA-256 (`manifiesto_v1.0.md`). |
| `scripts/extraccion_v1/` | **CONGELADO (solo lectura)** | Pipeline histórico de extracción y auditoría 100% de 2006. Nunca modificar ni re-ejecutar sobre `libro/`. |
| `dist/` | **Temporal (ignorado por Git)** | Salidas desechables: entregas PDF/DOCX, reportes comparativos e índice local `dist/indice_externos/corpus.db` (SQLite FTS5) + `txt/`. |

---

## 4. Política de Lectura Progresiva (Ahorro de Contexto)

* **Al editar un capítulo:** lee únicamente `SSOT/guia_estilo_editorial.md`, `libro/<archivo>.md`, `notas/capitulos/<archivo>.md`, los puntos pertinentes de `notas/NOTAS.md` y las fichas asignadas en `notas/fuentes/` (vía `buscar_externos.py --para-capitulo <id>`).
* **NO cargar en sesiones normales:**
  * Múltiples capítulos de `libro/` ni el directorio `respaldo_v1.0/md/` (salvo comparación puntual del mismo capítulo vía `reporte_cambios.py`).
  * Libros o PDFs completos de `externos/` (consultar siempre mediante `buscar_externos.py` por búsqueda FTS5 o rangos cortos de páginas `--leer <slug> --paginas A-B`).
  * `SSOT/proceso_conversion_pdf_a_md.md`, `SSOT/detalle_ejecucion_y_auditoria_conversion.md` y `scripts/extraccion_v1/` (solo ante dudas históricas sobre 2006).

---

## 5. Reglas Inviolables de Seguridad, Autoría y Git

1. **Directorios prohibidos para escritura:** Nunca modificar, renombrar, mover ni escribir dentro de `respaldo_v1.0/`, `fuente/`, `scripts/extraccion_v1/` ni `externos/`.
2. **Textos de autores invitados protegidos (NO reescribir contenido sin orden expresa del usuario/autor):**
   * `libro/03_liminar.md` — Michel Maffesoli.
   * `libro/04_prologo_1_rigoberto_lanz.md` — Rigoberto Lanz.
   * `libro/05_prologo_2_nelson_guzman.md` — Nelson Guzmán.
   * `libro/06_prologo_3_magaldy_tellez.md` — Magaldy Téllez.
   * `libro/29_post_scriptum.md` — *Tercer movimiento: Entre dinosaurios y unicornios* (Javier Biardeau).
3. **Prohibición absoluta en todos los `README.md` públicos:** Nunca mencionar «IA» ni «Inteligencia Artificial» en `README.md`, `libro/README.md`, `notas/README.md`, `respaldo_v1.0/README.md` ni `SSOT/README.md`. Usar siempre *edición asistida* o *ejecución asistida de scripts*.
4. **Git lineal y aprobaciones:**
   * Trabajar siempre en `main`; **no crear ramas ni tags**.
   * **Nunca ejecutar `git commit` ni `git push`** sin instrucción explícita del usuario.
   * **Nunca cambiar `estado: "aprobado"` en `libro.yaml`** por iniciativa propia: solo tras confirmación explícita del usuario de que el autor aprobó el capítulo.
5. **Separación `notas/` vs. `CHANGELOG.md`:** Todo lo pendiente va en `notas/`; `CHANGELOG.md` registra solo capítulos aprobados e hitos ya cerrados.
6. **Índices protegidos hasta el cierre:** No editar `libro/01_indice.md` manualmente ni modificar `libro/32_indice_onomastico.md` hasta el cierre editorial.

---

## 6. Reglas Editoriales, de Estilo y Límites de Compilación

1. **Fidelidad de voz y argumentos:** Conservar el registro filosófico-ensayístico de Juan Barreto Cipriani; nunca resumir ni recortar argumentos sin instrucción expresa.
2. **Vocabulario conceptual protegido (no sustituir ni quitar guiones):** `massmediática`, `mass-media`, `biopolítica`, `biopoder`, `agenciamiento`, `significante-signo`, `cuerpo-potencia`, `rostro-proceso`, `hecha-en-común`, `trabajo-valor`, `ético-política`, `post-scriptum`, `rizoma`, `pliegue`, `líneas de fuga`, `subjetividad`, `performativo`, `habitus`, `multitud`, `dispositivo`, `aura`.
3. **Sintaxis Markdown en `libro/*.md` (compatibilidad con PangoCairo en `compilar_pdf.py`):**
   * **Permitida:** `#`, `##`, `###`, epígrafes (`> *...*` + `> — Autor`), citas a bando (`> ...`), listas `- `, listas numeradas `1.`, `2.` **con una línea en blanco entre cada ítem**, inline `***...***`, `**...**`, `*...*`, llamadas `[^id]` y definiciones `[^id]: texto` en un solo párrafo al final tras `---`.
   * **PROHIBIDA en `libro/*.md`:** `####`, tablas Markdown (`|...|`), bloques de código (`` ``` ``), imágenes (`![...]`), asteriscos impares/cruzando líneas y notas al pie divididas en varios párrafos.
   * No reformatear `libro/31_glosario.md` (`· Término:`) sin decisión expresa al cierre.
4. **Citas europeas y política anti-alucinación bibliográfica:**
   * Formato obligatorio en notas al pie: `Inicial. Apellido, *Título del libro*, Editorial, Ciudad, Año, p. X.` (*Ibíd.*, *Op. cit.* y punto final). Preferir comillas latinas `«»` para citas textuales y `""` para citas internas/énfasis; evitar `‹›`.
   * **Nunca inventar citas textuales ni números de página.** Si la obra está en `externos/`, verificar el texto exacto y la página mediante `buscar_externos.py`. Si está en otro idioma (p. ej. francés), indicar `[trad. propia]` o contrastar con edición publicada en español. Si no hay fuente literal verificada, usar paráfrasis analítica o anotar `[VERIFICAR CITA/PÁG.]` en `notas/capitulos/<archivo>.md`.
5. **Notas al pie:** Nunca borrar ni desconectar notas existentes sin autorización. Al insertar una nota nueva en medio de un capítulo ya numerado, **no renumerar manualmente**: usar identificador temporal (`[^14b]`, `[^algoritmo]`) hasta el cierre.
6. **6 advertencias / 7 omisiones confirmadas del impreso de 2006 (NO son fallos de conversión; consultar con el autor al editar cada archivo):**
   * `11_parte2_ensayo_1.md`: definiciones `[^15]:` y `[^19]:` sin llamada (y salto del `17`).
   * `17_parte4_ensayo_1.md`: definición `[^28]:` sin llamada.
   * `20_parte4_ensayo_4.md`: llamada `[^3]` sin definición al pie (folio 377).
   * `24_parte5_ensayo_4.md`: llamada `[^4]` sin definición (folio 467) y definición `[^2]:` sin llamada.
   * `27_parte6_ensayo_3.md`: definición `[^3]:` sin llamada.

---

## 7. Flujos Operativos en Lenguaje Natural (Cero Comandos Manuales para el Usuario)

El usuario nunca necesita invocar scripts manualmente. El agente ejecuta los comandos de `scripts/edicion/` de forma silenciosa y transparente según la intención del usuario:

### Flujo A — Edición capítulo por capítulo (`libro/`)
1. **Inicio / edición:** Leer `libro/<archivo>.md`, `notas/capitulos/<archivo>.md`, `notas/NOTAS.md` y fuentes mapeadas (`python3 -B scripts/edicion/buscar_externos.py --para-capitulo <id>`). Aplicar cambios en `libro/<archivo>.md`, pasar `estado` a `"en_revision"` en `libro.yaml` (si estaba en `"pendiente"`) y validar con `python3 -B scripts/edicion/validar_libro.py --capitulo <id>`.
2. **Entrega al autor:** Compilar solo ese capítulo en `dist/` (`compilar_pdf.py --capitulo <id>`, añadiendo `--formato docx` si el autor pide Word, o `--etiquetar-parrafos` para PDF etiquetado `[ID.PPP]`), ejecutar `reporte_cambios.py --capitulo <id>` y redactar un resumen breve (5–10 viñetas) para acompañar el envío.
3. **Observaciones del autor:** Registrarlas en `notas/capitulos/<archivo>.md`, aplicar los ajustes en `libro/<archivo>.md`, revalidar y recompilar.
4. **Cierre (solo tras confirmación explícita de aprobación):** Marcar `- [x]` en `notas/capitulos/<archivo>.md`, `notas/fuentes/<slug>.md` y `notas/NOTAS.md`; anotar nuevos términos de Glosario/Bibliografía en `notas/NOTAS.md`; marcar `estado: "aprobado"` en `libro.yaml`; registrar el capítulo en `CHANGELOG.md`. Dejar listo para `commit`/`push` del usuario.

### Flujo B — Incorporación y consulta de bibliografía externa (`externos/` → `notas/fuentes/`)
Cuando el usuario diga que añadió, modificó o quitó archivos en `externos/` (ej. *"Añadí nueva bibliografía en `externos/`"*):
1. Ejecutar `python3 -B scripts/edicion/indexar_externos.py` (escaneo incremental por SHA-256 → actualiza `dist/indice_externos/corpus.db` en SQLite FTS5, genera textos paginados en `dist/indice_externos/txt/` y da de alta las fuentes nuevas en `notas/fuentes/catalogo.yaml` sin sobrescribir campos ya curados).
2. Para cada fuente nueva (`estado: pendiente_ficha`), inspeccionar metadatos, colofón y TOC mediante `buscar_externos.py --info <slug>` y `--leer <slug> --paginas 1-6` (más páginas de créditos finales si aplica), sin volcar el documento completo al contexto.
3. Completar en `notas/fuentes/catalogo.yaml`: título, autor, año, editorial, ciudad, URL, idioma, `cita_europea`, `postura_dialogo` (`afin` | `dialogo_critico` | `critica` | `insumo_empirico`), `temas`, `capitulos_destino` y `estado: "fichado"`.
4. Crear/actualizar la ficha curada `notas/fuentes/<slug>.md` (tesis, estructura, ejes de diálogo con el libro, advertencias técnicas/idioma y checklist de capítulos) y enlazar la obra en `notas/NOTAS.md`.
5. Entregar al usuario un resumen breve de las fuentes incorporadas y su mapeo sugerido por capítulo.
* **Auto-sincronización silenciosa:** `buscar_externos.py` comprueba automáticamente si hay archivos nuevos o modificados en `externos/` (o si `corpus.db` falta tras un `git clone`) y reindexa en segundo plano antes de responder cualquier consulta.

### Flujo C — Nuevos capítulos, índice y cierre editorial
* **Añadir capítulo nuevo** (ej. futuro `libro/prefacio_segunda_edicion.md`, hoy solo planificado en `notas/capitulos/prefacio_segunda_edicion.md`): crear el `.md` en `libro/` con nombre descriptivo, declararlo en `libro.yaml` (`id` único, `estado: "pendiente"`), añadirlo a `libro/README.md` y enlazar/crear su ficha en `notas/capitulos/`.
* **Reordenar partes o capítulos:** Nunca renombrar archivos existentes en `libro/`; reordenar únicamente en `libro.yaml` y reflejarlo en `libro/README.md`.
* **Cierre editorial (una sola vez, al aprobar todos los capítulos):** Consolidar `30_bibliografia.md` (apoyándose en `notas/fuentes/catalogo.yaml` y `notas/NOTAS.md`) y `31_glosario.md`; sanear encabezados partidos y regenerar `01_indice.md` con `generar_indice.py --escribir`; validar todo el libro; compilar borrador completo; actualizar `32_indice_onomastico.md` con la paginación definitiva.

---

## 8. Catálogo de Herramientas Internas (`scripts/edicion/`)

Ejecutar siempre con `python3 -B` para evitar cachés `__pycache__`:

| Script | Propósito | Ejemplo de invocación interna |
| :--- | :--- | :--- |
| `manifiesto.py` | Módulo compartido que carga `libro.yaml` o `respaldo_v1.0/libro.yaml` y bloquea escrituras en `respaldo_v1.0/`. | *(importado por los demás scripts)* |
| `validar_libro.py` | Valida estructura, notas al pie, enlaces locales, tablero de `estado` y SHA-256 del respaldo (`--verificar-respaldo`). | `python3 -B scripts/edicion/validar_libro.py --capitulo 19` |
| `compilar_pdf.py` | Compila 1 capítulo (`--capitulo`) o el libro completo en `dist/` en PDF o Word (`--formato docx`). Soporta `--manifiesto respaldo_v1.0/libro.yaml` y `--etiquetar-parrafos`. | `python3 -B scripts/edicion/compilar_pdf.py --capitulo 19` |
| `reporte_cambios.py` | Compara 1 capítulo o el libro completo contra `respaldo_v1.0/` (o `--desde-git`) generando informe en `dist/`. | `python3 -B scripts/edicion/reporte_cambios.py --capitulo 19 --incluir-diffs` |
| `generar_indice.py` | Genera el Índice General desde `libro.yaml` y encabezados `#`/`##` (en `dist/` por defecto; `--escribir` actualiza `libro/01_indice.md`). | `python3 -B scripts/edicion/generar_indice.py --escribir` |
| `indexar_externos.py` | Indexa incrementalmente `externos/` (PDF, HTML, TXT, MD, DOCX, EPUB) en SQLite FTS5 (`dist/indice_externos/corpus.db`) y sincroniza `notas/fuentes/catalogo.yaml`. | `python3 -B scripts/edicion/indexar_externos.py` |
| `buscar_externos.py` | Consulta FTS5 BM25, lee rangos exactos (`--leer <slug> --paginas A-B`), inspecciona TOC (`--info`) y lista fuentes por capítulo (`--para-capitulo <id>`) con auto-sync silencioso. | `python3 -B scripts/edicion/buscar_externos.py "regimen de verdad" --limite 8` |

**Limitaciones técnicas conocidas (vigilar hasta resolverse en `notas/NOTAS.md`):**
* `compilar_pdf.py --formato docx` funciona limpio para **un capítulo** (`--capitulo <id>`), pero al compilar el **libro completo a `.docx`** los IDs de notas (`[^1]`, `[^2]`, …) repetidos entre capítulos colisionan en Pandoc si no se prefijan previamente por capítulo.
* `generar_indice.py --escribir` no debe ejecutarse hasta unificar los encabezados partidos en 2–3 líneas y los guiones sueltos (`## -` / `### -`) heredados de 2006.

---

## 9. Protocolo de Mantenimiento y Evolución del Proyecto

Cuando el usuario solicite modificar la arquitectura del repositorio (añadir o cambiar scripts, directorios, funciones, reglas o pasos del flujo de trabajo), **mantener sincronizada toda la documentación rectora** según esta matriz para impedir derivas o contradicciones:

| Tipo de cambio realizado | Archivos que DEBEN actualizarse en el mismo turno | Verificación obligatoria |
| :--- | :--- | :--- |
| **Añadir, renombrar o cambiar interfaz/comportamiento de un script en `scripts/edicion/`** | 1. El script correspondiente (protegiendo siempre `respaldo_v1.0/` vía `es_ruta_dentro_de_respaldo`).<br>2. Tabla de herramientas en `AGENTS.md` (Sección 8).<br>3. Tabla de herramientas en `SSOT/flujo_editorial_segunda_edicion.md` (Sección 6.1).<br>4. Árbol y lista de scripts en `README.md` (sin mencionar «IA»). | Ejecutar el script modificado con casos reales + `validar_libro.py --verificar-respaldo`. |
| **Crear, mover o redefinir un directorio del proyecto** | 1. Mapa de responsabilidades en `AGENTS.md` (Sección 3) y `SSOT/README.md`.<br>2. Árbol y descripciones en `README.md` (sin mencionar «IA»).<br>3. `README.md` interno del directorio afectado (si existe) y `.gitignore` (solo si el nuevo directorio genera artefactos desechables). | Comprobar enlaces locales rotos en todos los `.md` editados + `validar_libro.py --verificar-respaldo`. |
| **Cambiar el flujo editorial, reglas de estilo, citas o seguridad** | 1. Documento rector en `SSOT/` (`flujo_editorial_segunda_edicion.md` y/o `guia_estilo_editorial.md`).<br>2. Resumen operativo correspondiente en `AGENTS.md` (Secciones 5, 6 o 7).<br>3. Si afecta decisiones/pendientes globales, reflejarlo en `notas/NOTAS.md`. | Revisar manualmente que no exista contradicción entre `AGENTS.md` y `SSOT/`. |
| **Añadir o reordenar capítulos / partes** | 1. Archivo en `libro/` (si es nuevo).<br>2. `libro.yaml` (orden, sección, `id`, `estado`).<br>3. `libro/README.md` y ficha espejo en `notas/capitulos/`. | Ejecutar `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo`. |
| **Resolver un hallazgo técnico listado en `notas/NOTAS.md`** | 1. Marcar `- [x]` en `notas/NOTAS.md`.<br>2. Retirar la advertencia de la Sección 8 de `AGENTS.md` (si aplicaba).<br>3. Registrar el hito técnico cerrado en `CHANGELOG.md` si corresponde. | Ejecutar pruebas del componente corregido + `validar_libro.py`. |

### Checklist obligatorio antes de cerrar cualquier cambio estructural o documental
1. `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo` pasa sin errores (`33/33` SHA-256 intactos en `respaldo_v1.0/md/`).
2. `grep -rnE '\b(IA|Inteligencia Artificial)\b' README.md libro/README.md notas/README.md respaldo_v1.0/README.md SSOT/README.md` devuelve **0 coincidencias**.
3. `AGENTS.md` permanece por debajo del límite estricto de `24,000` bytes (idealmente `< 22,000` bytes) para garantizar carga íntegra sin truncamiento.
4. No se modificó ningún archivo dentro de `fuente/`, `respaldo_v1.0/`, `scripts/extraccion_v1/` ni `externos/`, y no se ejecutó `git commit` ni `git push` sin orden expresa.
