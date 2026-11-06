# Detalle Completo del Proceso Ejecutado y Auditoría de Conversión (PDF a Markdown)

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Archivo Fuente:** `fuente/Libro Crítica de La Razon Mediatica.pdf` (`21,078,531 bytes`, `666 páginas físicas`)  
**Método Implementado:** Método 1 — Extracción Estructural Determinista por Coordenadas, Fuentes y Color (`pdftohtml -xml` + Python)  
**Especificación Base:** `SSOT/proceso_conversion_pdf_a_md.md`  

---

## 1. Resumen Ejecutivo de Resultados

| Métrica de Control | Valor Verificado | Estado |
| :--- | :---: | :---: |
| **Páginas físicas totales del PDF analizadas** | `666 / 666` (`650` texto + `16` gráficas) | **100% Cubierto** |
| **Archivos Markdown generados en `libro/`** | `33` archivos (incluyendo `01_indice.md`) | **100% Completado** |
| **Palabras totales en Markdown (`libro/*.md`)** | `197,741` palabras | **Verificado** |
| **Bloques estructurales (títulos, párrafos, citas, notas)** | `2,688` bloques | **Verificado** |
| **Notas al pie extraídas y enlazadas (`[^n]:`)** | `513` notas al pie (`0` huérfanas) | **100% Íntegro** |
| **Caracteres alfanuméricos en capa útil del PDF (XML)** | `1,008,962` caracteres | **Base Contable** |
| **Caracteres alfanuméricos en archivos Markdown (`libro/`)** | `1,008,962` caracteres | **Exactitud 100.000%** |
| **Caracteres perdidos (`missing`) / añadidos (`extra`)** | `0` perdidos / `0` extra | **0% Pérdida / 0% Mezcla** |
| **Consumo de tokens de IA para lectura del libro** | `0` tokens (100% procesado por scripts locales) | **Óptimo** |

---

## 2. Arquitectura de Scripts Implementados en `scripts/`

### 2.1. `scripts/01_extraer_xml.py` — Extracción Vectorial y Filtrado de Imprenta
1. **Invocación de Poppler:** Ejecuta `pdftohtml -xml -i -stdout` sobre `fuente/Libro Crítica de La Razon Mediatica.pdf`, extrayendo las 666 páginas sin procesar imágenes pesadas (`-i`), generando un árbol XML de `4,490,886 bytes` con coordenadas precisas (`top`, `left`, `width`, `height`) y especificaciones tipográficas (`<fontspec>`).
2. **Resolución de Herencia de Fuentes en Poppler:** Mantiene una tabla acumulativa global de `<fontspec id="...">` a lo largo de las 666 páginas, ya que Poppler declara cada `id` de fuente únicamente en la primera página donde aparece.
3. **Filtrado Determinista de los 5 Ruidos de Maquetación (QuarkXPress 9.51):**
   * **Sombras tipográficas duplicadas (Drop Shadows):** Elimina todos los nodos con `color` en `(#cccccc, #bdbbbc, #918f8f)`, que en QuarkXPress duplican epígrafes, capitulares y cabeceras con un desfase de 1–2 píxeles.
   * **Sellos editoriales verticales en márgenes laterales:** Elimina los nodos rotados 90° (`width="0"`) que deletrean verticalmente `Crítica de la Razón Mediática` y `Juan Barreto` en la esquina inferior de cada página.
   * **Líneas de registro de imprenta QuarkXPress:** Filtra los nodos `Helvetica 12pt` en `top < 25` con el formato `*.qxp* Page N`.
   * **Folios marginales (Números de página impresos):** Registra como metadato y retira del flujo de texto los números en `Bauhaus93 14pt` situados en `top < 145` en los márgenes exteriores.
   * **Cabeceras corridas superiores:** Retira del flujo de texto las cabeceras de sección (`Garamond 12pt/14pt` en `top < 65` para páginas de `616px` de ancho en la *Primera Parte* y `top < 105` para páginas de `697px` en el resto del libro).

### 2.2. `scripts/02_convertir_a_md.py` — Reconstrucción Estructural y Tipográfica en Markdown
1. **Agrupación Horizontal de Líneas (`±4 px`):** Reúne en una misma línea visual todos los fragmentos `<text>` con igual coordenada base `top`, reconociendo como llamadas de nota al pie en superíndice (`[^n]`) los nodos numéricos `Garamond 14pt/15pt` elevados hasta `6 px` respecto a la línea base `Garamond 18pt`, así como llamadas pospuestas a signos de puntuación al cierre de línea.
2. **Integración de Letras Capitulares (Drop Caps):** Identifica las 53 letras capitulares (`AmigaForeverPro2`, tamaños `28pt` a `65pt` de un carácter) y las une sin espacio espurio al primer vocablo del párrafo inicial (o como encabezado alfabético `**A**.-` en el *Alfabeto de signos incompletos* del Epílogo), evitando además que las dos líneas contiguas desplazadas por la caja de la capitular se partan como párrafos distintos.
3. **Separación Exacta de Notas al Pie y Continuaciones entre Páginas:**
   * Calcula en cada página la coordenada `max_g18` (última línea de cuerpo principal `Garamond 18pt`) y el margen izquierdo base `base_left`.
   * Distingue las citas a bando (blockquotes en `Garamond 15pt` sangradas a `left >= base_left + 35`) de la zona de notas al pie (ubicada debajo de `max_g18` e iniciada en el margen izquierdo `abs(left - base_left) <= 25`).
   * Une automáticamente las **12 continuaciones de notas extensas** que en el PDF original se partieron entre dos o tres páginas consecutivas (págs. PDF `102, 136, 174, 182, 212, 231, 232, 240, 281, 296, 321, 437`) y coloca todas las definiciones `[^n]: ...` al final de cada capítulo.
4. **Des-hifenación Inteligente Basada en Léxico Interno:**
   * Construye primero el diccionario completo del libro (`18,931` palabras simples sin guion y `619` palabras compuestas con guion explícito en medio de línea).
   * Al unir líneas terminadas en guion, elimina el guion de corte silábico (`arti-` + `culación` → `articulación`) pero preserva los compuestos conceptuales del autor (`significante-signo`, `ético-política`, `rostro-proceso`, `cuerpo-potencia`, etc.).
5. **Formateadores Especializados:** Procesa con reglas específicas `00_preliminares.md`, `01_indice.md` (uniendo títulos multilínea y limpiando líneas de puntos), `30_bibliografia.md` (lista de obras citadas), `31_glosario.md` (términos `· Concepto:`) y `32_indice_onomastico.md` (autores y páginas).

### 2.3. `scripts/03_auditar_integridad.py` — Verificación Contable 100%
Compara carácter por carácter el flujo alfanumérico de los nodos útiles del XML en cada rango de páginas contra el archivo `.md` generado en `libro/`, verificando que no falte ni sobre ni un solo carácter alfanumérico en ninguno de los 33 archivos.

---

## 3. Tabla de Auditoría Capítulo por Capítulo (`libro/`)

| Nº | Archivo en `libro/` | Págs. PDF | Folios | Palabras | Bloques | Notas | Chars XML | Chars MD | Pérdida / Extra |
| :-: | :--- | :---: | :---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 00 | `00_preliminares.md` | 2–4 (3) | 2–5 | 254 | 5 | 0 | 1,361 | 1,361 | **0 / 0 (100%)** |
| 01 | `01_indice.md` | 5–8 (4) | 7–10 | 930 | 14 | 0 | 3,799 | 3,799 | **0 / 0 (100%)** |
| 02 | `02_agradecimientos.md` | 9–10 (2) | 11–12 | 544 | 9 | 0 | 2,627 | 2,627 | **0 / 0 (100%)** |
| 03 | `03_liminar.md` | 12–14 (3) | s/n 1–5 | 881 | 13 | 0 | 4,136 | 4,136 | **0 / 0 (100%)** |
| 04 | `04_prologo_1_rigoberto_lanz.md` | 16–23 (8) | 15–23 | 1,907 | 27 | 0 | 10,042 | 10,042 | **0 / 0 (100%)** |
| 05 | `05_prologo_2_nelson_guzman.md` | 24–30 (7) | 25–31 | 1,866 | 31 | 0 | 9,178 | 9,178 | **0 / 0 (100%)** |
| 06 | `06_prologo_3_magaldy_tellez.md` | 31–38 (8) | 33–41 | 2,580 | 23 | 0 | 12,891 | 12,891 | **0 / 0 (100%)** |
| 07 | `07_preambulo.md` | 40–81 (42) | 43–84 | 12,784 | 197 | 32 | 65,498 | 65,498 | **0 / 0 (100%)** |
| 08 | `08_parte1_ensayo_1.md` | 83–105 (23) | 87–109 | 7,084 | 94 | 15 | 36,651 | 36,651 | **0 / 0 (100%)** |
| 09 | `09_parte1_ensayo_2.md` | 106–117 (12) | 111–121 | 3,520 | 51 | 6 | 18,212 | 18,212 | **0 / 0 (100%)** |
| 10 | `10_parte1_ensayo_3.md` | 118–169 (52) | 123–174 | 17,044 | 251 | 75 | 87,800 | 87,800 | **0 / 0 (100%)** |
| 11 | `11_parte2_ensayo_1.md` | 171–186 (16) | 177–193 | 5,108 | 59 | 18 | 26,388 | 26,388 | **0 / 0 (100%)** |
| 12 | `12_parte2_ensayo_2.md` | 187–201 (15) | 195–209 | 4,550 | 82 | 20 | 23,697 | 23,697 | **0 / 0 (100%)** |
| 13 | `13_parte2_ensayo_3.md` | 202–220 (19) | 211–229 | 6,086 | 114 | 26 | 30,431 | 30,431 | **0 / 0 (100%)** |
| 14 | `14_parte3_ensayo_1.md` | 222–246 (25) | 233–258 | 7,864 | 124 | 33 | 39,780 | 39,780 | **0 / 0 (100%)** |
| 15 | `15_parte3_ensayo_2.md` | 247–266 (20) | 259–278 | 6,154 | 122 | 35 | 30,675 | 30,675 | **0 / 0 (100%)** |
| 16 | `16_parte3_ensayo_3.md` | 267–283 (17) | 279–295 | 5,003 | 94 | 28 | 24,892 | 24,892 | **0 / 0 (100%)** |
| 17 | `17_parte4_ensayo_1.md` | 285–306 (22) | 299–321 | 7,605 | 102 | 28 | 39,209 | 39,209 | **0 / 0 (100%)** |
| 18 | `18_parte4_ensayo_2.md` | 307–325 (19) | 323–341 | 6,175 | 87 | 19 | 31,653 | 31,653 | **0 / 0 (100%)** |
| 19 | `19_parte4_ensayo_3.md` | 326–354 (29) | 343–371 | 9,868 | 144 | 37 | 49,875 | 49,875 | **0 / 0 (100%)** |
| 20 | `20_parte4_ensayo_4.md` | 355–359 (5) | 373–377 | 1,084 | 16 | 0 | 5,501 | 5,501 | **0 / 0 (100%)** |
| 21 | `21_parte5_ensayo_1.md` | 361–384 (24) | 381–405 | 7,127 | 102 | 19 | 36,281 | 36,281 | **0 / 0 (100%)** |
| 22 | `22_parte5_ensayo_2.md` | 385–402 (18) | 407–424 | 5,633 | 81 | 21 | 28,412 | 28,412 | **0 / 0 (100%)** |
| 23 | `23_parte5_ensayo_3.md` | 403–432 (30) | 425–454 | 9,359 | 126 | 27 | 48,646 | 48,646 | **0 / 0 (100%)** |
| 24 | `24_parte5_ensayo_4.md` | 433–447 (15) | 455–469 | 4,714 | 57 | 5 | 24,654 | 24,654 | **0 / 0 (100%)** |
| 25 | `25_parte6_ensayo_1.md` | 449–470 (22) | 473–495 | 6,542 | 85 | 13 | 33,314 | 33,314 | **0 / 0 (100%)** |
| 26 | `26_parte6_ensayo_2.md` | 471–500 (30) | 497–526 | 9,757 | 119 | 27 | 49,836 | 49,836 | **0 / 0 (100%)** |
| 27 | `27_parte6_ensayo_3.md` | 501–531 (31) | 527–559 | 9,779 | 126 | 20 | 49,987 | 49,987 | **0 / 0 (100%)** |
| 28 | `28_epilogo.md` | 533–555 (23) | 561–584 | 6,780 | 104 | 9 | 35,974 | 35,974 | **0 / 0 (100%)** |
| 29 | `29_post_scriptum.md` | 557–588 (32) | 587–618 | 9,250 | 130 | 0 | 49,241 | 49,241 | **0 / 0 (100%)** |
| 30 | `30_bibliografia.md` | 590–609 (20) | 621–641 | 4,481 | 2 | 0 | 22,219 | 22,219 | **0 / 0 (100%)** |
| 31 | `31_glosario.md` | 611–655 (45) | 643–687 | 13,690 | 95 | 0 | 70,180 | 70,180 | **0 / 0 (100%)** |
| 32 | `32_indice_onomastico.md` | 657–665 (9) | 691–699 | 1,738 | 2 | 0 | 5,922 | 5,922 | **0 / 0 (100%)** |
| **TOTAL** | **33 archivos en `libro/`** | **650 págs. texto (+16 gráf.)** | **2–699** | **197,741** | **2,688** | **513** | **1,008,962** | **1,008,962** | **0 / 0 (100.000%)** |

---

## 4. Comandos para Reproducir el Proceso y la Auditoría

```bash
# 1. Extraer y validar las 666 páginas del PDF a XML vectorial
python3 scripts/01_extraer_xml.py

# 2. Generar los 33 archivos Markdown por capítulo en libro/
python3 scripts/02_convertir_a_md.py

# 3. Ejecutar la auditoría matemática de integridad (0% pérdida) y actualizar este reporte
python3 scripts/03_auditar_integridad.py
```
