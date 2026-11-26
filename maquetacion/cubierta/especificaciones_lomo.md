# Especificaciones de Cubierta y Lomo (`maquetacion/cubierta/`)

La **tripa (interior)** y la **cubierta (portada + lomo + contraportada + solapas)** deben entregarse a imprenta siempre como **dos archivos PDF independientes**.

## Referencia de la Primera Edición (2006)
* Artes originales (solo lectura): `fuente/PORTADA/` (`repujado1.tif`, `repujado2.tif`, `uv.tif`) y página 1 de `fuente/Libro Crítica de La Razon Mediatica.pdf` (`250.4 × 211.4 mm`, portada + solapa/contraportada calculadas para `666` páginas en el papel de 2006).

## Fórmula para el lomo de la Segunda Edición
El ancho exacto del lomo solo puede fijarse al cierre editorial, cuando el conteo definitivo de páginas de la tripa esté cerrado (ajustado a múltiplo de pliego, normalmente 16 páginas) y la imprenta confirme el calibre del papel:

$$\text{lomo\_mm} = \left(\frac{\text{paginas\_totales}}{2}\right) \times \text{calibre\_hoja\_mm} + \text{holgura\_tapa\_mm}$$

* **Sangrado mínimo de cubierta:** `5 mm` por los cuatro lados exteriores.
* **Resolución de mapas de bits / barniz UV / repujado:** `300 DPI` mínimo, tintas en CMYK + tintas planas separadas para UV/repujado si se conserva el acabado de 2006.
