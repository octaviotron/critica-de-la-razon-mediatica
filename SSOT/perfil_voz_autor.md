# SSOT: Perfil Empírico de Voz del Autor y Léxico Conceptual

**Obra:** *Crítica de la Razón Mediática* — **Juan Barreto Cipriani**  
**Propósito:** Proveer a cualquier agente de IA una referencia concreta del registro ensayístico real del autor, los anti-patrones de prosa sintética a evitar y el inventario completo de los **92 términos definidos en el Glosario** (`libro/31_glosario.md`). Complementa [`SSOT/guia_estilo_editorial.md`](guia_estilo_editorial.md).

---

## 1. Poética Explícita del Autor (extraída de `libro/07_preambulo.md`)

En *El drama de la escritura* (`libro/07_preambulo.md`), Juan Barreto define explícitamente cómo concibe su escritura y su diálogo con las fuentes:
* **El ensayo como forma:** escribe en un registro *doble, crítico y jubiloso* (citando a Adorno y Savater), alejado del manual escolástico, del informe técnico y de la escritura burocrática.
* **Las fuentes como «tribu» / «mosaico»:** siguiendo el comentario de Hannah Arendt sobre Walter Benjamin, los autores citados no se incrustan como fichas de catálogo aisladas, sino que concurren en diálogo orgánico dentro de una misma trama argumental.

---

## 2. Rasgos Característicos de la Prosa de Juan Barreto

1. **Sintaxis periódica y filosófica:** prefiere párrafos largos y rítmicos que despliegan una idea por capas mediante subordinadas, incisos aclaratorios y giros propios (*«Es, pues, …»*, *«Y es que …»*, *«En la medida en que …»*, *«Lo que podríamos denominar …»*, *«No se trata únicamente de… sino del desplazamiento…»*).
2. **Interrogaciones retóricas como bisagras:** abre o cierra bloques con preguntas filosófico-políticas que preparan el movimiento siguiente (*«¿Qué se pone en juego en este replanteamiento?»*).
3. **Articulación orgánica de tradiciones:** entrelaza el vocabulario del posestructuralismo y la teoría crítica (*dispositivo*, *pliegue*, *rizoma*, *líneas de fuga*, *semiosis social*, *aura*, *biopolítica*, *subjetividad*) con categorías materialistas y políticas (*metabolismo del capital*, *acumulación*, *poder constituyente*, *sujetos subordinados*, *socialismo*).
4. **Compuestos conceptuales con guion:** crea y sostiene pares tensionales (`significante-signo`, `cuerpo-potencia`, `rostro-proceso`, `trabajo-valor`, `hecha-en-común`, `ético-política`, `mass-media`). Nunca simplificarlos ni retirar sus guiones.

### Cuatro párrafos modelo del propio libro (referencia de tono y cadencia)

* **Apertura ensayística y manejo de fuentes (`libro/07_preambulo.md`):**
  > Este libro ha sido escrito como un compendio de ensayos, es decir, una “forma” que, en palabras de Adorno, nos permite «inflamarnos sin escrúpulos […] apelando a la fortuna y al juego, que son esenciales», para la creación. Y, también, ser escépticos, ya que «el dogmático no ensaya»…

* **Economía política y diálogo con autores (`libro/08_parte1_ensayo_1.md`):**
  > L. Boltanski y E. Chiapello, nos hablan de una necesaria redefinición «mínima del capitalismo» y proponen retener esta fórmula: «La exigencia de acumulación ilimitada del capital mediante medios formalmente pacíficos», lo que sugiere una afiliación más o menos voluntaria de los sujetos actores al modelo de transformación constante del capital como proyecto autónomo. Es, pues, el desapego vergonzoso e infeliz que muestra el capital respecto de las formas materiales de la riqueza, lo que le otorga su carácter verdaderamente abstracto, por el que se reproduce la acumulación.

* **Análisis de dispositivos y semiosis (`libro/19_parte4_ensayo_3.md`):**
  > El antagonismo de los agentes y sus dispositivos de auto-referencia, al interior de la semiosis social, crean un sentido efímero que se recompone en la recuperación de discursos oficiales y contextos residuales que absorben todo lo social en su gramática. La institución total de los medios es aquí un dispositivo no lineal de ordenación de los roles convencionales de los discursos…

* **Horizonte político-subjetivo (`libro/25_parte6_ensayo_1.md`):**
  > En una época de desencanto en la política, la recuperación de nuevas formas [de] la pasión política desde los sujetos subordinados, es un hecho. Aquello que generan los medios creando una teledemocracia y su control sobre los sujetos está en riesgo por el desencadenamiento de la desterritorialización y el surgimiento de espacios lisos…

---

## 3. Anti-Patrones de Prosa de IA Prohibidos en Este Libro

Al redactar adiciones, transiciones 2006 → actualidad o comentarios sobre nuevos autores, **evitar estrictamente**:
1. **Aperturas y muletillas de molde:** *«En el vertiginoso mundo actual…»*, *«En la era digital contemporánea…»*, *«Cabe destacar que…»*, *«Es importante señalar que…»*, *«En este sentido…»*, *«En última instancia…»*, *«En conclusión, podemos afirmar que…»*.
2. **Antítesis mecánicas repetitivas:** abusar de la fórmula *«No se trata solo de X, sino de Y»* o *«Más que un simple A, es un verdadero B»* en párrafos consecutivos.
3. **Esquematización de informe o presentación:** convertir la prosa ensayística en listas con viñetas con títulos en negrita (`- **Aspecto 1:** ...`) cuando el capítulo fluye en párrafos argumentativos (salvo en capítulos que ya son enumerativos, como los 40 puntos de `20_parte4_ensayo_4.md` o el alfabeto de `28_epilogo.md`).
4. **Tono neutro de manual o cierre moralizante:** suavizar la crítica materialista/política del autor con cierres tipo *«debemos encontrar un equilibrio ético entre innovación y responsabilidad»*.
5. **Presentación escolar de autores nuevos:** evitar *«El filósofo surcoreano Byung-Chul Han, nacido en 1959, plantea en su libro…»*; integrarlos directamente en la discusión conceptual como parte de la «tribu» teórica del texto (*«Como advierte É. Sadin al examinar el giro conminatorio de la técnica…»*).

---

## 4. Inventario Completo de los 92 Términos del Glosario (`libro/31_glosario.md`)

Antes de usar, redefinir o añadir variantes de cualquiera de estos 92 conceptos ya definidos por Juan Barreto en `libro/31_glosario.md`, consultar su acepción exacta mediante `python3 -B scripts/edicion/buscar_libro.py --glosario <término>`:

> **A–C:** Acontecimiento · Actualidad · Afección · Agenciamientos · Agujeros negros · Amo · Arte · Aura · Banalización · Biopoder · Biopolítica · Campo · Campo Cultural · Campo semiótico · Capital · Capitalismo · Cibercultura · Condición epocal · Consenso · Cuerpo · Cuerpo sin órganos · Cultura de masas  
> **D–H:** Deconstrucción · Democracia · Descentramiento · Deseo · Devenir · Diferencia · Discurso · Dispositivo · Estado · Estriado · Ética · Fractal · Gel mediático · Gusto · Hegemonía · Hermenéutica · Hiperrealidad  
> **I–M:** Imagen · Imaginario · Imperialismo · Imperio · Industria Cultural · Información-Comunicación · Internet · Lenguaje · Límite y exceso · Líneas de fuga · Lógica de sentido · Máquina · Máquina mediática · Mediación mediática · Mercado · Mercancía · Mito · Modo · Múltiple · Multitud  
> **O–R:** Opacidad · Opinión pública · Performatividad · Poder · Poder constituyente · Pliegue · Plusvalía · Política · Posmodernidad · Pueblo · Randomizar · Razón instrumental · Resistencia · Rizoma  
> **S–V:** Saber · Semiosis social · Semiótica · Sensibilidad · Signo · Símbolo · Simulacro · Sobrepliegue · Socialismo · Sociedad de control · Subjetividad · Sustancia · Teoría del valor · Totalización · Trabajo · Trabajo inmaterial · Tribus urbanas · Virtual · Voluntad de poder
