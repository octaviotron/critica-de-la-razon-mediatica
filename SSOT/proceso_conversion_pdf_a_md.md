# SSOT: Proceso Detallado de Extracción y Conversión de PDF a Markdown (Método 1)

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani, 2006)  
**Documento Fuente:** `fuente/Libro Crítica de La Razon Mediatica.pdf`  
**Método Seleccionado:** Método 1 — Extracción Estructural por Coordenadas, Fuentes y Color (`pdftohtml -xml` + Parser Determinista en Python + Auditoría Contable 100%)  
**Directorio de Scripts:** `scripts/` (o `script/`)  
**Directorio de Salida:** `libro/` (un archivo `.md` por capítulo, incluyendo un archivo independiente para el Índice)

---

## 1. Objetivo y Garantías de Calidad

1. **Integridad del 100% del contenido (0% pérdida):** Extraer la totalidad del texto útil de las **666 páginas físicas** del PDF original sin omitir párrafos, epígrafes, citas a bando, notas al pie, entradas bibliográficas, términos del glosario ni referencias del índice onomástico.
2. **Aislamiento estricto por capítulos (0% mezcla):** Segmentar el libro en **33 archivos Markdown (`.md`)** independientes siguiendo el Índice original (págs. impresas 7–10 / págs. PDF 5–8) más el capítulo *Liminar* de Michel Maffesoli, mediante fronteras exactas y disjuntas de páginas físicas del PDF.
3. **Eficiencia de Tokens:** Realizar el 100% del procesamiento pesado mediante scripts deterministas locales en Python + Poppler (`pdftohtml -xml -i`), evitando enviar los ~1.32 MB de texto del libro a través de la ventana de contexto del modelo de IA.
4. **Fidelidad Tipográfica y Semántica:** Conservar automáticamente cursivas (`*texto*`), negritas (`**texto**`), jerarquía de títulos (`#`, `##`, `###`), epígrafes, citas en bloque (`>`) y notas al pie en sintaxis estándar Markdown (`[^n]`).

---

## 2. Caracterización Técnica del PDF Fuente

El archivo `fuente/Libro Crítica de La Razon Mediatica.pdf` (21,078,531 bytes, PDF v1.6) fue exportado desde **QuarkXPress 9.51** y presenta las siguientes características estructurales:

### 2.1. Distribución de las 666 Páginas Físicas
* **16 páginas exclusivamente gráficas (sin texto de contenido):**
  * `Pág. PDF 1`: Portada exterior.
  * `Págs. PDF 11, 15, 39, 82, 170, 221, 284, 360, 448, 532, 556, 589, 610, 656`: 14 portadillas ilustradas a página completa (300 DPI) que preceden a cada gran bloque del libro.
  * `Pág. PDF 666`: Contraportada exterior.
* **650 páginas con contenido textual:** Contienen ~208,285 palabras brutas (incluyendo cabeceras y sellos repetidos en cada página).
* **Desfase entre numeración impresa (Folio) y página física del PDF:**
  * En la maquetación original (que llega hasta la página impresa `699`), las páginas pares en blanco previas a portadillas o inicios de ensayo fueron omitidas al exportar el PDF.
  * Entre *Agradecimientos* (folio 12 / PDF 10) y *Pro(Logos)* (folio 15 / PDF 16) se insertó el documento `liminar.qxp` (*Liminar*, por Michel Maffesoli) en las páginas físicas **11 a 14 del PDF** con numeración propia (`1` a `5`).

### 2.2. Dos Geometrías de Página en el XML (`pdftohtml -xml -i`)
Al convertir el PDF a XML con Poppler (`pdftohtml -xml -i`), existen dos cajas de recorte (*CropBox*) distintas que el parser debe normalizar:

| Bloque del Libro | Rango Págs. PDF | Dimensiones XML (`width × height`) | Características de Coordenadas (`left`, `top`) |
| :--- | :---: | :---: | :--- |
| **Resto del libro** (`INICIAL`, `liminar`, `2a PARTE` a `POSTERIOR`) | `2–81` y `170–665` | `697 × 973 px` | Incluye línea de registro QuarkXPress en `top="1"`. Margen izquierdo de cuerpo en `left ≈ 125–126` (sangría de párrafo en `left ≈ 176`). Folio en `top ≈ 125–126`. Cabecera corrida en `top ≈ 90`. |
| **Primera Parte** (`1a PARTE`) | `83–169` | `616 × 892 px` | Exportado sin línea de registro QuarkXPress. Coordenadas desplazadas `-40 px` en `left` y `-42 px` en `top`: margen izquierdo de cuerpo en `left ≈ 85–87` (sangría en `left ≈ 136–138`). Folio en `top ≈ 84`. Cabecera corrida en `top ≈ 48`. |

### 2.3. Mapa Tipográfico y de Color en el XML
Cada nodo `<text top="..." left="..." width="..." height="..." font="...">` está asociado a un `<fontspec id="..." size="..." family="..." color="..."/>` con roles inequívocos:

1. **Sombras duplicadas de QuarkXPress (Drop Shadow) — A DESCARTAR:**
   * Nodos con `color="#cccccc"` o `color="#bdbbbc"`. Son duplicados exactos de epígrafes, capitulares y cabeceras desplazados `(top+1, left+1)` para crear sombra impresa.
2. **Línea de registro de imprenta QuarkXPress — A DESCARTAR:**
   * Nodos con `family` `Helvetica` (`size="12"`, `color="#000000"`) en `top < 25` cuyo texto coincide con el patrón `^.*?\d+/\d+/\d+\s+\d+:\d+\s+[AP]M\s+Page\s+\d+$`.
3. **Sello editorial vertical en margen exterior — A DESCARTAR:**
   * Nodos con `width="0"` (texto rotado 90°) y fuentes `Bauhaus93` (`size="9"`), `AmigaForeverPro2` (`size="8"`) o `FranklinGothic-DemiCond` (`size="9"`) en los márgenes laterales (`left > 560` o `left < 80`), que deletrean verticalmente `Crítica de la Razón Mediática` y `Juan Barreto`.
4. **Cabeceras corridas superiores y Folios (números de página) — A DESCARTAR DELFLUJO DE TEXTO (usados solo como metadato de control):**
   * **Cabecera corrida:** Nodos `Garamond` (`size="12"`) en `top < 60` (págs. de ancho `616`) o `top < 105` (págs. de ancho `697`), más la cabecera `Liminar` centrada en págs. PDF 13–14.
   * **Folio impreso:** Nodos `Bauhaus93` (`size="14"`) puramente numéricos ubicados en el margen exterior superior (`left < 85` en páginas pares, `left > 550` en páginas impares, `top < 145`).
5. **Títulos y Subtítulos — A CONVERTIR EN ENCABEZADOS MARKDOWN (`#`, `##`, `###`):**
   * **Título de Parte:** `Garamond` (`size="21"`) + `Bauhaus93` (`size="36"`) + `AmigaForeverPro2` (`size="27"`).
   * **Número Romano y Título de Ensayo:** `Garamond` (`size="27"`, `<b>I</b>`, `<b>II</b>`, etc.) + `Bauhaus93` (`size="21"` / `"27"`) + `AmigaForeverPro2` (`size="16"` / `"18"` / `"21"`).
   * **Subtítulo interno de sección:** `AmigaForeverPro2` (`size="15"`, o `size="18"` en Preámbulo/Epílogo). *Nota: Como la fuente `AmigaForeverPro2` tiene glifos idénticos para mayúsculas y minúsculas, se normaliza la capitalización del título contrastándola con la entrada correspondiente del Índice (págs. 7–10).*
6. **Letra Capitular (Drop Cap) — A INTEGRAR AL INICIO DEL PRIMER PÁRRAFO:**
   * Nodo de 1 carácter con fuente `AmigaForeverPro2` (`size="48"`, color `#231f20`) al inicio de cada ensayo/capítulo (ej. `M`, `C`, `e`, `l`). Se antepone directamente al primer fragmento de texto de cuerpo (`size="18"`) de esa página, corrigiendo su capitalización si la capitular fue digitada en minúscula (`e` + `n las páginas` → `En las páginas`).
7. **Epígrafes — A CONVERTIR EN CITA DE APERTURA (`> *...*`):**
   * Bloques en `Garamond` (`size="15"`, color `#231f20`) situados inmediatamente después de un título de Parte, Ensayo o Subtítulo, alineados hacia el margen derecho (`left > 150` en pág. `616` o `left > 190` en pág. `697`), cerrados por una línea de autor en negrita (`<b>M. Foucault.</b>`, `<b>C. Marx.</b>`, etc.).
8. **Cuerpo Principal y Citas a Bando (Blockquotes):**
   * **Cuerpo principal:** `Garamond` (`size="18"`, o `size="17"` en Bibliografía). Un salto de párrafo se detecta de forma exacta cuando `left` tiene sangría de primera línea (`left ≈ 136–138` en pág. `616` o `left ≈ 176–178` en pág. `697`, es decir, `+50 px` respecto al margen izquierdo del bloque de texto) o tras un salto vertical mayor al interlineado normal (`Δtop > 30 px`).
   * **Citas extensas sangradas (Blockquotes):** Bloques en `Garamond` (`size="15"`) dentro del cuerpo de la página (por encima de la zona de notas al pie) cuyo margen izquierdo está sangrado `+50 px` respecto al margen normal (`left ≈ 137–140` en pág. `616` o `left ≈ 176–180` en pág. `697`) en todas sus líneas. Se formatean con `> `.
9. **Llamadas y Textos de Notas al Pie (`[^n]`):**
   * **Llamada en el cuerpo:** Nodo numérico en `Garamond` (`size="15"`) incrustado en una línea de cuerpo (`size="18"`) cuya coordenada `top` está `2–4 px` más arriba que la línea base (`top_nota ≈ top_linea - 3`). Se inserta como `[^n]` (reiniciando o manteniendo numeración por capítulo según el original, ej. `[^p89-1]` o correlativo por archivo).
   * **Cuerpo de la nota al pie:** Bloques en `Garamond` (`size="15"`) ubicados al pie de la página (debajo del último renglón de `size="18"`, con `left` en el margen izquierdo normal `86` o `126`) que comienzan con el número de la nota (`1 `, `2 `, etc.). Se extraen fuera del flujo del párrafo principal (para no romper oraciones que continúan en la página siguiente) y se colocan al final del archivo Markdown correspondiente.

---

## 3. Mapa Maestro de Capítulos y Archivos de Salida (`libro/`)

La siguiente tabla define la partición **exacta, exhaustiva y sin solapamientos** de las 666 páginas del PDF en **33 archivos Markdown** dentro de `libro/`:

| Nº | Nombre de Archivo en `libro/` | Título del Capítulo / Sección | Folios Impresos | Págs. PDF (Texto) | Págs. PDF (Gráficas) |
| :-: | :--- | :--- | :---: | :---: | :---: |
| 00 | `00_preliminares.md` | Créditos, Portadilla Interior y Epígrafe General (Deleuze y Guattari) | 2 – 5 | 2 – 4 | 1 (Portada) |
| 01 | `01_indice.md` | Índice General | 7 – 10 | 5 – 8 | — |
| 02 | `02_agradecimientos.md` | Agradecimientos | 11 – 12 | 9 – 10 | — |
| 03 | `03_liminar.md` | Liminar: La belleza con agudeza y rigor *(Michel Maffesoli)* | [s/n 1 – 5] | 12 – 14 | 11 |
| 04 | `04_prologo_1_rigoberto_lanz.md` | Pro(Logos) — Comunicación: El clímax de la era posmoderna *(Rigoberto Lanz)* | 15 – 23 | 16 – 23 | 15 |
| 05 | `05_prologo_2_nelson_guzman.md` | Pro(Logos) — Los nuevos mundos simbólicos *(Nelson Guzmán)* | 25 – 31 | 24 – 30 | — |
| 06 | `06_prologo_3_magaldy_tellez.md` | Pro(Logos) — Trayectos claves para pensar el socialismo como pasión *(Magaldy Téllez)* | 33 – 41 | 31 – 38 | — |
| 07 | `07_preambulo.md` | Un intento para hacerse cargo de la massmediática. A modo de preámbulo | 43 – 84 | 40 – 81 | 39 |
| 08 | `08_parte1_ensayo_1.md` | Primera Parte: Aproximación a una caja de herramientas — Ensayo I: Crisis de la teoría del valor y nuevo dispositivo información-comunicación | 87 – 109 | 83 – 105 | 82 |
| 09 | `09_parte1_ensayo_2.md` | Primera Parte — Ensayo II: Un ejercicio sobre materia oscura y agujeros negros, virus y ADN | 111 – 121 | 106 – 117 | — |
| 10 | `10_parte1_ensayo_3.md` | Primera Parte — Ensayo III: Un acercamiento crítico a las tradiciones teóricas en el campo de la comunicación | 123 – 174 | 118 – 169 | — |
| 11 | `11_parte2_ensayo_1.md` | Segunda Parte: Cultura(s), campos y massmediática — Ensayo I: Campos híbridos y lecturas transversales | 177 – 193 | 171 – 186 | 170 |
| 12 | `12_parte2_ensayo_2.md` | Segunda Parte — Ensayo II: ¿Una teoría lingüística del valor? | 195 – 209 | 187 – 201 | — |
| 13 | `13_parte2_ensayo_3.md` | Segunda Parte — Ensayo III: Una incursión en la estética | 211 – 229 | 202 – 220 | — |
| 14 | `14_parte3_ensayo_1.md` | Tercera Parte: Una visión del significante-signo y del lenguaje — Ensayo I: Caminos de la semiótica | 233 – 258 | 222 – 246 | 221 |
| 15 | `15_parte3_ensayo_2.md` | Tercera Parte — Ensayo II: Los fantasmas del sentido: en el giro hermenéutico de la semiótica | 259 – 278 | 247 – 266 | — |
| 16 | `16_parte3_ensayo_3.md` | Tercera Parte — Ensayo III: El mito: pasaje narrativo del significante-signo al símbolo | 279 – 295 | 267 – 283 | — |
| 17 | `17_parte4_ensayo_1.md` | Cuarta Parte: Subjetividad, dispositivos y mass-media — Ensayo I: Massmediática y construcción de subjetividad | 299 – 321 | 285 – 306 | 284 |
| 18 | `18_parte4_ensayo_2.md` | Cuarta Parte — Ensayo II: La subjetividad massmediática | 323 – 341 | 307 – 325 | — |
| 19 | `19_parte4_ensayo_3.md` | Cuarta Parte — Ensayo III: TV: ¿Dispositivo o aparato? | 343 – 371 | 326 – 354 | — |
| 20 | `20_parte4_ensayo_4.md` | Cuarta Parte — Ensayo IV: Entonces lo mediático: Manual para ver TV | 373 – 377 | 355 – 359 | — |
| 21 | `21_parte5_ensayo_1.md` | Quinta Parte: De la opinión pública a las democracias mass-mediáticas — Ensayo I: La mediática en la hegemonía de la producción inmaterial | 381 – 405 | 361 – 384 | 360 |
| 22 | `22_parte5_ensayo_2.md` | Quinta Parte — Ensayo II: La sociedad mediática | 407 – 424 | 385 – 402 | — |
| 23 | `23_parte5_ensayo_3.md` | Quinta Parte — Ensayo III: La massmediatización de la política: su devenir hoy | 425 – 454 | 403 – 432 | — |
| 24 | `24_parte5_ensayo_4.md` | Quinta Parte — Ensayo IV: La mediática en su ocurrencia política | 455 – 469 | 433 – 447 | — |
| 25 | `25_parte6_ensayo_1.md` | Sexta Parte: La apuesta por la distopía de las multitudes — Ensayo I: Subjetividad y política: del consenso a la voluntad política de la multitud | 473 – 495 | 449 – 470 | 448 |
| 26 | `26_parte6_ensayo_2.md` | Sexta Parte — Ensayo II: De la revuelta a la reinvención del pueblo | 497 – 526 | 471 – 500 | — |
| 27 | `27_parte6_ensayo_3.md` | Sexta Parte — Ensayo III: El final de la mosca: la tela arácnida al hilo del cuerpo-potencia | 527 – 559 | 501 – 531 | — |
| 28 | `28_epilogo.md` | Epílogo: ¿Se pueden cartografiar los mass-media? | 561 – 584 | 533 – 555 | 532 |
| 29 | `29_post_scriptum.md` | Post-scriptum: Por el socialismo *(con ensayo de Javier Biardeau)* | 587 – 618 | 557 – 588 | 556 |
| 30 | `30_bibliografia.md` | Bibliografía | 621 – 641 | 590 – 609 | 589 |
| 31 | `31_glosario.md` | Glosario | 643 – 687 | 611 – 655 | 610 |
| 32 | `32_indice_onomastico.md` | Índice Onomástico | 691 – 699 | 657 – 665 | 656, 666 |

> **Verificación de Cobertura de Páginas:**  
> $650\text{ páginas de texto} + 16\text{ páginas gráficas} = 666\text{ páginas físicas totales del PDF}$. Ninguna página queda fuera de rango ni asignada a dos archivos simultáneamente.

---

## 4. Pipeline de Ejecución paso a paso (Scripts en `scripts/`)

### Paso 1: Exportación de Capa Vectorial a XML (`scripts/01_extraer_xml.py`)
1. Ejecuta `pdftohtml -xml -i -stdout "fuente/Libro Crítica de La Razon Mediatica.pdf"` para obtener el árbol XML completo en memoria o en un archivo intermedio temporal.
2. Verifica que el XML contenga exactamente `<page number="1">` hasta `<page number="666">`.

### Paso 2: Parser Estructural y Generador de Markdown (`scripts/02_convertir_a_md.py`)
Para cada uno de los **33 capítulos** definidos en el Mapa Maestro (Sección 3):

1. **Filtrado de Ruido de Imprenta (por página):**
   * Elimina nodos con `color in ("#cccccc", "#bdbbbc")` (sombras duplicadas).
   * Elimina nodos con `width="0"` (sello lateral rotado `Crítica de la Razón Mediática / Juan Barreto`).
   * Elimina nodos de registro QuarkXPress (`top < 25` con patrón `Page \d+`).
   * Extrae y registra el folio impreso (`Bauhaus93`, `size="14"`, `top < 145` en márgenes laterales) y descarta la cabecera corrida superior (`Garamond`, `size="12"`, `top < 60` en pág. `616` o `top < 105` en pág. `697`).
2. **Reconstrucción de Líneas Visuales:**
   * Agrupa los nodos `<text>` de una misma línea horizontal cuya coordenada `top` difiera en $\le 4\text{ px}$ (detectando como superíndice `[^n]` cualquier nodo numérico `size="15"` incrustado en una línea de `size="18"` con `top` menor en $2\text{–}4\text{ px}$).
   * Ordena los fragmentos de cada línea de izquierda a derecha por `left` y preserva las etiquetas `<i>` (`*...*`) y `<b>` (`**...**`).
3. **Separación de Zonas de la Página (Encabezados / Cuerpo / Notas al Pie):**
   * **Notas al pie:** Identifica en la parte inferior de la página las líneas en `Garamond` (`size="15"`) que comienzan en el margen izquierdo base (`left ≈ 86` o `126`) con un número de nota correspondiente a los superíndices de esa página (o continuación de nota previa) y las separa en una cola de notas del capítulo.
   * **Letra capitular (Drop Cap):** Si la página contiene un nodo `AmigaForeverPro2` de `size="48"`, lo une al inicio de la primera línea del cuerpo principal.
   * **Títulos, Subtítulos y Epígrafes:** Clasifica los bloques por familia y tamaño de fuente (`Bauhaus93` / `AmigaForeverPro2` → `#`, `##`, `###`; `Garamond 15pt` alineado a la derecha bajo título → epígrafe `> *...*`).
4. **Unión de Párrafos e Hifenación (Corte de Palabra al Final de Línea y de Página):**
   * Une las líneas consecutivas de un mismo párrafo y continúa el párrafo a través del salto de página cuando la primera línea de la página siguiente **no** tiene sangría de párrafo nuevo (`left < margen_base + 25`).
   * **Des-hifenación inteligente:** Cuando una línea termina en guion (`palabra-`), une los fragmentos (`arti-` + `culación` → `articulación`), **excepto** cuando se trata de compuestos conceptuales propios del autor (ej. `significante-signo`, `rostro-proceso`, `hecha-en-común`, `cuerpo-potencia`, `trabajo-valor`, `post-scriptum`, `mass-media`, `ético-política`, o cuando la segunda parte inicia en mayúscula).
5. **Formateo Especial para Secciones Finales (`01_indice.md`, `30_bibliografia.md`, `31_glosario.md`, `32_indice_onomastico.md`):**
   * **Índice (`01_indice.md`):** Reconstruye la estructura jerárquica limpia eliminando las secuencias de puntos (`..........`) y conservando la referencia al número de página original más el enlace al archivo `.md` correspondiente.
   * **Bibliografía (`30_bibliografia.md`):** Cada entrada bibliográfica (sangría francesa o inicio en mayúsculas/guiones bajos `______________:`) se formatea como ítem de lista (`- `) conservando las cursivas de los títulos de libros/revistas.
   * **Glosario (`31_glosario.md`):** Cada término que inicia con `· Término:` en negrita se convierte en un subtítulo `### Término` seguido de su definición completa.
   * **Índice Onomástico (`32_indice_onomastico.md`):** Cada autor y su lista de páginas en cursiva se formatea como lista estructurada (`- **APELLIDO, Nombre:** *págs.*`).

### Paso 3: Auditoría Contable y Verificación de Integridad (`scripts/03_auditar_integridad.py`)
Una vez generados los 33 archivos `.md` en `libro/`, este script ejecuta cuatro pruebas automáticas obligatorias y genera un reporte de auditoría (`SSOT/reporte_auditoria_conversion.md`):

1. **Prueba de Cobertura de Páginas (666/666):** Verifica que las 650 páginas con texto hayan sido procesadas exactamente una vez.
2. **Prueba Contable de Palabras y Caracteres (Página por Página y Capítulo por Capítulo):**
   * Compara el conjunto de tokens alfanuméricos extraídos del XML limpio de cada rango de páginas contra el conjunto de tokens alfanuméricos del archivo `.md` generado.
   * Cualquier discrepancia $> 0$ palabras perdidas o añadidas se marca como error crítico indicando página y línea exacta.
3. **Prueba de Fronteras de Capítulos (Anti-mezcla):**
   * Verifica que cada uno de los 33 archivos `.md` inicie con el título exacto esperado según el Índice y termine con la última frase de la página final de su rango antes del inicio del capítulo siguiente.
4. **Prueba de Integridad de Notas al Pie:**
   * Verifica que el número total de llamadas a notas al pie `[^n]` en el cuerpo de cada capítulo coincida exactamente con el número de definiciones `[^n]: ...` al final del archivo.
