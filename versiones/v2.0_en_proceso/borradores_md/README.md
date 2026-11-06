# Carpeta de Borradores Markdown en Proceso (`borradores_md/`)

Esta carpeta aloja las copias de trabajo de los capítulos Markdown (`.md`) mientras están siendo intervenidos para la **Segunda Edición**, antes de ser promovidos a una nueva versión consolidada.

## Flujo de Trabajo Recomendado

1. **Preparar los capítulos para editar una nueva versión:**
   Si desea experimentar o preparar cambios sin tocar directamente `libro/`, copie los 33 archivos desde `libro/` (o desde [`../../v1.0_original/md/`](../../v1.0_original/md/)) hacia esta carpeta:
   ```bash
   cp libro/*.md versiones/v2.0_en_proceso/borradores_md/
   ```
2. **Aplicar las modificaciones dictadas por el autor:**
   Edite los capítulos correspondientes guiándose por los códigos `[CC.PPP]` registrados en [`../notas_autor/`](../notas_autor/).
3. **Generar el nuevo PDF de lectura numerado (`v1.1`, `v1.2`, etc.):**
   ```bash
   python3 -B scripts/04_generar_pdf_lectura.py --version v1.1 --source-dir versiones/v2.0_en_proceso/borradores_md
   ```
4. **Promover cambios aprobados:**
   Una vez que el autor valide el PDF de la nueva versión, sincronice los archivos aprobados hacia `libro/` y registre el corte en [`../bitacora_cambios.md`](../bitacora_cambios.md).
