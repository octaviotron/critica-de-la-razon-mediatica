# Bitácora de Versiones y Modificaciones — Segunda Edición

**Obra:** *Crítica de la Razón Mediática: Ensayos sobre biopolítica y potencia política del cuerpo*  
**Autor:** Juan Barreto Cipriani  
**Asesor Informático (2ª Edición):** Octavio Rossell Tabet (`octavio.rossell@gmail.com`)

---

## 1. Índice de Versiones Generadas

| Versión | Fecha | Archivo PDF de Lectura | Capítulos Modificados | Párrafos Etiquetados | Notas al Pie | Estado / Descripción |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **`v1.0`** | 2026-11-06 | [`Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf`](../Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf) | Ninguno (Base original 2006) | 2,641 | 513 | **Línea base inmutable (1ª Edición)**. Respaldo congelado en [`v1.0_original/md/`](../v1.0_original/md/). |
| **`v1.1`** | *Pendiente* | `Critica_de_la_Razon_Mediatica_Lectura_v1.1.pdf` | *Por definir* | — | — | *Próxima versión tras el primer lote de notas de voz del autor.* |

---

## 2. Registro Detallado de Cambios por Versión

### Versión `v1.0` (2026-11-06) — Línea Base Original (Edición 2006)
- **Origen:** Extracción determinista y auditada al `100.000%` (`1,008,962 / 1,008,962` caracteres alfanuméricos) a partir de `fuente/Libro Crítica de La Razon Mediatica.pdf`.
- **Respaldo congelado:** 33 archivos Markdown en [`versiones/v1.0_original/md/`](../v1.0_original/md/) verificados con hashes SHA-256 en [`versiones/v1.0_original/manifiesto_v1.0.md`](../v1.0_original/manifiesto_v1.0.md).
- **PDF de lectura generado:** [`versiones/Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf`](../Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf) (658 páginas en formato Carta, con guía de uso por voz en la página 1 y etiquetas `[CC.PPP]` en cada párrafo).

---

### Plantilla para Registrar Próximas Versiones (`v1.1`, `v1.2`, etc.)

```markdown
### Versión `v1.X` (AAAA-MM-DD) — [Título breve del lote de revisión]
- **Nota(s) de voz origen:** `notas_autor/AAAA-MM-DD_capXX_notas.md`
- **Archivo(s) Markdown intervenidos:** `XX_nombre_capitulo.md`
- **Detalle de modificaciones aplicadas:**
  1. **`[XX.PPP]`** (*Tipo de acción*): Descripción breve del cambio aplicado en el párrafo.
  2. **`[XX.NYY]`** (*Nota al pie*): Descripción de la nota agregada o actualizada.
- **Reporte de diferencias (diff):** `historial_cambios/diff_v1.0_a_v1.X.patch`
```
