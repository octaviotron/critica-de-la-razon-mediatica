# Índice y Guía Técnica del Repositorio (`SSOT/`)

*Single Source of Truth* (fuente única de verdad) del proyecto **Segunda Edición — *Crítica de la Razón Mediática*** (Juan Barreto Cipriani).

---

## 1. Qué leer y qué NO leer en cada sesión

| Prioridad | Documentos / Carpetas | Cuándo leerlos |
| :--- | :--- | :--- |
| **0. Regla raíz y Skills del workspace** | [`AGENTS.md`](../AGENTS.md) y [`.agents/skills/`](../.agents/skills/) | `AGENTS.md` se carga automáticamente en cada sesión (contexto raíz, límites inviolables y arranque rápido); las 4 Skills (`editar-capitulo`, `procesar-externos`, `cierre-editorial`, `mantenimiento-proyecto`) se activan bajo demanda según la tarea. |
| **1. Obligatorio al editar un capítulo** | [`SSOT/guia_estilo_editorial.md`](guia_estilo_editorial.md), [`SSOT/perfil_voz_autor.md`](perfil_voz_autor.md), [`SSOT/flujo_editorial_segunda_edicion.md`](flujo_editorial_segunda_edicion.md), [`notas/mapa_obra.md`](../notas/mapa_obra.md), el archivo objetivo en [`libro/`](../libro/), su ficha espejo en [`notas/capitulos/`](../notas/capitulos/), los puntos pertinentes de [`notas/NOTAS.md`](../notas/NOTAS.md) y las fichas aplicables en [`notas/fuentes/`](../notas/fuentes/). | En cada sesión de edición asistida (siempre **un capítulo a la vez** para mantener foco y bajo consumo de contexto). Al retomar en una conversación nueva, `contexto_capitulo.py --estado` resume el estado local de sesión (`notas/estado_sesion.md`, si existe), el tablero y el último registro (ver `flujo_editorial_segunda_edicion.md` §2.2). |
| **2. Solo consulta histórica** | [`SSOT/proceso_conversion_pdf_a_md.md`](proceso_conversion_pdf_a_md.md), [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](detalle_ejecucion_y_auditoria_conversion.md) y [`scripts/extraccion_v1/`](../scripts/extraccion_v1/). | **No cargar en sesiones normales.** Se conservan en esta ruta exacta por compatibilidad con `respaldo_v1.0/README.md` (inmutable) y `scripts/extraccion_v1/` (congelado). Consultar solo ante dudas sobre la extracción de 2006. |
| **3. Intocables / solo lectura** | [`fuente/`](../fuente/), [`respaldo_v1.0/`](../respaldo_v1.0/), [`scripts/extraccion_v1/`](../scripts/extraccion_v1/) y [`externos/`](../externos/). | **Nunca editar, renombrar ni sobrescribir.** `externos/` se consulta únicamente mediante el índice local y las fichas de `notas/fuentes/` (sin cargar PDFs completos en memoria). |

---

## 2. Mapa de responsabilidades del repositorio (sin solapamientos)

* **[`AGENTS.md`](../AGENTS.md) y [`.agents/skills/`](../.agents/skills/):** Regla universal siempre activa del workspace y 4 guías procedimentales modulares bajo demanda (`editar-capitulo`, `procesar-externos`, `cierre-editorial`, `mantenimiento-proyecto`).
* **[`libro/`](../libro/):** Única copia viva del texto publicable (sin anotaciones internas ni borradores); su índice navegable vive en [`libro/README.md`](../libro/README.md).
* **[`libro.yaml`](../libro.yaml):** Manifiesto maestro del orden de partes/capítulos y tablero de `estado` (`pendiente` | `en_revision` | `aprobado`) bajo la **Opción A** (los nombres actuales de `libro/` funcionan como IDs estables).
* **[`notas/`](../notas/):** Espacio para pendientes y seguimiento editorial ([`notas/NOTAS.md`](../notas/NOTAS.md), [`notas/mapa_obra.md`](../notas/mapa_obra.md), [`notas/registro_cambios_edicion.md`](../notas/registro_cambios_edicion.md), [`notas/capitulos/`](../notas/capitulos/) y [`notas/fuentes/`](../notas/fuentes/)), más `notas/estado_sesion.md` (archivo local de seguimiento operativo, ignorado por Git, que puede no existir en un clon nuevo).
* **[`externos/`](../externos/):** Biblioteca bibliográfica de consulta (solo lectura) con PDFs, artículos HTML y textos de apoyo para la 2.ª edición; se indexa localmente en `dist/indice_externos/` y se ficha en `notas/fuentes/`.
* **[`CHANGELOG.md`](../CHANGELOG.md):** Único registro de **hechos cerrados** (capítulos ya aprobados por el autor e hitos completados).
* **[`scripts/`](../scripts/):** Herramientas internas de edición (`scripts/edicion/`) y pipeline histórico congelado (`scripts/extraccion_v1/`); documentación completa y comandos en [`scripts/README.md`](../scripts/README.md).
* **[`maquetacion/`](../maquetacion/):** Configuración declarativa (`diseno_2ed.yaml`), plantillas modulares `LuaLaTeX` (`plantilla/`), activos nuevos de 2.ª edición (`activos/`) y especificaciones de cubierta/lomo (`cubierta/`).
* **[`respaldo_v1.0/`](../respaldo_v1.0/):** Respaldo inmutable de la 1.ª edición (2006) para comparaciones y compilación garantizada de `v1.0.0` ([`respaldo_v1.0/README.md`](../respaldo_v1.0/README.md)).
* **`dist/`:** Carpeta local ignorada por Git para entregas temporales (PDF/Word `.docx`), maquetas compiladas (`dist/maqueta/`), reportes comparativos y el índice reconstruible `dist/indice_externos/`; es desechable y puede limpiarse libremente.

---

## 3. Árbol Técnico del Repositorio e Inventario de `fuente/`

```text
critica-de-la-razon-mediatica/
├── README.md                  # Presentación pública general de la obra y del proyecto
├── AGENTS.md                  # Reglas universales del workspace, mapa y protocolo de mantenimiento
├── .agents/skills/            # 4 guías procedimentales modulares bajo demanda:
│   ├── editar-capitulo/       #   Flujo por capítulo (briefing, edición, validación, entrega y cierre)
│   ├── procesar-externos/     #   Indexación incremental, colofones y fichado de externos/
│   ├── cierre-editorial/      #   Consolidación final (bibliografía, glosario, notas, índices y anexo A1)
│   └── mantenimiento-proyecto/#   Matriz de sincronización y auditoría ante cambios estructurales
├── CHANGELOG.md               # Bitácora editorial de capítulos aprobados e hitos completados
├── libro.yaml                 # Manifiesto maestro: orden del índice y estado por capítulo (Opción A)
├── .gitignore                 # Excluye dist/ (PDFs/DOCX/reportes/índice local), notas/estado_sesion.md (local) y temporales
├── externos/                  # [Solo lectura] Biblioteca bibliográfica de apoyo (PDF, HTML, TXT…)
├── fuente/                    # [Inmutable] Material original de la 1.ª edición (2006)
│   ├── Libro Crítica de La Razon Mediatica.pdf  # PDF maestro (21.08 MB, 666 págs. físicas / folios 2–699)
│   ├── FUENTES/               # Tipografías originales (.ttf): Garamond, Bauhaus93, AmigaForeverPro2, Swis721, Arial Black
│   ├── PORTADA/               # Artes originales de portada (.tif): repujado1, repujado2 y uv
│   └── RAZON/                 # Maquetación QuarkXPress (INICIAL.qxp, liminar.qxp, 1a–6a parte.qxp, POST-Escriptum.qxp, POSTERIOR.qxp),
│       ├── UBICACION DE liminar.txt             # nota editorial original de ubicación del Liminar
│       └── images/            # 14 portadillas gráficas separadoras (.tif / .jpg)
├── libro/                     # Única fuente viva en Markdown (33 archivos base + anexo_cambios_segunda_edicion.md + libro/README.md)
├── maquetacion/               # Diseño editorial LuaLaTeX (diseno_2ed.yaml, plantilla/, activos/, cubierta/ y README.md)
├── notas/                     # NOTAS.md, mapa_obra.md, registro_cambios_edicion.md, capitulos/, fuentes/, README.md y estado_sesion.md (local, ignorado por Git)
├── respaldo_v1.0/             # [Inmutable] README.md, libro.yaml v1.0, manifiesto_v1.0.md (SHA-256) y md/ (33 archivos)
├── dist/                      # [Ignorado por Git] Entregas PDF/DOCX, maquetas (maqueta/), reportes diff e índice local de externos/
├── scripts/                   # README.md + edicion/ (11 scripts activos) + extraccion_v1/ (3 scripts congelados)
└── SSOT/                      # Documentación rectora (este índice + 6 documentos normativos/históricos)
```

---

## 4. Documentos de este Directorio (`SSOT/`)

* **[`flujo_editorial_segunda_edicion.md`](flujo_editorial_segunda_edicion.md):** Flujo oficial simplificado de edición asistida capítulo por capítulo, incorporación de `externos/`, gestión de nuevos capítulos e índice en `libro.yaml`, y operación de `respaldo_v1.0/`.
* **[`guia_estilo_editorial.md`](guia_estilo_editorial.md):** Reglas de fidelidad estilística, vocabulario conceptual protegido, 7 decisiones editoriales confirmadas, ejemplo práctico de integración híbrida, citas europeas, política anti-alucinación y reglas de seguridad.
* **[`perfil_voz_autor.md`](perfil_voz_autor.md):** Referencia empírica de la cadencia ensayística del autor, anti-patrones a evitar e inventario completo de los 93 términos del Glosario.
* **[`guia_maquetacion_segunda_edicion.md`](guia_maquetacion_segunda_edicion.md):** Receta oficial, parámetros ajustables (`maquetacion/diseno_2ed.yaml` y `plantilla/`), auditoría de glifos de 2006, comandos de compilación `LuaLaTeX`, recálculo del Índice Onomástico y checklist pre-imprenta.
* **[`proceso_conversion_pdf_a_md.md`](proceso_conversion_pdf_a_md.md):** *(Histórico)* Especificación técnica del Método 1 (2006) y política del respaldo inmutable `respaldo_v1.0/`.
* **[`detalle_ejecucion_y_auditoria_conversion.md`](detalle_ejecucion_y_auditoria_conversion.md):** *(Histórico)* Memoria técnica de la conversión ejecutada y tabla de auditoría contable al `100.000%` capítulo por capítulo.
