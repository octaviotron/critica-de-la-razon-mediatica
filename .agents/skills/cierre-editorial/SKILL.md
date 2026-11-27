---
name: cierre-editorial
description: >-
  Usar únicamente en la fase final de la Segunda Edición (cuando los capítulos principales
  estén aprobados en `libro.yaml`) o cuando el usuario pida consolidar Bibliografía,
  Glosario, renumerar notas al pie, regenerar el Índice General o preparar el Índice Onomástico
  y la compilación completa del manuscrito.
---

# Procedimiento: Fase Final de Cierre Editorial (Una Sola Vez)

Este flujo se ejecuta **una sola vez al cierre de la Segunda Edición** (o por bloques expresamente solicitados por el usuario), después de aprobar los capítulos de contenido en `libro.yaml`.

---

## 1. Verificación Previa del Tablero (`libro.yaml`)

1. Ejecutar validación global completa:
   ```bash
   python3 -B scripts/edicion/validar_libro.py --verificar-respaldo
   ```
2. Comprobar que:
   * Todos los ensayos editables estén en `estado: "aprobado"` (y sin marcadores `[VERIFICAR`, `TODO` ni `TBD`).
   * Las **7 advertencias heredadas** en `validar_libro.py` (`6` líneas que agrupan `7` omisiones reales de notas de 2006: `11`: `[^15]`, `[^19]`; `17`: `[^28]`; `20`: `[^3]`; `24`: `[^2]`, `[^4]`; `27`: `[^3]` + `1` asterisco impar en `17:L19`) y la nota truncada `14:[^6]` hayan sido resueltas o ratificadas por el autor.
   * Los textos invitados (`03`–`06` y `29` desde `L101`) permanecen íntegros salvo orden expresa.

---

## 2. Renumeración Secuencial de Notas al Pie (si hubo IDs temporales)

* Si durante la edición se insertaron identificadores temporales (`[^14b]`, `[^sadin]`, etc.), renumerar secuencialmente `1..N` dentro de cada capítulo afectado verificando biyección exacta `llamadas == definiciones` mediante `validar_libro.py --capitulo <id> --estricto`.
* Verificar uniformidad de notas (`Ibíd.`, `Op. cit.`, punto final) y comillas (`«»` / `""`, 0 comillas `‹›`).

---

## 3. Consolidación de Bibliografía (`30_bibliografia.md`) y Glosario (`31_glosario.md`)

1. **Bibliografía (`libro/30_bibliografia.md`):**
   * Cruzar todas las fuentes efectivamente citadas en `notas/fuentes/catalogo.yaml` y en `notas/NOTAS.md` con el listado existente usando `buscar_libro.py --bibliografia`.
   * Corregir las erratas históricas pendientes (`Gumis` → `Gomis`, `Foweler` → `Fowler`, separación de `ŽIŽEK` respecto a `ZIBECHI`) y ordenar alfabéticamente siguiendo el formato `- APELLIDO, Nombre: *Título*, Editorial, Ciudad, Año.`.
2. **Glosario (`libro/31_glosario.md`):**
   * Incorporar los términos nuevos acordados desde `notas/NOTAS.md` (Sección 4) respetando la voz filosófica (`SSOT/perfil_voz_autor.md`).
   * Confirmar con el autor si se conserva el formato `· Término:` o se migra a subtítulos `### Término`.

---

## 4. Saneamiento de Encabezados e Índice General (`01_indice.md`)

1. Verificar que todos los encabezados de apertura partidos en 2–3 líneas (`03`–`19`, `21`–`27`, `29`) y guiones sueltos (`## -` / `### -` en `14`, `16`, `22`, `27`) estén unificados *(consultar al autor antes de tocar encabezados de `03`–`06`)*.
2. Previsualizar primero el índice en `dist/indice_generado.md`:
   ```bash
   python3 -B scripts/edicion/generar_indice.py
   ```
3. Tras revisar la vista previa, escribir `libro/01_indice.md`:
   ```bash
   python3 -B scripts/edicion/generar_indice.py --escribir
   ```

---

## 5. Compilación Completa, Índice Onomástico y Revisión Final

1. **Verificar orden final de `libro.yaml` y limpiar `dist/`:** Confirmar que todos los capítulos nuevos (como el futuro `prefacio_segunda_edicion.md`, si se creó) y `A1` (`anexo_cambios_segunda_edicion.md`) estén en su posición definitiva en `libro.yaml`, y retirar borradores antiguos de `dist/` antes de la compilación final.
2. Ejecutar validación estricta global y reporte completo contra 2006:
   ```bash
   python3 -B scripts/edicion/validar_libro.py --verificar-respaldo --estricto
   python3 -B scripts/edicion/reporte_cambios.py
   ```
3. Compilar el manuscrito completo en `dist/` (entregas de lectura PDF/DOCX y **maqueta editorial `LuaLaTeX`** siguiendo [`SSOT/guia_maquetacion_segunda_edicion.md`](../../../SSOT/guia_maquetacion_segunda_edicion.md)):
   ```bash
   python3 -B scripts/edicion/compilar_pdf.py
   python3 -B scripts/edicion/compilar_pdf.py --formato docx
   python3 -B scripts/edicion/compilar_maqueta.py --modo digital
   python3 -B scripts/edicion/compilar_maqueta.py --modo imprenta
   ```
   Verificar en `dist/maqueta/reporte_libro_2ed_*.json` que `missing_characters == 0`, `latex_warnings == 0` y que no existan `overfull_hbox > 2 pt` sin revisar.
4. **Cierre del Anexo editorial (`libro/anexo_cambios_segunda_edicion.md`, `id: A1`):** Consolidar desde `notas/registro_cambios_edicion.md` la relación definitiva de cambios estructurales, actualizaciones por capítulo y aparato crítico (retirando cualquier nota provisional de avance), compilar su PDF limpio para revisión del autor y marcar `estado: "aprobado"` en `libro.yaml` únicamente tras su visto bueno explícito.
5. **Índice Onomástico (`libro/32_indice_onomastico.md`) y pre-prensa:** Una vez cerrada la paginación de la maqueta `LuaLaTeX`, previsualizar el recálculo sobre el PDF final, auditar entradas sin coincidencias, aplicar con `--escribir` y recompilar el PDF definitivo:
   ```bash
   python3 -B scripts/edicion/recalcular_onomastico.py
   python3 -B scripts/edicion/recalcular_onomastico.py --escribir
   python3 -B scripts/edicion/compilar_maqueta.py --modo imprenta
   ```
   Confirmar fuentes 100 % embebidas (`pdffonts`) y preparar la cubierta/lomo en PDF separado (`maquetacion/cubierta/especificaciones_lomo.md`).
6. Actualizar `obra.edicion` y `obra.version` en `libro.yaml`, registrar el cierre en `CHANGELOG.md` y dejar listo para el `commit`/`push` del usuario.
