---
name: editar-capitulo
description: >-
  Usar cuando el usuario pida editar, actualizar, revisar, validar, entregar al autor
  o cerrar tras aprobación un capítulo específico de `libro/` para la Segunda Edición
  de Crítica de la Razón Mediática.
---

# Procedimiento: Edición Capítulo por Capítulo (`libro/`)

Sigue este flujo de principio a fin trabajando siempre **un solo capítulo `.md` a la vez**. Para reglas de voz, vocabulario protegido y citas europeas, consulta [`SSOT/guia_estilo_editorial.md`](../../../SSOT/guia_estilo_editorial.md) y [`SSOT/perfil_voz_autor.md`](../../../SSOT/perfil_voz_autor.md).

---

## Fase 1 — Preparación y Briefing (antes de tocar `libro/`)

1. **Generar el briefing completo en un solo paso:**
   ```bash
   python3 -B scripts/edicion/contexto_capitulo.py --capitulo <id>
   ```
   Verifica en la salida:
   * Si el archivo es un texto de autor invitado protegido (`03`, `04`, `05`, `06` íntegros; `29` desde la línea `101`, `### Tercer movimiento:`). **No reescribir contenido protegido sin orden expresa.**
   * Diagnóstico técnico activo (notas huérfanas de 2006, asteriscos impares, comillas `‹›`, encabezados partidos).
   * Ficha espejo en `notas/capitulos/<archivo>.md` y fuentes externas asignadas.
2. **Leer el contexto mínimo obligatorio:**
   * `libro/<archivo>.md` (solo el capítulo objetivo).
   * `notas/mapa_obra.md` (evitar repetir autores/conceptos ya introducidos en otros capítulos).
   * `SSOT/perfil_voz_autor.md` (cadencia de Juan Barreto, anti-patrones prohibidos y los 93 términos del Glosario).
   * Las fichas de `notas/fuentes/<slug>.md` pertinentes al capítulo.
3. **Consultas quirúrgicas bajo demanda (sin cargar otros capítulos ni PDFs completos):**
   * Otros capítulos, Glosario o Bibliografía de 2006:
     ```bash
     python3 -B scripts/edicion/buscar_libro.py --glosario "<término>"
     python3 -B scripts/edicion/buscar_libro.py "<autor o concepto>" --solo-conteo
     ```
   * Citas literales verificadas y páginas exactas en `externos/`:
     ```bash
     python3 -B scripts/edicion/buscar_externos.py "<consulta>" --limite 8
     python3 -B scripts/edicion/buscar_externos.py --leer <slug> --paginas A-B
     ```
4. **Plan previo de intervención y densidad de fuentes (antes de modificar `libro/`):**
   * En capítulos extensos (`> 3,000` palabras) y cuando el usuario no haya dado instrucciones puntuales párrafo por párrafo, proponer primero un **plan breve (5–8 viñetas)**: qué apartados se intervendrán, qué **2–3 fuentes** entrarán en diálogo profundo y qué erratas/omisiones de 2006 se consultarán.
   * **Repertorio, no cuota obligatoria:** las fuentes mapeadas en `notas/fuentes/catalogo.yaml` son insumos disponibles; priorizar **2–3 diálogos sustantivos** antes que forzar menciones superficiales de todos los autores listados.

---

## Fase 2 — Edición en `libro/<archivo>.md`

Aplicar las **7 decisiones editoriales confirmadas** (`SSOT/guia_estilo_editorial.md` §1.1):
1. **Integración híbrida:** tejer los aportes nuevos orgánicamente dentro del ensayo sin borrar argumentos de 2006; abrir subapartados nuevos (`##` o `###`) solo ante giros históricos mayores.
2. **Anclaje temporal:** contextualizar cifras y ejemplos de 2006 históricamente (*«hace dos décadas…»*) y tender puente inmediato al presente verificado.
3. **Citas verificadas y anti-alucinación (`Pág. PDF` ≠ folio impreso):** nunca inventar citas ni páginas. Usar estilo europeo (`Inicial. Apellido, *Título*, Editorial, Ciudad, Año, p. X.`). Al citar obras de `externos/`, verificar siempre el **folio impreso visible dentro del texto** devuelto por `--leer` (no copiar mecánicamente `Pág. PDF N` si existe desfase por portada/preliminares; usar `p. X [PDF]` solo si carece de paginación impresa). Para fuentes en otro idioma (p. ej. francés), traducir al español en el cuerpo e indicar `[trad. propia]` al pie. Si falta verificar algo, anotar `[VERIFICAR CITA/PÁG.]` en `notas/capitulos/<archivo>.md`.
4. **Notas al pie:** no borrar notas existentes ni renumerar manualmente; usar IDs temporales (`[^14b]`, `[^sadin]`) en un solo párrafo tras `---`.
5. **Uniformidad al paso:** `«»` para citas textuales, `""` para énfasis/citas internas, eliminar `‹›`; estandarizar `Ibíd.`, `Op. cit.` y punto final; corregir `Masmediática`, `S. i ek`, `Gumis`, `Foweler`, `Lippman` y encabezados partidos en 2–3 líneas.
6. **Sintaxis PangoCairo:** prohibidos `####`, tablas `|...|`, bloques `` ``` ``, imágenes `![...]`, asteriscos impares y notas multipárrafo. En listas numeradas extensas, dejar una línea en blanco entre ítems.
7. **Casos especiales:**
   * **`29_post_scriptum.md`:** editar únicamente las líneas `1–100` (Juan Barreto); **nunca** modificar desde la línea `101` (`### Tercer movimiento:`, Javier Biardeau) sin orden expresa.
   * **Capítulos nuevos sin base en `respaldo_v1.0/`** (ej. `A1` `anexo_cambios_segunda_edicion.md` o el futuro `prefacio_segunda_edicion.md`): `reporte_cambios.py` los reportará como capítulos nuevos; seguir el mismo flujo de validación y entrega.
8. **Auto-revisión de voz y limpieza OCR (antes de compilar):**
   * Releer los párrafos nuevos frente a `SSOT/perfil_voz_autor.md` para asegurar que **no contienen ninguno de los 5 anti-patrones de prosa sintética** ni redefinen sin consultar los 93 términos del Glosario.
   * Si se citaron PDFs con capa OCR previa (p. ej. `Sadin-Eric-La-Inteligencia-Artificial...pdf`), verificar y limpiar cualquier errata OCR en la cita literal.
9. **Actualizar estado:** si el capítulo estaba en `estado: "pendiente"` en `libro.yaml`, pasarlo a `estado: "en_revision"`.

---

## Fase 3 — Validación y Entrega al Autor

1. **Validar el capítulo:**
   ```bash
   python3 -B scripts/edicion/validar_libro.py --capitulo <id>
   ```
   Corregir cualquier error antes de compilar.
2. **Compilar entrega en `dist/` (por defecto: PDF limpio de lectura):**
   ```bash
   python3 -B scripts/edicion/compilar_pdf.py --capitulo <id>
   ```
   *(Usar `--formato docx` o `--etiquetar-parrafos` únicamente si el usuario/autor lo pide.)*
3. **Generar reporte de cambios contra 2006:**
   ```bash
   python3 -B scripts/edicion/reporte_cambios.py --capitulo <id>
   ```
4. **Entregar al usuario:** ruta del archivo compilado en `dist/` + **resumen breve (5–10 viñetas)** de los cambios y cualquier duda puntual de 2006 para Juan Barreto.

---

## Fase 4 — Iteración y Cierre (solo tras aprobación explícita)

* **Si el autor envía observaciones:** registrarlas en `notas/capitulos/<archivo>.md` (y cualquier pauta general en `notas/NOTAS.md` Sección 7), aplicar ajustes en `libro/<archivo>.md`, revalidar y recompilar.
* **Si el autor descarta un borrador completo:** revertir limpiamente el archivo al último estado confirmado (`git checkout -- libro/<archivo>.md` o restaurando desde `respaldo_v1.0/md/<archivo>.md` solo bajo confirmación del usuario) y anotar en `notas/capitulos/<archivo>.md` qué enfoque evitar.
* **Cuando el usuario confirme explícitamente que el autor aprobó el capítulo:**
  1. Marcar `- [x]` en `notas/capitulos/<archivo>.md`, `notas/fuentes/<slug>.md` (si se integraron fuentes) y `notas/NOTAS.md`.
  2. Actualizar la entrada del capítulo y el registro de autores/conceptos introducidos en `notas/mapa_obra.md`, documentar los cambios sustantivos en `notas/registro_cambios_edicion.md` y añadir su síntesis publicable en `libro/anexo_cambios_segunda_edicion.md` (`id: A1`).
  3. Anotar términos nuevos para Glosario o referencias para Bibliografía en `notas/NOTAS.md`.
  4. Verificar que no queden marcadores `[VERIFICAR` sin resolver y cambiar `estado: "aprobado"` en `libro.yaml`.
  5. Registrar el capítulo aprobado en `CHANGELOG.md`.
  6. Ejecutar `python3 -B scripts/edicion/validar_libro.py --capitulo <id>` y dejar listo para el `commit`/`push` del usuario (nunca ejecutar `git commit` ni `git push` sin orden expresa).
