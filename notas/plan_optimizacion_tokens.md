# Plan Técnico: Optimización de Tokens (Pilares 1 y 2)

> **Estado del plan:** `propuesto` — sin ejecutar. Ningún otro archivo del proyecto ha sido modificado por este plan.
> **Ubicación:** `notas/plan_optimizacion_tokens.md` (seguimiento técnico y pendientes).
> **Enfoque:** Máximo ahorro real de tokens con **riesgo nulo**, sin tocar `libro/`, sin alterar `SSOT/guia_estilo_editorial.md` ni `SSOT/perfil_voz_autor.md`, y manteniendo 100 % la compatibilidad actual de todos los scripts (`11` scripts activos).
> **Fecha:** 2026-11-26.

---

## 0. Reglas Inviolables al Ejecutar (de `AGENTS.md`)

1. **Confirmar alcance antes de tocar archivos** (disciplina conversacional, `AGENTS.md` §5.4).
2. **Activar `.agents/skills/mantenimiento-proyecto/SKILL.md`** al aplicar cambios en scripts, Skills o documentación.
3. **Directorios prohibidos para escritura:** nunca escribir en `respaldo_v1.0/`, `fuente/`, `scripts/extraccion_v1/` ni `externos/`.
4. **No modificar `libro/`** ni marcar ningún capítulo como `aprobado`.
5. **No ejecutar `git commit` ni `git push`** sin instrucción expresa del usuario.
6. **Higiene en los 6 `README.md` públicos:** 0 menciones de «IA» ni «Inteligencia Artificial» (`validar_libro.py` lo verifica).
7. **Límite de `AGENTS.md`:** mantenerlo `<= 20,000 B` (actualmente `12,372 B`; tope estricto `24,000 B`).
8. **Mantener intactos los `11` scripts activos** (se extiende `contexto_capitulo.py` y se añade una comprobación ligera opcional en `validar_libro.py`; no se crean scripts nuevos).
9. **No reintroducir tablas duplicadas de scripts:** el catálogo completo vive únicamente en `scripts/README.md`.

---

## 1. Diagnóstico y Objetivo

El mayor consumo evitable de tokens en la edición asistida no proviene de leer archivos normativos pequeños (`SSOT/perfil_voz_autor.md` pesa solo `7.7 KB`), sino de dos factores operativos:

1. **Crecimiento cuadrático del historial de conversación:** en cada turno se reenvía toda la conversación acumulada. Mantener un mismo chat abierto durante decenas de turnos tras cargar capítulos extensos (`07`: `82 KB`, `10`: `109 KB`, `19`/`26`/`27`: `62 KB`) multiplica el gasto de entrada por `5×–10×`.
2. **Pérdida de continuidad al abrir sesiones nuevas:** sin una memoria de sesión mínima en disco, retomar el trabajo («sigamos») obliga a volver a inspeccionar varios archivos o mantener chats demasiado largos por temor a perder el hilo.

**Objetivo:** reducir sustancialmente el consumo de cuota mediante **dos pilares de riesgo nulo**:
* **Pilar 1:** Pautas operativas de higiene de conversación, verificación por `git diff` y uso racional del modelo Pro (0 código, aplicable de inmediato).
* **Pilar 2:** Memoria mínima entre sesiones (`notas/estado_sesion.md` + `contexto_capitulo.py --estado`) para poder cerrar y abrir conversaciones limpias sin perder contexto.

---

## 2. Pilar 1 — Higiene de Conversación y Uso de Cuota *(Riesgo: nulo | Código: 0)*

Pautas operativas para adoptar en el flujo diario (y reflejar brevemente en `.agents/skills/editar-capitulo/SKILL.md` al ejecutar el Pilar 2):

1. **Una conversación nueva por capítulo:** al cerrar o entregar un capítulo (o cada 2–3 bloques en ensayos `> 50 KB` como `07`, `10`, `19`, `26`, `27`), abrir una sesión nueva (o ejecutar `/compact` antes de continuar).
2. **Separar trabajo mecánico vs. redacción filosófica:**
   * Usar **modelo ligero** (o subagentes `flash` / `flash_lite`) para tareas mecánicas: validar, compilar PDF/maqueta, buscar citas en `externos/`, fichar nuevos libros, revisar logs de `LuaLaTeX` o sincronizar documentación.
   * Reservar el **modelo Pro** exclusivamente para el trabajo editorial fino: planear intervenciones, dialogar con autores y redactar prosa en la voz de Juan Barreto.
3. **Verificación por diff, nunca relectura completa:** tras editar un capítulo en `libro/`, verificar cambios con `git diff libro/<archivo>.md` y `validar_libro.py --capitulo <id>` en lugar de volver a leer el archivo completo.
4. **Agrupar peticiones afines:** en rondas de correcciones editoriales o ajustes visuales de maquetación, reunir 4–6 cambios en un mismo mensaje en vez de consumir un turno por cada ajuste mínimo.

---

## 3. Pilar 2 — Memoria Mínima entre Sesiones *(Riesgo: nulo | 100 % aditivo)*

Pieza técnica liviana que hace viable abrir conversaciones limpias (Pilar 1) sin perder continuidad.

### 3.1. Nuevo archivo local (ignorado por Git): `notas/estado_sesion.md`

* **Ubicación y Git:** `notas/estado_sesion.md`, añadido a `.gitignore` como archivo local de trabajo (no se versiona en Git; tras un `git clone` se crea bajo demanda y `contexto_capitulo.py --estado` funciona sin error aunque todavía no exista). **No** sustituye a `notas/registro_cambios_edicion.md`, `CHANGELOG.md` ni a las fichas espejo de `notas/capitulos/`.
* **Tope estricto:** `<= 2,048 B` (recomendado `<= 1 KB`, 7–8 líneas). Se **sobrescribe** en cada cambio de etapa; **no** acumula historial.
* **Plantilla inicial:**

```markdown
# Estado de sesión (trabajo en curso)

> Máx. 2 KB. Se sobrescribe al cambiar de paso; no acumula historial.

- **Capítulo en curso:** —
- **Tramo / sección en curso:** —
- **Último paso completado:** —
- **Próximo paso:** —
- **Pendientes inmediatos (citas `[VERIFICAR]`, notas temporales):** —
- **Instrucciones vigentes del autor:** —
- **Actualizado:** 2026-MM-DD
```

* **Cuándo se actualiza:** únicamente al finalizar un bloque sustantivo, entregar un borrador al autor, recibir observaciones o cerrar sesión (nunca en cada micro-edición). Al aprobarse un capítulo, se restablece a `—` (o apunta al siguiente capítulo).

### 3.2. Nuevo flag en `scripts/edicion/contexto_capitulo.py`: `--estado`

```bash
python3 -B scripts/edicion/contexto_capitulo.py --estado
```

* **Compatibilidad hacia atrás garantizada:** `contexto_capitulo.py --capitulo <id>` **no cambia en nada** su salida ni comportamiento actual.
* **Cambios en `contexto_capitulo.py`:**
  1. Cambiar `--capitulo` a `required=False` y exigir que se pase `--capitulo` **o** `--estado` (código de salida `2` con mensaje claro en español si faltan ambos o se mezclan de forma inválida).
  2. En modo `--estado` (solo lectura, salida `<= 1,500 B`, ~400 tokens):
     * Imprime el contenido de `notas/estado_sesion.md` (si no existe, muestra `No existe notas/estado_sesion.md` y continúa con código `0`).
     * Imprime un **tablero compacto** desde `libro.yaml`: conteo `aprobado` / `en_revision` / `pendiente` y la lista breve de capítulos en `en_revision`.
     * Imprime la última entrada registrada (`### [E-NN]` o último encabezado de registro) de `notas/registro_cambios_edicion.md`.

### 3.3. Comprobación ligera en `scripts/edicion/validar_libro.py`

Dentro de `verificar_salud_workspace()`, añadir únicamente **una advertencia suave** (nunca error):
* Si `notas/estado_sesion.md` existe y supera `2,048 B`, emitir advertencia recordando compactarlo.
* Si el archivo no existe, no emitir nada.

---

## 4. Sincronización Documental Mínima (al ejecutar el Pilar 2)

Aplicar únicamente los ajustes estrictamente necesarios siguiendo `.agents/skills/mantenimiento-proyecto/SKILL.md`:

| Archivo | Cambio puntual |
| :--- | :--- |
| `AGENTS.md` | §1 («Arranque rápido»): usar `contexto_capitulo.py --estado` antes de `validar_libro.py`. §2 y §3 (fila `notas/`): mencionar `estado_sesion.md` como archivo local (ignorado por Git) de seguimiento operativo. §7: mencionar `--estado` en el resumen de `contexto_capitulo.py`. |
| `.gitignore` | Añadir `notas/estado_sesion.md` para excluirlo del control de versiones. |
| `.agents/skills/editar-capitulo/SKILL.md` | Añadir la pauta de verificación por `git diff` (sin releer capítulos largos completos tras editar) y actualizar `notas/estado_sesion.md` al entregar/cerrar ronda o capítulo. |
| `scripts/README.md` | Documentar el flag `--estado` en la fila y ejemplos de `contexto_capitulo.py` (sin «IA»). |
| `notas/README.md` | Documentar `estado_sesion.md` como archivo local de sesión ignorado por Git (sin «IA»). |
| `CHANGELOG.md` | Al cerrar y verificar todo, registrar el hito en *Arquitectura editorial*. |

*(No se modifica `SSOT/guia_estilo_editorial.md`, ni `SSOT/perfil_voz_autor.md`, ni `SSOT/flujo_editorial_segunda_edicion.md` §6.1, ni `libro/`.)*

---

## 5. Decisión Confirmada

* **`notas/estado_sesion.md` en Git:** **ignorado mediante `.gitignore`** (archivo local por equipo; `contexto_capitulo.py --estado` tolera su ausencia tras un `git clone` saliendo con código `0`, y `validar_libro.py` no emite advertencia si no existe).

---

## 6. Verificación Obligatoria al Ejecutar

1. **Cero regresiones en `contexto_capitulo.py --capitulo <id>`:** comparar con `diff` antes y después en al menos 2 capítulos (`08` y `A1`).
2. **Pruebas de `--estado` y `.gitignore`:**
   * Con `notas/estado_sesion.md` inicial (`<= 1,500 B`, código `0`) y comprobar que `git status` no lo lista como archivo sin seguimiento.
   * Sin `notas/estado_sesion.md` (simulando `git clone`): `--estado` sigue funcionando con código `0` y `validar_libro.py` no avisa.
   * Sin `--capitulo` ni `--estado` (código `2`, mensaje claro).
   * Con archivo temporal `> 2,048 B`: `validar_libro.py` emite advertencia (0 errores).
3. **Auditoría integral del repositorio:**
   ```bash
   python3 -B scripts/edicion/validar_libro.py --verificar-respaldo
   ```
   Esperado: **0 errores**, `33/33` SHA-256 íntegros, mismas **7 advertencias heredadas**, `0` menciones prohibidas en los 6 `README.md`, `AGENTS.md <= 20,000 B` y `0` enlaces locales rotos.

---

## 7. Registro de Ejecución *(rellenar solo cuando se ejecute)*

- [ ] Pilar 1 adoptado en flujo diario y reflejado en `editar-capitulo/SKILL.md`
- [ ] `notas/estado_sesion.md` añadido a `.gitignore` y creado localmente (`<= 2 KB`)
- [ ] `contexto_capitulo.py --estado` implementado y verificado (con y sin archivo local, y sin regresión en `--capitulo`)
- [ ] Aviso de tamaño (`> 2,048 B`) añadido en `validar_libro.py`
- [ ] Documentación sincronizada (`AGENTS.md`, `scripts/README.md`, `notas/README.md`, `CHANGELOG.md`)
- [ ] `validar_libro.py --verificar-respaldo` en `0` errores
- [ ] Estado del plan cambiado a `ejecutado`
