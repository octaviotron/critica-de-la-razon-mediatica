# Bitácora Editorial de Cambios (`CHANGELOG.md`)

Registro editorial de alto nivel por capítulo aprobado e hitos de ***Crítica de la Razón Mediática*** (Juan Barreto Cipriani). Las viñetas se listan en orden cronológico inverso y reflejan el estado al cierre de cada hito; los conteos y reglas vigentes siempre se consultan en [`AGENTS.md`](AGENTS.md) y [`libro.yaml`](libro.yaml).  
El detalle exacto de cambios contra 2006 puede consultarse en cualquier momento frente al respaldo inmutable [`respaldo_v1.0/`](respaldo_v1.0/).

---

## Segunda Edición — En proceso (`libro/`)

### Capítulos aprobados por el autor
* *(Ninguno aún — todos los capítulos en [`libro/`](libro/) se encuentran en su estado base de 2006, `estado: pendiente` en [`libro.yaml`](libro.yaml). Los pendientes de Glosario, Bibliografía, autores e índice se centralizan en [`notas/NOTAS.md`](notas/NOTAS.md).)*

### Arquitectura editorial
* Optimización de consumo de contexto entre sesiones: nuevo flag `--estado` en `scripts/edicion/contexto_capitulo.py` (excluyente con `--capitulo`), archivo local `notas/estado_sesion.md` ignorado por Git (`<= 2 KB`), aviso suave de tamaño en `scripts/edicion/validar_libro.py`, subsección de higiene de sesión en [`SSOT/flujo_editorial_segunda_edicion.md`](SSOT/flujo_editorial_segunda_edicion.md) (§2.2) y sincronización de [`AGENTS.md`](AGENTS.md), `SSOT/README.md`, `scripts/README.md`, `notas/README.md` y la Skill `editar-capitulo`.
* Incorporación del subsistema modular de maquetación editorial `LuaLaTeX` fiel al diseño de 2006: directorio [`maquetacion/`](maquetacion/) (`diseno_2ed.yaml` declarativo, plantillas `plantilla/libro_2ed.tex` y `plantilla/estilos_especiales.tex`, guías de `activos/` y `cubierta/`), scripts `scripts/edicion/compilar_maqueta.py` (modos `digital` e `imprenta`, compilación por capítulo o libro completo) y `scripts/edicion/recalcular_onomastico.py`, y guía rectora [`SSOT/guia_maquetacion_segunda_edicion.md`](SSOT/guia_maquetacion_segunda_edicion.md).
* Pulido integral de consistencia en arranque en frío: nueva 4.ª Skill [`.agents/skills/mantenimiento-proyecto/SKILL.md`](.agents/skills/mantenimiento-proyecto/SKILL.md), protocolo de arranque rápido y aligeramiento de [`AGENTS.md`](AGENTS.md), ejemplo práctico de integración híbrida en [`SSOT/guia_estilo_editorial.md`](SSOT/guia_estilo_editorial.md), banners históricos en los documentos de 2006 de `SSOT/`, verificación automática del tamaño de `AGENTS.md` y fichas espejo en `scripts/edicion/validar_libro.py`, soporte completo de los **93 términos** del Glosario (incluyendo `Habitus`) en `scripts/edicion/buscar_libro.py`, y requisitos del entorno en [`scripts/README.md`](scripts/README.md).
* Incorporación del nuevo anexo de cierre [`libro/anexo_cambios_segunda_edicion.md`](libro/anexo_cambios_segunda_edicion.md) (*Anexo editorial: Relación de cambios respecto a la Primera Edición (2006)*, `id: "A1"`, `tipo: "anexo"` en [`libro.yaml`](libro.yaml)) junto a su bitácora detallada [`notas/registro_cambios_edicion.md`](notas/registro_cambios_edicion.md) y ficha espejo [`notas/capitulos/anexo_cambios_segunda_edicion.md`](notas/capitulos/anexo_cambios_segunda_edicion.md), integrado en el flujo continuo de edición y cierre editorial.
* Reorganización estructural en [`libro.yaml`](libro.yaml) (de 8 a 10 secciones, manteniendo los nombres de archivo originales como IDs estables bajo la Opción A): integración del antiguo *Liminar* de Michel Maffesoli (`libro/03_liminar.md`, intercalado sin foliar fuera del índice en 2006) como **Pro(Logos) I** junto a `04`–`06` (`Pro(Logos)` II–IV) dentro de la sección `prologos_2006`, y creación de la sección `apertura` para alojar el futuro *Prefacio a la Segunda Edición* antes de `07_preambulo.md`.
* Reestructuración del [`README.md`](README.md) raíz para el público general, reubicando el detalle técnico y los comandos en [`scripts/README.md`](scripts/README.md) y el árbol/inventario técnico en [`SSOT/README.md`](SSOT/README.md).
* Creación de [`AGENTS.md`](AGENTS.md) como regla universal del workspace y de las 3 Skills modulares iniciales en [`.agents/skills/`](.agents/skills/) (`editar-capitulo`, `procesar-externos`, `cierre-editorial`; ampliado luego a 4 Skills con `mantenimiento-proyecto`), manteniendo la regla raíz liviana.
* Incorporación del sistema automático de bibliografía externa ([`externos/`](externos/) → [`notas/fuentes/`](notas/fuentes/) + índice SQLite FTS5 en `dist/indice_externos/corpus.db`) mediante `scripts/edicion/indexar_externos.py` y `scripts/edicion/buscar_externos.py`, con las primeras 12 fuentes indexadas y fichadas.
* Creación del mapa argumental condensado [`notas/mapa_obra.md`](notas/mapa_obra.md), la guía empírica de voz y el inventario inicial del Glosario [`SSOT/perfil_voz_autor.md`](SSOT/perfil_voz_autor.md) (`92` términos iniciales; ampliado luego a `93` con `Habitus`), el buscador interno `scripts/edicion/buscar_libro.py` y el briefing unificado `scripts/edicion/contexto_capitulo.py`.
* Endurecimiento de `scripts/edicion/validar_libro.py` (sintaxis PangoCairo, asteriscos impares, marcadores `[VERIFICAR/TODO/TBD]`, protección activa de textos invitados incluyendo la frontera `L101` en `29_post_scriptum.md` y verificación automática de `README.md`) y corrección de colisiones de notas al pie en compilación `.docx` multi-capítulo en `scripts/edicion/compilar_pdf.py`.
* Creación de la carpeta escalable [`notas/`](notas/) con [`notas/NOTAS.md`](notas/NOTAS.md) (ideas globales y autores por incorporar) y 33 fichas personalizadas en [`notas/capitulos/`](notas/capitulos/) con sugerencias basadas en el contenido de cada capítulo.
* Definición del flujo simplificado capítulo por capítulo: edición directa de cada `.md` en `libro/` con IA → revisión e iteración con el autor (entrega por capítulo en PDF o Word `.docx`) → aprobación en `libro.yaml` (`estado: aprobado`) → commit y push simple en `main`.
* Incorporación de [`SSOT/guia_estilo_editorial.md`](SSOT/guia_estilo_editorial.md) con las reglas de voz filosófica, vocabulario protegido y protocolo operativo por capítulo.
* Incorporación del manifiesto declarativo [`libro.yaml`](libro.yaml) (**Opción A**: nombres de archivo estables, orden flexible del índice y seguimiento de `estado` por capítulo).
* Creación del respaldo inmutable [`respaldo_v1.0/`](respaldo_v1.0/) con copia testigo de los 33 capítulos originales, manifiesto congelado (`respaldo_v1.0/libro.yaml`), huellas SHA-256 (`respaldo_v1.0/manifiesto_v1.0.md`) y guía propia (`respaldo_v1.0/README.md`).
* Separación de scripts en `scripts/extraccion_v1/` (pipeline histórico congelado de 2006, protegido contra sobrescritura) y `scripts/edicion/` (herramientas internas ejecutadas por la IA bajo demanda, con soporte por capítulo en PDF/DOCX).
* Exclusión de artefactos compilados en `dist/` mediante [`.gitignore`](.gitignore).

---

## Primera Edición (2006) — Base Digital Íntegra (`respaldo_v1.0/`)

### Extracción y verificación
* Extracción determinista desde `fuente/Libro Crítica de La Razon Mediatica.pdf` (666 páginas físicas) a 33 archivos Markdown en `libro/` y copia inmutable en `respaldo_v1.0/md/`.
* Depuración única de artefactos técnicos de conversión (sin cambios de contenido): corrección de formato/cortes de párrafo en 6 archivos (`09`, `10`, `11`, `13`, `20` y `28`) y recuperación de 27 enlaces/definiciones de notas al pie (`07`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `18` y `19`), sincronizada en `respaldo_v1.0/md/` con regeneración de huellas SHA-256 antes de iniciar ediciones de la 2.ª edición.
* Auditoría contable matemática al **100.000%**: `1,008,962 / 1,008,962` caracteres alfanuméricos, `197,690` palabras, `535` notas al pie enlazadas (`0` pérdidas, `0` mezclas entre capítulos).
