# SSOT: Guía Metodológica para la Edición y Creación de la Segunda Edición (Autor con IA de Voz + Control de Versiones)

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Asesor Informático:** Octavio Rossell Tabet (<octavio.rossell@gmail.com> — https://github.com/octaviotron)  
**Propósito:** Establecer las reglas operativas, editoriales y técnicas (Recomendaciones 2, 3 y 4) para articular el trabajo del autor (mediante dictado y notas en un dispositivo IA de voz) con la gestión de versiones y edición estructurada en Markdown y Git.

---

## 1. Reglas de Oro y Protocolo para el Dispositivo IA de Voz del Autor (Recomendación 2)

El autor cuenta con un dispositivo IA que procesa la voz en alta calidad, lo que le permite dictar modificaciones en voz alta o grabar notas conceptuales sin necesidad de manejar herramientas informáticas ni Git. Para proteger la densidad conceptual de la obra (~198,000 palabras y 513 notas al pie) y evitar que la IA altere el estilo filosófico del autor, se aplican las siguientes tres reglas operativas:

### 1.1. Uso de Etiquetas de Párrafo `[CC.PPP]` sobre la Versión de Lectura en PDF
* El autor trabaja sobre el **PDF de Lectura Etiquetado** (ubicado en `versiones/Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf`), donde cada párrafo lleva al inicio un identificador único con el formato **`[CC.PPP]`**:
  * **`CC`** indica el número de capítulo (`00` a `32`, correspondiente al archivo en `libro/`).
  * **`PPP`** indica el número correlativo de párrafo o bloque dentro de ese capítulo (`001`, `002`, `003`...).
  * **`[CC.NXX]`** identifica cada nota al pie al final del capítulo (ej. `[08.N01]`).
* **Regla de oro:** El autor **nunca debe pedirle a su dispositivo IA que reescriba un capítulo entero de golpe**, ya que los modelos de lenguaje tienden a resumir argumentos complejos, aplanar el registro estilístico y perder llamadas a notas al pie (`[^n]`). En su lugar, el autor dicta **intervenciones ancladas al código `[CC.PPP]`**.

### 1.2. Configuración del "Prompt Base" en el Dispositivo IA del Autor
Se recomienda configurar como instrucción fija (System Prompt) en el dispositivo de voz del autor el siguiente texto:

> *"Actúa como asistente editorial del profesor Juan Barreto Cipriani para la preparación de la segunda edición de su libro 'Crítica de la Razón Mediática'. Cuando dicte en voz alta sigue estrictamente estas reglas:*
> *1. Corrige únicamente muletillas del habla oral y signos de puntuación, pero conserva intacto mi estilo académico y mi vocabulario filosófico (massmediática, biopolítica, biopoder, agenciamiento, significante-signo, cuerpo-potencia, rizoma, pliegue, líneas de fuga, subjetividad, performativo, habitus).*
> *2. Nunca resumas ni recortes mis ideas.*
> *3. Estructura cada nota dictada con esta ficha:*
> *- **Ubicación:** [Código de capítulo y párrafo dicho por el autor, ej. 08.014, o título de sección]*
> *- **Acción solicitada:** [Reemplazar párrafo / Insertar después / Agregar nota al pie / Idea para desarrollar / Nuevo término para el Glosario]*
> *- **Texto dictado:** [Transcripción limpia y fiel de lo dictado]"*

### 1.3. Separación en Dos Modos de Dictado por Voz
1. **Modo A — Dictado Literal de Edición (Reemplazo, Inserción o Adenda):**
   * Cuando el autor tiene redactada mentalmente la frase o el párrafo definitivo que desea insertar o sustituir en un punto específico (`[CC.PPP]`).
   * Ejemplo de dictado: *"Ubicación: párrafo 08 punto 014. Acción: insertar después de este párrafo. Texto: Veinte años después de la publicación original, el dispositivo información-comunicación ya no opera únicamente mediante la pantalla televisiva, sino a través de la captura algorítmica..."*.
2. **Modo B — Lluvia de Ideas y Notas Conceptuales (Para desarrollo asistido):**
   * Cuando el autor desea dejar asentada una reflexión o directriz temática en voz alta sin preocuparse por la redacción final.
   * Ejemplo de dictado: *"Nota conceptual para el capítulo 19 sobre la TV: aquí necesito desarrollar cómo la televisión fue desplazada por las redes sociales y el teléfono inteligente como prótesis del cuerpo"*.
   * Estas notas del Modo B se reciben en `versiones/v2.0_en_proceso/notas_autor/`, donde el asesor informático utiliza la IA del entorno de edición para elaborar una propuesta redactada con el estilo exacto del autor en ese capítulo y someterla a su aprobación en la siguiente versión del PDF de lectura (`v1.1`, `v1.2`, etc.).

---

## 2. Estrategia Editorial (2006 → 2026) para la Segunda Edición (Recomendación 3)

Dado que la primera edición fue publicada en **2006**, se propone una estrategia de actualización en **cuatro frentes modulares** que aprovechan al máximo la fluidez del dictado por voz sin desarticular el aparato crítico existente:

### 2.1. Nuevo Estudio Introductorio o "Prefacio a la Segunda Edición (Veinte Años Después)"
* Es el espacio ideal para que el autor dicte con total libertad en su dispositivo de voz un ensayo preliminar donde dialogue con su obra de 2006 desde el horizonte contemporáneo (inteligencia artificial, plataformas digitales, hipervigilancia, redes sociales y nuevas disputas biopolíticas).
* Al ser un capítulo nuevo e independiente (ej. `03b_prefacio_segunda_edicion.md`), el autor puede dictarlo de corrido sin preocuparse por alterar la numeración de notas al pie de los capítulos posteriores.

### 2.2. Actualización por "Cápsulas o Adendas" en Capítulos Estratégicos
En lugar de desmontar párrafos que contienen múltiples citas bibliográficas y llamadas a notas al pie de 2006, se recomienda priorizar inserciones o subsecciones nuevas al cierre de los apartados tecnológicos y mediáticos clave:
* **[`libro/07_preambulo.md`](../libro/07_preambulo.md)** (*Profecías y realidades tecnológicas* y *La era de las conexiones*): contraste entre las proyecciones tecnológicas de 2006 y la consolidación actual de la computación ubicua, la nube y la IA generativa.
* **[`libro/08_parte1_ensayo_1.md`](../libro/08_parte1_ensayo_1.md)** (*Crisis de la teoría del valor y nuevo dispositivo información-comunicación*): actualización sobre trabajo digital, extractivismo de datos y valorización algorítmica.
* **[`libro/19_parte4_ensayo_3.md`](../libro/19_parte4_ensayo_3.md)** y **[`libro/20_parte4_ensayo_4.md`](../libro/20_parte4_ensayo_4.md)** (*TV: ¿Dispositivo o aparato?* y *Manual para ver TV*): transición del régimen televisivo al régimen de pantallas móviles, *streaming* y plataformas de micro-video.
* **[`libro/21_parte5_ensayo_1.md`](../libro/21_parte5_ensayo_1.md)** a **[`libro/24_parte5_ensayo_4.md`](../libro/24_parte5_ensayo_4.md)** (*De la opinión pública a las democracias mass-mediáticas*): cámaras de eco, posverdad, micro-segmentación política y guerra cognitiva.

### 2.3. Ampliación de la "Caja de Herramientas" ([`libro/31_glosario.md`](../libro/31_glosario.md)) mediante Micro-Sesiones de Voz
* El Glosario original reúne 94 conceptos breves. Su formato diccionario (`· Término: Definición...`) se adapta de manera óptima al dictado por voz.
* El autor puede grabar cápsulas cortas de 2 a 5 minutos definiendo nuevos conceptos para la segunda edición (por ejemplo: *Algoritmo*, *Big Data*, *Biopolítica digital*, *Enjambre*, *Extractivismo atencional*, *Inteligencia Artificial*, *Plataforma*).

### 2.4. Corrección Técnica de Erratas Tipográficas de la Primera Edición
* Las erratas de imprenta detectadas en el PDF original de 2006 (como caracteres ausentes en la fuente Garamond de 1998 —ej. `S.  i ek` por `S. Žižek`— o erratas en títulos del índice como `preformativo` por `performativo`) serán corregidas de forma sistemática y documentada por el asesor informático mediante scripts, liberando al autor de esa carga mecánica.

---

## 3. Organización Técnica de Versiones, Historial y Flujo en Git (Recomendación 4)

Para mantener un control riguroso de cada modificación, conservar intacta la versión original y disponer de un historial completo de versiones entregables al autor, el proyecto implementa la siguiente arquitectura en [`versiones/`](../versiones/) y Git:

### 3.1. Estructura de la Carpeta [`versiones/`](../versiones/)
* **`versiones/Critica_de_la_Razon_Mediatica_Lectura_vX.Y.pdf`**: Archivos PDF de lectura numerados según la versión (`v1.0`, `v1.1`, `v1.2`, ..., `v2.0`), con etiquetas `[CC.PPP]` al inicio de cada párrafo para revisión del autor.
* **`versiones/v1.0_original/`**: Respaldo congelado e inmutable de la primera conversión (`v1.0`, correspondiente al 100% del texto de la 1.ª edición de 2006). Contiene en `md/` la copia exacta de los 33 archivos Markdown originales y su manifiesto de control, sirviendo como línea base permanente para comparar cualquier versión futura.
* **`versiones/v2.0_en_proceso/`**:
  * `notas_autor/`: Bandeja de entrada donde se archivan por fecha y capítulo las transcripciones o notas de voz enviadas por el autor desde su dispositivo IA (ej. `2026-11-10_cap08_notas.md`).
  * `borradores_md/`: Espacio de preparación de capítulos en revisión.
  * `bitacora_cambios.md`: Registro cronológico de todas las modificaciones aplicadas en cada versión (`v1.1`, `v1.2`, etc.).
* **`versiones/historial_cambios/`**: Almacena los reportes automáticos de diferencias (`diff`) entre `v1.0_original` y cada nueva versión generada.

### 3.2. Ciclo de Trabajo por cada Entrega del Autor
1. **Recepción:** El autor envía las notas dictadas en su dispositivo IA indicando los códigos `[CC.PPP]`. El archivo se guarda en `versiones/v2.0_en_proceso/notas_autor/`.
2. **Aplicación y Registro:** Se aplican los cambios en los archivos correspondientes de `libro/`, se documenta la intervención en `versiones/v2.0_en_proceso/bitacora_cambios.md` y se realiza un `git commit` en español describiendo el capítulo y los párrafos actualizados.
3. **Generación de Nueva Versión de Lectura en PDF:** Se ejecuta `python3 scripts/04_generar_pdf_lectura.py --version v1.X` para producir el nuevo PDF numerado en `versiones/Critica_de_la_Razon_Mediatica_Lectura_v1.X.pdf` y entregárselo al autor.
4. **Cierre de Índices al Finalizar la Edición:** Una vez aprobada la versión definitiva (`v2.0`), se regeneran automáticamente [`libro/01_indice.md`](../libro/01_indice.md), [`libro/30_bibliografia.md`](../libro/30_bibliografia.md) y [`libro/32_indice_onomastico.md`](../libro/32_indice_onomastico.md) para reflejar las nuevas secciones, obras citadas y paginación final.
