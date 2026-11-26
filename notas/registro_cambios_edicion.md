# Registro Editorial de Cambios — Segunda Edición (`2006 → Segunda Edición`)

Registro exclusivo de **cambios sustantivos sobre la obra** (estructura, contenido, aparato crítico y corrección de erratas respecto a la Primera Edición de Caracas, 2006), separado de los hitos técnicos del repositorio ([`CHANGELOG.md`](../CHANGELOG.md)).

**Doble finalidad:**
1. Servir de base para emitir un **reporte editorial de cambios** (para el autor, la editorial o el lector especializado).
2. Alimentar, al cierre editorial, la redacción de una **nota editorial o anexo publicable** dentro del propio libro.

> **Decisión confirmada de estructura y diseño:** El título y ubicación definitivos dentro de la obra son ***Anexo editorial: Relación de cambios respecto a la Primera Edición (2006)***, incorporado como **anexo de cierre** al final del volumen en [`libro/anexo_cambios_segunda_edicion.md`](../libro/anexo_cambios_segunda_edicion.md) (`id: "A1"`, `tipo: "anexo"` en [`libro.yaml`](../libro.yaml)). Este archivo (`notas/registro_cambios_edicion.md`) funciona como su bitácora detallada de trabajo; cada cambio relevante se documenta aquí y se sintetiza en prosa publicable dentro de `libro/anexo_cambios_segunda_edicion.md`.

---

## 1. Criterios Rectores de esta Segunda Edición

* **Actualización híbrida sin borrado de la memoria de 2006:** Los desarrollos contemporáneos (plataformas digitales, algoritmos, hiperconectividad e inteligencia artificial) se tejen orgánicamente en el cuerpo de los ensayos sin suprimir los argumentos históricos de 2006, abriendo subapartados nuevos ante giros históricos mayores.
* **Anclaje temporal:** Las cifras y ejemplos de 2006 se preservan como hito genealógico y se contrastan con el horizonte contemporáneo verificado.
* **Conservación íntegra de textos invitados de 2006:** Los cuatro prólogos de la Primera Edición (Michel Maffesoli, Rigoberto Lanz, Nelson Guzmán y Magaldy Téllez) y el ensayo invitado de Javier Biardeau en el *Post-scriptum* (*Tercer movimiento: Entre dinosaurios y unicornios*) se conservan intactos como testimonio histórico de la edición original.

---

## 2. Cambios Estructurales y de Índice

### [E-01] Integración del antiguo *Liminar* de Michel Maffesoli como *Pro(Logos) I* y separación de la sección de apertura
* **Alcance:** Estructura editorial del libro ([`libro.yaml`](../libro.yaml)), sin alteración del texto de los ensayos (`0` palabras modificadas).
* **Antecedente en la Primera Edición (2006):** El texto de Michel Maffesoli (*La belleza con agudeza y rigor*) se incorporó cuando la maquetación y la foliación de 2006 ya estaban cerradas, por lo que fue intercalado sin numeración de páginas entre *Agradecimientos* (pág. 12) y *Pro(Logos)* (pág. 15) bajo el título «Liminar» y **quedó omitido del Índice General original**.
* **Cambio realizado en la Segunda Edición:**
  1. Se creó la sección específica **`Pro(Logos) (Primera Edición, 2006)`** (`prologos_2006`) que agrupa en igualdad jerárquica los **cuatro prólogos invitados** de la edición original:
     * **Pro(Logos) I:** Michel Maffesoli — *La belleza con agudeza y rigor* *(archivo estable `03_liminar.md`)*.
     * **Pro(Logos) II:** Rigoberto Lanz — *Comunicación: El clímax de la era posmoderna* *(antes Pro(Logos) I)*.
     * **Pro(Logos) III:** Nelson Guzmán — *Los nuevos mundos simbólicos* *(antes Pro(Logos) II)*.
     * **Pro(Logos) IV:** Magaldy Téllez — *Trayectos claves para pensar el socialismo como pasión* *(antes Pro(Logos) III)*.
  2. Se separaron los **Preliminares** (`00`–`02`: créditos, índice y agradecimientos) de la nueva sección **`Apertura y Preámbulo`** (`apertura`), que aloja el *Preámbulo* del autor (`07_preambulo.md`) y deja dispuesto el espacio editorial para el futuro *Prefacio a la Segunda Edición*.
* **Impacto para el lector:** Corrige la omisión histórica del prólogo de Michel Maffesoli en el Índice General y delimita con claridad los prólogos de 2006 frente a la apertura del autor en la Segunda Edición.

### [E-02] Incorporación del *Anexo editorial: Relación de cambios respecto a la Primera Edición (2006)* como anexo de cierre
* **Alcance:** Nuevo archivo [`libro/anexo_cambios_segunda_edicion.md`](../libro/anexo_cambios_segunda_edicion.md) declarado en [`libro.yaml`](../libro.yaml) (`id: "A1"`, `tipo: "anexo"`, sección `cierre`, tras `32_indice_onomastico.md`) sin prefijo numérico bajo la Opción A.
* **Propósito:** Informar explícitamente al lector los criterios editoriales, las reorganizaciones de estructura, las actualizaciones de contenido por capítulo y las correcciones de aparato crítico respecto a la edición de 2006.
* **Mantenimiento:** Se actualiza de forma incremental con cada cambio estructural y cada capítulo aprobado, y pasa a revisión final del autor en el cierre editorial.

---

## 3. Actualizaciones y Ampliaciones de Contenido por Capítulo

*(Registrar aquí cada capítulo aprobado en `libro.yaml`: qué argumentos se ampliaron, qué autores/fuentes nuevas ingresaron y qué subapartados se añadieron.)*

* *(Aún sin capítulos de contenido aprobados — se completará progresivamente capítulo por capítulo.)*

---

## 4. Aparato Crítico, Erratas de 2006, Bibliografía y Glosario

*(Registrar aquí las erratas sistemáticas saneadas, la resolución de las 7 omisiones de notas al pie de la edición impresa de 2006, los nuevos términos del Glosario y la ampliación bibliográfica.)*

* *(Pendiente de aplicación progresiva por capítulo y consolidación al cierre editorial.)*
