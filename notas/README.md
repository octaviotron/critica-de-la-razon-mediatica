# Carpeta de Anotaciones Editoriales (`notas/`)

Espacio de trabajo separado de [`libro/`](../libro/) para registrar ideas, autores por incorporar, argumentos por ampliar, frases, erratas detectadas y observaciones del autor **sin contaminar los archivos `.md` publicables** ni las compilaciones en `dist/`.

## Estructura

```text
notas/
├── README.md          # Esta guía breve
├── NOTAS.md           # Ideas globales del libro, autores por incluir, frases, glosario e índice
└── capitulos/         # Una ficha de notas por cada capítulo (mismo nombre exacto que en libro/)
    ├── 00_preliminares.md
    ├── ...
    └── 32_indice_onomastico.md
```

## Cómo usar estas notas

1. **Captura rápida de ideas generales:** Añade cualquier autor, cita, frase o idea transversal en [`NOTAS.md`](NOTAS.md) usando casillas `- [ ]`.
2. **Trabajo por capítulo:** Al abordar un capítulo en [`libro/`](../libro/), revisa su ficha espejo en `notas/capitulos/<mismo_nombre>.md`. Allí se concentran las sugerencias de actualización, erratas técnicas heredadas de 2006 y el espacio para pegar observaciones del autor durante las rondas de revisión.
3. **Seguimiento limpio:** Conforme cada punto se integra al manuscrito y recibe aprobación del autor, cambia `- [ ]` por `- [x]` para conservar memoria de lo ya resuelto.
4. **Nuevos capítulos:** Si añades un capítulo nuevo en `libro/` y [`libro.yaml`](../libro.yaml), puedes crear su ficha correspondiente en `notas/capitulos/` con el mismo nombre de archivo.

> Para el flujo completo de edición asistida, véanse [`SSOT/flujo_editorial_segunda_edicion.md`](../SSOT/flujo_editorial_segunda_edicion.md) y [`SSOT/guia_estilo_editorial.md`](../SSOT/guia_estilo_editorial.md).
