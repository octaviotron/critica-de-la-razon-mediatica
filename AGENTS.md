# Reglas Universales del Workspace — *Crítica de la Razón Mediática* (2.ª Edición)

Contexto raíz, límites inviolables, decisiones editoriales cerradas y protocolo de mantenimiento del proyecto para cualquier agente de IA. Los procedimientos paso a paso viven en las **Skills modulares** de `.agents/skills/` (carga bajo demanda).

---

## 1. Identidad y Objetivo del Proyecto

* **Obra:** *Crítica de la Razón Mediática. Ensayos sobre biopolítica y potencia política del cuerpo (Pre-textos para un debate por el socialismo)*
* **Autor:** Juan Barreto Cipriani (1.ª ed.: UCV / CIPOST, Caracas, 2006; ISBN `980-12-1936-X`) | **Asesoría informática:** Octavio Rossell Tabet (`octavio.rossell@gmail.com`)
* **Objetivo activo:** Preparar la **Segunda Edición** trabajando **un capítulo `.md` a la vez** en `libro/`, con cero fricción CLI para el usuario (el usuario opera en lenguaje natural; el agente ejecuta silenciosamente `scripts/edicion/`).
* **Base digital verificada (2006):** `33` archivos `.md`, `197,690` palabras, `2,685` bloques, `535` notas al pie, `1,008,962 / 1,008,962` caracteres alfanuméricos (`100.000%` de integridad).

---

## 2. Jerarquía de Verdad (Prevención de Contradicciones)

1. **`AGENTS.md` (este archivo):** Reglas siempre activas, seguridad, mapa del repositorio y protocolo de sincronización.
2. **`SSOT/` (`guia_estilo_editorial.md`, `perfil_voz_autor.md`, `flujo_editorial_segunda_edicion.md`):** Fuente única de verdad operativa para estilo, voz, citas y flujo.
3. **`.agents/skills/` (`editar-capitulo`, `procesar-externos`, `cierre-editorial`):** Procedimientos detallados bajo demanda subordinados al `SSOT/` (nunca duplican ni contradicen el `SSOT/`).
4. **`libro.yaml`:** Manifiesto maestro del orden de partes/capítulos y `estado` (`pendiente` | `en_revision` | `aprobado`).
5. **`notas/` (`NOTAS.md`, `mapa_obra.md`, `capitulos/`, `fuentes/`):** Único espacio para pendientes, panorámica de la obra, observaciones del autor y fichas de `externos/`.
6. **`CHANGELOG.md`:** Único registro de hechos ya cerrados y capítulos aprobados.

> Si detectas una contradicción entre cualquiera de estos archivos o un script, **detente, repórtala al usuario** y sincroniza aplicando la Sección 8.

---

## 3. Mapa del Repositorio (Responsabilidades sin Solapamientos)

| Ruta | Naturaleza | Responsabilidad exacta |
| :--- | :--- | :--- |
| `AGENTS.md` | Editable (mantener `< 18 KB`) | Regla universal siempre activa del workspace. |
| `.agents/skills/` | Editable (carga bajo demanda) | Skills procedimentales: `editar-capitulo`, `procesar-externos` y `cierre-editorial`. |
| `libro/` | **Única copia viva** | Capítulos publicables en Markdown (sin notas internas). Los 33 nombres originales son IDs estables (**Opción A**). |
| `libro.yaml` | Editable (manifiesto maestro) | Orden del índice, 10 secciones (`preliminares`, `prologos_2006`, `apertura`, Partes I–VI, `cierre`) y `estado` por capítulo. |
| `notas/` | Editable | `NOTAS.md` (pendientes globales y preferencias del autor), `mapa_obra.md` (panorámica de 33 caps. y registro 2.ª ed.), `capitulos/` (fichas espejo + futuro `prefacio_segunda_edicion.md`) y `fuentes/` (`catalogo.yaml` + fichas `<slug>.md`). |
| `externos/` | **Solo lectura (en Git)** | Biblioteca de bibliografía externa (PDF, HTML, TXT, MD, DOCX, EPUB). Nunca editar ni renombrar. |
| `CHANGELOG.md` | Editable (hechos cerrados) | Exclusivo para capítulos aprobados e hitos ya completados. |
| `scripts/edicion/` | Editable (herramientas internas) | Scripts Python ejecutados con `python3 -B` bajo demanda por el agente. |
| `SSOT/` | Editable (documentación rectora) | Activos: `README.md`, `flujo_editorial_segunda_edicion.md`, `guia_estilo_editorial.md`, `perfil_voz_autor.md`. Históricos (no cargar en sesiones normales): `proceso_conversion_pdf_a_md.md` y `detalle_ejecucion_y_auditoria_conversion.md`. |
| `fuente/` | **INTOCABLE (solo lectura)** | PDF maestro de 2006, QuarkXPress (`.qxp`), `FUENTES/`, `PORTADA/`, `RAZON/images/`. |
| `respaldo_v1.0/` | **INTOCABLE (solo lectura)** | Copia testigo congelada de los 33 `.md` de 2006, `libro.yaml` v1.0 y SHA-256 (`manifiesto_v1.0.md`). |
| `scripts/extraccion_v1/` | **CONGELADO (solo lectura)** | Pipeline histórico de 2006. Nunca modificar ni re-ejecutar sobre `libro/`. |
| `dist/` | **Temporal (ignorado por Git)** | Entregas PDF/DOCX, reportes diff e índice local `dist/indice_externos/corpus.db` (SQLite FTS5) + `txt/`. |

---

## 4. Política de Lectura Progresiva (Ahorro de Contexto)

* **Al editar un capítulo:** activar la skill `editar-capitulo` (ejecuta `contexto_capitulo.py --capitulo <id>` y lee solo `libro/<archivo>.md`, `notas/mapa_obra.md`, `SSOT/perfil_voz_autor.md` y las fichas asignadas en `notas/fuentes/`). Usar `buscar_libro.py` y `buscar_externos.py` para consultas puntuales.
* **NO cargar completos en sesiones normales:** múltiples capítulos de `libro/`, `respaldo_v1.0/md/`, libros/PDFs enteros de `externos/` ni la documentación histórica de conversión (`SSOT/proceso_conversion_pdf_a_md.md`, `SSOT/detalle_ejecucion_y_auditoria_conversion.md`, `scripts/extraccion_v1/`).

---

## 5. Reglas Inviolables de Seguridad, Autoría y Git

1. **Directorios prohibidos para escritura:** Nunca modificar, renombrar ni escribir en `respaldo_v1.0/`, `fuente/`, `scripts/extraccion_v1/` ni `externos/`.
2. **Textos de autores invitados protegidos (NO reescribir sin orden expresa; verificados por `validar_libro.py`):**
   * Íntegros (`prologos_2006`): `03_liminar.md` (*Pro(Logos) I*, Michel Maffesoli; antes «Liminar» en 2006), `04_prologo_1_rigoberto_lanz.md` (*Pro(Logos) II*, Rigoberto Lanz), `05_prologo_2_nelson_guzman.md` (*Pro(Logos) III*, Nelson Guzmán), `06_prologo_3_magaldy_tellez.md` (*Pro(Logos) IV*, Magaldy Téllez).
   * Parcial: `29_post_scriptum.md` — líneas `1–100` (Juan Barreto, editables); desde **línea `101`** (`### Tercer movimiento: Entre dinosaurios y unicornios`) es de **Javier Biardeau** (protegido).
3. **Prohibición absoluta en todos los `README.md` públicos:** Nunca mencionar «IA» ni «Inteligencia Artificial» en `README.md`, `libro/README.md`, `notas/README.md`, `respaldo_v1.0/README.md`, `scripts/README.md` ni `SSOT/README.md` (verificado automáticamente por `validar_libro.py`). Usar *edición asistida* o *ejecución asistida de scripts*.
4. **Git lineal y aprobaciones:** Trabajar solo en `main`; **no crear ramas ni tags**; **nunca ejecutar `git commit` ni `git push`** sin instrucción expresa; **nunca marcar `estado: "aprobado"` en `libro.yaml`** sin confirmación explícita del usuario.
5. **Índices protegidos hasta el cierre:** No editar `libro/01_indice.md` manualmente ni tocar `libro/32_indice_onomastico.md` hasta el cierre editorial.

---

## 6. Reglas Editoriales Esenciales y Decisiones Confirmadas

Detalle completo en `SSOT/guia_estilo_editorial.md` (§1 y §1.1) y `SSOT/perfil_voz_autor.md`:
* **Voz y léxico protegido:** Conservar el registro filosófico-ensayístico de Juan Barreto, evitar anti-patrones de prosa sintética y respetar los 21 compuestos protegidos (`massmediática`, `mass-media`, `biopolítica`, `biopoder`, `agenciamiento`, `significante-signo`, `cuerpo-potencia`, `rostro-proceso`, `hecha-en-común`, `trabajo-valor`, `ético-política`, `post-scriptum`, `rizoma`, `pliegue`, `líneas de fuga`, `subjetividad`, `performativo`, `habitus`, `multitud`, `dispositivo`, `aura`) más los 92 términos de `31_glosario.md`.
* **Sintaxis PangoCairo (`libro/*.md`):** Permitido `#`/`##`/`###`, `>`, `- `, listas numeradas con línea en blanco entre ítems, `*`/`**`/`***`, `[^id]` y definiciones en 1 párrafo tras `---`. **Prohibido:** `####`, tablas `|...|`, bloques `` ``` ``, imágenes `![...]`, asteriscos impares y notas multipárrafo.
* **Citas europeas y política anti-alucinación:** Formato `Inicial. Apellido, *Título*, Editorial, Ciudad, Año, p. X.` **Nunca inventar citas ni páginas** (verificar siempre vía `buscar_externos.py` o marcar `[VERIFICAR CITA/PÁG.]`). No borrar notas existentes ni renumerar manualmente (usar IDs temporales `[^14b]`, `[^sadin]`).
* **7 omisiones confirmadas del impreso 2006 (consultar al autor al editar):** `11` (`[^15]`, `[^19]` sin llamada + salto `17`), `17` (`[^28]` sin llamada), `20` (`[^3]` sin definición), `24` (`[^4]` sin definición, `[^2]` sin llamada), `27` (`[^3]` sin llamada).
* **6 decisiones editoriales fijas (no volver a preguntar):**
  1. **Actualizaciones:** integración híbrida (tejido orgánico sin borrar 2006 + subapartados nuevos ante giros históricos mayores).
  2. **Anclaje temporal:** contextualizar cifras/ejemplos de 2006 históricamente y tender puente al presente verificado.
  3. **Fuentes en otro idioma:** traducir cita al español en el cuerpo + nota europea a la edición original con `[trad. propia]`.
  4. **Autores invitados (`03`–`06`, `29` L101+):** conservar íntegros como memoria de 2006 (explicado en el futuro Prefacio).
  5. **Entrega por defecto al autor:** **PDF limpio** (`compilar_pdf.py --capitulo <id>`) + resumen de 5–10 viñetas (`.docx` o `--etiquetar-parrafos` solo bajo pedido).
  6. **Uniformidad al paso:** `«»` citas / `""` énfasis / sustituir `‹›`; `Ibíd.`, `Op. cit.` y punto final; corregir `Masmediática`, `S. i ek`, `Gumis`, `Foweler`, `Lippman` y encabezados partidos; conservar `· Término:` en `31_glosario.md` hasta el cierre.

---

## 7. Flujos en Lenguaje Natural (Skills) y Herramientas (`scripts/edicion/`)

El usuario opera en lenguaje natural; según su solicitud, activar la Skill correspondiente:
* **Editar / validar / entregar / aprobar un capítulo:** `.agents/skills/editar-capitulo/SKILL.md`
* **Añadir, indexar o fichar bibliografía en `externos/`:** `.agents/skills/procesar-externos/SKILL.md`
* **Cierre editorial final (bibliografía, glosario, índice, onomástico):** `.agents/skills/cierre-editorial/SKILL.md`

### Catálogo de scripts internos (ejecutar siempre con `python3 -B`)

| Script | Propósito | Ejemplo |
| :--- | :--- | :--- |
| `manifiesto.py` | Carga `libro.yaml` / `respaldo_v1.0/libro.yaml` y bloquea escrituras en `respaldo_v1.0/`. | *(módulo compartido)* |
| `contexto_capitulo.py` | Briefing completo en 1 paso (metadatos, protección, diagnóstico, ficha, fuentes y notas). | `python3 -B scripts/edicion/contexto_capitulo.py --capitulo 19` |
| `validar_libro.py` | Valida estructura, notas, PangoCairo, asteriscos, `[VERIFICAR]`, invitados, `README.md` y SHA-256. | `python3 -B scripts/edicion/validar_libro.py --capitulo 19` |
| `compilar_pdf.py` | Compila 1 capítulo (`--capitulo`) o el libro completo en `dist/` en PDF o Word (`--formato docx`). | `python3 -B scripts/edicion/compilar_pdf.py --capitulo 19` |
| `reporte_cambios.py` | Compara 1 capítulo o el libro completo contra `respaldo_v1.0/` (o `--desde-git`) en `dist/`. | `python3 -B scripts/edicion/reporte_cambios.py --capitulo 19` |
| `generar_indice.py` | Genera el Índice General desde `libro.yaml` (`--escribir` solo tras sanear encabezados partidos). | `python3 -B scripts/edicion/generar_indice.py --escribir` |
| `indexar_externos.py` | Indexa incrementalmente `externos/` en SQLite FTS5 (`dist/indice_externos/corpus.db`) y `catalogo.yaml`. | `python3 -B scripts/edicion/indexar_externos.py` |
| `buscar_externos.py` | Consulta FTS5 BM25, lee rangos (`--leer`), TOC (`--info`) y fuentes por capítulo (`--para-capitulo`) con auto-sync. | `python3 -B scripts/edicion/buscar_externos.py "regimen de verdad"` |
| `buscar_libro.py` | Busca en `libro/`, Glosario (`--glosario`) y Bibliografía (`--bibliografia`) con distribución por capítulo. | `python3 -B scripts/edicion/buscar_libro.py --glosario "cuerpo"` |

---

## 8. Protocolo de Mantenimiento y Evolución del Proyecto

Ante cualquier cambio arquitectónico (scripts, directorios, funciones, reglas, Skills o capítulos), mantener sincronizada la documentación **en el mismo turno**:

| Tipo de cambio | Archivos a actualizar obligatoriamente | Verificación obligatoria |
| :--- | :--- | :--- |
| **Script en `scripts/edicion/`** | Script (con `es_ruta_dentro_de_respaldo`) + `AGENTS.md` (§7) + `SSOT/flujo_editorial_segunda_edicion.md` (§6.1) + `.agents/skills/` afectada + `scripts/README.md` (sin «IA»). | Probar el script con casos reales + `validar_libro.py --verificar-respaldo`. |
| **Directorio o Skill nueva/modificada** | `AGENTS.md` (§3 y §7) + `SSOT/README.md` + `README.md` (resumen público, sin «IA») + `README.md` interno / `.gitignore` si aplica. | Comprobar enlaces locales rotos + `validar_libro.py --verificar-respaldo`. |
| **Regla editorial, estilo o flujo** | `SSOT/guia_estilo_editorial.md` y/o `flujo_editorial_segunda_edicion.md` + `AGENTS.md` (§5–§6) + `.agents/skills/` afectada + `notas/NOTAS.md` si corresponde. | Revisar ausencia de contradicciones entre `AGENTS.md`, `SSOT/` y `.agents/skills/`. |
| **Añadir o reordenar capítulos** | `libro/` (si es nuevo) + `libro.yaml` + `libro/README.md` + `notas/capitulos/` + `notas/mapa_obra.md`. | `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo`. |
| **Cerrar hallazgo técnico de `notas/NOTAS.md`** | Marcar `- [x]` en `notas/NOTAS.md` + actualizar `AGENTS.md` (si aplicaba) + registrar hito en `CHANGELOG.md`. | Probar corrección + `validar_libro.py --verificar-respaldo`. |

### Checklist obligatorio tras cambios estructurales
1. `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo` pasa con **0 errores** (incluye `33/33` SHA-256 e higiene de los 6 `README.md`).
2. `AGENTS.md` permanece cómodamente por debajo de `24,000` bytes (objetivo `< 18,000` bytes).
3. Ningún archivo modificado en `fuente/`, `respaldo_v1.0/`, `scripts/extraccion_v1/` ni `externos/`, y ningún `git commit`/`git push` ejecutado sin orden expresa.
