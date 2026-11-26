# Activos Gráficos Exclusivos de la Segunda Edición (`maquetacion/activos/`)

Este directorio aloja únicamente **nuevos artes gráficos creados para la Segunda Edición** que no existen en `fuente/RAZON/images/` (que permanece intacto en solo lectura).

## Especificaciones recomendadas para nuevas portadillas
Para mantener coherencia exacta con las 14 portadillas originales de 2006 (`fuente/RAZON/images/*.tif`):
* **Dimensiones:** `1476 × 2185 px` a **`300 DPI`** (`125.0 × 185.0 mm` sobre el trim `126.4 × 191.1 mm`).
* **Modo de color:** Escala de grises `8-bit Grayscale` (sin tintas RGB/CMYK compuestas).
* **Formato:** `.tif` (sin pérdida) o `.png` de `300 DPI`.
* **Ejemplos futuros:** `anexo_editorial.tif` (para `A1`) o `prefacio_2ed.tif` (para el futuro *Prefacio a la Segunda Edición*).

Al añadir un archivo aquí, basta declararlo en `portadillas.por_capitulo` o `portadillas.por_seccion` dentro de [`../diseno_2ed.yaml`](../diseno_2ed.yaml); `compilar_maqueta.py` busca primero en `maquetacion/activos/` y luego en `fuente/RAZON/images/`.
