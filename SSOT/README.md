# Índice y Guía Técnica del Repositorio (`SSOT/`)

*Single Source of Truth* (fuente única de verdad) del proyecto **Segunda Edición — *Crítica de la Razón Mediática*** (Juan Barreto Cipriani).

---

## 1. Qué leer y qué NO leer en cada sesión

| Prioridad | Documentos / Carpetas | Cuándo leerlos |
| :--- | :--- | :--- |
| **0. Regla raíz y Skills del workspace** | [`AGENTS.md`](../AGENTS.md) y [`.agents/skills/`](../.agents/skills/) | `AGENTS.md` se carga automáticamente en cada sesión (contexto raíz, límites inviolables y mantenimiento); las Skills (`editar-capitulo`, `procesar-externos`, `cierre-editorial`) se activan bajo demanda según la tarea. |
| **1. Obligatorio al editar un capítulo** | [`SSOT/guia_estilo_editorial.md`](guia_estilo_editorial.md), [`SSOT/perfil_voz_autor.md`](perfil_voz_autor.md), [`SSOT/flujo_editorial_segunda_edicion.md`](flujo_editorial_segunda_edicion.md), [`notas/mapa_obra.md`](../notas/mapa_obra.md), el archivo objetivo en [`libro/`](../libro/), su ficha espejo en [`notas/capitulos/`](../notas/capitulos/), los puntos pertinentes de [`notas/NOTAS.md`](../notas/NOTAS.md) y las fichas aplicables en [`notas/fuentes/`](../notas/fuentes/). | En cada sesión de edición asistida (siempre **un capítulo a la vez** para mantener foco y bajo consumo de contexto). |
| **2. Solo consulta histórica** | [`SSOT/proceso_conversion_pdf_a_md.md`](proceso_conversion_pdf_a_md.md), [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](detalle_ejecucion_y_auditoria_conversion.md) y [`scripts/extraccion_v1/`](../scripts/extraccion_v1/). | **No cargar en sesiones normales.** Consultar únicamente si surge una duda sobre la extracción original del PDF de 2006 o sus métricas de auditoría. |
| **3. Intocables / solo lectura** | [`fuente/`](../fuente/), [`respaldo_v1.0/`](../respaldo_v1.0/), [`scripts/extraccion_v1/`](../scripts/extraccion_v1/) y [`externos/`](../externos/). | **Nunca editar, renombrar ni sobrescribir.** `externos/` se consulta únicamente mediante el índice local y las fichas de `notas/fuentes/` (sin cargar PDFs completos en memoria). |

---

## 2. Mapa de responsabilidades del repositorio (sin solapamientos)

* **[`AGENTS.md`](../AGENTS.md) y [`.agents/skills/`](../.agents/skills/):** Regla universal siempre activa del workspace y guías procedimentales modulares bajo demanda (`editar-capitulo`, `procesar-externos`, `cierre-editorial`).
* **[`libro/`](../libro/):** Única copia viva del texto publicable (sin anotaciones internas ni borradores); su índice navegable vive en [`libro/README.md`](../libro/README.md).
* **[`libro.yaml`](../libro.yaml):** Manifiesto maestro del orden de partes/capítulos y tablero de `estado` (`pendiente` | `en_revision` | `aprobado`) bajo la **Opción A** (los nombres actuales de `libro/` funcionan como IDs estables).
* **[`notas/`](../notas/):** Único espacio para **todo lo pendiente** ([`notas/NOTAS.md`](../notas/NOTAS.md), [`notas/mapa_obra.md`](../notas/mapa_obra.md), [`notas/capitulos/`](../notas/capitulos/) y [`notas/fuentes/`](../notas/fuentes/)).
* **[`externos/`](../externos/):** Biblioteca bibliográfica de consulta (solo lectura) con PDFs, artículos HTML y textos de apoyo para la 2.ª edición; se indexa localmente en `dist/indice_externos/` y se ficha en `notas/fuentes/`.
* **[`CHANGELOG.md`](../CHANGELOG.md):** Único registro de **hechos cerrados** (capítulos ya aprobados por el autor e hitos completados).
* **[`scripts/`](../scripts/):** Herramientas internas de edición (`scripts/edicion/`) y pipeline histórico congelado (`scripts/extraccion_v1/`); documentación completa y comandos en [`scripts/README.md`](../scripts/README.md).
* **[`respaldo_v1.0/`](../respaldo_v1.0/):** Respaldo inmutable de la 1.ª edición (2006) para comparaciones y compilación garantizada de `v1.0.0` ([`respaldo_v1.0/README.md`](../respaldo_v1.0/README.md)).
* **`dist/`:** Carpeta local ignorada por Git para entregas temporales (PDF/Word `.docx`), reportes comparativos y el índice reconstruible `dist/indice_externos/`; es desechable y puede limpiarse libremente.

---

## 3. Árbol Técnico del Repositorio e Inventario de `fuente/`

```text
critica-de-la-razon-mediatica/
├── README.md                  # Presentación pública general de la obra y del proyecto
├── AGENTS.md                  # Reglas universales del workspace, mapa y protocolo de mantenimiento
├── .agents/skills/            # Guías procedimentales modulares bajo demanda:
│   ├── editar-capitulo/       #   Flujo por capítulo (briefing, edición, validación, entrega y cierre)
│   ├── procesar-externos/     #   Indexación incremental, colofones y fichado de externos/
│   └── cierre-editorial/      #   Consolidación final (bibliografía, glosario, notas, índices)
├── CHANGELOG.md               # Bitácora editorial de capítulos aprobados e hitos completados
├── libro.yaml                 # Manifiesto maestro: orden del índice y estado por capítulo (Opción A)
├── .gitignore                 # Excluye dist/ (PDFs/DOCX/reportes/índice local) y temporales
├── externos/                  # [Solo lectura] Biblioteca bibliográfica de apoyo (PDF, HTML, TXT…)
├── fuente/                    # [Inmutable] Material original de la 1.ª edición (2006)
│   ├── Libro Crítica de La Razon Mediatica.pdf  # PDF maestro (21.08 MB, 666 págs. físicas / folios 2–699)
│   ├── FUENTES/               # Tipografías originales (.ttf): Garamond, Bauhaus93, AmigaForeverPro2, Swis721, Arial Black
│   ├── PORTADA/               # Artes originales de portada (.tif): repujado1, repujado2 y uv
│   └── RAZON/                 # Maquetación QuarkXPress (INICIAL.qxp, liminar.qxp, 1a–6a parte.qxp, POST-Escriptum.qxp, POSTERIOR.qxp),
│       ├── UBICACION DE liminar.txt             # nota editorial original de ubicación del Liminar
│       └── images/            # 14 portadillas gráficas separadoras (.tif / .jpg)
├── libro/                     # Única fuente viva de edición en Markdown (33 archivos base + libro/README.md)
├── notas/                     # NOTAS.md, mapa_obra.md, capitulos/ (33 + prefacio futuro), fuentes/ (catalogo.yaml + fichas) y README.md
├── respaldo_v1.0/             # [Inmutable] README.md, libro.yaml v1.0, manifiesto_v1.0.md (SHA-256) y md/ (33 archivos)
├── dist/                      # [Ignorado por Git] Entregas PDF/DOCX, reportes diff e índice local de externos/
├── scripts/                   # README.md + edicion/ (9 scripts activos) + extraccion_v1/ (3 scripts congelados)
└── SSOT/                      # Documentación rectora (este índice + 5 documentos normativos/históricos)
```

---

## 4. Documentos de este Directorio (`SSOT/`)

* **[`flujo_editorial_segunda_edicion.md`](flujo_editorial_segunda_edicion.md):** Flujo oficial simplificado de edición asistida capítulo por capítulo, incorporación de `externos/`, gestión de nuevos capítulos e índice en `libro.yaml`, y operación de `respaldo_v1.0/`.
* **[`guia_estilo_editorial.md`](guia_estilo_editorial.md):** Reglas de fidelidad estilística, vocabulario conceptual protegido, 6 decisiones editoriales confirmadas, citas europeas, política anti-alucinación y reglas de seguridad.
* **[`perfil_voz_autor.md`](perfil_voz_autor.md):** Referencia empírica de la cadencia ensayística del autor, anti-patrones a evitar e inventario completo de los 92 términos del Glosario.
* **[`proceso_conversion_pdf_a_md.md`](proceso_conversion_pdf_a_md.md):** *(Histórico)* Especificación técnica del Método 1 (2006) y política del respaldo inmutable `respaldo_v1.0/`.
* **[`detalle_ejecucion_y_auditoria_conversion.md`](detalle_ejecucion_y_auditoria_conversion.md):** *(Histórico)* Memoria técnica de la conversión ejecutada y tabla de auditoría contable al `100.000%` capítulo por capítulo.
