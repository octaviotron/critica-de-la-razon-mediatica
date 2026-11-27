# Plan de Implementación — Corrección de Inconsistencias, Omisiones y Obsolescencias (`notas/PLAN_PENDIENTE.md`)

Plan operativo para resolver los **12 hallazgos** detectados en la auditoría documental sobre `SSOT/`, `notas/`, `scripts/` y `.agents/skills/*`.

> **Nota sobre este archivo:** Plan de trabajo temporal en `notas/`. No afecta a `libro/`, `libro.yaml` ni a las compilaciones en `dist/`. Al completarse todos los puntos, puede eliminarse o archivarse.

---

## Criterios de Calificación

* **Impacto** *(según la cantidad de archivos y capas estructurales del repositorio que deben modificarse)*:
  * **Bajo:** `1–5` archivos acotados a una sola capa documental (`notas/`, `SSOT/`, una Skill o un `README.md`).
  * **Medio:** `4–8` archivos que cruzan varias capas (`AGENTS.md`, Skills, `SSOT/`, `maquetacion/`, `scripts/edicion/` o un capítulo en `libro/`).
  * **Alto:** `> 10` archivos distribuidos en lotes (p. ej. las `23` fichas de `notas/fuentes/` o las `24` fichas de `notas/capitulos/`).
* **Riesgo** *(según la probabilidad de romper otras partes del proyecto: manuscrito vivo, validadores, compilación PDF/DOCX/`LuaLaTeX`, índices, tope de bytes de `AGENTS.md` o regla de los `README.md`)*:
  * **Bajo:** Cambios puramente documentales en `notas/`, Skills o `SSOT/` sin efecto sobre código ejecutable ni texto del libro (verificando enlaces locales).
  * **Medio:** Cambios que tocan scripts de `scripts/edicion/`, `maquetacion/diseno_2ed.yaml`, `AGENTS.md` (límite `20,000` / `24,000 B`), `README.md` públicos (prohibición estricta del término prohibido por `validar_libro.py`) o notas al pie de `libro/07_preambulo.md`.
  * **Alto:** Cambios que puedan alterar textos protegidos, índices finales antes de tiempo o paginación cerrada *(ningún ítem de este plan requiere asumir riesgo alto si se respeta el orden propuesto)*.

---

## Detalle del Plan por Asunto (`A-01` – `A-12`)

### `A-01` — Flujo seguro del Índice Onomástico y orden de compilación en cierre editorial
* **Impacto:** **Bajo** (`3` archivos MD; `4` si se aplica refuerzo opcional en script — ver `D-01`)
* **Riesgo:** **Bajo** *(documental)* / **Medio** *(si se modifica `recalcular_onomastico.py`)*
* **Archivos implicados:** [`../.agents/skills/cierre-editorial/SKILL.md`](../.agents/skills/cierre-editorial/SKILL.md), [`../SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md), [`../SSOT/guia_maquetacion_segunda_edicion.md`](../SSOT/guia_maquetacion_segunda_edicion.md) *(y opcionalmente [`../scripts/edicion/recalcular_onomastico.py`](../scripts/edicion/recalcular_onomastico.py))*.
* **Acciones de implementación:**
  1. En `cierre-editorial/SKILL.md` (§5.5), añadir como **paso obligatorio previo** a `recalcular_onomastico.py` el saneamiento de [`../libro/32_indice_onomastico.md`](../libro/32_indice_onomastico.md) documentado en [`capitulos/32_indice_onomastico.md`](capitulos/32_indice_onomastico.md): separar `ZIBECHI, Raúl` de `ŽIŽEK, Slavoj` (L211, evitando su borrado silencioso al ejecutar `--escribir`), corregir `FOWELER` → `FOWLER` y `GUMIS` → `GOMIS`, e insertar alfabéticamente a los nuevos autores efectivamente citados en la 2.ª edición (cruzando `mapa_obra.md` y `30_bibliografia.md`).
  2. Reflejar este prerrequisito en `SSOT/flujo_editorial_segunda_edicion.md` (§4) y `SSOT/guia_maquetacion_segunda_edicion.md` (§4 y §5).
  3. Reordenar §5 de `cierre-editorial/SKILL.md` para que el cierre y aprobación de `A1` (`anexo_cambios_segunda_edicion.md`) ocurra **antes** de la compilación definitiva, y tras `recalcular_onomastico.py --escribir` se recompilen **todos** los formatos finales (`compilar_pdf.py`, `compilar_pdf.py --formato docx`, `compilar_maqueta.py --modo digital` y `compilar_maqueta.py --modo imprenta`), evitando que los artefactos digitales queden desfasados.
  4. *(Según `D-01`)* Endurecer `parsear_entradas_onomastico()` en `recalcular_onomastico.py` para detectar si una línea contiene más de un patrón `APELLIDO, Nombre:` y emitir advertencia/error antes de sobrescribir.

---

### `A-02` — Comando `buscar_externos.py --fuente <slug>` sin `<consulta>` en Skill y 23 fichas
* **Impacto:** **Alto** *(si se actualizan las 23 fichas + Skill = `24–25` archivos)* / **Bajo** *(si solo se ajusta CLI + Skill = `2` archivos; ver `D-02`)*
* **Riesgo:** **Bajo**
* **Archivos implicados:** [`../scripts/edicion/buscar_externos.py`](../scripts/edicion/buscar_externos.py), [`../.agents/skills/procesar-externos/SKILL.md`](../.agents/skills/procesar-externos/SKILL.md) y `23` fichas en [`fuentes/`](fuentes/).
* **Acciones de implementación (según `D-02`):**
  1. En `buscar_externos.py` (`main()`), hacer que cuando se invoque `--fuente <slug>` sin `consulta` muestre los metadatos y TOC de esa fuente (`cmd_info(conn, args.fuente)`) más una nota de uso para buscar texto dentro de ella, en vez de ignorar `--fuente` y listar las 27 obras.
  2. En `procesar-externos/SKILL.md` (Paso 4, L67), cambiar la plantilla a `buscar_externos.py "<consulta>" --fuente <slug>` (y/o `--info <slug>`).
  3. *(Si se elige la opción completa en `D-02`)* Actualizar la línea de comando de ejemplo en las `23` fichas de `notas/fuentes/*.md` para mostrar `"<consulta>" --fuente <slug>` con el `<slug>` completo exacto.

---

### `A-03` — Sincronización post-edición del Capítulo `07` (`07_preambulo.md`) y verificación de folios
* **Impacto:** **Medio** (`4–5` archivos entre `notas/`, raíz y opcionalmente `libro/07_preambulo.md` — ver `D-03`)
* **Riesgo:** **Medio** *(si se ajustan notas al pie en `libro/07_preambulo.md`, requiere revalidar y recompilar `dist/cap_07_preambulo.pdf`; **Bajo** si solo se actualizan `notas/` y `CHANGELOG.md`)*
* **Archivos implicados:** [`capitulos/07_preambulo.md`](capitulos/07_preambulo.md), [`mapa_obra.md`](mapa_obra.md), [`NOTAS.md`](NOTAS.md), [`../CHANGELOG.md`](../CHANGELOG.md) *(y según `D-03`, [`../libro/07_preambulo.md`](../libro/07_preambulo.md))*.
* **Acciones de implementación:**
  1. Actualizar [`capitulos/07_preambulo.md`](capitulos/07_preambulo.md): marcar `- [x]` las erratas e inserciones ya aplicadas en el commit `f23e550`, ajustar las referencias de líneas a la numeración actual (`421` líneas), actualizar la sección *Observaciones del autor* indicando que el borrador `dist/cap_07_preambulo.pdf` está en revisión, y copiar desde `estado_sesion.md` los pendientes persistentes de verificación bibliográfica (`[^5c]` año de *El Derecho*, `[^10b]` editorial/año de *La vie spectrale*, `[^20b]` editorial/ciudad de *Infocracia*) y las `7` notas con IDs temporales (`[^5b]`–`[^20d]`).
  2. *(Según `D-03`)* Comprobar con `buscar_externos.py --leer` los folios impresos visibles de Sadin 2020 (`[^5b]`, p. 119 PDF), Harari *Nexus* (`[^11b]`, pp. 235–236 PDF) y Cortina 2024 (`[^20d]`, p. 134 PDF): sustituir `p. X [PDF]` por el folio impreso real en `libro/07_preambulo.md` (revalidando y recompilando el PDF limpio) o dejarlos explícitamente anotados como `[VERIFICAR FOLIO IMPRESO]` en `notas/capitulos/07_preambulo.md` para resolverlos en Fase 4.
  3. En [`mapa_obra.md`](mapa_obra.md) (L26), cambiar `*2.ª ed.:* pendiente` a `*2.ª ed.:* en revisión (borrador con Sadin, Harari, Han y Cortina)` y completar las fuentes mapeadas de `07`.
  4. En [`NOTAS.md`](NOTAS.md) (L52), marcar `- [x]` la elección del capítulo inicial indicando que el flujo comenzó por `07_preambulo.md`.
  5. En [`../CHANGELOG.md`](../CHANGELOG.md) (L11), ajustar el paréntesis informativo para reflejar que aún hay `0` capítulos *aprobados*, sin afirmar que todos los archivos de `libro/` permanecen intactos en `estado: pendiente`.

---

### `A-04` — Cierre del ítem obsoleto sobre maquetación final en `notas/NOTAS.md`
* **Impacto:** **Bajo** (`1` archivo)
* **Riesgo:** **Bajo**
* **Archivo implicados:** [`NOTAS.md`](NOTAS.md) (L108).
* **Acción de implementación:** Marcar `- [x]` el punto *Maquetación final de imprenta / publicación*, enlazando a [`../maquetacion/README.md`](../maquetacion/README.md), `compilar_maqueta.py`, `recalcular_onomastico.py` y [`../SSOT/guia_maquetacion_segunda_edicion.md`](../SSOT/guia_maquetacion_segunda_edicion.md).

---

### `A-05` — Corrección de conteos base (2006) pre-depuración en 5 fichas de `notas/capitulos/`
* **Impacto:** **Bajo** (`5` archivos en `notas/capitulos/`)
* **Riesgo:** **Bajo**
* **Archivos implicados:** [`capitulos/09_parte1_ensayo_2.md`](capitulos/09_parte1_ensayo_2.md), [`capitulos/10_parte1_ensayo_3.md`](capitulos/10_parte1_ensayo_3.md), [`capitulos/13_parte2_ensayo_3.md`](capitulos/13_parte2_ensayo_3.md), [`capitulos/20_parte4_ensayo_4.md`](capitulos/20_parte4_ensayo_4.md) y [`capitulos/28_epilogo.md`](capitulos/28_epilogo.md).
* **Acción de implementación:** Alinear las cifras con `respaldo_v1.0/md/` y `mapa_obra.md`:
  * `09`: `3,520` → `3,519` palabras.
  * `10`: `75 notas` → `76 notas`.
  * `13`: `6,086` → `6,078` palabras.
  * `20`: `1,084` → `1,080` palabras.
  * `28`: `6,780` → `6,742` palabras.

---

### `A-06` — Sincronización de las 27 fuentes de `catalogo.yaml` y conteo `33 + A1` en `notas/`
* **Impacto:** **Medio** (`5` archivos troncales) / **Alto** *(si además se editan las ~20 fichas `capitulos/08`–`29`; ver `D-04`)*
* **Riesgo:** **Bajo** *(cuidando mantener `0` menciones prohibidas en [`README.md`](README.md) de `notas/`)*
* **Archivos implicados:** [`mapa_obra.md`](mapa_obra.md), [`README.md`](README.md), [`NOTAS.md`](NOTAS.md), [`capitulos/30_bibliografia.md`](capitulos/30_bibliografia.md), [`capitulos/prefacio_segunda_edicion.md`](capitulos/prefacio_segunda_edicion.md) *(y opcionalmente `capitulos/08`–`29` según `D-04`)*.
* **Acciones de implementación:**
  1. Actualizar todas las líneas `*Fuentes mapeadas:*` de [`mapa_obra.md`](mapa_obra.md) contra [`fuentes/catalogo.yaml`](fuentes/catalogo.yaml) (incorporando las 15 fuentes añadidas en el commit `1e8bad6` y retirando `Varoufakis (pendiente)` en `08`).
  2. Precisar `33 capítulos base + anexo A1 (34 entradas)` en el encabezado de `mapa_obra.md` (L3), `notas/README.md` (L11) y `NOTAS.md` (L5).
  3. En [`capitulos/30_bibliografia.md`](capitulos/30_bibliografia.md) y [`capitulos/prefacio_segunda_edicion.md`](capitulos/prefacio_segunda_edicion.md), incluir al resto de autores primarios de `catalogo.yaml` (Sadin, C. Reyes, Cortina, Olmedo Neri, etc.) y advertir que de Kingsley L. Dennis solo existe ficha de contexto (no obra primaria citable en Bibliografía salvo que ingrese el libro).
  4. Aplicar la opción elegida en `D-04` respecto a las fichas individuales `capitulos/08`–`29`.

---

### `A-07` — Armonización de precauciones en fichas de prólogos invitados (`04`–`06`)
* **Impacto:** **Bajo** (`3` archivos)
* **Riesgo:** **Bajo**
* **Archivos implicados:** [`capitulos/04_prologo_1_rigoberto_lanz.md`](capitulos/04_prologo_1_rigoberto_lanz.md), [`capitulos/05_prologo_2_nelson_guzman.md`](capitulos/05_prologo_2_nelson_guzman.md) y [`capitulos/06_prologo_3_magaldy_tellez.md`](capitulos/06_prologo_3_magaldy_tellez.md).
* **Acción de implementación:** Alinear las tres fichas con [`capitulos/03_liminar.md`](capitulos/03_liminar.md) y la Decisión Editorial 4 (`SSOT/guia_estilo_editorial.md` §1.1): retirar sugerencias de modificar subtítulos o puntuación del cuerpo, e indicar que la unificación de encabezados partidos solo se haría en el cierre editorial con confirmación expresa del autor y flag `--permitir-invitados` en `validar_libro.py`.

---

### `A-08` — Cobertura de los 8 `README.md` del repositorio tras incorporar `maquetacion/`
* **Impacto:** **Medio** (`6` archivos transversales — ver `D-05`)
* **Riesgo:** **Medio** *(modifica `validar_libro.py`, `AGENTS.md` —vigilar peso `<= 20,000 B`— y `scripts/README.md`)*
* **Archivos implicados:** [`../scripts/edicion/validar_libro.py`](../scripts/edicion/validar_libro.py), [`../AGENTS.md`](../AGENTS.md), [`../.agents/skills/mantenimiento-proyecto/SKILL.md`](../.agents/skills/mantenimiento-proyecto/SKILL.md), [`../SSOT/guia_estilo_editorial.md`](../SSOT/guia_estilo_editorial.md), [`../SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md) y [`../scripts/README.md`](../scripts/README.md).
* **Acción de implementación (según `D-05`):** Incorporar `maquetacion/README.md` y `maquetacion/activos/README.md` a `READMES_PUBLICOS` en `validar_libro.py` (o escanear automáticamente todos los `README.md` versionados) y actualizar la mención de «los 6 `README.md`» a «los 8 `README.md`» (o «todos los `README.md` públicos») en los 5 documentos rectores.

---

### `A-09` — Ajuste de glifos faltantes (`Š`, `š`, `…`) y conteo de pasadas en `maquetacion/` y `SSOT/`
* **Impacto:** **Bajo** (`3` archivos)
* **Riesgo:** **Medio** *(al tocar `maquetacion/diseno_2ed.yaml` conviene verificar compilación rápida de 1 capítulo con `compilar_maqueta.py --capitulo 08`)*
* **Archivos implicados:** [`../SSOT/guia_maquetacion_segunda_edicion.md`](../SSOT/guia_maquetacion_segunda_edicion.md), [`../maquetacion/diseno_2ed.yaml`](../maquetacion/diseno_2ed.yaml) y [`../maquetacion/README.md`](../maquetacion/README.md).
* **Acciones de implementación:**
  1. En `SSOT/guia_maquetacion_segunda_edicion.md` (§2.2, L42–43), añadir `Š` y `š` a las listas de glifos ausentes de `amiga4ever pro2.ttf` (completando los `15` glifos reales y mencionando `…` en la sanitización) y de `BAUHS93.TTF` (completando los `9` glifos reales).
  2. En `maquetacion/diseno_2ed.yaml` (`tipografia.sanitizacion_amiga`), añadir `"Š": "S"` y `"š": "s"`.
  3. En `maquetacion/README.md` (L24), cambiar «con 3 pasadas automáticas» por «hasta 4 pasadas automáticas» para coincidir con `compilar_maqueta.py` y `SSOT/guia_maquetacion_segunda_edicion.md`.

---

### `A-10` — Alineación de lecturas por sesión en `SSOT/README.md` con Lectura Progresiva
* **Impacto:** **Bajo** (`1` archivo)
* **Riesgo:** **Bajo** *(cuidando mantener `0` menciones prohibidas en `SSOT/README.md`)*
* **Archivo implicado:** [`../SSOT/README.md`](../SSOT/README.md) (L12).
* **Acción de implementación:** Ajustar la fila `1. Obligatorio al editar un capítulo` para alinearla con `AGENTS.md` (§4) y `editar-capitulo/SKILL.md`: indicar que `contexto_capitulo.py --capitulo <id>` ya consolida la ficha espejo, fuentes y extractos de `NOTAS.md`, por lo que en cada sesión solo se cargan directamente `libro/<archivo>.md`, `notas/mapa_obra.md`, `SSOT/perfil_voz_autor.md` y las fichas pertinentes de `notas/fuentes/` (consultando `guia_estilo_editorial.md` y `flujo_editorial_segunda_edicion.md` como referencia normativa sin volcar `NOTAS.md` completo).

---

### `A-11` — Corrección de `-B`, formato del Glosario y nota de huérfanas en los 2 `SSOT/` históricos
* **Impacto:** **Bajo** (`2` archivos — ver `D-06`)
* **Riesgo:** **Bajo** *(no toca `respaldo_v1.0/` ni `scripts/extraccion_v1/`; previene escritura accidental de `__pycache__` en carpeta congelada)*
* **Archivos implicados:** [`../SSOT/proceso_conversion_pdf_a_md.md`](../SSOT/proceso_conversion_pdf_a_md.md) y [`../SSOT/detalle_ejecucion_y_auditoria_conversion.md`](../SSOT/detalle_ejecucion_y_auditoria_conversion.md).
* **Acciones de implementación (según `D-06`):**
  1. Anteponer `-B` en todas las invocaciones `python3 scripts/...` de `proceso_conversion_pdf_a_md.md` (L175) y `detalle_ejecucion_y_auditoria_conversion.md` (L113–122).
  2. Corregir `proceso_conversion_pdf_a_md.md` (L149) para reflejar que `31_glosario.md` preservó el formato `· Término:` (en lugar de `### Término`).
  3. Precisar en la tabla de `detalle_ejecucion_y_auditoria_conversion.md` (L22): `535 notas al pie extraídas (0 pérdidas de conversión; 7 omisiones del impreso de 2006 documentadas en §2.5)`.

---

### `A-12` — Documentación completa de banderas CLI en `scripts/README.md`
* **Impacto:** **Bajo** (`1` archivo)
* **Riesgo:** **Medio** *(archivo auditado por `validar_libro.py`: mantener `0` apariciones del término prohibido al redactar descripciones y ejemplos)*
* **Archivo implicado:** [`../scripts/README.md`](../scripts/README.md).
* **Acción de implementación:** Incorporar de forma concisa los flags existentes omitidos:
  * `validar_libro.py`: `--estricto`, `--permitir-invitados`, `--manifiesto`.
  * `buscar_externos.py`: `--fuente`, `--listar`, `--max-chars`, `--sin-auto-indexar`.
  * `buscar_libro.py`: `--capitulo`, `--limite`.
  * `recalcular_onomastico.py`: `--pdf`, `--desde-pagina`, `--hasta-pagina`.
  * `generar_indice.py`: `--incluir-h3`, `--salida`.
  * `indexar_externos.py`: `--forzar`.
  * `compilar_pdf.py`: `--version`, `--salida`.
  * `compilar_maqueta.py`: `--diseno`, `--pasadas`, `--salida`.

---

## Orden Recomendado de Ejecución y Verificación Final

1. **Bloque 1 (Decisiones y reglas/scripts base):** `A-08`, `A-09`, `A-02` (script + Skill), `A-01` y `A-12`.
2. **Bloque 2 (`SSOT/`):** `A-10` y `A-11`.
3. **Bloque 3 (`notas/` y seguimiento de Cap. `07`):** `A-03`, `A-04`, `A-05`, `A-06`, `A-07` y `A-02` (fichas de `fuentes/` si aplica).
4. **Auditoría final obligatoria (`mantenimiento-proyecto`):**
   * `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo` (`0` errores, `AGENTS.md <= 20,000 B`, `0` menciones prohibidas en todos los `README.md`).
   * Prueba rápida de maqueta (`python3 -B scripts/edicion/compilar_maqueta.py --capitulo 08`) y de CLI (`buscar_externos.py --fuente han_unlp_infocracia`).
   * Verificación automática de `0` enlaces Markdown rotos en `AGENTS.md`, `.agents/skills/`, `SSOT/`, `notas/`, `scripts/` y `maquetacion/`.

---

## Decisiones Necesarias antes de Implementar (Marcar con `[x]`)

### `D-01` — Protección en `recalcular_onomastico.py` ante entradas fusionadas en una misma línea (`A-01`)
- [ ] **Opción A (Recomendada):** Además de corregir el flujo en `cierre-editorial/SKILL.md` y `SSOT/`, añadir validación en `recalcular_onomastico.py` para advertir/abortar si una línea de `32_indice_onomastico.md` contiene dos entradas pegadas (como `ZIBECHI ... ŽIŽEK`).
- [ ] **Opción B:** Resolverlo únicamente en la documentación (`cierre-editorial/SKILL.md` y `SSOT/`) sin tocar `recalcular_onomastico.py`.

### `D-02` — Alcance de corrección para `buscar_externos.py --fuente <slug>` (`A-02`)
- [ ] **Opción A (Recomendada):** Ajustar `buscar_externos.py` (para que `--fuente <slug>` sin `<consulta>` muestre `--info <slug>` en lugar de listar todo) **y** actualizar `procesar-externos/SKILL.md` + las `23` fichas de `notas/fuentes/*.md` con `"<consulta>" --fuente <slug>`.
- [ ] **Opción B (Mínimo cambio de archivos):** Ajustar `buscar_externos.py` para que `--fuente <slug>` sin `<consulta>` funcione mostrando `cmd_info` (haciendo válidos los 23 comandos actuales) y actualizar solo `procesar-externos/SKILL.md`.
- [ ] **Opción C (Solo documentación):** No tocar `buscar_externos.py` y actualizar únicamente `procesar-externos/SKILL.md` y las `23` fichas de `notas/fuentes/*.md`.

### `D-03` — Folios `[PDF]` en notas nuevas de `libro/07_preambulo.md` (`A-03`)
- [ ] **Opción A (Recomendada):** Verificar ahora con `buscar_externos.py --leer` los folios impresos reales de Sadin 2020 (`[^5b]`), Harari *Nexus* (`[^11b]`) y Cortina 2024 (`[^20d]`), sustituir `p. X [PDF]` por el folio impreso en `libro/07_preambulo.md` y regenerar `dist/cap_07_preambulo.pdf`.
- [ ] **Opción B (No tocar `libro/07_preambulo.md` mientras está con el autor):** Dejar `libro/07_preambulo.md` intacto por ahora y registrar esos 3 folios junto con `[^5c]`, `[^10b]` y `[^20b]` como pendientes explícitos en `notas/capitulos/07_preambulo.md` para resolverlos al recibir respuesta del autor.

### `D-04` — Nivel de detalle de fuentes externas en las fichas `notas/capitulos/08`–`29` (`A-06`)
- [ ] **Opción A (Recomendada — evita doble mantenimiento):** Actualizar exhaustivamente `notas/mapa_obra.md`, `30_bibliografia.md` y `prefacio_segunda_edicion.md`, y añadir una nota breve o remisión a `catalogo.yaml` / `contexto_capitulo.py` sin duplicar manualmente cada `<slug>` en las 22 fichas `08`–`29` (salvo al preparar cada capítulo en su propia sesión, como se hizo en `07`).
- [ ] **Opción B (Sincronización exhaustiva lote completo):** Editar también las ~20 fichas de `notas/capitulos/08`–`29` que tienen fuentes en `catalogo.yaml` para enlazar explícitamente todas sus fichas de `notas/fuentes/<slug>.md`.

### `D-05` — Vigilancia de `README.md` públicos en `validar_libro.py` (`A-08`)
- [ ] **Opción A (Recomendada):** Detectar dinámicamente todos los `README.md` del repositorio (o ampliar `READMES_PUBLICOS` a los **8 `README.md`**, incluyendo `maquetacion/README.md` y `maquetacion/activos/README.md`) y hablar en la documentación de «todos los `README.md` del repositorio (8 actualmente)».
- [ ] **Opción B:** Mantener la lista fija de 6 `README.md` en `validar_libro.py` y aclarar en `SSOT/guia_estilo_editorial.md` que la verificación automática cubre esos 6 `README.md` principales.

### `D-06` — Intervención sobre los 2 documentos históricos de `SSOT/` (`A-11`)
- [ ] **Opción A (Recomendada):** Aplicar las 3 correcciones puntuales de higiene (`python3 -B`, nota `· Término:` y precisión sobre las 7 omisiones de 2006) en `SSOT/proceso_conversion_pdf_a_md.md` y `SSOT/detalle_ejecucion_y_auditoria_conversion.md`.
- [ ] **Opción B:** Añadir únicamente `-B` a los comandos `python3` (por seguridad del directorio congelado `scripts/extraccion_v1/`) y conservar el resto del texto histórico sin cambios.
- [ ] **Opción C:** No tocar ninguno de los 2 archivos históricos de `SSOT/`.

---

## Lista Resumida de Control (`Cambio / Impacto / Riesgo`)

- [ ] **`A-01`** — Prerrequisitos del Índice Onomástico (evitar borrado de `ŽIŽEK` + alta de nuevos autores) y recompilación final completa en `cierre-editorial` · **Impacto:** Bajo · **Riesgo:** Bajo *(Medio si incluye `D-01A`)*
- [ ] **`A-02`** — Solución al comando `buscar_externos.py --fuente <slug>` sin `<consulta>` en CLI, `procesar-externos` y `23` fichas de `notas/fuentes/` · **Impacto:** Alto *(o Bajo con `D-02B`)* · **Riesgo:** Bajo
- [ ] **`A-03`** — Sincronización post-edición del Cap. `07` en `notas/capitulos/07_preambulo.md`, `mapa_obra.md`, `NOTAS.md`, `CHANGELOG.md` y folios `[PDF]` · **Impacto:** Medio · **Riesgo:** Medio *(Bajo con `D-03B`)*
- [ ] **`A-04`** — Marcar como resuelto el pendiente obsoleto de maquetación final en `notas/NOTAS.md` (L108) · **Impacto:** Bajo · **Riesgo:** Bajo
- [ ] **`A-05`** — Corregir conteos base de 2006 pre-depuración en `5` fichas de `notas/capitulos/` (`09`, `10`, `13`, `20`, `28`) · **Impacto:** Bajo · **Riesgo:** Bajo
- [ ] **`A-06`** — Sincronizar las `27` fuentes de `catalogo.yaml` y el conteo `33 + A1` en `notas/mapa_obra.md`, `notas/README.md`, `NOTAS.md` y fichas · **Impacto:** Medio *(Alto con `D-04B`)* · **Riesgo:** Bajo
- [ ] **`A-07`** — Armonizar advertencias de protección y `--permitir-invitados` en fichas de prólogos invitados (`04`, `05`, `06`) · **Impacto:** Bajo · **Riesgo:** Bajo
- [ ] **`A-08`** — Ampliar cobertura y referencias de `README.md` públicos de `6` a `8` tras crear `maquetacion/` · **Impacto:** Medio · **Riesgo:** Medio
- [ ] **`A-09`** — Completar glifos faltantes (`Š`, `š`, `…`) en `SSOT/guia_maquetacion_segunda_edicion.md` y `diseno_2ed.yaml`, y ajustar pasadas en `maquetacion/README.md` · **Impacto:** Bajo · **Riesgo:** Medio
- [ ] **`A-10`** — Alinear tabla de lecturas por sesión en `SSOT/README.md` con la Política de Lectura Progresiva (`AGENTS.md` §4 / `editar-capitulo`) · **Impacto:** Bajo · **Riesgo:** Bajo
- [ ] **`A-11`** — Añadir `-B` a comandos `python3` y precisar formato de Glosario y notas huérfanas de 2006 en los `2` documentos históricos de `SSOT/` · **Impacto:** Bajo · **Riesgo:** Bajo
- [ ] **`A-12`** — Completar flags CLI omitidos en el catálogo único `scripts/README.md` · **Impacto:** Bajo · **Riesgo:** Medio
- [ ] **`V-01`** — Auditoría final post-implementación (`validar_libro.py --verificar-respaldo`, prueba `compilar_maqueta.py --capitulo 08` y `0` enlaces rotos) · **Impacto:** Bajo · **Riesgo:** Bajo

---

## Prioridades frente a la Edición Activa del Libro (¿Qué atender antes de seguir editando?)

> **Diagnóstico directo:** **Sí se puede proseguir hoy mismo con la edición de capítulos** (redacción, validación con `validar_libro.py --capitulo <id>` y compilación de borradores con `compilar_pdf.py --capitulo <id>`), sin esperar a resolver el resto del plan. Todos los scripts activos (`contexto_capitulo.py`, `buscar_libro.py`, `buscar_externos.py` con consulta, `validar_libro.py`, `compilar_pdf.py` y `reporte_cambios.py`) funcionan sin errores, y `contexto_capitulo.py` lee las 27 fuentes directamente desde `notas/fuentes/catalogo.yaml`.
>
> **Única precaución inmediata antes de abrir un capítulo nuevo (ej. `08` o `19`):** `notas/estado_sesion.md` **se sobrescribe** al cambiar de capítulo, por lo que conviene guardar antes en `notas/capitulos/07_preambulo.md` los pendientes del Cap. `07` para no perderlos.

### 1. Prioridad Inmediata — Atender antes de pasar al siguiente capítulo (~2 archivos en `notas/`, 0 riesgo)
- [x] **`A-03` *(solo resguardo en `notas/`, sin tocar `libro/07_preambulo.md`)*:**
  * Volcar los pendientes actuales de `notas/estado_sesion.md` (notas temporales `[^5b]`–`[^20d]` y verificación editorial de `[^5c]`, `[^10b]` y `[^20b]`, más revisión de folios `[PDF]` en `[^5b]`, `[^11b]`, `[^20d]`) hacia [`capitulos/07_preambulo.md`](capitulos/07_preambulo.md), para que no se borren cuando `estado_sesion.md` se sobrescriba con el siguiente capítulo.
  * Anotar en [`mapa_obra.md`](mapa_obra.md) (L26) que `07_preambulo.md` ya está *en revisión* e introdujo a Sadin, Harari, Han y Cortina (*giro conminatorio*, *dataísmo*, *infocracia*, *promptismo*), evitando re-presentarlos desde cero como si fueran inéditos al editar el próximo capítulo.

### 2. Prioridad Media — Útiles para comodidad en sesiones de edición (NO bloqueantes; resolubles en cualquier pausa)
- [ ] **`A-02` *(al menos en `buscar_externos.py` / Skill)*:** Evita que un agente invoque `buscar_externos.py --fuente <slug>` sin `<consulta>` copiándolo de una ficha *(mientras tanto, basta usar siempre `buscar_externos.py "<término>" --fuente <slug>` o `--leer <slug> --paginas A-B`, como ya indica `editar-capitulo/SKILL.md`)*.
- [ ] **`A-06` *(en `mapa_obra.md`)*:** Tener visibles las 15 fuentes recientes en la panorámica general *(no bloquea porque `contexto_capitulo.py --capitulo <id>` ya las muestra completas desde `catalogo.yaml`)*.
- [ ] **`A-07` y `A-10`:** Claridad preventiva sobre prólogos invitados (`04`–`06`, que igual no deben editarse) y ahorro de contexto en `SSOT/README.md`.

### 3. Prioridad Diferible — Exclusivos de mantenimiento general, Fase 4 o Cierre Editorial (0 impacto al editar capítulos hoy)
- [ ] **`A-03` (`D-03` — ajuste de folios `[PDF]` en `libro/07_preambulo.md`):** Puede aplicarse tranquilamente en Fase 4 junto con las observaciones del autor sobre el Cap. `07`.
- [ ] **`A-01` y `A-09`:** Exclusivos de la fase final (`cierre-editorial` / maquetación `LuaLaTeX` e Índice Onomástico).
- [ ] **`A-04`, `A-05`, `A-08`, `A-11` y `A-12`:** Higiene documental y catálogo CLI; no intervienen en la redacción ni validación de ensayos individuales.
