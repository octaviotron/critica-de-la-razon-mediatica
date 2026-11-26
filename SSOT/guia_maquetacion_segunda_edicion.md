# SSOT: Guía de Maquetación Editorial — Segunda Edición (`maquetacion/`)

**Proyecto:** Segunda Edición — *Crítica de la Razón Mediática* (Juan Barreto Cipriani)  
**Motor tipográfico:** `LuaLaTeX` (TeX Live) + configuración declarativa YAML + plantillas `.tex` modulares  
**Propósito:** Documentar la receta oficial, verificada y fácilmente modificable para compilar la **maqueta editorial (digital y de imprenta)** fiel a la identidad visual de la Primera Edición (2006), directamente desde [`libro/`](../libro/), [`libro.yaml`](../libro.yaml) y los insumos en solo lectura de [`fuente/`](../fuente/).

> **Separación de herramientas de compilación:**
> * **`scripts/edicion/compilar_pdf.py`** (PangoCairo / Pandoc): se mantiene intacto para entregas rápidas de lectura y revisión de capítulos individuales durante la edición (PDF limpio, PDF etiquetado `[ID.PPP]` o Word `.docx`).
> * **`scripts/edicion/compilar_maqueta.py`** (`LuaLaTeX` + `maquetacion/`): compila la **maqueta editorial de libro** con las tipografías, caja espejo, sello lateral y portadillas gráficas originales de 2006 (tanto de un capítulo aislado para pruebas visuales como del libro completo en modo `--modo digital` o `--modo imprenta`).

---

## 1. Arquitectura Modular (Diseñada para Ajustes Rápidos)

Todo lo ajustable del diseño vive desacoplado del código Python en [`maquetacion/`](../maquetacion/):

| Archivo | Qué se ajusta allí |
| :--- | :--- |
| [`maquetacion/diseno_2ed.yaml`](../maquetacion/diseno_2ed.yaml) | Trim (`126.4 × 191.1 mm`), márgenes, sangrado de imprenta, **saltos de página (`paginacion_saltos`) para eliminar o controlar páginas en blanco**, tipografías, capitulares, sello lateral, cabeceras, parámetros del Índice General, notas al pie y mapeo de portadillas. |
| [`maquetacion/plantilla/libro_2ed.tex`](../maquetacion/plantilla/libro_2ed.tex) | Preámbulo maestro `LuaLaTeX`, estilos de página `libro2006` / `plain2006`, geometría y marco lateral. |
| [`maquetacion/plantilla/estilos_especiales.tex`](../maquetacion/plantilla/estilos_especiales.tex) | Epígrafes indivisibles, citas a bando, formato de notas al pie, portadillas gráficas/tipográficas y **layout completo del Índice General** (`\l@part`, `\l@chapter`, `\l@section`, `\tableofcontents`). |
| [`maquetacion/activos/`](../maquetacion/activos/README.md) | Nuevos artes exclusivos de la 2.ª edición (p. ej., nuevas portadillas `1476 × 2185 px` a `300 DPI` para *Prefacio* o *Anexo editorial*). |
| [`maquetacion/cubierta/especificaciones_lomo.md`](../maquetacion/cubierta/especificaciones_lomo.md) | Fórmula de lomo y criterios para generar la cubierta en PDF separado de la tripa. |
| [`scripts/edicion/compilar_maqueta.py`](../scripts/edicion/compilar_maqueta.py) | Compilador principal (lee `libro.yaml`, `maquetacion/` y `fuente/` en solo lectura; escribe solo en `dist/maqueta/`). |
| [`scripts/edicion/recalcular_onomastico.py`](../scripts/edicion/recalcular_onomastico.py) | Recalcula los números de página de `libro/32_indice_onomastico.md` contra el PDF final compilado (modo vista previa por defecto; `--escribir` solo al cierre). |

---

## 2. Especificación Visual Base (Heredada y Verificada de 2006)

### 2.1. Geometría y caja
* **Formato de recorte (trim):** `126.4 × 191.1 mm` (el PDF maestro de 2006 mide `145.4 × 210.2 mm` en la mayoría de páginas porque incluye marcas de corte de QuarkXPress).
* **Paginación:** arábiga continua desde la página 1 (`numeracion: arabiga_continua`), suprimiendo folio visible en portada interior, créditos y portadillas.
* **Margen exterior gráfico (`marco_externo`):** línea vertical superior + folio en `Bauhaus 93`; línea vertical inferior coronada por `fuente/RAZON/images/hoyo.jpg` + rótulo rotado `90°` (*Crítica de la Razón Mediática* / *Juan Barreto*), espejado automáticamente entre páginas pares e impares.
* **Modo `--modo imprenta`:** añade sangrado (`3 mm`) con marcas de corte (`crop`) y convierte las portadillas `.tif` a `PNG` sin pérdida en escala de grises a `300 DPI`.

### 2.2. Tipografías originales y auditoría de glifos (`fuente/FUENTES/`)

| Rol | Archivo | Cobertura real verificada | Regla técnica |
| :--- | :--- | :--- | :--- |
| Cuerpo, citas, epígrafes y notas al pie | `GARA.TTF`, `GARABD.TTF`, `GARAIT.TTF` | **100 % completa** (`0` glifos faltantes para español + `ŽžŠšĆćČč`) | Uso directo; el antiguo error `S. i ek` de 2006 era codificación 8-bit de QuarkXPress, no ausencia de glifos. |
| Títulos duales, subtítulos `##`, capitulares y marca lateral | `amiga4ever pro2.ttf` | **Faltan 15 glifos:** `°`, `Ž`, `ž`, `–`, `—`, `‘`, `’`, `“`, `”`, `Ć`, `ć`, `Č`, `č` | Sanitización automática desde `tipografia.sanitizacion_amiga` en `diseno_2ed.yaml`. |
| Folios, títulos principales y portadillas tipográficas | `BAUHS93.TTF` | **Faltan 9 glifos:** `·`, `Ž`, `ž`, `Ć`, `ć`, `Č`, `č` | Seguro para folios arábigos y títulos españoles; evitar romanos en minúscula. |
| Firma lateral *Juan Barreto* | `SWZCONBI.TTF` | Completa para texto latino/español | Embebida como `CID TrueType` Unicode. |

### 2.3. Portadillas originales (`fuente/RAZON/images/`)
Las 14 portadillas `.tif` miden `1476 × 2185 px` (`1476 × 2165 px` en 3 archivos), equivalentes a **`125.0 × 185.0 mm` a `300 DPI`**. El compilador busca primero en `maquetacion/activos/` (permitiendo sustituir o añadir artes nuevos sin tocar `fuente/`) y luego en `fuente/RAZON/images/`.

---

## 3. Reglas Técnicas Incorporadas en el Compilador (Lecciones del Dry-Run)

Para evitar regresiones al modificar plantillas o editar capítulos, `compilar_maqueta.py` garantiza de fábrica:

1. **Caché local de `luaotfload`:** exporta `TEXMFVAR`, `TEXMFCACHE` y `XDG_CACHE_HOME` hacia `dist/maqueta/build/texmf-var`, evitando errores de escritura en entornos aislados.
2. **Separación limpia de Parte + Ensayo I (`08`, `11`, `14`, `17`, `21`, `25`):** extrae el encabezado `# <N-ésima> Parte` y su epígrafe de Parte para mostrarlos en la página titular de Parte antes de iniciar el Ensayo I, evitando títulos duplicados y mezcla de epígrafes.
3. **Epígrafes indivisibles:** fusiona bloques `> *cita*` seguidos de `> — Autor` (aunque estén separados por una línea en blanco) dentro de un único `minipage`, impidiendo atribuciones huérfanas al inicio de la página siguiente.
4. **Saneamiento de código inline (`` `...` ``):** convierte backticks en `\textup{...}` antes de escapar TeX, impidiendo que ISBN o códigos salgan rodeados de comillas tipográficas `‘...‘`.
5. **Capitulares sin versalitas falsas:** `\LettrineTextFont{\normalfont}` con `findent=1.5pt` aplicado únicamente a la primera letra y el resto de la primera palabra, eliminando desbordamientos `Overfull \hbox`.
6. **Notas al pie estilo 2006:** numeración plana con sangría francesa colgante (`estilo: plano_2006`, configurable a `superindice` en `diseno_2ed.yaml`) y reinicio por capítulo.
7. **Multi-pasada automática:** ejecuta `lualatex` en bucle (hasta 4 pasadas) hasta que desaparecen `Label(s) may have changed` y `Rerun`.
8. **Protección de rutas inmutables:** bloquea toda escritura en `respaldo_v1.0/`, `fuente/`, `externos/` y `scripts/extraccion_v1/`.
9. **Reporte de calidad JSON:** cada compilación deja en `dist/maqueta/reporte_<etiqueta>.json` el conteo de páginas, `missing_characters`, `overfull_hbox`, `underfull_hbox`, `latex_warnings` y hallazgos pre-compilación.

---

## 4. Comandos Operativos y Flujo de Iteración Visual

```bash
# 1. Prueba rápida de 1 capítulo (~4-5 s) mientras se ajusta diseno_2ed.yaml o estilos_especiales.tex
python3 -B scripts/edicion/compilar_maqueta.py --capitulo 08

# 2. Compilar el libro completo (modo digital) y revisar dist/maqueta/reporte_libro_2ed_digital.json
python3 -B scripts/edicion/compilar_maqueta.py

# 3. Compilar versión de imprenta (sangrado 3 mm + marcas de corte + portadillas PNG 300 DPI)
python3 -B scripts/edicion/compilar_maqueta.py --modo imprenta

# 4. Recalcular Índice Onomástico (primero en vista previa; --escribir solo en cierre editorial)
python3 -B scripts/edicion/recalcular_onomastico.py
python3 -B scripts/edicion/recalcular_onomastico.py --escribir
```

---

## 5. Checklist de Calidad Pre-Imprenta (Cierre Editorial)

- [ ] `python3 -B scripts/edicion/validar_libro.py --verificar-respaldo --estricto` concluye con **0 errores** (`0` `[VERIFICAR]`, `0` asteriscos impares, `0` notas huérfanas, `33/33` SHA-256 intactos).
- [ ] Todos los capítulos de `libro.yaml` (incluido `A1`, Anexo editorial) están en `estado: "aprobado"`.
- [ ] `compilar_maqueta.py --modo imprenta` concluye con `missing_characters == 0`, `latex_warnings == 0` y `overfull_hbox > 2 pt == 0`.
- [ ] `libro/32_indice_onomastico.md` recalculado con `recalcular_onomastico.py`, verificado por muestreo y recompilado en el PDF definitivo.
- [ ] `pdffonts` confirma **100 % fuentes embebidas** (`emb: yes`, `sub: yes`, `uni: yes`).
- [ ] Si la imprenta exige PDF/X-1a en negro puro `K=100%`, convertir la tripa con Ghostscript en escala de grises y entregar la cubierta/lomo en archivo separado (`maquetacion/cubierta/especificaciones_lomo.md`).
