# SSOT: Flujo Editorial de la Segunda Edición (Edición Asistida por IA, Capítulo por Capítulo)

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Asesor Informático:** Octavio Rossell Tabet (<octavio.rossell@gmail.com> — https://github.com/octaviotron)  
**Propósito:** Establecer el flujo editorial simple, centrado en editar los archivos `.md` de [`libro/`](../libro/) con asistencia de IA, someter cada capítulo a revisión y aprobación del autor, minimizar el uso manual de comandos CLI y preservar un respaldo inmutable de la primera edición en [`respaldo_v1.0/`](../respaldo_v1.0/).

> **Inicio rápido para agentes nuevos:** La regla universal siempre activa vive en [`AGENTS.md`](../AGENTS.md) y los procedimientos paso a paso en las 4 Skills de [`.agents/skills/`](../.agents/skills/) (`editar-capitulo`, `procesar-externos`, `cierre-editorial`, `mantenimiento-proyecto`). Consulta [`SSOT/README.md`](README.md) para ver qué archivos leer (y cuáles NO cargar) y revisa la normativa en [`SSOT/guia_estilo_editorial.md`](guia_estilo_editorial.md) y [`SSOT/perfil_voz_autor.md`](perfil_voz_autor.md).

---

## 1. Principios del Flujo de Trabajo

1. **Edición directa y secuencial (`libro/`):** Los capítulos Markdown en [`libro/`](../libro/) son la única copia viva del texto. Se trabaja **un capítulo `.md` a la vez** (o máximo dos mientras se espera respuesta del autor).
2. **Mínima fricción técnica (cero burocracia CLI):** El usuario no necesita memorizar comandos, scripts, `Makefile`, ramas complejas ni *tags* obligatorios. Los scripts de [`scripts/edicion/`](../scripts/edicion/) actúan como **herramientas internas que la IA ejecuta bajo demanda** cuando se le pide en lenguaje natural (validar notas, compilar un capítulo en PDF/Word para el autor, ver avance o actualizar el índice).
3. **Git simple y lineal:** Se trabaja directamente sobre `main`. Al aprobarse cada capítulo el usuario realiza **un commit + push** claro (por ejemplo `cap 08 aprobado`). Las etiquetas (*tags*) y ramas adicionales son opcionales; el agente **no** crea ramas ni tags y **no** ejecuta `git commit` ni `git push` sin instrucción expresa.
4. **Orden y avance centralizados en [`libro.yaml`](../libro.yaml) (Opción A):** Los nombres de archivo existentes en `libro/` (`00_preliminares.md` … `32_indice_onomastico.md`) se conservan como **identificadores estables**; el orden del índice, las partes y el `estado` de cada capítulo (`pendiente` | `en_revision` | `aprobado`) viven en [`libro.yaml`](../libro.yaml). Un capítulo solo pasa a `"aprobado"` tras confirmación explícita del usuario.
5. **Separación clara entre pendientes/seguimiento ([`notas/`](../notas/)) e historial cerrado ([`CHANGELOG.md`](../CHANGELOG.md)):** En [`notas/`](../notas/) viven las ideas/pendientes globales ([`NOTAS.md`](../notas/NOTAS.md)), la panorámica de la obra ([`mapa_obra.md`](../notas/mapa_obra.md)), la bitácora detallada de cambios al libro ([`registro_cambios_edicion.md`](../notas/registro_cambios_edicion.md)), las fichas espejo por ensayo ([`notas/capitulos/`](../notas/capitulos/)) y el catálogo/fichas de bibliografía externa ([`notas/fuentes/`](../notas/fuentes/)). [`CHANGELOG.md`](../CHANGELOG.md) registra únicamente capítulos ya *aprobados* e hitos técnicos completados.
6. **Respaldo inmutable de la 1.ª edición ([`respaldo_v1.0/`](../respaldo_v1.0/)):** Conserva congelados los 33 archivos originales de 2006 y su manifiesto estructural (`respaldo_v1.0/libro.yaml`) para tener siempre una referencia exacta y poder compilar la 1.ª edición (`v1.0.0`) aunque cambien los archivos de `libro/` o la estructura del índice.
7. **Artefactos compilados fuera de Git (`dist/`):** Los PDFs y archivos Word (`.docx`) generados para lectura/revisión del autor se escriben en `dist/`, carpeta excluida en [`.gitignore`](../.gitignore) (que además excluye el archivo local `notas/estado_sesion.md`, ver §2.2).

---

## 2. Ciclo Principal: Edición Capítulo por Capítulo

Todo el avance de la Segunda Edición se basa en repetir este ciclo simple:

```text
1. Elegir un archivo .md en libro/ y revisar sus notas en notas/capitulos/ (y notas/NOTAS.md)
        │
        ▼
2. Editar y actualizar el contenido con la IA (siguiendo SSOT/guia_estilo_editorial.md)
        │
        ▼
3. La IA valida ese capítulo y prepara la entrega al autor (PDF limpio en dist/ por defecto + resumen breve)
        │
        ▼
4. Revisión del autor ──► ¿Solicita cambios? ──► Sí ──► Registrar observaciones en notas/capitulos/
        │                                                 y volver al paso 2
        │ No (Capítulo aprobado)
        ▼
5. Cierre del capítulo (solo tras confirmación de aprobación del autor):
   • Marcar como resueltas (- [x]) las notas aplicadas en notas/capitulos/ y notas/NOTAS.md
   • Actualizar notas/mapa_obra.md, notas/registro_cambios_edicion.md y libro/anexo_cambios_segunda_edicion.md
   • Anotar nuevos pendientes de glosario/bibliografía en notas/NOTAS.md
   • Marcar estado: "aprobado" en libro.yaml y registrar el capítulo aprobado en CHANGELOG.md
   • 1 commit + push por el usuario (ej. "cap 08 aprobado")
        │
        ▼
6. Pasar al siguiente archivo .md
```

### Cómo operar en lenguaje natural con la IA (sin comandos manuales)
En cada etapa basta pedirle a la IA:
* **Al empezar un capítulo:** *"Lee `SSOT/guia_estilo_editorial.md` y actualiza `libro/19_parte4_ensayo_3.md` con estas orientaciones..."*
* **Para enviarlo al autor:** *"Valida el capítulo 19, genera su PDF limpio en `dist/` para el autor y dame un resumen breve de los cambios."* *(Si el autor pide Word `.docx` o PDF etiquetado `[ID.PPP]`, indícalo expresamente.)*
* **Al recibir comentarios del autor:** *"Aplica estas observaciones del autor sobre `libro/19_parte4_ensayo_3.md` y vuelve a generar el PDF del capítulo."*
* **Al aprobarse el capítulo:** *"El autor aprobó el capítulo 19; márcalo como aprobado en `libro.yaml` y regístralo en `CHANGELOG.md`."*
* **Para consultar avance:** *"Muéstrame el avance de los capítulos según `libro.yaml`."*
* **Al retomar en una conversación nueva:** *"Sigamos"* o *"¿cómo vamos?"* (el agente ejecuta `contexto_capitulo.py --estado`; ver §2.2).
* **Al añadir nueva bibliografía en `externos/`:** *"Añadí nuevos archivos en `externos/`, procésalos e indexa todo."*
* **Al buscar citas verificadas en `externos/`:** *"Busca qué dice Éric Sadin (o Harari / Palantir) sobre el cuerpo-pantalla y verifica las páginas exactas."*

### 2.1. Incorporación y Consulta de Bibliografía Externa (`externos/` → `notas/fuentes/`)
Para incorporar bibliografía contemporánea (PDFs, artículos HTML, TXT, MD, DOCX, EPUB) sin ejecutar comandos manuales ni saturar el contexto con libros completos:
1. **El usuario solo deposita los archivos en [`externos/`](../externos/)** (carpeta versionada de solo lectura) y avisa al agente en lenguaje natural.
2. **El agente ejecuta internamente** `python3 -B scripts/edicion/indexar_externos.py`, que procesa de forma incremental únicamente los archivos nuevos o modificados (por SHA-256), actualiza el índice local SQLite FTS5 en `dist/indice_externos/corpus.db` y agrega las entradas nuevas en [`notas/fuentes/catalogo.yaml`](../notas/fuentes/catalogo.yaml) sin sobrescribir campos ya curados.
3. **Fichado curado:** El agente inspecciona metadatos, créditos y tabla de contenidos mediante `buscar_externos.py --info` / `--leer`, completa en `notas/fuentes/catalogo.yaml` la cita en estilo europeo, postura de diálogo (`afin` | `dialogo_critico` | `critica` | `insumo_empirico`), temas y capítulos destino, y redacta la ficha resumida `notas/fuentes/<slug>.md` (enlazándola en [`notas/NOTAS.md`](../notas/NOTAS.md) si aplica).
4. **Auto-sincronización silenciosa en consulta:** `buscar_externos.py` verifica automáticamente si hay novedades en `externos/` (o si `corpus.db` aún no existe tras un `git clone`) y reindexa en segundo plano antes de buscar. Al editar un capítulo, permite extraer citas literales con **página exacta verificada**.

### 2.2. Higiene de Sesión y Memoria Mínima entre Conversaciones
El historial de una conversación se reenvía completo en cada turno, de modo que un chat largo tras cargar capítulos extensos (`07`, `10`, `19`, `26`, `27`) encarece cada paso. Para abrir conversaciones limpias sin perder continuidad:
1. **Una conversación nueva por capítulo:** al entregar o cerrar un capítulo (o cada 2–3 bloques en ensayos `> 50 KB`), abrir una sesión nueva o compactar el contexto antes de continuar.
2. **Retomar con `--estado`:** al empezar una sesión, ejecutar `python3 -B scripts/edicion/contexto_capitulo.py --estado`. Muestra `notas/estado_sesion.md`, el tablero de `libro.yaml` y el último registro de `notas/registro_cambios_edicion.md`. `--estado` y `--capitulo` son excluyentes (usar uno u otro).
3. **Estado de sesión (`notas/estado_sesion.md`):** archivo local, ignorado por Git (puede no existir tras un `git clone`; se crea bajo demanda), `<= 2,048 B`, que se **sobrescribe** sin acumular historial al terminar un bloque sustantivo, entregar un borrador, recibir observaciones o cerrar sesión (no en cada micro-edición). Solo apunta al trabajo en curso: **no** sustituye ni contradice a `notas/capitulos/` (observaciones del autor), `notas/registro_cambios_edicion.md` ni `CHANGELOG.md`; ante discrepancia prevalecen estos.
4. **Verificar por diff:** tras editar `libro/`, comprobar con `git diff libro/<archivo>.md` y `validar_libro.py --capitulo <id>` en lugar de releer el capítulo completo.
5. **Agrupar peticiones afines:** en rondas de correcciones o ajustes de maquetación, reunir varios cambios en un mismo mensaje.
6. **Recomendación de uso (no obligatoria, depende del entorno):** reservar el modelo más potente para planear intervenciones y redactar prosa en la voz del autor, y usar uno ligero para tareas mecánicas (validar, compilar, buscar citas, fichar libros, sincronizar documentación).

---

## 3. Cambios Futuros: Nuevos Capítulos y Reordenamiento del Índice

Cuando el proceso requiera incorporar ensayos nuevos o modificar el índice:

1. **Añadir un capítulo nuevo (ej. *Anexo editorial* o futuro *Prefacio a la Segunda Edición*):**
   * Se crea un archivo con nombre descriptivo en [`libro/`](../libro/) sin necesidad de prefijo numérico (ej. `libro/anexo_cambios_segunda_edicion.md` —ya creado con `id: "A1"`, `tipo: "anexo"` al cierre de la obra— o el futuro `libro/prefacio_segunda_edicion.md`).
   * Se registra en [`libro.yaml`](../libro.yaml) en la sección y posición deseadas con un `id` único y `estado` inicial, se añade al catálogo navegable [`libro/README.md`](../libro/README.md) y se crea su ficha en `notas/capitulos/<mismo_nombre>.md`.
   * Pasa exactamente por el mismo ciclo de la Sección 2 (edición con IA → revisión del autor → aprobación → commit/push).
2. **Cambiar el orden del índice o agrupar distinto las Partes:**
   * **No se renombran los archivos `.md` existentes** en `libro/` (así las comparaciones contra `respaldo_v1.0/md/` siguen funcionando sin fricción).
   * Se reordenan las entradas o secciones únicamente en [`libro.yaml`](../libro.yaml) y se refleja el orden vigente en [`libro/README.md`](../libro/README.md).
   * *Caso ya aplicado en la 2.ª edición:* el texto de Michel Maffesoli (`libro/03_liminar.md`, intercalado originalmente como «Liminar» sin foliar ni figurar en el Índice de 2006) se integró en [`libro.yaml`](../libro.yaml) dentro de la sección `prologos_2006` como **Pro(Logos) I** junto a Rigoberto Lanz (`II`), Nelson Guzmán (`III`) y Magaldy Téllez (`IV`), separando además la sección `apertura` para el futuro Prefacio y el Preámbulo (`07_preambulo.md`), sin renombrar ningún archivo.
   * Se le pide a la IA: *"Regenera `libro/01_indice.md` desde `libro.yaml` y compila el libro completo en `dist/` para revisión."*

---

## 4. Fase Final de Cierre Editorial (Una Sola Vez)

Mientras se editan los capítulos individuales **no** conviene tocar todavía el Índice General ni el Índice Onomástico. Una vez aprobados todos los capítulos:
1. **Bibliografía y Glosario:** Consolidar en [`libro/30_bibliografia.md`](../libro/30_bibliografia.md) y [`libro/31_glosario.md`](../libro/31_glosario.md) las obras y conceptos acumulados en [`notas/NOTAS.md`](../notas/NOTAS.md).
2. **Índice General y validación global:** Pedir a la IA regenerar `libro/01_indice.md` desde `libro.yaml`, validar notas al pie y enlaces en todo el libro, y compilar el manuscrito completo en `dist/`.
3. **Revisión final, Anexo editorial, Maquetación e Índice Onomástico:** Consolidar y someter a aprobación final del autor el [`libro/anexo_cambios_segunda_edicion.md`](../libro/anexo_cambios_segunda_edicion.md) (desde [`notas/registro_cambios_edicion.md`](../notas/registro_cambios_edicion.md)), compilar la maqueta editorial `LuaLaTeX` fiel al diseño de 2006 (`scripts/edicion/compilar_maqueta.py`, ver [`SSOT/guia_maquetacion_segunda_edicion.md`](guia_maquetacion_segunda_edicion.md)) y recalcular [`libro/32_indice_onomastico.md`](../libro/32_indice_onomastico.md) sobre el PDF definitivo (`scripts/edicion/recalcular_onomastico.py`).

---

## 5. Respaldo Inmutable de la Primera Edición (`respaldo_v1.0/`)

```text
respaldo_v1.0/
├── README.md           # Guía de uso, reglas de inmutabilidad y comandos
├── libro.yaml          # Manifiesto estructural congelado de la 1.ª edición (v1.0.0)
├── manifiesto_v1.0.md  # Huellas SHA-256 de los 33 archivos originales
└── md/                 # Copia testigo bit a bit de los 33 archivos de 2006
```

* **Inmutabilidad estricta:** Ningún script permite escribir dentro de `respaldo_v1.0/`, y jamás debe editarse manualmente.
* **Base depurada y sellada (`535` notas al pie, `0` cortes de formato):** Antes de iniciar cambios de contenido de la 2.ª edición, `respaldo_v1.0/md/` fue sellado tras depurar únicamente artefactos técnicos de conversión (saltos de línea, listas numeradas en caps. 13/20/28 y 27 enlaces/definiciones de notas al pie), preservando el **100.000% de integridad alfanumérica** frente al PDF de 2006 (`SSOT/proceso_conversion_pdf_a_md.md`, Sección 5.1). Las **7 advertencias heredadas** en el validador corresponden a **6 líneas de notas al pie** (que agrupan **7 omisiones reales** del impreso de 2006) más **1 asterisco impar** en `17_parte4_ensayo_1.md:L19` (detalladas en `SSOT/guia_estilo_editorial.md`).
* **Reproducibilidad garantizada:** Aunque cambien todos los archivos de `libro/` y el orden de `libro.yaml`, siempre se puede compilar la 1.ª edición intacta en `dist/` o auditarla al 100.000% contra el PDF original de 2006 (ver [`respaldo_v1.0/README.md`](../respaldo_v1.0/README.md)).

---

## 6. Referencia de Herramientas Internas (`scripts/`)

> Estos scripts están pensados para que los ejecute la IA automáticamente cuando lo necesites, aunque también pueden invocarse manualmente en cualquier momento.

### 6.1. Herramientas Activas de Edición (`scripts/edicion/`)

El catálogo oficial completo de los 11 scripts activos (`manifiesto.py`, `contexto_capitulo.py`, `validar_libro.py`, `compilar_pdf.py`, `compilar_maqueta.py`, `recalcular_onomastico.py`, `reporte_cambios.py`, `generar_indice.py`, `indexar_externos.py`, `buscar_externos.py` y `buscar_libro.py`), sus opciones CLI y requisitos del entorno se mantiene en un **único sitio** para evitar duplicaciones: **[`scripts/README.md`](../scripts/README.md)**.

> **Sincronización ante cambios del proyecto:** Siempre que se añada o modifique un script, directorio, función, Skill o paso del flujo editorial, activar la Skill [`.agents/skills/mantenimiento-proyecto/SKILL.md`](../.agents/skills/mantenimiento-proyecto/SKILL.md) para mantener alineados `AGENTS.md`, las 4 Skills, `SSOT/` y los 6 `README.md` sin contradicciones.

### 6.2. Pipeline Histórico de Extracción 2006 (`scripts/extraccion_v1/`)
Congelado para trazabilidad y auditoría reproducible de la 1.ª edición:
* [`scripts/extraccion_v1/01_extraer_xml.py`](../scripts/extraccion_v1/01_extraer_xml.py): Extrae el XML vectorial de las 666 páginas del PDF de 2006.
* [`scripts/extraccion_v1/02_convertir_a_md.py`](../scripts/extraccion_v1/02_convertir_a_md.py): Reproduce la conversión histórica en `dist/extraccion_v1_md/` (bloqueado sobre `respaldo_v1.0/` y protegido sobre `libro/`).
* [`scripts/extraccion_v1/03_auditar_integridad.py`](../scripts/extraccion_v1/03_auditar_integridad.py): Audita al 100.000% los caracteres alfanuméricos de `respaldo_v1.0/md/` contra el PDF de 2006.

---

## 7. Guía Temática de Actualización (2006 → Actualidad)

Como orientación editorial opcional al abordar cada capítulo con el autor:
1. **Prefacio a la Segunda Edición:** Capítulo nuevo e independiente (`libro/prefacio_segunda_edicion.md`) sobre el horizonte contemporáneo (IA, plataformas digitales, hipervigilancia y nuevas disputas biopolíticas).
2. **Capítulos tecnológicos y mediáticos prioritarios:**
   * [`libro/07_preambulo.md`](../libro/07_preambulo.md): contraste entre las proyecciones tecnológicas de 2006 y la computación ubicua/IA actual.
   * [`libro/08_parte1_ensayo_1.md`](../libro/08_parte1_ensayo_1.md): trabajo digital, extractivismo de datos y valorización algorítmica.
   * [`libro/19_parte4_ensayo_3.md`](../libro/19_parte4_ensayo_3.md) y [`libro/20_parte4_ensayo_4.md`](../libro/20_parte4_ensayo_4.md): transición del régimen televisivo al régimen de pantallas móviles, *streaming* y plataformas.
   * [`libro/21_parte5_ensayo_1.md`](../libro/21_parte5_ensayo_1.md) a [`libro/24_parte5_ensayo_4.md`](../libro/24_parte5_ensayo_4.md): cámaras de eco, posverdad, micro-segmentación política y guerra cognitiva.
3. **Glosario ([`libro/31_glosario.md`](../libro/31_glosario.md)):** Incorporar nuevos conceptos al cierre (*Algoritmo*, *Big Data*, *Biopolítica digital*, *Extractivismo atencional*, *Inteligencia Artificial*, *Plataforma*, etc.).
4. **Erratas de 2006:** Corregir durante la revisión de cada capítulo los glifos ausentes de la imprenta original (ej. `S.  i ek` → `S. Žižek`) y las advertencias heredadas de notas al pie detectadas por `validar_libro.py`.
