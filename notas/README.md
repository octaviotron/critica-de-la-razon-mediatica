# Carpeta de Anotaciones Editoriales (`notas/`)

Espacio de trabajo separado de [`libro/`](../libro/) para registrar ideas, autores por incorporar, argumentos por ampliar, frases, erratas detectadas y observaciones del autor **sin contaminar los archivos `.md` publicables** ni las compilaciones en `dist/`.

## Estructura

```text
notas/
├── README.md                    # Esta guía breve
├── NOTAS.md                     # Ideas globales del libro, autores por incluir, frases, glosario e índice
├── mapa_obra.md                 # Panorámica argumental condensada de los 33 capítulos y registro de 2.ª edición
├── registro_cambios_edicion.md  # Bitácora editorial de cambios sustantivos al libro (base de futuro reporte/anexo)
├── estado_sesion.md             # [Local, ignorado por Git] Estado operativo de la sesión en curso (<= 2 KB)
├── capitulos/                   # Una ficha de notas por cada capítulo (mismo nombre exacto que en libro/)
│   ├── 00_preliminares.md
│   ├── ...
│   ├── 32_indice_onomastico.md
│   ├── anexo_cambios_segunda_edicion.md  # Ficha del anexo editorial de cierre (id: A1)
│   └── prefacio_segunda_edicion.md       # Planificación previa (capítulo futuro)
└── fuentes/                     # Catálogo y fichas de lectura curadas de la bibliografía en externos/
    ├── catalogo.yaml            # Manifiesto bibliográfico maestro (citas europeas, temas, capítulos destino)
    └── <slug>.md                # Ficha resumida y banco de citas verificadas por cada fuente externa
```

> **Separación `notas/registro_cambios_edicion.md` vs. `libro/anexo_cambios_segunda_edicion.md`:** `notas/registro_cambios_edicion.md` es la bitácora detallada de trabajo (códigos `[E-01]`, notas técnicas y seguimiento), mientras que [`libro/anexo_cambios_segunda_edicion.md`](../libro/anexo_cambios_segunda_edicion.md) (`id: A1`) aloja la síntesis publicable destinada al lector al cierre del libro.

## Cómo usar estas notas

1. **Captura rápida de ideas generales:** Añade cualquier autor, cita, frase o idea transversal en [`NOTAS.md`](NOTAS.md) usando casillas `- [ ]`.
2. **Trabajo por capítulo:** Al abordar un capítulo en [`libro/`](../libro/), revisa su ficha espejo en `notas/capitulos/<mismo_nombre>.md`. Allí se concentran las sugerencias de actualización, erratas técnicas heredadas de 2006 y el espacio para pegar observaciones del autor durante las rondas de revisión.
3. **Bibliografía externa (`externos/` → `notas/fuentes/`):** Cuando añadas nuevos documentos en [`externos/`](../externos/), solo avisa durante la sesión de edición asistida; el catálogo [`notas/fuentes/catalogo.yaml`](fuentes/catalogo.yaml), el índice local de búsqueda y la ficha de lectura en `notas/fuentes/` se actualizarán automáticamente sin ejecutar comandos manuales.
4. **Seguimiento limpio:** Conforme cada punto se integra al manuscrito y recibe aprobación del autor, cambia `- [ ]` por `- [x]` para conservar memoria de lo ya resuelto.
5. **Nuevos capítulos:** Si añades un capítulo nuevo en `libro/` y [`libro.yaml`](../libro.yaml), puedes crear su ficha correspondiente en `notas/capitulos/` con el mismo nombre de archivo.
6. **Retomar sesiones:** `notas/estado_sesion.md` es un archivo local (ignorado por Git; puede no existir en un clon nuevo), de `<= 2 KB`, que se sobrescribe al terminar un bloque de trabajo y se consulta con `python3 -B scripts/edicion/contexto_capitulo.py --estado`. No sustituye al registro de cambios ni a las fichas de `capitulos/`.

> Para el flujo completo de edición asistida, véanse [`SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md) y [`SSOT/guia_estilo_editorial.md`](../SSOT/guia_estilo_editorial.md).
