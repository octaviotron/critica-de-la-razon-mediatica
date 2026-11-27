---
name: mantenimiento-proyecto
description: >-
  Usar cuando se añada, modifique o elimine cualquier script en `scripts/edicion/`,
  directorio, Skill de `.agents/skills/`, regla editorial en `SSOT/`, estructura de
  `libro.yaml` o `README.md`, para sincronizar toda la documentación y verificar
  ausencia de contradicciones.
---

# Procedimiento: Mantenimiento y Evolución Consistente del Repositorio

Sigue esta matriz y su auditoría final **en el mismo turno** ante cualquier cambio estructural del proyecto para impedir derivas entre `AGENTS.md`, `.agents/skills/`, `SSOT/`, `libro.yaml`, `notas/` y los `README.md`.

---

## 1. Matriz de Sincronización Obligatoria

| Tipo de cambio | Archivos que DEBEN sincronizarse |
| :--- | :--- |
| **Script en `scripts/edicion/`** | El script (siempre protegiendo `respaldo_v1.0/` vía `es_ruta_dentro_de_respaldo`) + `scripts/README.md` (catálogo único, sin «IA») + resumen de nombres en `AGENTS.md` (§7) y Skill afectada si se añade/renombra un script. |
| **Directorio o Skill nueva/modificada** | `AGENTS.md` (§3 y §7) + `SSOT/README.md` + `README.md` (resumen público, sin «IA») + `README.md` interno / `.gitignore` si aplica. |
| **Maquetación (`maquetacion/` o `compilar_maqueta.py`)** | `maquetacion/diseno_2ed.yaml` / `maquetacion/plantilla/*.tex` + `maquetacion/README.md` + `SSOT/guia_maquetacion_segunda_edicion.md` + prueba rápida (`compilar_maqueta.py --capitulo 08`). |
| **Regla editorial, decisión o flujo** | `SSOT/guia_estilo_editorial.md` y/o `SSOT/flujo_editorial_segunda_edicion.md` + `AGENTS.md` (§5–§6) + `.agents/skills/` afectada + `notas/NOTAS.md` (y `notas/registro_cambios_edicion.md` si afecta al libro). |
| **Añadir, eliminar o reordenar capítulos/secciones** | `libro/` (si es archivo nuevo) + `libro.yaml` + `libro/README.md` + `README.md` (tabla de bloques) + `notas/capitulos/` (ficha espejo) + `notas/mapa_obra.md` + `notas/registro_cambios_edicion.md` + `libro/anexo_cambios_segunda_edicion.md`. |
| **Cerrar hallazgo técnico de `notas/NOTAS.md`** | Marcar `- [x]` en `notas/NOTAS.md` + retirar limitación en `AGENTS.md` (si aplicaba) + registrar hito en `CHANGELOG.md`. |

---

## 2. Reglas de Seguridad Inviolables durante Mantenimiento

* **Nunca escribir** en `fuente/`, `respaldo_v1.0/`, `scripts/extraccion_v1/` ni `externos/`.
* **Prohibición absoluta en los 6 `README.md` públicos** (`README.md`, `libro/README.md`, `notas/README.md`, `respaldo_v1.0/README.md`, `scripts/README.md`, `SSOT/README.md`): **0** menciones de «IA» ni «Inteligencia Artificial».
* **Nunca ejecutar `git commit` ni `git push`** sin instrucción expresa del usuario.

---

## 3. Auditoría Automatizada Obligatoria (Post-Cambio)

Ejecutar estos tres chequeos antes de cerrar el turno:

1. **Validación editorial, SHA-256, `README.md`, tamaño de `AGENTS.md` y fichas espejo:**
   ```bash
   python3 -B scripts/edicion/validar_libro.py --verificar-respaldo
   ```
   Debe concluir con **0 errores** (`33/33` SHA-256 íntegros, `0` menciones prohibidas en los 6 `README.md` y `AGENTS.md` `<= 20,000` bytes sin aviso / tope estricto `24,000` bytes).
2. **Probar con casos reales cualquier script creado o modificado** (y comprobar idempotencia si aplica).
3. **Verificar enlaces locales rotos, frontmatter de Skills y consistencia de conteos** (número de decisiones editoriales, secciones en `libro.yaml`, capítulos base + nuevos, entradas del Glosario) entre `AGENTS.md`, `.agents/skills/`, `SSOT/` y los `README.md`.
