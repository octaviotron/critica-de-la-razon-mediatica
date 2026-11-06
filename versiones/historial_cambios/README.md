# Historial de Cambios y Comparativas entre Versiones (`historial_cambios/`)

Esta carpeta almacena los archivos de diferencias (`diff` / `.patch`) y reportes comparativos entre la **Primera Edición original (`v1.0_original`)** y cada una de las versiones sucesivas (`v1.1`, `v1.2`, ..., `v2.0`).

## Cómo Generar un Reporte de Diferencias entre `v1.0` y la Versión Actual

Para dejar constancia exacta de cada línea agregada, modificada o eliminada respecto a la edición original de 2006 (almacenada de forma inmutable en [`../v1.0_original/md/`](../v1.0_original/md/)), ejecute desde la raíz del proyecto:

```bash
# Comparar los capítulos en libro/ contra el respaldo congelado v1.0_original/md/
diff -u versiones/v1.0_original/md/ libro/ > versiones/historial_cambios/diff_v1.0_a_v1.1.patch
```

O si los cambios se encuentran en `versiones/v2.0_en_proceso/borradores_md/`:

```bash
diff -u versiones/v1.0_original/md/ versiones/v2.0_en_proceso/borradores_md/ > versiones/historial_cambios/diff_v1.0_a_v1.1.patch
```

## Convención de Nombres en esta Carpeta

- `diff_v1.0_a_v1.1.patch`: Diferencias completas entre la versión original `v1.0` y la versión `v1.1`.
- `diff_v1.1_a_v1.2.patch`: Diferencias incrementales entre `v1.1` y `v1.2`.
- `resumen_v1.X.md`: Resumen ejecutivo opcional en Markdown para compartir con el autor indicando qué párrafos `[CC.PPP]` cambiaron en esa versión.
