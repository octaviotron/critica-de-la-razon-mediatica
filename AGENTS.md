# Reglas Universales del Workspace — *Crítica de la Razón Mediática* (2.ª Edición)

Contexto raíz, límites inviolables, decisiones editoriales cerradas y arranque rápido para cualquier agente de IA. Los procedimientos paso a paso viven en las **4 Skills modulares** de `.agents/skills/` (carga bajo demanda).

---

## 1. Identidad, Objetivo y Arranque Rápido de Sesión

* **Obra:** *Crítica de la Razón Mediática. Ensayos sobre biopolítica y potencia política del cuerpo (Pre-textos para un debate por el socialismo)*
* **Autor:** Juan Barreto Cipriani (1.ª ed.: UCV / CIPOST, Caracas, 2006; ISBN `980-12-1936-X`) | **Asesoría informática:** Octavio Rossell Tabet (`octavio.rossell@gmail.com`)
* **Objetivo activo:** Preparar la **Segunda Edición** trabajando **un capítulo `.md` a la vez** en `libro/`, con cero fricción CLI para el usuario (opera en lenguaje natural; el agente ejecuta silenciosamente `scripts/edicion/` con `python3 -B`).
* **Base verificada (2006):** `33` archivos `.md` (`197,690` palabras, `535` notas al pie, `100.000%` integridad alfanumérica) + anexo de cierre `A1` (`34` entradas actuales en `libro.yaml`).
* **Arranque rápido en sesión nueva:** Si el usuario dice *«sigamos»* o pregunta *«¿cómo vamos?»*, ejecutar primero `python3 -B scripts/edicion/validar_libro.py` (para leer el tablero de `estado` en `libro.yaml`) y revisar el último registro de `notas/registro_cambios_edicion.md` antes de proponer el siguiente paso.

---

## 2. Jerarquía de Verdad (Prevención de Contradicciones)

1. **`AGENTS.md` (este archivo):** Reglas siempre activas, seguridad, mapa del repositorio y disparador de mantenimiento.
2. **`SSOT/` (`guia_estilo_editorial.md`, `perfil_voz_autor.md`, `flujo_editorial_segunda_edicion.md`):** Fuente única de verdad operativa para estilo, voz, citas, vocabulario y flujo.
3. **`.agents/skills/` (`editar-capitulo`, `procesar-externos`, `cierre-editorial`, `mantenimiento-proyecto`):** Procedimientos paso a paso bajo demanda subordinados al `SSOT/`.
4. **`libro.yaml`:** Manifiesto maestro del orden de partes/capítulos (`10` secciones, `34` entradas) y `estado` (`pendiente` | `en_revision` | `aprobado`).
5. **`notas/` (`NOTAS.md`, `mapa_obra.md`, `registro_cambios_edicion.md`, `capitulos/`, `fuentes/`):** Pendientes, panorámica, bitácora de cambios al libro, observaciones del autor y fichas de `externos/`.
6. **`CHANGELOG.md`:** Registro exclusivo de capítulos aprobados e hitos técnicos ya cerrados.

> Ante cualquier contradicción entre estos archivos o un script, **detente, repórtala al usuario** y activa `.agents/skills/mantenimiento-proyecto/SKILL.md`.

---

## 3. Mapa del Repositorio (Responsabilidades sin Solapamientos)

| Ruta | Naturaleza | Responsabilidad exacta |
| :--- | :--- | :--- |
| `AGENTS.md` | Editable (`< 18 KB`, tope `24 KB`) | Regla universal siempre activa del workspace. |
| `.agents/skills/` | Editable (bajo demanda) | 4 Skills: `editar-capitulo`, `procesar-externos`, `cierre-editorial`, `mantenimiento-proyecto`. |
| `libro/` | **Única copia viva** | Capítulos publicables en Markdown (sin notas internas). Los 33 nombres originales son IDs estables (**Opción A**); los nuevos usan nombre descriptivo (`anexo_cambios_segunda_edicion.md`, `id: A1`). |
| `libro.yaml` | Editable (manifiesto maestro) | Orden del índice (`10` secciones: `preliminares`, `prologos_2006`, `apertura`, Partes I–VI, `cierre`), `34` entradas y `estado`. |
| `notas/` | Editable | `NOTAS.md`, `mapa_obra.md`, `registro_cambios_edicion.md`, `capitulos/` (fichas espejo + futuro `prefacio_segunda_edicion.md`) y `fuentes/` (`catalogo.yaml` + fichas `<slug>.md`). |
| `externos/` | **Solo lectura (en Git)** | Biblioteca de bibliografía externa (PDF, HTML, TXT, MD, DOCX, EPUB). Nunca editar ni renombrar. |
| `CHANGELOG.md` | Editable (hechos cerrados) | Exclusivo para capítulos aprobados e hitos ya completados. |
| `scripts/edicion/` | Editable (herramientas internas) | 9 scripts Python ejecutados con `python3 -B` (detalle CLI y requisitos en `scripts/README.md`). |
| `SSOT/` | Editable (documentación rectora) | Activos: `README.md`, `flujo_editorial_segunda_edicion.md`, `guia_estilo_editorial.md`, `perfil_voz_autor.md`. Históricos (NO cargar en sesiones normales): `proceso_conversion_pdf_a_md.md` y `detalle_ejecucion_y_auditoria_conversion.md`. |
| `fuente/` | **INTOCABLE (solo lectura)** | PDF maestro de 2006, QuarkXPress (`.qxp`), `FUENTES/`, `PORTADA/`, `RAZON/images/`. |
| `respaldo_v1.0/` | **INTOCABLE (solo lectura)** | Copia congelada de los 33 `.md` de 2006, `libro.yaml` v1.0 y SHA-256 (`manifiesto_v1.0.md`). |
| `scripts/extraccion_v1/` | **CONGELADO (solo lectura)** | Pipeline histórico de 2006. Nunca modificar ni re-ejecutar sobre `libro/`. |
| `dist/` | **Temporal (ignorado por Git)** | Entregas PDF/DOCX, reportes diff e índice local `dist/indice_externos/corpus.db` (SQLite FTS5) + `txt/`. |

---

## 4. Política de Lectura Progresiva (Ahorro de Contexto)

* **Al editar un capítulo:** activar `editar-capitulo` (ejecuta `contexto_capitulo.py --capitulo <id>` y lee solo `libro/<archivo>.md`, `notas/mapa_obra.md`, `SSOT/perfil_voz_autor.md` y las fichas asignadas en `notas/fuentes/`). Consultar el resto del libro o `externos/` únicamente vía `buscar_libro.py` y `buscar_externos.py`.
* **NO cargar completos en sesiones normales:** múltiples capítulos de `libro/`, `respaldo_v1.0/md/`, libros/PDFs enteros de `externos/` ni los 2 documentos históricos de `SSOT/`.

---

## 5. Reglas Inviolables de Seguridad, Autoría, Disciplina y Git

1. **Directorios prohibidos para escritura:** Nunca modificar, renombrar ni escribir en `respaldo_v1.0/`, `fuente/`, `scripts/extraccion_v1/` ni `externos/`.
2. **Textos de autores invitados protegidos (NO reescribir sin orden expresa; verificados por `validar_libro.py`):**
   * Íntegros (`prologos_2006`): `03_liminar.md` (*Pro(Logos) I*, Michel Maffesoli; antes «Liminar» en 2006), `04_prologo_1_rigoberto_lanz.md` (*Pro(Logos) II*, Rigoberto Lanz), `05_prologo_2_nelson_guzman.md` (*Pro(Logos) III*, Nelson Guzmán), `06_prologo_3_magaldy_tellez.md` (*Pro(Logos) IV*, Magaldy Téllez).
   * Parcial: `29_post_scriptum.md` — líneas `1–100` (Juan Barreto, editables); desde **línea `101`** (`### Tercer movimiento: Entre dinosaurios y unicornios`) es de **Javier Biardeau** (protegido).
3. **Prohibición absoluta en los 6 `README.md` públicos:** Nunca mencionar «IA» ni «Inteligencia Artificial» en `README.md`, `libro/README.md`, `notas/README.md`, `respaldo_v1.0/README.md`, `scripts/README.md` ni `SSOT/README.md` (verificado por `validar_libro.py`). Usar *edición asistida* o *ejecución asistida de scripts*.
4. **Disciplina conversacional:** Cuando el usuario pida *análisis, recomendaciones o explicaciones*, **no modificar archivos** hasta recibir confirmación; ante cambios estructurales que afecten `libro.yaml`, confirmar alcance antes de aplicar.
5. **Git lineal y aprobaciones:** Trabajar solo en `main`; **no crear ramas ni tags**; **nunca ejecutar `git commit` ni `git push`** sin instrucción expresa; **nunca marcar `estado: "aprobado"` en `libro.yaml`** sin confirmación explícita del usuario.
6. **Índices protegidos hasta el cierre:** No editar `libro/01_indice.md` manualmente ni tocar `libro/32_indice_onomastico.md` hasta el cierre editorial.

---

## 6. Reglas Editoriales Esenciales y 7 Decisiones Confirmadas

Detalle normativo (21 compuestos protegidos, ejemplo antes/después, las 7 omisiones de notas de 2006 y 1 asterisco impar heredado en `17:L19`) en `SSOT/guia_estilo_editorial.md` (§1–§1.2) y los **93 términos del Glosario** + anti-patrones en `SSOT/perfil_voz_autor.md`:
* **Sintaxis PangoCairo (`libro/*.md`):** Permitido `#`/`##`/`###`, `>`, `- `, listas numeradas con línea en blanco entre ítems, `*`/`**`/`***`, `[^id]` y definiciones en 1 párrafo tras `---`. **Prohibido:** `####`, tablas `|...|`, bloques `` ``` ``, imágenes `![...]`, asteriscos impares y notas multipárrafo.
* **Citas europeas y anti-alucinación:** `Inicial. Apellido, *Título*, Editorial, Ciudad, Año, p. X.` **Nunca inventar citas ni páginas** (verificar vía `buscar_externos.py` comprobando el **folio impreso** dentro del texto, ya que `Pág. PDF` suele diferir, o marcar `[VERIFICAR CITA/PÁG.]`). Las fuentes de `catalogo.yaml` son repertorio disponible, no cuota obligatoria (priorizar 2–3 diálogos sustantivos por capítulo). No borrar notas existentes ni renumerar manualmente (usar IDs temporales `[^14b]`, `[^sadin]`).
* **7 decisiones editoriales fijas (no volver a preguntar):**
  1. **Actualizaciones:** integración híbrida (tejido orgánico sin borrar 2006 + subapartados nuevos ante giros históricos mayores).
  2. **Anclaje temporal:** contextualizar cifras/ejemplos de 2006 históricamente y tender puente al presente verificado.
  3. **Fuentes en otro idioma:** traducir cita al español en el cuerpo + nota europea a la edición original con `[trad. propia]`.
  4. **Autores invitados (`03`–`06`, `29` L101+):** conservar íntegros como memoria de 2006 (explicado en el futuro Prefacio y en el Anexo `A1`).
  5. **Entrega por defecto al autor:** **PDF limpio** (`compilar_pdf.py --capitulo <id>`) + resumen de 5–10 viñetas (`.docx` o `--etiquetar-parrafos` solo bajo pedido).
  6. **Uniformidad al paso:** `«»` citas / `""` énfasis / sustituir `‹›`; `Ibíd.`, `Op. cit.` y punto final; corregir `Masmediática`, `S. i ek`, `Gumis`, `Foweler`, `Lippman` y encabezados partidos; mantener `· Término:` en `31_glosario.md` hasta el cierre.
  7. **Anexo editorial de cierre (`libro/anexo_cambios_segunda_edicion.md`, `id: A1`):** *Anexo editorial: Relación de cambios respecto a la Primera Edición (2006)* al final de `cierre`; actualizarlo junto a `notas/registro_cambios_edicion.md` con cada cambio estructural y cada capítulo aprobado, y cerrarlo tras aprobación del autor.

---

## 7. Skills en Lenguaje Natural y Herramientas (`scripts/edicion/`)

Activar la Skill correspondiente según la solicitud del usuario:
* **Editar / validar / entregar / aprobar un capítulo:** `.agents/skills/editar-capitulo/SKILL.md`
* **Añadir, indexar o fichar bibliografía en `externos/`:** `.agents/skills/procesar-externos/SKILL.md`
* **Cierre editorial final (bibliografía, glosario, índice, anexo `A1`, onomástico):** `.agents/skills/cierre-editorial/SKILL.md`
* **Modificar scripts, directorios, Skills, reglas o estructura del repo:** `.agents/skills/mantenimiento-proyecto/SKILL.md`

### Catálogo de scripts internos (ejecutar siempre con `python3 -B`; detalle completo en `scripts/README.md`)

| Script | Propósito | Ejemplo |
| :--- | :--- | :--- |
| `manifiesto.py` | Carga `libro.yaml` / `respaldo_v1.0/libro.yaml` y bloquea escrituras en `respaldo_v1.0/`. | *(módulo compartido)* |
| `contexto_capitulo.py` | Briefing completo en 1 paso (metadatos, protección, diagnóstico, ficha, fuentes y notas). | `python3 -B scripts/edicion/contexto_capitulo.py --capitulo 19` |
| `validar_libro.py` | Valida estructura, notas, PangoCairo, asteriscos, `[VERIFICAR]`, invitados, 6 `README.md`, `AGENTS.md`, fichas espejo y SHA-256. | `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo` |
| `compilar_pdf.py` | Compila 1 capítulo (`--capitulo`) o el libro completo en `dist/` en PDF limpio (por defecto) o Word (`--formato docx`). | `python3 -B scripts/edicion/compilar_pdf.py --capitulo 19` |
| `reporte_cambios.py` | Compara 1 capítulo o el libro completo contra `respaldo_v1.0/` (o `--desde-git`) en `dist/`. | `python3 -B scripts/edicion/reporte_cambios.py --capitulo 19` |
| `generar_indice.py` | Genera el Índice General desde `libro.yaml` (`--escribir` solo tras sanear encabezados partidos). | `python3 -B scripts/edicion/generar_indice.py --escribir` |
| `indexar_externos.py` | Indexa incrementalmente `externos/` en SQLite FTS5 (`dist/indice_externos/corpus.db`) y `catalogo.yaml`. | `python3 -B scripts/edicion/indexar_externos.py` |
| `buscar_externos.py` | Consulta FTS5 BM25, lee rangos (`--leer`), TOC (`--info`) y fuentes por capítulo (`--para-capitulo`) con auto-sync. | `python3 -B scripts/edicion/buscar_externos.py "regimen de verdad"` |
| `buscar_libro.py` | Busca en `libro/`, Glosario (`--glosario`, `93` términos) y Bibliografía (`--bibliografia`) por capítulo. | `python3 -B scripts/edicion/buscar_libro.py --glosario "habitus"` |

---

## 8. Mantenimiento y Verificación Post-Cambio

Ante cualquier cambio en scripts, directorios, Skills, reglas editoriales o estructura de `libro.yaml`, **activar obligatoriamente `.agents/skills/mantenimiento-proyecto/SKILL.md`** y verificar en el mismo turno que `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo` concluya con **0 errores** (`33/33` SHA-256, `0` menciones prohibidas en los 6 `README.md`, `AGENTS.md < 20 KB` y `0` enlaces locales rotos).
