# Respaldo Inmutable — Primera Edición (`respaldo_v1.0/`)

> **⚠️ DIRECTORIO INMUTABLE — SOLO LECTURA DE REFERENCIA**  
> No edites, renombres ni elimines archivos dentro de esta carpeta. Todas las ediciones de la Segunda Edición deben realizarse exclusivamente en [`libro/`](../libro/) y [`libro.yaml`](../libro.yaml).

## Propósito

Este directorio conserva de forma congelada e íntegra el estado inicial de la obra correspondiente a la **Primera Edición (2006)** de ***Crítica de la Razón Mediática*** (Juan Barreto Cipriani), verificada al **100.000%** contra el PDF maestro (`1,008,962` caracteres alfanuméricos, `197,741` palabras, `513` notas al pie, `0` pérdidas).

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
* [`SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md) — Flujo editorial con Git, `libro.yaml` y uso de este respaldo.
