# SSOT: Flujo Editorial, Versionamiento en Git y Manifiesto Estructural (Segunda Edición)

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Asesor Informático:** Octavio Rossell Tabet (<octavio.rossell@gmail.com> — https://github.com/octaviotron)  
**Propósito:** Definir la arquitectura oficial de edición directa en Markdown, versionamiento nativo en Git, gestión flexible de la estructura del índice mediante `libro.yaml` (**Opción A**) y preservación inmutable de la primera edición en `respaldo_v1.0/`.

---

## 1. Principios de la Arquitectura Editorial

1. **Una sola fuente viva del texto (`libro/`):** Los capítulos en Markdown de [`libro/`](../libro/) se editan directamente. No se duplican borradores ni copias temporales dentro del repositorio.
2. **Versionamiento nativo en Git (sin carpetas `versiones/`):** El historial de modificaciones, ramas de trabajo y versiones cerradas se gestionan mediante commits, ramas y *tags* anotados de Git, complementados por la bitácora editorial [`CHANGELOG.md`](../CHANGELOG.md).
3. **Respaldo inmutable de la 1.ª edición ([`respaldo_v1.0/`](../respaldo_v1.0/)):** Existe un directorio dedicado y congelado con los 33 `.md` originales de 2006 (`respaldo_v1.0/md/`), sus huellas SHA-256 (`respaldo_v1.0/manifiesto_v1.0.md`), su documentación (`respaldo_v1.0/README.md`) y su manifiesto propio (`respaldo_v1.0/libro.yaml`). Esto garantiza que **siempre se podrá consultar la estructura inicial, auditar al 100% contra el PDF de 2006 y compilar la Primera Edición (`v1.0.0`)** aunque cambien por completo los archivos de `libro/` o el índice de la Segunda Edición.
4. **Orden e índice desacoplados mediante [`libro.yaml`](../libro.yaml) (Opción A):** Los nombres de archivo existentes en `libro/` (`00_preliminares.md` … `32_indice_onomastico.md`) se conservan como **identificadores estables** para evitar renombramientos masivos y mantener limpio el historial `git diff` contra 2006. El orden real de lectura, la agrupación por partes y los títulos del índice los gobierna exclusivamente [`libro.yaml`](../libro.yaml).
5. **Artefactos compilados fuera de Git (`dist/`):** Los PDFs generados localmente, vistas previas de índice y reportes comparativos se escriben en `dist/` (ignorado en [`.gitignore`](../.gitignore)). Los binarios de hitos cerrados se publican como adjuntos en *Releases* de GitHub.

---

## 2. Respaldo Inmutable de Referencia (`respaldo_v1.0/`)

```text
respaldo_v1.0/
├── README.md           # Guía de uso, políticas de inmutabilidad y comandos
├── libro.yaml          # Manifiesto estructural congelado de la 1.ª edición (v1.0.0)
├── manifiesto_v1.0.md  # Checksums SHA-256 de los 33 archivos originales
└── md/                 # Copia testigo bit a bit de los 33 archivos de 2006
```

### Reglas sobre `respaldo_v1.0/`
* **Inmutabilidad estricta:** Ningún script de `scripts/extraccion_v1/` ni de `scripts/edicion/` permite escribir dentro de `respaldo_v1.0/`. Nunca se debe editar manualmente ningún archivo allí alojado.
* **Compilación garantizada de la 1.ª edición (`v1.0.0`):**
  ```bash
  python3 scripts/edicion/compilar_pdf.py --manifiesto respaldo_v1.0/libro.yaml
  ```
* **Verificación criptográfica SHA-256 del respaldo:**
  ```bash
  python3 scripts/edicion/validar_libro.py --manifiesto respaldo_v1.0/libro.yaml --verificar-respaldo
  ```
* **Re-auditoría matemática contra el PDF de 2006:**
  ```bash
  python3 scripts/extraccion_v1/03_auditar_integridad.py
  ```

---

## 3. Convención de Versionamiento en Git

### 3.1. Etiquetas (*Tags*) Semánticas Editoriales
* **`v1.0.0`**: Primera edición íntegra (2006), auditada al 100.000% (equivalente al estado de `respaldo_v1.0/`).
* **`v1.0.1`** *(opcional)*: Corrección exclusiva de erratas tipográficas de 2006 antes de iniciar la reescritura conceptual.
* **`v2.0.0-alpha.N`**: Hitos intermedios de edición de la Segunda Edición (por ejemplo, al completar la revisión de una Parte).
* **`v2.0.0-rc.N`**: Versiones candidatas a publicación (texto, índice, glosario y bibliografía cerrados para revisión final).
* **`v2.0.0`**: Segunda edición definitiva.

### 3.2. Estrategia de Ramas
* **`main`**: Rama principal siempre válida y compilable con el progreso consolidado hacia la 2.ª edición.
* **Ramas temáticas cortas (opcionales para reescrituras amplias):** p. ej. `edicion/cap-07-preambulo` o `edicion/cap-19-tv`.
* **Ramas de experimento estructural (recomendado si cambias el índice):** p. ej. `estructura/nuevo-indice`. Permite reordenar partes, mover ensayos en `libro.yaml`, regenerar el índice y compilar un PDF de prueba en `dist/` sin afectar `main` hasta aprobar el resultado.

### 3.3. Convención de Mensajes de Commit
Usar prefijos semánticos claros en español:
* `errata(cap-XX): ...` — Correcciones tipográficas o de caracteres faltantes de 2006.
* `edicion(cap-XX): ...` — Modificaciones, adendas o reescrituras de contenido.
* `glosario: ...` / `bibliografia: ...` — Actualizaciones del aparato crítico.
* `estructura: ...` — Cambios de orden, partes, capítulos nuevos o regeneración de índice en `libro.yaml`.
* `docs: ...` / `scripts: ...` — Cambios en documentación (`README.md`, `SSOT/`, `CHANGELOG.md`) o herramientas.

---

## 4. Gestión de la Estructura del Índice con `libro.yaml` (Opción A)

El archivo [`libro.yaml`](../libro.yaml) define:
* `obra`: Título, subtítulo, autor, etiqueta de edición, versión semántica y marca `inmutable`.
* `carpeta_base`: Carpeta donde viven los `.md` (`libro` en el manifiesto raíz; `md` en `respaldo_v1.0/libro.yaml`).
* `secciones`: Lista ordenada de partes/bloques y sus `capitulos`, cada uno con `id`, `archivo`, `titulo`, `tipo` (`preliminares`, `indice`, `cuerpo`, `bibliografia`, `glosario`, `onomastico`) y `folios_2006` (opcional).

### Escenarios frecuentes
1. **Editar el texto de un capítulo existente:**
   * Modifica directamente el archivo correspondiente en `libro/` (por ejemplo `libro/19_parte4_ensayo_3.md`).
   * Ejecuta `python3 scripts/edicion/validar_libro.py`.
2. **Añadir un capítulo nuevo (ej. *Prefacio a la Segunda Edición*):**
   * Crea un archivo con nombre descriptivo sin prefijo numérico en `libro/` (ej. `libro/prefacio_segunda_edicion.md`).
   * Regístralo en la posición deseada dentro de `libro.yaml` con un `id` único (ej. `prefacio_2da`).
   * Ejecuta `validar_libro.py` y `generar_indice.py --escribir`.
3. **Reordenar capítulos o cambiar la estructura de Partes:**
   * Crea una rama de prueba (`git checkout -b estructura/reorganizacion`).
   * Mueve las entradas de capítulos o crea/renombra secciones únicamente dentro de `libro.yaml` (**sin renombrar los archivos existentes en `libro/`**).
   * Regenera el índice con `python3 scripts/edicion/generar_indice.py --escribir` y compila el PDF con `python3 scripts/edicion/compilar_pdf.py` para evaluar la lectura en `dist/`.
   * Si el resultado te convence, haz *merge* a `main`; de lo contrario, descarta la rama.

---

## 5. Catálogo de Scripts del Proyecto

### 5.1. Herramientas Activas de Edición (`scripts/edicion/`)

| Script | Propósito | Comando habitual |
| :--- | :--- | :--- |
| [`manifiesto.py`](../scripts/edicion/manifiesto.py) | Módulo compartido que carga `libro.yaml` o `respaldo_v1.0/libro.yaml` y resuelve rutas relativas de forma segura. | *(Importado por los demás scripts)* |
| [`validar_libro.py`](../scripts/edicion/validar_libro.py) | Comprueba archivos faltantes/huérfanos, IDs duplicados, correspondencia 1:1 de notas al pie (`[^n]` ↔ `[^n]:`), enlaces locales rotos y (con `--verificar-respaldo`) hashes SHA-256 de `respaldo_v1.0/md/`. | `python3 scripts/edicion/validar_libro.py --verificar-respaldo` |
| [`generar_indice.py`](../scripts/edicion/generar_indice.py) | Construye el Índice General a partir de `libro.yaml` y los encabezados reales (`#`, `##`, opcionalmente `###`). Por defecto previsualiza en `dist/indice_generado.md`; con `--escribir` actualiza `libro/01_indice.md`. | `python3 scripts/edicion/generar_indice.py --escribir` |
| [`compilar_pdf.py`](../scripts/edicion/compilar_pdf.py) | Compila un PDF de lectura limpio en `dist/` siguiendo el orden de `libro.yaml` (o de `respaldo_v1.0/libro.yaml` para la 1.ª edición). Soporta `--etiquetar-parrafos` como modo opcional de revisión. | `python3 scripts/edicion/compilar_pdf.py` |
| [`reporte_cambios.py`](../scripts/edicion/reporte_cambios.py) | Genera en `dist/reporte_cambios.md` un informe de cambios estructurales (índice/orden) y textuales (palabras y diffs) comparando `libro/` contra `respaldo_v1.0/` o contra un tag Git (`--desde-git v1.0.0`). | `python3 scripts/edicion/reporte_cambios.py --incluir-diffs` |

### 5.2. Pipeline Histórico de Extracción 2006 (`scripts/extraccion_v1/`)
Congelado para trazabilidad histórica y auditoría reproducible de la 1.ª edición:
* [`scripts/extraccion_v1/01_extraer_xml.py`](../scripts/extraccion_v1/01_extraer_xml.py): Extrae el XML vectorial de las 666 páginas del PDF de 2006.
* [`scripts/extraccion_v1/02_convertir_a_md.py`](../scripts/extraccion_v1/02_convertir_a_md.py): Reproduce la conversión histórica en `dist/extraccion_v1_md/` por defecto (bloqueado sobre `respaldo_v1.0/` y protegido sobre `libro/` salvo `--confirmar-sobrescritura`).
* [`scripts/extraccion_v1/03_auditar_integridad.py`](../scripts/extraccion_v1/03_auditar_integridad.py): Audita al 100.000% los caracteres alfanuméricos contra el PDF original (apunta por defecto a `respaldo_v1.0/md/`).

---

## 6. Estrategia Editorial (2006 → 2026) para la Segunda Edición

Como guía temática de actualización frente a la primera edición de 2006, se sugieren cuatro frentes modulares que respetan el aparato crítico existente:

1. **Nuevo Estudio Introductorio o Prefacio a la Segunda Edición:** Capítulo independiente (ej. `libro/prefacio_segunda_edicion.md`) registrado en `libro.yaml` para dialogar con la obra veinte años después (IA, plataformas digitales, hipervigilancia, nuevas disputas biopolíticas).
2. **Actualizaciones o Adendas en Capítulos Estratégicos:**
   * [`libro/07_preambulo.md`](../libro/07_preambulo.md): contraste entre las proyecciones tecnológicas de 2006 y la computación ubicua/IA actual.
   * [`libro/08_parte1_ensayo_1.md`](../libro/08_parte1_ensayo_1.md): trabajo digital, extractivismo de datos y valorización algorítmica.
   * [`libro/19_parte4_ensayo_3.md`](../libro/19_parte4_ensayo_3.md) y [`libro/20_parte4_ensayo_4.md`](../libro/20_parte4_ensayo_4.md): transición del régimen televisivo al régimen de pantallas móviles, *streaming* y micro-video.
   * [`libro/21_parte5_ensayo_1.md`](../libro/21_parte5_ensayo_1.md) a [`libro/24_parte5_ensayo_4.md`](../libro/24_parte5_ensayo_4.md): cámaras de eco, posverdad, micro-segmentación política y guerra cognitiva.
3. **Ampliación del Glosario ([`libro/31_glosario.md`](../libro/31_glosario.md)):** Incorporación de nuevos conceptos contemporáneos (*Algoritmo*, *Big Data*, *Biopolítica digital*, *Extractivismo atencional*, *Inteligencia Artificial*, *Plataforma*, etc.).
4. **Corrección Sistemática de Erratas de 2006:** Limpieza de erratas heredadas de la edición impresa original (ej. glifos ausentes en la fuente Garamond de 1998 como `S.  i ek` → `S. Žižek`, o erratas tipográficas puntuales), idealmente en un commit inicial de tipo `errata(...)` antes de las reescrituras conceptuales.
