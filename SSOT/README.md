# Índice y Guía de Inicio Rápido (`SSOT/`)

*Single Source of Truth* (fuente única de verdad) del proyecto **Segunda Edición — *Crítica de la Razón Mediática*** (Juan Barreto Cipriani).

---

## 1. Qué leer y qué NO leer en cada sesión

| Prioridad | Documentos / Carpetas | Cuándo leerlos |
| :--- | :--- | :--- |
| **0. Regla raíz del workspace** | [`AGENTS.md`](../AGENTS.md) | Se carga automáticamente al iniciar cualquier sesión y resume el mapa del proyecto, las reglas inviolables y el protocolo de mantenimiento. |
| **1. Obligatorio al editar un capítulo** | [`SSOT/guia_estilo_editorial.md`](guia_estilo_editorial.md), [`SSOT/perfil_voz_autor.md`](perfil_voz_autor.md), [`SSOT/flujo_editorial_segunda_edicion.md`](flujo_editorial_segunda_edicion.md), [`notas/mapa_obra.md`](../notas/mapa_obra.md), el archivo objetivo en [`libro/`](../libro/), su ficha espejo en [`notas/capitulos/`](../notas/capitulos/), los puntos pertinentes de [`notas/NOTAS.md`](../notas/NOTAS.md) y las fichas aplicables en [`notas/fuentes/`](../notas/fuentes/). | En cada sesión de edición asistida (siempre **un capítulo a la vez** para mantener foco y bajo consumo de contexto). |
| **2. Solo consulta histórica** | [`SSOT/proceso_conversion_pdf_a_md.md`](proceso_conversion_pdf_a_md.md), [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](detalle_ejecucion_y_auditoria_conversion.md) y [`scripts/extraccion_v1/`](../scripts/extraccion_v1/). | **No cargar en sesiones normales.** Consultar únicamente si surge una duda sobre la extracción original del PDF de 2006 o sus métricas de auditoría. |
| **3. Intocables / solo lectura** | [`fuente/`](../fuente/), [`respaldo_v1.0/`](../respaldo_v1.0/), [`scripts/extraccion_v1/`](../scripts/extraccion_v1/) y [`externos/`](../externos/). | **Nunca editar, renombrar ni sobrescribir.** `externos/` se consulta únicamente mediante el índice local y las fichas de `notas/fuentes/` (sin cargar PDFs completos en memoria). |

---

## 2. Mapa de responsabilidades del repositorio (sin solapamientos)

* **[`AGENTS.md`](../AGENTS.md):** Regla universal del workspace (contexto completo de entrada y protocolo de sincronización ante cambios de scripts, directorios o flujo).
* **[`libro/`](../libro/):** Única copia viva del texto publicable (sin anotaciones internas ni borradores).
* **[`libro.yaml`](../libro.yaml):** Manifiesto maestro del orden de partes/capítulos y tablero de `estado` (`pendiente` | `en_revision` | `aprobado`).
* **[`notas/NOTAS.md`](../notas/NOTAS.md), [`notas/capitulos/`](../notas/capitulos/) y [`notas/fuentes/`](../notas/fuentes/):** Único espacio para **todo lo pendiente** (autores por incorporar, ideas, frases, términos candidatos para el Glosario, referencias futuras para Bibliografía, observaciones del autor y fichas curadas de la bibliografía externa).
* **[`externos/`](../externos/):** Biblioteca bibliográfica de consulta (solo lectura) con PDFs, artículos HTML y textos de apoyo para la 2.ª edición; se indexa localmente en `dist/indice_externos/` y se ficha en `notas/fuentes/`.
* **[`CHANGELOG.md`](../CHANGELOG.md):** Único registro de **hechos cerrados** (capítulos ya aprobados por el autor e hitos completados).
* **[`respaldo_v1.0/`](../respaldo_v1.0/):** Respaldo inmutable de la 1.ª edición (2006) para comparaciones y compilación garantizada de `v1.0.0`.
* **`dist/`:** Carpeta local ignorada por Git para entregas temporales (PDF/Word `.docx`), reportes comparativos y el índice reconstruible `dist/indice_externos/`; es desechable y puede limpiarse libremente.
