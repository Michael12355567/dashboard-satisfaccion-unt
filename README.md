# Dashboard UNT — versión alineada al Word base del instrumento

Esta versión toma como regla metodológica principal la **Propuesta del Instrumento de Medición** y evita clasificaciones que no forman parte del cálculo del indicador.

## Regla aplicada
- **Por pregunta P1–P17:** respuestas **4 o 5 = Satisfecho**; respuestas **1, 2 o 3 = No satisfecho**.
- **Dimensión 1 (P1–P4):** estudiante satisfecho si el promedio de sus cuatro respuestas es **>= 4**.
- **Dimensión 2 (P5–P8):** estudiante satisfecho si el promedio es **>= 4**.
- **Dimensión 3 (P9–P12):** estudiante satisfecho si el promedio es **>= 4**.
- **Dimensión 4 (P13–P16):** estudiante satisfecho si el promedio es **>= 4**.
- **Satisfacción general:** P17; 4 o 5 = satisfecho, 1, 2 o 3 = no satisfecho.
- **Fórmula del indicador:** (N de estudiantes satisfechos / total de estudiantes evaluados) x 100.

## Cambios visibles en el dashboard
- Eliminado el bloque **“Marco documental / Referencia de la ficha PEI”**.
- Eliminadas las categorías **Favorable / Neutral / Desfavorable**.
- La distribución principal usa solo dos categorías: **No satisfechos (1–3)** y **Satisfechos (4–5)**.
- La alternativa 3 conserva su nombre original únicamente en el detalle técnico de respuestas 1–5, pero no se presenta como una categoría “Neutral”.
- La pestaña final se denomina **“Método y calidad”**.
- Se mantiene el análisis por cada pregunta y por cada dimensión conforme a las reglas del instrumento.

## Ejecutar
```bash
python -m streamlit run app.py
```
