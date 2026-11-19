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
  * *Rol:* Arquitectura de extracción documental sin pérdida, conversión automatizada a Markdown, diseño del flujo editorial simplificado capítulo por capítulo asistido por IA, manifiesto estructural declarativo (`libro.yaml`), respaldo inmutable de la primera edición (`respaldo_v1.0/`), auditoría de integridad textual y herramientas internas de validación y compilación editorial.

---

## Estructura del Proyecto

El repositorio está organizado alrededor de cinco directorios versionados ([`fuente/`](fuente/), [`libro/`](libro/), [`respaldo_v1.0/`](respaldo_v1.0/), [`scripts/`](scripts/) y [`SSOT/`](SSOT/)), el manifiesto estructural y de avance [`libro.yaml`](libro.yaml), la bitácora [`CHANGELOG.md`](CHANGELOG.md) y una carpeta local `dist/` (ignorada por Git) para entregas compiladas (PDF o Word `.docx`).

```text
critica-de-la-razon-mediatica/
├── README.md                  # Documentación general, créditos, flujo editorial e índice navegable
├── CHANGELOG.md               # Bitácora editorial de capítulos aprobados y pendientes para el cierre
├── libro.yaml                 # Manifiesto maestro: orden flexible del índice y estado por capítulo (Opción A)
├── .gitignore                 # Excluye dist/ (PDFs/DOCX/reportes compilados) y temporales
├── fuente/                    # [Inmutable] Archivos originales de la 1.ª edición (PDF, QuarkXPress, fuentes, artes)
│   ├── Libro Crítica de La Razon Mediatica.pdf
│   ├── FUENTES/               # Fuentes tipográficas TrueType (.ttf) originales
│   ├── PORTADA/               # Artes originales de portada (.tif)
│   └── RAZON/                 # Maquetación QuarkXPress (.qxp/.qxb) y portadillas (.tif/.jpg)
│       └── images/            # Ilustraciones separadoras de cada parte y sección
├── libro/                     # Única fuente viva de edición en Markdown (se edita 1 capítulo .md a la vez)
├── respaldo_v1.0/             # [Inmutable] Respaldo congelado de estructura y contenido inicial (1.ª edición 2006)
│   ├── README.md              # Documentación, reglas de inmutabilidad y comandos para compilar v1.0.0
│   ├── libro.yaml             # Manifiesto estructural congelado de la 1.ª edición (v1.0.0)
│   ├── manifiesto_v1.0.md     # Huellas criptográficas SHA-256 de los 33 archivos originales
│   └── md/                    # Copia testigo intacta de los 33 archivos .md originales
├── dist/                      # [Ignorado por Git] Entregas PDF/DOCX por capítulo o libro completo y reportes diff
├── scripts/
│   ├── extraccion_v1/         # [Congelado] Pipeline histórico de extracción y auditoría del PDF de 2006
│   │   ├── 01_extraer_xml.py
│   │   ├── 02_convertir_a_md.py
│   │   └── 03_auditar_integridad.py
│   └── edicion/               # [Herramientas internas] Ejecutadas por la IA bajo demanda (sin uso manual diario)
│       ├── manifiesto.py      # Cargador compartido de libro.yaml y respaldo_v1.0/libro.yaml
│       ├── validar_libro.py   # Validación por capítulo o libro completo, tablero de avance y SHA-256
│       ├── compilar_pdf.py    # Compilador de un capítulo o libro completo a PDF o Word (.docx) en dist/
│       ├── reporte_cambios.py # Resumen comparativo por capítulo o libro completo contra respaldo_v1.0/
│       └── generar_indice.py  # Regeneración automática de libro/01_indice.md desde libro.yaml
└── SSOT/                      # Single Source of Truth (Especificación, Auditoría, Flujo y Guía de Estilo IA)
    ├── proceso_conversion_pdf_a_md.md
    ├── detalle_ejecucion_y_auditoria_conversion.md
    ├── flujo_editorial_segunda_edicion.md
    └── guia_estilo_ia.md
```

### Descripción y Vínculos a las Carpetas Principales

1. **[`fuente/`](fuente/) — Material Fuente de la Primera Edición (Inmutable):**
   * **[`fuente/Libro Crítica de La Razon Mediatica.pdf`](<fuente/Libro Crítica de La Razon Mediatica.pdf>):** Documento PDF maestro de la primera edición (`21.08 MB`, `666` páginas físicas, numeración impresa hasta la pág. `699`).
   * **[`fuente/FUENTES/`](fuente/FUENTES/):** Tipografías empleadas en la edición original (`Garamond`, `Bauhaus93`, `AmigaForeverPro2`, `Swis721`, `Arial Black`).
   * **[`fuente/PORTADA/`](fuente/PORTADA/):** Archivos `.tif` de arte de portada (`PORTADA repujado1.tif`, `PORTADA repujado2.tif`, `PORTADA uv.tif`).
   * **[`fuente/RAZON/`](fuente/RAZON/):** Documentos nativos de maquetación en QuarkXPress (`INICIAL.qxp`, `liminar.qxp`, `1a PARTE.qxp` a `6a parte.qxp`, `POST-Escriptum.qxp`, `POSTERIOR.qxp`), nota editorial [`UBICACION DE liminar.txt`](<fuente/RAZON/UBICACION DE liminar.txt>) y subcarpeta **[`fuente/RAZON/images/`](fuente/RAZON/images/)** con las 14 portadillas gráficas separadoras.
2. **[`libro/`](libro/) y [`libro.yaml`](libro.yaml) — Manuscrito Vivo de la Segunda Edición (Opción A):**
   * [`libro/`](libro/) aloja los **33 archivos Markdown** iniciales extraídos con **100% de integridad textual** (`197,741` palabras, `513` notas al pie y `1,008,962` caracteres alfanuméricos) y se edita directamente **un capítulo `.md` a la vez** con asistencia de IA.
   * [`libro.yaml`](libro.yaml) gobierna el orden de lectura, la agrupación en partes y el `estado` de avance de cada capítulo (`pendiente` | `en_revision` | `aprobado`). Los nombres actuales en `libro/` permanecen como **IDs estables**; cualquier capítulo nuevo o reordenamiento futuro del índice se declara únicamente en `libro.yaml`.
3. **[`respaldo_v1.0/`](respaldo_v1.0/) — Respaldo Inmutable de Estructura y Contenido Inicial (2006):**
   * **[`respaldo_v1.0/README.md`](respaldo_v1.0/README.md):** Política de inmutabilidad y comandos para auditar o compilar la Primera Edición.
   * **[`respaldo_v1.0/libro.yaml`](respaldo_v1.0/libro.yaml):** Manifiesto estructural congelado de la 1.ª edición (`v1.0.0`), independiente de [`libro.yaml`](libro.yaml).
   * **[`respaldo_v1.0/manifiesto_v1.0.md`](respaldo_v1.0/manifiesto_v1.0.md):** Huellas criptográficas SHA-256 de los 33 archivos originales.
   * **[`respaldo_v1.0/md/`](respaldo_v1.0/md/):** Copia testigo intacta de los 33 capítulos de 2006, que permite **compilar siempre la primera versión (`v1.0.0`)** aunque cambien los archivos dentro de [`libro/`](libro/).
4. **[`scripts/`](scripts/) — Herramientas Internas de Edición y Pipeline Histórico:**
   * **`scripts/edicion/` (herramientas ejecutadas por la IA bajo demanda):**
     * **[`scripts/edicion/manifiesto.py`](scripts/edicion/manifiesto.py):** Cargador compartido para `libro.yaml` y `respaldo_v1.0/libro.yaml`.
     * **[`scripts/edicion/validar_libro.py`](scripts/edicion/validar_libro.py):** Valida un capítulo (`--capitulo`) o el libro completo (notas al pie, enlaces locales, tablero de `estado` y SHA-256 de `respaldo_v1.0/md/` con `--verificar-respaldo`).
     * **[`scripts/edicion/compilar_pdf.py`](scripts/edicion/compilar_pdf.py):** Compila un único capítulo (`--capitulo`) o el libro completo en `dist/` en formato **PDF** o **Word (`.docx`)** (`--formato docx`), tanto desde `libro.yaml` como desde `respaldo_v1.0/libro.yaml`.
     * **[`scripts/edicion/reporte_cambios.py`](scripts/edicion/reporte_cambios.py):** Genera en `dist/` un reporte comparativo de un capítulo (`--capitulo`) o del libro completo contra `respaldo_v1.0/`.
     * **[`scripts/edicion/generar_indice.py`](scripts/edicion/generar_indice.py):** Regenera `libro/01_indice.md` automáticamente desde `libro.yaml` y los encabezados reales cuando cambie el índice o al cierre editorial.
   * **`scripts/extraccion_v1/` (pipeline histórico congelado de 2006):**
     * **[`scripts/extraccion_v1/01_extraer_xml.py`](scripts/extraccion_v1/01_extraer_xml.py):** Extrae la capa vectorial XML de las 666 páginas del PDF mediante `pdftohtml -xml -i` y filtra determinísticamente el ruido de QuarkXPress.
     * **[`scripts/extraccion_v1/02_convertir_a_md.py`](scripts/extraccion_v1/02_convertir_a_md.py):** Reconstruye los 33 archivos Markdown (protegido: escribe por defecto en `dist/extraccion_v1_md/` y bloquea sobrescrituras accidentales sobre `respaldo_v1.0/` o `libro/`).
     * **[`scripts/extraccion_v1/03_auditar_integridad.py`](scripts/extraccion_v1/03_auditar_integridad.py):** Ejecuta la auditoría contable al 100.000% contra el PDF original (por defecto sobre `respaldo_v1.0/md/`).
5. **[`SSOT/`](SSOT/) — *Single Source of Truth* (Documentación de Proceso, Auditoría, Flujo y Estilo):**
   * **[`SSOT/flujo_editorial_segunda_edicion.md`](SSOT/flujo_editorial_segunda_edicion.md):** Flujo oficial simplificado capítulo por capítulo con IA, revisión/aprobación del autor, gestión de nuevos capítulos e índice en `libro.yaml`, y operación de `respaldo_v1.0/`.
   * **[`SSOT/guia_estilo_ia.md`](SSOT/guia_estilo_ia.md):** Reglas de fidelidad estilística, vocabulario filosófico protegido y protocolo operativo que la IA sigue en cada capítulo.
   * **[`SSOT/proceso_conversion_pdf_a_md.md`](SSOT/proceso_conversion_pdf_a_md.md):** Especificación técnica histórica del Método 1 (2006) y política del respaldo inmutable `respaldo_v1.0/`.
   * **[`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md):** Memoria técnica de la conversión ejecutada y tabla de auditoría contable capítulo por capítulo.

---

## Estructura del Libro y Vínculos a Cada Parte y Capítulo ([`libro/`](libro/))

A continuación se presenta la estructura completa de la obra con acceso directo a cada uno de los **33 archivos Markdown** alojados en [`libro/`](libro/):

### Preliminares, Índice, Prólogos y Preámbulo
* **[`00_preliminares.md`](libro/00_preliminares.md)** — Créditos editoriales, Portadilla interior y Epígrafe general (*G. Deleuze y F. Guattari*) | *Págs. impresas 2–5 (PDF 2–4)*
* **[`01_indice.md`](libro/01_indice.md)** — **Índice General de la Obra** | *Págs. impresas 7–10 (PDF 5–8)*
* **[`02_agradecimientos.md`](libro/02_agradecimientos.md)** — **Agradecimientos** | *Págs. impresas 11–12 (PDF 9–10)*
* **[`03_liminar.md`](libro/03_liminar.md)** — **Liminar:** *La belleza con agudeza y rigor* — **Michel Maffesoli** | *Págs. s/n 1–5 (PDF 12–14)*
* **PRO(LOGOS):**
  * **[`04_prologo_1_rigoberto_lanz.md`](libro/04_prologo_1_rigoberto_lanz.md)** — *Comunicación: El clímax de la era posmoderna* — **Rigoberto Lanz** | *Págs. impresas 15–23 (PDF 16–23)*
  * **[`05_prologo_2_nelson_guzman.md`](libro/05_prologo_2_nelson_guzman.md)** — *Los nuevos mundos simbólicos* — **Nelson Guzmán** | *Págs. impresas 25–31 (PDF 24–30)*
  * **[`06_prologo_3_magaldy_tellez.md`](libro/06_prologo_3_magaldy_tellez.md)** — *Trayectos claves para pensar el socialismo como pasión* — **Magaldy Téllez** | *Págs. impresas 33–41 (PDF 31–38)*
* **[`07_preambulo.md`](libro/07_preambulo.md)** — **Un intento para hacerse cargo de la massmediática. A modo de preámbulo** | *Págs. impresas 43–84 (PDF 40–81)*
  * *Incluye:* Profecías y realidades tecnológicas · La era de las conexiones · Las urgencias de la teoría · Cuestión de Método: La aventura de hablar y escribir sobre lo múltiple (O cómo dar con el problema) · El drama de la escritura (El cómo de la forma o estilo) · Algo sobre nosotros mismos.

---

### Primera Parte: Aproximación a una caja de herramientas
* **[`08_parte1_ensayo_1.md`](libro/08_parte1_ensayo_1.md)** — **Portadilla Primera Parte + Ensayo I:** *Crisis de la teoría del valor y nuevo dispositivo información-comunicación* | *Págs. impresas 87–109 (PDF 83–105)*
* **[`09_parte1_ensayo_2.md`](libro/09_parte1_ensayo_2.md)** — **Ensayo II:** *Un ejercicio sobre materia oscura y agujeros negros, virus y ADN* | *Págs. impresas 111–121 (PDF 106–117)*
* **[`10_parte1_ensayo_3.md`](libro/10_parte1_ensayo_3.md)** — **Ensayo III:** *Un acercamiento crítico a las tradiciones teóricas en el campo de la comunicación* | *Págs. impresas 123–174 (PDF 118–169)*
  * *Incluye:* La Escuela de Frankfurt y sus críticos · Masas e Industria · La ilusión como performativo · El espíritu americano · Influencia, inoculación y efectos · Problema de modelos · Otros aportes · Tendencias y aportes desde América Latina.

---

### Segunda Parte: Cultura(s), campos y massmediática
* **[`11_parte2_ensayo_1.md`](libro/11_parte2_ensayo_1.md)** — **Portadilla Segunda Parte + Ensayo I:** *Campos híbridos y lecturas transversales* | *Págs. impresas 177–193 (PDF 171–186)*
* **[`12_parte2_ensayo_2.md`](libro/12_parte2_ensayo_2.md)** — **Ensayo II:** *¿Una teoría lingüística del valor?* | *Págs. impresas 195–209 (PDF 187–201)*
  * *Incluye:* Las interacciones lingüísticas como soporte de relaciones de poder simbólico · Poder oblicuo y metafórico.
* **[`13_parte2_ensayo_3.md`](libro/13_parte2_ensayo_3.md)** — **Ensayo III:** *Una incursión en la estética* | *Págs. impresas 211–229 (PDF 202–220)*
  * *Incluye:* Una estética · Pérdida o extravío del aura.

---

### Tercera Parte: Una visión del significante-signo y del lenguaje
* **[`14_parte3_ensayo_1.md`](libro/14_parte3_ensayo_1.md)** — **Portadilla Tercera Parte + Ensayo I:** *Caminos de la semiótica* | *Págs. impresas 233–258 (PDF 222–246)*
  * *Incluye:* La implicación significante-signo-sentido-lenguaje · El significante-signo como pliegue · La construcción simbólica · Lenguaje y hegemonía · El sentido como performativo.
* **[`15_parte3_ensayo_2.md`](libro/15_parte3_ensayo_2.md)** — **Ensayo II:** *Los fantasmas del sentido: en el giro hermenéutico de la semiótica* | *Págs. impresas 259–278 (PDF 247–266)*
  * *Incluye:* Hermenéutica y reconstrucción · Hermes, el ladrón · Por una semiótica hermenéutica · Una aproximación a la opacidad.
* **[`16_parte3_ensayo_3.md`](libro/16_parte3_ensayo_3.md)** — **Ensayo III:** *El mito: pasaje narrativo del significante-signo al símbolo* | *Págs. impresas 279–295 (PDF 267–283)*
  * *Incluye:* Simbolizar: ¿una tarea del lenguaje? · La interpretación, o la comprensión de un significante-signo que se hace símbolo · El mito como agenciamiento · El sentido fuera del sentido.

---

### Cuarta Parte: Subjetividad, dispositivos y mass-media
* **[`17_parte4_ensayo_1.md`](libro/17_parte4_ensayo_1.md)** — **Portadilla Cuarta Parte + Ensayo I:** *Massmediática y construcción de subjetividad* | *Págs. impresas 299–321 (PDF 285–306)*
  * *Incluye:* La subjetividad: heterogénesis descentrada del sujeto · Massmediática: una lógica de sentido.
* **[`18_parte4_ensayo_2.md`](libro/18_parte4_ensayo_2.md)** — **Ensayo II:** *La subjetividad massmediática* | *Págs. impresas 323–341 (PDF 307–325)*
  * *Incluye:* Las marcas de los signos massmediáticos · Entre operadores y operaciones.
* **[`19_parte4_ensayo_3.md`](libro/19_parte4_ensayo_3.md)** — **Ensayo III:** *TV: ¿Dispositivo o aparato?* | *Págs. impresas 343–371 (PDF 326–354)*
  * *Incluye:* TV: Un collage de lo social y un tinglado de sentido · La forma y lo sagrado · La superabundancia del signo mediático.
* **[`20_parte4_ensayo_4.md`](libro/20_parte4_ensayo_4.md)** — **Ensayo IV:** *Entonces lo mediático: Manual para ver TV* | *Págs. impresas 373–377 (PDF 355–359)*

---

### Quinta Parte: De la opinión pública a las democracias mass-mediáticas
* **[`21_parte5_ensayo_1.md`](libro/21_parte5_ensayo_1.md)** — **Portadilla Quinta Parte + Ensayo I:** *La mediática en la hegemonía de la producción inmaterial* | *Págs. impresas 381–405 (PDF 361–384)*
  * *Incluye:* Una lectura de la opinión pública como régimen · Aún Marx · Por qué el poder de la mediática · La sobredeterminación mediática de la producción inmaterial.
* **[`22_parte5_ensayo_2.md`](libro/22_parte5_ensayo_2.md)** — **Ensayo II:** *La sociedad mediática* | *Págs. impresas 407–424 (PDF 385–402)*
  * *Incluye:* El predominio del significante en la forma-signo · La colonización de la democracia.
* **[`23_parte5_ensayo_3.md`](libro/23_parte5_ensayo_3.md)** — **Ensayo III:** *La massmediatización de la política: su devenir hoy* | *Págs. impresas 425–454 (PDF 403–432)*
  * *Incluye:* La banalización de la política: una tecnología del biopoder · La massmediática y los procesos de desintegración · Problemas de legitimación en las democracias mediáticas · El aura no desaparece, se desplaza.
* **[`24_parte5_ensayo_4.md`](libro/24_parte5_ensayo_4.md)** — **Ensayo IV:** *La mediática en su ocurrencia política* | *Págs. impresas 455–469 (PDF 433–447)*
  * *Incluye:* La mediática como dispositivo de captura · Líneas de fuga a la máquina total del sentido hegemónico.

---

### Sexta Parte: La apuesta por la distopía de las multitudes: hacia una refundación de la política
* **[`25_parte6_ensayo_1.md`](libro/25_parte6_ensayo_1.md)** — **Portadilla Sexta Parte + Ensayo I:** *Subjetividad y política: del consenso a la voluntad política de la multitud* | *Págs. impresas 473–495 (PDF 449–470)*
  * *Incluye:* Otra idea de Estado: entre lo efímero y lo permanente · La aporía del proceso constituyente: una nueva subjetividad política.
* **[`26_parte6_ensayo_2.md`](libro/26_parte6_ensayo_2.md)** — **Ensayo II:** *De la revuelta a la reinvención del pueblo* | *Págs. impresas 497–526 (PDF 471–500)*
  * *Incluye:* Adiós a la sociedad civil · La resistencia, o el poder constituyente del pueblo.
* **[`27_parte6_ensayo_3.md`](libro/27_parte6_ensayo_3.md)** — **Ensayo III:** *El final de la mosca: la tela arácnida al hilo del cuerpo-potencia* | *Págs. impresas 527–559 (PDF 501–531)*

---

### Epílogo, Post-scriptum y Aparato Crítico
* **[`28_epilogo.md`](libro/28_epilogo.md)** — **Epílogo:** *¿Se pueden cartografiar los mass-media?* | *Págs. impresas 561–584 (PDF 533–555)*
  * *Incluye:* Tejiendo ciertas inquietudes · Mediática para principiantes: Un alfabeto de signos incompletos (`A`–`Z`).
* **[`29_post_scriptum.md`](libro/29_post_scriptum.md)** — **Post-scriptum:** *Por el socialismo (Con un ensayo de Javier Biardeau: Entre dinosaurios y unicornios)* | *Págs. impresas 587–618 (PDF 557–588)*
  * *Incluye:* Primer movimiento: Homenaje a la memoria · Segundo movimiento: Sobre lo escrito · Tercer movimiento: *Entre dinosaurios y unicornios. Un ensayo de Javier Biardeau*.
* **[`30_bibliografia.md`](libro/30_bibliografia.md)** — **Bibliografía** | *Págs. impresas 621–641 (PDF 590–609)*
* **[`31_glosario.md`](libro/31_glosario.md)** — **Glosario** (*La caja de herramientas conceptual*) | *Págs. impresas 643–687 (PDF 611–655)*
* **[`32_indice_onomastico.md`](libro/32_indice_onomastico.md)** — **Índice Onomástico** | *Págs. impresas 691–699 (PDF 657–665)*

---

## Flujo Editorial de la Segunda Edición

El proceso está diseñado para **reducir al mínimo los comandos manuales** y centrarse exclusivamente en editar los capítulos `.md` de [`libro/`](libro/):

1. **Elegir un capítulo `.md`** en [`libro/`](libro/) y editarlo/actualizarlo con la IA siguiendo [`SSOT/guia_estilo_ia.md`](SSOT/guia_estilo_ia.md).
2. **Entregar ese capítulo al autor:** La IA valida el archivo, genera solo ese capítulo en PDF o Word (`.docx`) dentro de `dist/` y redacta un resumen breve de los cambios realizados.
3. **Iterar hasta aprobación:** Se aplican sobre el mismo `.md` las orientaciones del autor hasta obtener su visto bueno.
4. **Cerrar capítulo y avanzar:** Se marca `estado: "aprobado"` en [`libro.yaml`](libro.yaml), se anota en [`CHANGELOG.md`](CHANGELOG.md), se hace un commit + push simple en `main` y se pasa al siguiente `.md`.
5. **Nuevos capítulos o cambios de índice (a futuro):** Los capítulos nuevos se añaden en `libro/` y se declaran en `libro.yaml`; si cambia el orden de las partes o ensayos, solo se reordena `libro.yaml` y la IA regenera `libro/01_indice.md`.

### Referencia de Scripts Internos (ejecutados por la IA bajo demanda o manualmente)

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
* [`SSOT/guia_estilo_ia.md`](SSOT/guia_estilo_ia.md)
* [`SSOT/proceso_conversion_pdf_a_md.md`](SSOT/proceso_conversion_pdf_a_md.md)
* [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md)
* [`respaldo_v1.0/README.md`](respaldo_v1.0/README.md)
