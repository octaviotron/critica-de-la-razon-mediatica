# Índice y Guía de Inicio Rápido (`SSOT/`)

*Single Source of Truth* (fuente única de verdad) del proyecto **Segunda Edición — *Crítica de la Razón Mediática*** (Juan Barreto Cipriani).

---

## 1. Qué leer y qué NO leer en cada sesión

| Prioridad | Documentos / Carpetas | Cuándo leerlos |
| :--- | :--- | :--- |
| **1. Obligatorio al editar un capítulo** | [`SSOT/guia_estilo_editorial.md`](guia_estilo_editorial.md), [`SSOT/flujo_editorial_segunda_edicion.md`](flujo_editorial_segunda_edicion.md), el archivo objetivo en [`libro/`](../libro/), su ficha espejo en [`notas/capitulos/`](../notas/capitulos/) y los puntos pertinentes de [`notas/NOTAS.md`](../notas/NOTAS.md). | En cada sesión de edición asistida (siempre **un capítulo a la vez** para mantener foco y bajo consumo de contexto). |
| **2. Solo consulta histórica** | [`SSOT/proceso_conversion_pdf_a_md.md`](proceso_conversion_pdf_a_md.md), [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](detalle_ejecucion_y_auditoria_conversion.md) y [`scripts/extraccion_v1/`](../scripts/extraccion_v1/). | **No cargar en sesiones normales.** Consultar únicamente si surge una duda sobre la extracción original del PDF de 2006 o sus métricas de auditoría. |
| **3. Intocables (solo lectura)** | [`fuente/`](../fuente/), [`respaldo_v1.0/`](../respaldo_v1.0/) y [`scripts/extraccion_v1/`](../scripts/extraccion_v1/). | **Nunca editar, renombrar ni sobrescribir.** Sirven como archivo original y respaldo congelado verificable por SHA-256. |

---

## 2. Mapa de responsabilidades del repositorio (sin solapamientos)

* **[`libro/`](../libro/):** Única copia viva del texto publicable (sin anotaciones internas ni borradores).
* **[`libro.yaml`](../libro.yaml):** Manifiesto maestro del orden de partes/capítulos y tablero de `estado` (`pendiente` | `en_revision` | `aprobado`).
* **[`notas/NOTAS.md`](../notas/NOTAS.md) y [`notas/capitulos/`](../notas/capitulos/):** Único espacio para **todo lo pendiente** (autores por incorporar, ideas, frases, términos candidatos para el Glosario, referencias futuras para Bibliografía y observaciones del autor).
* **[`CHANGELOG.md`](../CHANGELOG.md):** Único registro de **hechos cerrados** (capítulos ya aprobados por el autor e hitos completados).
* **[`respaldo_v1.0/`](../respaldo_v1.0/):** Respaldo inmutable de la 1.ª edición (2006) para comparaciones y compilación garantizada de `v1.0.0`.
* **`dist/`:** Carpeta local ignorada por Git para entregas temporales (PDF/Word `.docx`) y reportes comparativos; es desechable y puede limpiarse libremente.
