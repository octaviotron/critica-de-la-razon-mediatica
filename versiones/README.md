# Gestión de Versiones y PDFs de Lectura Etiquetados

Esta carpeta (`versiones/`) almacena las versiones numeradas en PDF de lectura con etiquetas de párrafo (`[CC.PPP]`) diseñadas para que el autor (**Juan Barreto Cipriani**) pueda dictar modificaciones y notas mediante su dispositivo de voz con IA, así como la estructura de respaldo y control histórico entre la **Primera Edición (2006)** y la **Segunda Edición (en preparación)**.

---

## 1. Archivos PDF de Lectura Numerados por Versión

En la raíz de esta carpeta se alojan los documentos PDF generados por [`scripts/04_generar_pdf_lectura.py`](../scripts/04_generar_pdf_lectura.py):

- **[`Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf`](./Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf)**: Versión `v1.0` (base original íntegra de 2006). Contiene **658 páginas**, **2,641 párrafos etiquetados** (`[00.001]` a `[32.028]`) y **513 notas al pie etiquetadas** (`[03.N01]` a `[29.N21]`).
- Próximas versiones numeradas se almacenarán siguiendo la misma convención:
  - `Critica_de_la_Razon_Mediatica_Lectura_v1.1.pdf`
  - `Critica_de_la_Razon_Mediatica_Lectura_v1.2.pdf`
  - `Critica_de_la_Razon_Mediatica_Lectura_v2.0.pdf`

### Cómo generar una nueva versión numerada en PDF

Desde la raíz del proyecto, ejecute el script [`scripts/04_generar_pdf_lectura.py`](../scripts/04_generar_pdf_lectura.py) indicando el número de versión:

```bash
# Generar versión a partir de los capítulos activos en libro/
python3 -B scripts/04_generar_pdf_lectura.py --version v1.1

# O generar versión a partir de los borradores en proceso de la 2da edición
python3 -B scripts/04_generar_pdf_lectura.py --version v1.1 --source-dir versiones/v2.0_en_proceso/borradores_md
```

---

## 2. Estructura de Directorios de `versiones/`

```text
versiones/
├── README.md                                              # Este documento explicativo
├── Critica_de_la_Razon_Mediatica_Lectura_v1.0.pdf         # PDF de lectura v1.0 con etiquetas [CC.PPP]
│
├── v1.0_original/                                         # Respaldo INMUTABLE de la 1ª Edición (2006)
│   ├── manifiesto_v1.0.md                                 # Hashes SHA-256 de los 33 capítulos originales
│   └── md/                                                # Copia congelada de los 33 archivos .md originales
│       ├── 00_preliminares.md
│       ├── 01_indice.md
│       └── ... (hasta 32_indice_onomastico.md)
│
├── v2.0_en_proceso/                                       # Espacio de trabajo de la 2ª Edición
│   ├── bitacora_cambios.md                                # Registro cronológico de versiones y cambios aplicados
│   ├── notas_autor/                                       # Transcripciones de voz del autor por sesión/capítulo
│   │   └── PLANTILLA_nota_autor.md                        # Plantilla estructurada para notas de voz con IA
│   └── borradores_md/                                     # Capítulos en revisión antes de consolidar versión
│       └── README.md                                      # Guía de uso de la carpeta de borradores
│
└── historial_cambios/                                     # Reportes de diferencias (diffs) entre versiones
    └── README.md                                          # Guía para generar comparativas contra v1.0_original
```

---

## 3. Reglas de Conservación e Historial

1. **Inmutabilidad de `v1.0_original/`**: Los 33 archivos dentro de [`v1.0_original/md/`](./v1.0_original/md/) y su [`manifiesto_v1.0.md`](./v1.0_original/manifiesto_v1.0.md) constituyen el testigo intacto de la primera edición de 2006 (`1,008,962` caracteres alfanuméricos verificados al `100.000%`). **Nunca deben editarse**, de modo que siempre sea posible comparar cualquier versión futura contra el texto original exacto.
2. **Trazabilidad por código `[CC.PPP]`**: Toda modificación dictada por el autor se registra primero en [`v2.0_en_proceso/notas_autor/`](./v2.0_en_proceso/notas_autor/) haciendo referencia al código `[CC.PPP]` de la versión de lectura activa, y queda asentada en [`v2.0_en_proceso/bitacora_cambios.md`](./v2.0_en_proceso/bitacora_cambios.md).
3. **Metodología completa**: Consulte [`SSOT/guia_edicion_segunda_edicion_ia_voz.md`](../SSOT/guia_edicion_segunda_edicion_ia_voz.md) para ver el protocolo detallado de dictado por voz, la plantilla de instrucciones para el dispositivo de IA del autor y la matriz de actualización conceptual.
