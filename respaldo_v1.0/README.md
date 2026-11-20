# Respaldo Inmutable — Primera Edición (`respaldo_v1.0/`)

> **⚠️ DIRECTORIO INMUTABLE — SOLO LECTURA DE REFERENCIA**  
> No edites, renombres ni elimines archivos dentro de esta carpeta. Todas las ediciones de la Segunda Edición deben realizarse exclusivamente en [`libro/`](../libro/) y [`libro.yaml`](../libro.yaml).

## Propósito

Este directorio conserva de forma congelada e íntegra el estado inicial de la obra correspondiente a la **Primera Edición (2006)** de ***Crítica de la Razón Mediática*** (Juan Barreto Cipriani), verificada al **100.000%** contra el PDF maestro (`1,008,962` caracteres alfanuméricos, `197,690` palabras, `535` notas al pie, `0` pérdidas).

Sus tres funciones permanentes son:

1. **Referencia estructural inicial:** Preserva en [`libro.yaml`](libro.yaml) el orden, agrupación por partes y metadatos exactos del índice de 2006, aun cuando el índice y la estructura de la Segunda Edición cambien en el futuro.
2. **Referencia textual original:** Preserva en [`md/`](md/) los 33 archivos Markdown originales para comparar diferencias contra cualquier avance en [`libro/`](../libro/) y para re-ejecutar en cualquier momento la auditoría matemática contra el PDF de 2006.
3. **Compilación garantizada de la Primera Edición (`v1.0.0`):** Permite regenerar el PDF completo de la primera versión en cualquier momento, independientemente de cuántas modificaciones, reordenamientos o nuevos capítulos se realicen en [`libro/`](../libro/).

---

## Contenido de este directorio

```text
respaldo_v1.0/
├── README.md           # Esta documentación y guía de uso del respaldo inmutable
├── libro.yaml          # Manifiesto estructural congelado de la 1.ª edición (v1.0.0)
├── manifiesto_v1.0.md  # Registro criptográfico SHA-256 y tamaño en bytes de los 33 archivos
└── md/                 # Copia testigo inmutable de los 33 archivos .md originales
    ├── 00_preliminares.md
    ├── ...
    └── 32_indice_onomastico.md
```

---

## Operaciones permitidas (solo lectura / generación externa en `dist/`)

### 1. Generar el PDF de la Primera Edición (`v1.0.0`)
Aunque los archivos de [`libro/`](../libro/) o el manifiesto raíz [`libro.yaml`](../libro.yaml) hayan cambiado completamente, este comando compila siempre la 1.ª edición intacta en `dist/`:

```bash
python3 scripts/edicion/compilar_pdf.py --manifiesto respaldo_v1.0/libro.yaml
```

*(Genera `dist/Critica_de_la_Razon_Mediatica_v1.0.0.pdf`.)*

### 2. Verificar la integridad criptográfica (SHA-256) del respaldo
Comprueba que ninguno de los 33 archivos de [`md/`](md/) haya sido alterado respecto a [`manifiesto_v1.0.md`](manifiesto_v1.0.md) y valida todas sus notas al pie:

```bash
python3 scripts/edicion/validar_libro.py --manifiesto respaldo_v1.0/libro.yaml --verificar-respaldo
```

### 3. Re-auditar contra el PDF maestro de 2006 (`fuente/`)
Comprueba al 100.000% los caracteres alfanuméricos de `respaldo_v1.0/md/` frente a la capa vectorial del PDF original:

```bash
python3 scripts/extraccion_v1/03_auditar_integridad.py
```

### 4. Comparar los cambios de la Segunda Edición frente a este respaldo
Genera en `dist/` un reporte detallado de cambios estructurales y textuales entre `respaldo_v1.0/` y el estado actual de [`libro/`](../libro/):

```bash
python3 scripts/edicion/reporte_cambios.py
```

---

## Referencias en el SSOT

* [`SSOT/proceso_conversion_pdf_a_md.md`](../SSOT/proceso_conversion_pdf_a_md.md) — Especificación de la extracción y política del respaldo inmutable `respaldo_v1.0/`.
* [`SSOT/detalle_ejecucion_y_auditoria_conversion.md`](../SSOT/detalle_ejecucion_y_auditoria_conversion.md) — Auditoría contable 100.000% de estos 33 archivos.
* [`SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md) — Flujo de edición asistida, `libro.yaml` y uso de este respaldo.

---

## Estructura Congelada de la Primera Edición (2006) — 33 Archivos en [`md/`](md/)

Catálogo completo e inmutable de los capítulos originales con sus folios impresos y páginas físicas del PDF maestro de 2006:

### Preliminares, Índice, Prólogos y Preámbulo
* **[`00_preliminares.md`](md/00_preliminares.md)** — Créditos editoriales, Portadilla interior y Epígrafe general (*G. Deleuze y F. Guattari*) | *Págs. impresas 2–5 (PDF 2–4)*
* **[`01_indice.md`](md/01_indice.md)** — **Índice General de la Obra** | *Págs. impresas 7–10 (PDF 5–8)*
* **[`02_agradecimientos.md`](md/02_agradecimientos.md)** — **Agradecimientos** | *Págs. impresas 11–12 (PDF 9–10)*
* **[`03_liminar.md`](md/03_liminar.md)** — **Liminar:** *La belleza con agudeza y rigor* — **Michel Maffesoli** | *Págs. s/n 1–5 (PDF 12–14)*
* **PRO(LOGOS):**
  * **[`04_prologo_1_rigoberto_lanz.md`](md/04_prologo_1_rigoberto_lanz.md)** — *Comunicación: El clímax de la era posmoderna* — **Rigoberto Lanz** | *Págs. impresas 15–23 (PDF 16–23)*
  * **[`05_prologo_2_nelson_guzman.md`](md/05_prologo_2_nelson_guzman.md)** — *Los nuevos mundos simbólicos* — **Nelson Guzmán** | *Págs. impresas 25–31 (PDF 24–30)*
  * **[`06_prologo_3_magaldy_tellez.md`](md/06_prologo_3_magaldy_tellez.md)** — *Trayectos claves para pensar el socialismo como pasión* — **Magaldy Téllez** | *Págs. impresas 33–41 (PDF 31–38)*
* **[`07_preambulo.md`](md/07_preambulo.md)** — **Un intento para hacerse cargo de la massmediática. A modo de preámbulo** | *Págs. impresas 43–84 (PDF 40–81)*
  * *Incluye:* Profecías y realidades tecnológicas · La era de las conexiones · Las urgencias de la teoría · Cuestión de Método: La aventura de hablar y escribir sobre lo múltiple (O cómo dar con el problema) · El drama de la escritura (El cómo de la forma o estilo) · Algo sobre nosotros mismos.

### Primera Parte: Aproximación a una caja de herramientas
* **[`08_parte1_ensayo_1.md`](md/08_parte1_ensayo_1.md)** — **Portadilla Primera Parte + Ensayo I:** *Crisis de la teoría del valor y nuevo dispositivo información-comunicación* | *Págs. impresas 87–109 (PDF 83–105)*
* **[`09_parte1_ensayo_2.md`](md/09_parte1_ensayo_2.md)** — **Ensayo II:** *Un ejercicio sobre materia oscura y agujeros negros, virus y ADN* | *Págs. impresas 111–121 (PDF 106–117)*
* **[`10_parte1_ensayo_3.md`](md/10_parte1_ensayo_3.md)** — **Ensayo III:** *Un acercamiento crítico a las tradiciones teóricas en el campo de la comunicación* | *Págs. impresas 123–174 (PDF 118–169)*
  * *Incluye:* La Escuela de Frankfurt y sus críticos · Masas e Industria · La ilusión como performativo · El espíritu americano · Influencia, inoculación y efectos · Problema de modelos · Otros aportes · Tendencias y aportes desde América Latina.

### Segunda Parte: Cultura(s), campos y massmediática
* **[`11_parte2_ensayo_1.md`](md/11_parte2_ensayo_1.md)** — **Portadilla Segunda Parte + Ensayo I:** *Campos híbridos y lecturas transversales* | *Págs. impresas 177–193 (PDF 171–186)*
* **[`12_parte2_ensayo_2.md`](md/12_parte2_ensayo_2.md)** — **Ensayo II:** *¿Una teoría lingüística del valor?* | *Págs. impresas 195–209 (PDF 187–201)*
  * *Incluye:* Las interacciones lingüísticas como soporte de relaciones de poder simbólico · Poder oblicuo y metafórico.
* **[`13_parte2_ensayo_3.md`](md/13_parte2_ensayo_3.md)** — **Ensayo III:** *Una incursión en la estética* | *Págs. impresas 211–229 (PDF 202–220)*
  * *Incluye:* Una estética · Pérdida o extravío del aura.

### Tercera Parte: Una visión del significante-signo y del lenguaje
* **[`14_parte3_ensayo_1.md`](md/14_parte3_ensayo_1.md)** — **Portadilla Tercera Parte + Ensayo I:** *Caminos de la semiótica* | *Págs. impresas 233–258 (PDF 222–246)*
  * *Incluye:* La implicación significante-signo-sentido-lenguaje · El significante-signo como pliegue · La construcción simbólica · Lenguaje y hegemonía · El sentido como performativo.
* **[`15_parte3_ensayo_2.md`](md/15_parte3_ensayo_2.md)** — **Ensayo II:** *Los fantasmas del sentido: en el giro hermenéutico de la semiótica* | *Págs. impresas 259–278 (PDF 247–266)*
  * *Incluye:* Hermenéutica y reconstrucción · Hermes, el ladrón · Por una semiótica hermenéutica · Una aproximación a la opacidad.
* **[`16_parte3_ensayo_3.md`](md/16_parte3_ensayo_3.md)** — **Ensayo III:** *El mito: pasaje narrativo del significante-signo al símbolo* | *Págs. impresas 279–295 (PDF 267–283)*
  * *Incluye:* Simbolizar: ¿una tarea del lenguaje? · La interpretación, o la comprensión de un significante-signo que se hace símbolo · El mito como agenciamiento · El sentido fuera del sentido.

### Cuarta Parte: Subjetividad, dispositivos y mass-media
* **[`17_parte4_ensayo_1.md`](md/17_parte4_ensayo_1.md)** — **Portadilla Cuarta Parte + Ensayo I:** *Massmediática y construcción de subjetividad* | *Págs. impresas 299–321 (PDF 285–306)*
  * *Incluye:* La subjetividad: heterogénesis descentrada del sujeto · Massmediática: una lógica de sentido.
* **[`18_parte4_ensayo_2.md`](md/18_parte4_ensayo_2.md)** — **Ensayo II:** *La subjetividad massmediática* | *Págs. impresas 323–341 (PDF 307–325)*
  * *Incluye:* Las marcas de los signos massmediáticos · Entre operadores y operaciones.
* **[`19_parte4_ensayo_3.md`](md/19_parte4_ensayo_3.md)** — **Ensayo III:** *TV: ¿Dispositivo o aparato?* | *Págs. impresas 343–371 (PDF 326–354)*
  * *Incluye:* TV: Un collage de lo social y un tinglado de sentido · La forma y lo sagrado · La superabundancia del signo mediático.
* **[`20_parte4_ensayo_4.md`](md/20_parte4_ensayo_4.md)** — **Ensayo IV:** *Entonces lo mediático: Manual para ver TV* | *Págs. impresas 373–377 (PDF 355–359)*

### Quinta Parte: De la opinión pública a las democracias mass-mediáticas
* **[`21_parte5_ensayo_1.md`](md/21_parte5_ensayo_1.md)** — **Portadilla Quinta Parte + Ensayo I:** *La mediática en la hegemonía de la producción inmaterial* | *Págs. impresas 381–405 (PDF 361–384)*
  * *Incluye:* Una lectura de la opinión pública como régimen · Aún Marx · Por qué el poder de la mediática · La sobredeterminación mediática de la producción inmaterial.
* **[`22_parte5_ensayo_2.md`](md/22_parte5_ensayo_2.md)** — **Ensayo II:** *La sociedad mediática* | *Págs. impresas 407–424 (PDF 385–402)*
  * *Incluye:* El predominio del significante en la forma-signo · La colonización de la democracia.
* **[`23_parte5_ensayo_3.md`](md/23_parte5_ensayo_3.md)** — **Ensayo III:** *La massmediatización de la política: su devenir hoy* | *Págs. impresas 425–454 (PDF 403–432)*
  * *Incluye:* La banalización de la política: una tecnología del biopoder · La massmediática y los procesos de desintegración · Problemas de legitimación en las democracias mediáticas · El aura no desaparece, se desplaza.
* **[`24_parte5_ensayo_4.md`](md/24_parte5_ensayo_4.md)** — **Ensayo IV:** *La mediática en su ocurrencia política* | *Págs. impresas 455–469 (PDF 433–447)*
  * *Incluye:* La mediática como dispositivo de captura · Líneas de fuga a la máquina total del sentido hegemónico.

### Sexta Parte: La apuesta por la distopía de las multitudes: hacia una refundación de la política
* **[`25_parte6_ensayo_1.md`](md/25_parte6_ensayo_1.md)** — **Portadilla Sexta Parte + Ensayo I:** *Subjetividad y política: del consenso a la voluntad política de la multitud* | *Págs. impresas 473–495 (PDF 449–470)*
  * *Incluye:* Otra idea de Estado: entre lo efímero y lo permanente · La aporía del proceso constituyente: una nueva subjetividad política.
* **[`26_parte6_ensayo_2.md`](md/26_parte6_ensayo_2.md)** — **Ensayo II:** *De la revuelta a la reinvención del pueblo* | *Págs. impresas 497–526 (PDF 471–500)*
  * *Incluye:* Adiós a la sociedad civil · La resistencia, o el poder constituyente del pueblo.
* **[`27_parte6_ensayo_3.md`](md/27_parte6_ensayo_3.md)** — **Ensayo III:** *El final de la mosca: la tela arácnida al hilo del cuerpo-potencia* | *Págs. impresas 527–559 (PDF 501–531)*

### Epílogo, Post-scriptum y Aparato Crítico
* **[`28_epilogo.md`](md/28_epilogo.md)** — **Epílogo:** *¿Se pueden cartografiar los mass-media?* | *Págs. impresas 561–584 (PDF 533–555)*
  * *Incluye:* Tejiendo ciertas inquietudes · Mediática para principiantes: Un alfabeto de signos incompletos (`A`–`Z`).
* **[`29_post_scriptum.md`](md/29_post_scriptum.md)** — **Post-scriptum:** *Por el socialismo (Con un ensayo de Javier Biardeau: Entre dinosaurios y unicornios)* | *Págs. impresas 587–618 (PDF 557–588)*
  * *Incluye:* Primer movimiento: Homenaje a la memoria · Segundo movimiento: Sobre lo escrito · Tercer movimiento: *Entre dinosaurios y unicornios. Un ensayo de Javier Biardeau*.
* **[`30_bibliografia.md`](md/30_bibliografia.md)** — **Bibliografía** | *Págs. impresas 621–641 (PDF 590–609)*
* **[`31_glosario.md`](md/31_glosario.md)** — **Glosario** (*La caja de herramientas conceptual*) | *Págs. impresas 643–687 (PDF 611–655)*
* **[`32_indice_onomastico.md`](md/32_indice_onomastico.md)** — **Índice Onomástico** | *Págs. impresas 691–699 (PDF 657–665)*
