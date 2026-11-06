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

### Asesoría Informática — Segunda Edición
* **Asesor Informático en la realización de este trabajo de creación de la Segunda Edición del libro:**  
  **Octavio Rossell Tabet**  
  * Correo electrónico: [<octavio.rossell@gmail.com>](mailto:octavio.rossell@gmail.com)  
  * GitHub: [https://github.com/octaviotron](https://github.com/octaviotron)

### Datos Editoriales de la Primera Edición (2006)
* **Institución:** Universidad Central de Venezuela (UCV) — Centro de Investigaciones Post-Doctorales (CIPOST)
* **Diseño Gráfico:** Gustavo Velásquez Purroy
* **Impresión:** Publigráfica 66, C.A.
* **ISBN:** `980-12-1936-X`
* **Depósito Legal:** `lf25220060702192`
* **Lugar y año:** Distrito Metropolitano de Caracas, República Bolivariana de Venezuela, 2006 — ver [`libro/00_preliminares.md`](libro/00_preliminares.md)

---

## Estructura del Proyecto

El repositorio está organizado en cuatro directorios principales: [`fuente/`](fuente/), [`libro/`](libro/), [`scripts/`](scripts/) y [`SSOT/`](SSOT/).

```text
critica-de-la-razon-mediatica/
├── README.md                  # Documentación general, créditos e índice navegable
├── .gitignore                 # Reglas de exclusión de archivos temporales y caché
├── fuente/                    # Archivos originales de la 1.ª edición (PDF, QuarkXPress, fuentes e imágenes)
│   ├── Libro Crítica de La Razon Mediatica.pdf
│   ├── FUENTES/               # Fuentes tipográficas TrueType (.ttf) originales
│   ├── PORTADA/               # Artes originales de portada (.tif)
│   └── RAZON/                 # Maquetación QuarkXPress (.qxp/.qxb) y portadillas (.tif/.jpg)
│       └── images/            # Ilustraciones separadoras de cada parte y sección
├── libro/                     # Libro convertido a Markdown (33 archivos .md por capítulo)
├── scripts/                   # Scripts deterministas de extracción XML, conversión y auditoría
│   ├── 01_extraer_xml.py
│   ├── 02_convertir_a_md.py
│   └── 03_auditar_integridad.py
└── SSOT/                      # Single Source of Truth (Especificación y Auditoría del proceso)
    ├── proceso_conversion_pdf_a_md.md
    └── detalle_ejecucion_y_auditoria_conversion.md
```

### Descripción y Vínculos a las Carpetas Principales

1. **[`fuente/`](fuente/) — Material Fuente de la Primera Edición:**
   * **[`fuente/Libro Crítica de La Razon Mediatica.pdf`](<fuente/Libro Crítica de La Razon Mediatica.pdf>):** Documento PDF maestro de la primera edición (`21.08 MB`, `666` páginas físicas, numeración impresa hasta la pág. `699`).
   * **[`fuente/FUENTES/`](fuente/FUENTES/):** Tipografías empleadas en la edición original (`Garamond`, `Bauhaus93`, `AmigaForeverPro2`, `Swis721`, `Arial Black`).
   * **[`fuente/PORTADA/`](fuente/PORTADA/):** Archivos `.tif` de arte de portada (`PORTADA repujado1.tif`, `PORTADA repujado2.tif`, `PORTADA uv.tif`).
   * **[`fuente/RAZON/`](fuente/RAZON/):** Documentos nativos de maquetación en QuarkXPress (`INICIAL.qxp`, `liminar.qxp`, `1a PARTE.qxp` a `6a parte.qxp`, `POST-Escriptum.qxp`, `POSTERIOR.qxp`), nota editorial [`UBICACION DE liminar.txt`](<fuente/RAZON/UBICACION DE liminar.txt>) y subcarpeta **[`fuente/RAZON/images/`](fuente/RAZON/images/)** con las 14 portadillas gráficas separadoras.
2. **[`libro/`](libro/) — Libro Convertido en Formato Markdown (`.md`):**
   * Aloja los **33 archivos Markdown** extraídos siguiendo la estructura principal del Índice (págs. 7–10) más el capítulo *Liminar*, asegurando el **100% de integridad textual** (`197,741` palabras, `513` notas al pie y `1,008,962` caracteres alfanuméricos verificados sin pérdidas ni mezclas entre capítulos).
3. **[`scripts/`](scripts/) — Pipeline de Extracción, Conversión y Auditoría:**
   * **[`scripts/01_extraer_xml.py`](scripts/01_extraer_xml.py):** Extrae la capa vectorial de las 666 páginas del PDF mediante `pdftohtml -xml -i`, resuelve la tabla acumulativa de fuentes y filtra determinísticamente el ruido de imprenta (sombras duplicadas `#cccccc`/`#bdbbbc`/`#918f8f`, sellos laterales rotados `width="0"`, líneas de registro QuarkXPress, cabeceras corridas y folios marginales).
   * **[`scripts/02_convertir_a_md.py`](scripts/02_convertir_a_md.py):** Reconstruye los párrafos, encabezados (`#`, `##`, `###`), cursivas (`*...*`), negritas (`**...**`), epígrafes, citas a bando (`>`), letras capitulares, palabras divididas por guion y notas al pie (`[^n]: ...`), generando los 33 archivos en [`libro/`](libro/).
   * **[`scripts/03_auditar_integridad.py`](scripts/03_auditar_integridad.py):** Ejecuta la auditoría contable comparando carácter por carácter el flujo alfanumérico del PDF contra los archivos en [`libro/`](libro/) y genera el reporte en [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md).
4. **[`SSOT/`](SSOT/) — *Single Source of Truth* (Documentación de Proceso y Auditoría):**
   * **[`SSOT/proceso_conversion_pdf_a_md.md`](SSOT/proceso_conversion_pdf_a_md.md):** Especificación técnica detallada del Método 1, caracterización geométrica y tipográfica del PDF y mapa maestro de capítulos.
   * **[`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md):** Memoria técnica de la conversión ejecutada y tabla de resultados de la auditoría contable capítulo por capítulo.

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

## Reproducción del Pipeline y Verificación de Integridad

Para ejecutar nuevamente la extracción desde [`fuente/Libro Crítica de La Razon Mediatica.pdf`](<fuente/Libro Crítica de La Razon Mediatica.pdf>), regenerar los archivos en [`libro/`](libro/) y verificar la auditoría contable en [`SSOT/`](SSOT/):

```bash
# 1. Extraer la capa vectorial XML de las 666 páginas del PDF
python3 scripts/01_extraer_xml.py

# 2. Convertir las 650 páginas de texto en los 33 archivos Markdown en libro/
python3 scripts/02_convertir_a_md.py

# 3. Auditar al 100% la integridad de caracteres, palabras, capítulos y notas al pie
python3 scripts/03_auditar_integridad.py
```

Para consultar el detalle técnico completo del proceso y la tabla de auditoría capítulo por capítulo, véanse:
* [`SSOT/proceso_conversion_pdf_a_md.md`](SSOT/proceso_conversion_pdf_a_md.md)
* [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](SSOT/detalle_ejecucion_y_auditoria_conversion.md)
