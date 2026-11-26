# Crítica de la Razón Mediática

> **Ensayos sobre biopolítica y potencia política del cuerpo**  
> *(Pre-textos para un debate por el socialismo)*

Repositorio oficial del proyecto de procesamiento digital, estructuración en formato Markdown y preparación de la **Segunda Edición** del libro ***Crítica de la Razón Mediática*** del autor **Juan Barreto Cipriani**.

---

## Créditos de la Obra y del Proyecto

### Autoría del Libro
* **Autor:** **Juan Barreto Cipriani**
* **Título original:** *Crítica de la Razón Mediática. Ensayos sobre biopolítica y potencia política del cuerpo (Pre-textos para un debate por el socialismo)*
* **Textos de apertura y ensayos invitados incluidos en la obra:**
  * **Liminar** (*La belleza con agudeza y rigor*): **Michel Maffesoli** (Profesor de la Universidad La Sorbona) — ver [`libro/03_liminar.md`](libro/03_liminar.md)
  * **Pro(Logos) I** (*Comunicación: El clímax de la era posmoderna*): **Rigoberto Lanz** — ver [`libro/04_prologo_1_rigoberto_lanz.md`](libro/04_prologo_1_rigoberto_lanz.md)
  * **Pro(Logos) II** (*Los nuevos mundos simbólicos*): **Nelson Guzmán** — ver [`libro/05_prologo_2_nelson_guzman.md`](libro/05_prologo_2_nelson_guzman.md)
  * **Pro(Logos) III** (*Trayectos claves para pensar el socialismo como pasión*): **Magaldy Téllez** — ver [`libro/06_prologo_3_magaldy_tellez.md`](libro/06_prologo_3_magaldy_tellez.md)
  * **Post-scriptum — Tercer movimiento** (*Entre dinosaurios y unicornios*): **Javier Biardeau** — ver [`libro/29_post_scriptum.md`](libro/29_post_scriptum.md)

### Datos Editoriales de la Primera Edición (2006)
* **Institución:** Universidad Central de Venezuela (UCV) — Centro de Investigaciones Post-Doctorales (CIPOST)
* **Diseño Gráfico:** Gustavo Velásquez Purroy
* **Impresión:** Publigráfica 66, C.A.
* **ISBN:** `980-12-1936-X`
* **Depósito Legal:** `lf25220060702192`
* **Lugar y año:** Distrito Metropolitano de Caracas, República Bolivariana de Venezuela, 2006 — ver [`libro/00_preliminares.md`](libro/00_preliminares.md)

### Asesoría Informática para la Segunda Edición
* **Asesor Informático:** **Octavio Rossell Tabet** <[octavio.rossell@gmail.com](mailto:octavio.rossell@gmail.com)> — [https://github.com/octaviotron](https://github.com/octaviotron)
  * *Rol:* Arquitectura de extracción documental sin pérdida, conversión automatizada a Markdown, diseño del flujo editorial simplificado de edición asistida capítulo por capítulo, manifiesto estructural declarativo (`libro.yaml`), respaldo inmutable de la primera edición (`respaldo_v1.0/`), auditoría de integridad textual y herramientas internas de validación y compilación editorial.

---

## Estructura del Proyecto

El repositorio está organizado alrededor de siete directorios versionados ([`externos/`](externos/), [`fuente/`](fuente/), [`libro/`](libro/), [`notas/`](notas/), [`respaldo_v1.0/`](respaldo_v1.0/), [`scripts/`](scripts/) y [`SSOT/`](SSOT/)), las reglas operativas del workspace [`AGENTS.md`](AGENTS.md) con sus guías modulares en [`.agents/skills/`](.agents/skills/), el manifiesto estructural y de avance [`libro.yaml`](libro.yaml), la bitácora [`CHANGELOG.md`](CHANGELOG.md) y una carpeta local `dist/` (ignorada por Git) para entregas compiladas (PDF o Word `.docx`) e índices locales de búsqueda.

```text
critica-de-la-razon-mediatica/
├── README.md                  # Documentación general, créditos, flujo editorial y resumen de la obra
├── AGENTS.md                  # Reglas universales del workspace, mapa completo y protocolo de mantenimiento
├── .agents/
│   └── skills/                # Guías procedimentales modulares bajo demanda (edición asistida)
│       ├── editar-capitulo/   # Flujo paso a paso para editar, validar, compilar y cerrar un capítulo
│       ├── procesar-externos/ # Procedimiento de indexación, fichado y mapeo de bibliografía en externos/
│       └── cierre-editorial/  # Guía final: bibliografía, glosario, notas, índice general y onomástico
├── CHANGELOG.md               # Bitácora editorial de capítulos aprobados e hitos completados
├── libro.yaml                 # Manifiesto maestro: orden flexible del índice y estado por capítulo (Opción A)
├── .gitignore                 # Excluye dist/ (PDFs/DOCX/reportes/índice local) y temporales
├── externos/                  # [Solo lectura] Biblioteca bibliográfica de apoyo para la 2.ª edición (PDF, HTML, TXT…)
├── fuente/                    # [Inmutable] Archivos originales de la 1.ª edición (PDF, QuarkXPress, fuentes, artes)
│   ├── Libro Crítica de La Razon Mediatica.pdf
│   ├── FUENTES/               # Fuentes tipográficas TrueType (.ttf) originales
│   ├── PORTADA/               # Artes originales de portada (.tif)
│   └── RAZON/                 # Maquetación QuarkXPress (.qxp/.qxb) y portadillas (.tif/.jpg)
│       └── images/            # Ilustraciones separadoras de cada parte y sección
├── libro/                     # Única fuente viva de edición en Markdown (se edita 1 capítulo .md a la vez)
│   ├── README.md              # Catálogo navegable detallado de todos los capítulos de la edición actual
│   └── *.md                   # Capítulos de la obra (33 iniciales como IDs estables)
├── notas/                     # Anotaciones de trabajo (ideas, autores, sugerencias, fuentes y notas del autor)
│   ├── README.md              # Guía breve de uso de la carpeta de anotaciones
│   ├── NOTAS.md               # Ideas globales del libro, autores por incluir, frases, glosario e índice
│   ├── mapa_obra.md           # Panorámica argumental condensada de los 33 capítulos y registro de 2.ª edición
│   ├── capitulos/             # Una ficha de notas y sugerencias por capítulo (mismo nombre que en libro/)
│   └── fuentes/               # Catálogo maestro (catalogo.yaml) y fichas curadas de la bibliografía en externos/
├── respaldo_v1.0/             # [Inmutable] Respaldo congelado de estructura y contenido inicial (1.ª edición 2006)
│   ├── README.md              # Guía, política de inmutabilidad y catálogo congelado con folios de 2006
│   ├── libro.yaml             # Manifiesto estructural congelado de la 1.ª edición (v1.0.0)
│   ├── manifiesto_v1.0.md     # Huellas criptográficas SHA-256 de los 33 archivos originales
│   └── md/                    # Copia testigo intacta de los 33 archivos .md originales
├── dist/                      # [Ignorado por Git] Entregas PDF/DOCX, reportes diff e índice local de externos/
├── scripts/
│   ├── extraccion_v1/         # [Congelado] Pipeline histórico de extracción y auditoría del PDF de 2006
│   │   ├── 01_extraer_xml.py
│   │   ├── 02_convertir_a_md.py
│   │   └── 03_auditar_integridad.py
│   └── edicion/               # [Herramientas internas] Ejecución asistida de scripts bajo demanda (sin uso manual diario)
│       ├── manifiesto.py      # Cargador compartido de libro.yaml y respaldo_v1.0/libro.yaml
│       ├── validar_libro.py   # Validación por capítulo o libro completo, tablero de avance y SHA-256
│       ├── compilar_pdf.py    # Compilador de un capítulo o libro completo a PDF o Word (.docx) en dist/
│       ├── reporte_cambios.py # Resumen comparativo por capítulo o libro completo contra respaldo_v1.0/
│       ├── generar_indice.py  # Regeneración automática de libro/01_indice.md desde libro.yaml
│       ├── indexar_externos.py # Indexador incremental de externos/ (SQLite FTS5 + notas/fuentes/catalogo.yaml)
│       ├── buscar_externos.py # Búsqueda de citas verificadas y lectura por rango de páginas en externos/
│       ├── buscar_libro.py    # Búsqueda interna sobre libro/, Glosario y Bibliografía por capítulo
│       └── contexto_capitulo.py # Briefing consolidado por capítulo (ficha, fuentes, diagnóstico y alertas)
└── SSOT/                      # Single Source of Truth (Índice, Especificación, Auditoría, Flujo, Estilo y Voz)
    ├── README.md              # Guía de inicio rápido y mapa de responsabilidades del repositorio
    ├── proceso_conversion_pdf_a_md.md
    ├── detalle_ejecucion_y_auditoria_conversion.md
    ├── flujo_editorial_segunda_edicion.md
    ├── guia_estilo_editorial.md
    └── perfil_voz_autor.md    # Referencia empírica de cadencia del autor e inventario de 92 términos del Glosario
```

### Descripción y Vínculos a las Carpetas Principales

1. **[`fuente/`](fuente/) — Material Fuente de la Primera Edición (Inmutable):**
   * **[`fuente/Libro Crítica de La Razon Mediatica.pdf`](<fuente/Libro Crítica de La Razon Mediatica.pdf>):** Documento PDF maestro de la primera edición (`21.08 MB`, `666` páginas físicas, numeración impresa hasta la pág. `699`).
   * **[`fuente/FUENTES/`](fuente/FUENTES/):** Tipografías empleadas en la edición original (`Garamond`, `Bauhaus93`, `AmigaForeverPro2`, `Swis721`, `Arial Black`).
   * **[`fuente/PORTADA/`](fuente/PORTADA/):** Archivos `.tif` de arte de portada (`PORTADA repujado1.tif`, `PORTADA repujado2.tif`, `PORTADA uv.tif`).
   * **[`fuente/RAZON/`](fuente/RAZON/):** Documentos nativos de maquetación en QuarkXPress (`INICIAL.qxp`, `liminar.qxp`, `1a PARTE.qxp` a `6a parte.qxp`, `POST-Escriptum.qxp`, `POSTERIOR.qxp`), nota editorial [`UBICACION DE liminar.txt`](<fuente/RAZON/UBICACION DE liminar.txt>) y subcarpeta **[`fuente/RAZON/images/`](fuente/RAZON/images/)** con las 14 portadillas gráficas separadoras.
2. **[`libro/`](libro/) y [`libro.yaml`](libro.yaml) — Manuscrito Vivo de la Segunda Edición (Opción A):**
   * [`libro/`](libro/) aloja los **33 archivos Markdown** iniciales extraídos con **100% de integridad textual** (`197,690` palabras, `535` notas al pie y `1,008,962` caracteres alfanuméricos) y se trabaja mediante **edición asistida capítulo por capítulo** (un archivo `.md` a la vez). Su índice detallado de archivos vive en **[`libro/README.md`](libro/README.md)**.
   * [`libro.yaml`](libro.yaml) gobierna el orden de lectura, la agrupación en partes y el `estado` de avance de cada capítulo (`pendiente` | `en_revision` | `aprobado`). Los nombres actuales en `libro/` permanecen como **IDs estables**; cualquier capítulo nuevo o reordenamiento futuro del índice se declara únicamente en `libro.yaml`.
3. **[`notas/`](notas/) — Anotaciones Editoriales, Autores, Fuentes e Ideas por Desarrollar:**
   * **[`notas/NOTAS.md`](notas/NOTAS.md):** Bandeja global con ideas transversales, lista de autores por incorporar, frases para ampliar, términos candidatos para el Glosario y propuestas sobre el índice.
   * **[`notas/capitulos/`](notas/capitulos/):** Una ficha independiente por cada capítulo (con el mismo nombre de archivo que en `libro/`), incluyendo sugerencias basadas en su contenido, erratas técnicas heredadas de 2006 y espacio para las observaciones del autor.
   * **[`notas/fuentes/`](notas/fuentes/):** Catálogo bibliográfico maestro ([`catalogo.yaml`](notas/fuentes/catalogo.yaml)) y fichas de lectura curadas para los documentos depositados en [`externos/`](externos/).
   * **[`notas/README.md`](notas/README.md):** Convención rápida de uso con casillas de seguimiento (`- [ ]` / `- [x]`), manteniendo `libro/` limpio de notas internas.
4. **[`externos/`](externos/) — Biblioteca Bibliográfica de Apoyo (Solo Lectura):**
   * Aloja PDFs, artículos HTML, textos y documentos de referencia para la Segunda Edición. Se indexa localmente en `dist/indice_externos/` mediante ejecución asistida de scripts y se documenta en [`notas/fuentes/`](notas/fuentes/).
5. **[`respaldo_v1.0/`](respaldo_v1.0/) — Respaldo Inmutable de Estructura y Contenido Inicial (2006):**
   * **[`respaldo_v1.0/README.md`](respaldo_v1.0/README.md):** Política de inmutabilidad y comandos para auditar o compilar la Primera Edición.
   * **[`respaldo_v1.0/libro.yaml`](respaldo_v1.0/libro.yaml):** Manifiesto estructural congelado de la 1.ª edición (`v1.0.0`), independiente de [`libro.yaml`](libro.yaml).
   * **[`respaldo_v1.0/manifiesto_v1.0.md`](respaldo_v1.0/manifiesto_v1.0.md):** Huellas criptográficas SHA-256 de los 33 archivos originales.
   * **[`respaldo_v1.0/md/`](respaldo_v1.0/md/):** Copia testigo intacta de los 33 capítulos de 2006, que permite **compilar siempre la primera versión (`v1.0.0`)** aunque cambien los archivos dentro de [`libro/`](libro/).
6. **[`scripts/`](scripts/) — Herramientas Internas de Edición y Pipeline Histórico:**
   * **`scripts/edicion/` (ejecución asistida de scripts bajo demanda):**
     * **[`scripts/edicion/manifiesto.py`](scripts/edicion/manifiesto.py):** Cargador compartido para `libro.yaml` y `respaldo_v1.0/libro.yaml`.
     * **[`scripts/edicion/validar_libro.py`](scripts/edicion/validar_libro.py):** Valida un capítulo (`--capitulo`) o el libro completo (notas al pie, enlaces locales, tablero de `estado` y SHA-256 de `respaldo_v1.0/md/` con `--verificar-respaldo`).
     * **[`scripts/edicion/compilar_pdf.py`](scripts/edicion/compilar_pdf.py):** Compila un único capítulo (`--capitulo`) o el libro completo en `dist/` en formato **PDF** o **Word (`.docx`)** (`--formato docx`), tanto desde `libro.yaml` como desde `respaldo_v1.0/libro.yaml`.
     * **[`scripts/edicion/reporte_cambios.py`](scripts/edicion/reporte_cambios.py):** Genera en `dist/` un reporte comparativo de un capítulo (`--capitulo`) o del libro completo contra `respaldo_v1.0/`.
     * **[`scripts/edicion/generar_indice.py`](scripts/edicion/generar_indice.py):** Regenera `libro/01_indice.md` automáticamente desde `libro.yaml` y los encabezados reales cuando cambie el índice o al cierre editorial.
     * **[`scripts/edicion/indexar_externos.py`](scripts/edicion/indexar_externos.py):** Indexa incrementalmente (por SHA-256) los archivos de `externos/` en un índice local SQLite FTS5 (`dist/indice_externos/corpus.db`) y sincroniza [`notas/fuentes/catalogo.yaml`](notas/fuentes/catalogo.yaml).
     * **[`scripts/edicion/buscar_externos.py`](scripts/edicion/buscar_externos.py):** Busca fragmentos literales con número de página exacto, lee rangos específicos de páginas y lista fuentes asignadas por capítulo con auto-sincronización silenciosa.
     * **[`scripts/edicion/buscar_libro.py`](scripts/edicion/buscar_libro.py):** Búsqueda interna insensible a tildes sobre `libro/`, el Glosario (`--glosario`) y la Bibliografía (`--bibliografia`) con distribución de ocurrencias por capítulo.
     * **[`scripts/edicion/contexto_capitulo.py`](scripts/edicion/contexto_capitulo.py):** Consolida en una sola salida el briefing de un capítulo (metadatos, ficha espejo, fuentes externas, diagnóstico técnico y alertas de textos protegidos).
   * **`scripts/extraccion_v1/` (pipeline histórico congelado de 2006):**
     * **[`scripts/extraccion_v1/01_extraer_xml.py`](scripts/extraccion_v1/01_extraer_xml.py):** Extrae la capa vectorial XML de las 666 páginas del PDF mediante `pdftohtml -xml -i` y filtra determinísticamente el ruido de QuarkXPress.
     * **[`scripts/extraccion_v1/02_convertir_a_md.py`](scripts/extraccion_v1/02_convertir_a_md.py):** Reconstruye los 33 archivos Markdown (protegido: escribe por defecto en `dist/extraccion_v1_md/` y bloquea sobrescrituras accidentales sobre `respaldo_v1.0/` o `libro/`).
     * **[`scripts/extraccion_v1/03_auditar_integridad.py`](scripts/extraccion_v1/03_auditar_integridad.py):** Ejecuta la auditoría contable al 100.000% contra el PDF original (por defecto sobre `respaldo_v1.0/md/`).
7. **[`SSOT/`](SSOT/) — *Single Source of Truth* (Documentación de Proceso, Auditoría, Flujo y Estilo):**
   * **[`SSOT/flujo_editorial_segunda_edicion.md`](SSOT/flujo_editorial_segunda_edicion.md):** Flujo oficial simplificado de edición asistida capítulo por capítulo, revisión/aprobación del autor, gestión de nuevos capítulos e índice en `libro.yaml`, y operación de `respaldo_v1.0/`.
   * **[`SSOT/guia_estilo_editorial.md`](SSOT/guia_estilo_editorial.md):** Reglas de fidelidad estilística, vocabulario filosófico protegido y protocolo operativo de edición asistida por capítulo.
   * **[`SSOT/perfil_voz_autor.md`](SSOT/perfil_voz_autor.md):** Referencia empírica de cadencia ensayística del autor, anti-patrones a evitar e inventario completo de los 92 términos del Glosario.
   * **[`SSOT/proceso_conversion_pdf_a_md.md`](SSOT/proceso_conversion_pdf_a_md.md):** Especificación técnica histórica del Método 1 (2006) y política del respaldo inmutable `respaldo_v1.0/`.
   * **[`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md):** Memoria técnica de la conversión ejecutada y tabla de auditoría contable capítulo por capítulo.
8. **[`AGENTS.md`](AGENTS.md) y [`.agents/skills/`](.agents/skills/) — Reglas del Workspace y Skills Procedimentales Modulares:**
   * **[`AGENTS.md`](AGENTS.md):** Punto de entrada universal con el mapa completo del repositorio, las reglas inviolables, las decisiones editoriales cerradas, el catálogo de herramientas internas y el protocolo de sincronización ante cambios estructurales.
   * **[`.agents/skills/`](.agents/skills/):** Guías operativas modulares de carga bajo demanda que encapsulan los procedimientos paso a paso sin sobrecargar la regla raíz:
     * **[`editar-capitulo/SKILL.md`](.agents/skills/editar-capitulo/SKILL.md):** Procedimiento completo por capítulo (briefing, edición híbrida, validación, compilación de entrega en PDF y cierre tras aprobación).
     * **[`procesar-externos/SKILL.md`](.agents/skills/procesar-externos/SKILL.md):** Procedimiento automático de indexación incremental, verificación de colofones, curado de `notas/fuentes/catalogo.yaml` y fichado cuando se añade bibliografía en `externos/`.
     * **[`cierre-editorial/SKILL.md`](.agents/skills/cierre-editorial/SKILL.md):** Guía exclusiva para la fase final (renumeración de notas, consolidación de Bibliografía y Glosario, saneamiento de encabezados, regeneración del Índice General y actualización del Índice Onomástico).

---

## Resumen de la Estructura del Libro

La obra se organiza en **8 grandes bloques** (33 archivos `.md` iniciales):

| Bloque | Contenido principal | Capítulos base |
| :--- | :--- | :---: |
| **Preliminares y Apertura** | Créditos, Índice, Agradecimientos, *Liminar* (M. Maffesoli), *Pro(Logos)* I–III y *Preámbulo* | `00` – `07` |
| **Primera Parte** | *Aproximación a una caja de herramientas* (Ensayos I–III) | `08` – `10` |
| **Segunda Parte** | *Cultura(s), campos y massmediática* (Ensayos I–III) | `11` – `13` |
| **Tercera Parte** | *Una visión del significante-signo y del lenguaje* (Ensayos I–III) | `14` – `16` |
| **Cuarta Parte** | *Subjetividad, dispositivos y mass-media* (Ensayos I–IV) | `17` – `20` |
| **Quinta Parte** | *De la opinión pública a las democracias mass-mediáticas* (Ensayos I–IV) | `21` – `24` |
| **Sexta Parte** | *La apuesta por la distopía de las multitudes: hacia una refundación de la política* (Ensayos I–III) | `25` – `27` |
| **Cierre y Aparato Crítico** | *Epílogo*, *Post-scriptum* (con ensayo de J. Biardeau), Bibliografía, Glosario e Índice Onomástico | `28` – `32` |

### Dónde consultar el listado detallado de capítulos (`.md`)
* **Edición actual en proceso (y futuras modificaciones):** [`libro/README.md`](libro/README.md) (catálogo navegable vivo) y [`libro.yaml`](libro.yaml) (orden maestro y estado de avance por capítulo).
* **Primera Edición inmutable (2006):** [`respaldo_v1.0/README.md`](respaldo_v1.0/README.md) (catálogo congelado con folios impresos y páginas PDF originales) y [`respaldo_v1.0/libro.yaml`](respaldo_v1.0/libro.yaml).

---

## Flujo Editorial de la Segunda Edición

El proceso está diseñado para **reducir al mínimo los comandos manuales** y centrarse exclusivamente en la edición asistida de los capítulos `.md` de [`libro/`](libro/):

1. **Elegir un capítulo `.md`** en [`libro/`](libro/), revisar sus anotaciones en [`notas/capitulos/`](notas/capitulos/) (y [`notas/NOTAS.md`](notas/NOTAS.md)) y actualizarlo mediante edición asistida siguiendo [`SSOT/guia_estilo_editorial.md`](SSOT/guia_estilo_editorial.md).
2. **Entregar ese capítulo al autor:** Mediante ejecución asistida de scripts, se valida el archivo, se compila solo ese capítulo en PDF o Word (`.docx`) dentro de `dist/` y se prepara un resumen breve de los cambios realizados.
3. **Iterar hasta aprobación:** Se aplican sobre el mismo `.md` las orientaciones del autor hasta obtener su visto bueno.
4. **Cerrar capítulo y avanzar:** Se marca `estado: "aprobado"` en [`libro.yaml`](libro.yaml), se anota en [`CHANGELOG.md`](CHANGELOG.md), se hace un commit + push simple en `main` y se pasa al siguiente `.md`.
5. **Nuevos capítulos o cambios de índice (a futuro):** Los capítulos nuevos se añaden en `libro/` y se declaran en `libro.yaml`; si cambia el orden de las partes o ensayos, solo se reordena `libro.yaml` y se regenera automáticamente `libro/01_indice.md`.

### Referencia de Scripts Internos (ejecución asistida bajo demanda o uso manual)

```bash
# Validar un capítulo recién editado (o sin --capitulo para ver el avance global y verificar respaldo_v1.0/)
python3 -B scripts/edicion/validar_libro.py --capitulo 19
python3 -B scripts/edicion/validar_libro.py --verificar-respaldo

# Generar entrega solo de un capítulo para revisión del autor (PDF o Word .docx) en dist/
python3 -B scripts/edicion/compilar_pdf.py --capitulo 19
python3 -B scripts/edicion/compilar_pdf.py --capitulo 19 --formato docx

# Generar resumen de cambios de un capítulo contra 2006 (respaldo_v1.0/)
python3 -B scripts/edicion/reporte_cambios.py --capitulo 19 --incluir-diffs

# Compilar el libro completo actual (2.ª edición) o regenerar el índice desde libro.yaml
python3 -B scripts/edicion/compilar_pdf.py
python3 -B scripts/edicion/generar_indice.py --escribir
```

### Compilar y Auditar Siempre la Primera Edición (`respaldo_v1.0/`)

Aunque los archivos de [`libro/`](libro/) o [`libro.yaml`](libro.yaml) cambien por completo, siempre es posible compilar y verificar la 1.ª edición intacta:

```bash
# Compilar el PDF completo de la 1.ª edición (v1.0.0) en dist/
python3 -B scripts/edicion/compilar_pdf.py --manifiesto respaldo_v1.0/libro.yaml

# Auditar al 100.000% respaldo_v1.0/md/ contra el PDF maestro de 2006
python3 -B scripts/extraccion_v1/03_auditar_integridad.py
```

Para consultar la especificación completa del proyecto, véanse:
* [`SSOT/flujo_editorial_segunda_edicion.md`](SSOT/flujo_editorial_segunda_edicion.md)
* [`SSOT/guia_estilo_editorial.md`](SSOT/guia_estilo_editorial.md)
* [`SSOT/proceso_conversion_pdf_a_md.md`](SSOT/proceso_conversion_pdf_a_md.md)
* [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md)
* [`respaldo_v1.0/README.md`](respaldo_v1.0/README.md)
