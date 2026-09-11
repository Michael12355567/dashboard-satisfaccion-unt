# Dashboard UNT — versión final metodológicamente alineada al Word

Esta versión usa el Word como base metodológica y `basededatos.xlsx` como fuente de datos. No modifica la base Excel.

## Reglas implementadas

- **P1–P16 (ítems):** se muestran de forma descriptiva. Para cada pregunta se presenta el porcentaje de respuestas 4–5, la respuesta 3 por separado, las respuestas 1–2 por separado y el promedio. No se asigna a cada ítem la categoría institucional Insatisfactorio/Regular/Satisfactorio/Muy satisfactorio, porque el Word no formaliza esa aplicación por ítem.
- **D1–D4 (dimensiones):** para cada estudiante se calcula el promedio de los cuatro ítems de la dimensión. `promedio >= 4` = satisfecho; `promedio < 4` = no satisfecho. Luego se calcula el porcentaje de estudiantes satisfechos.
- **P17 (satisfacción general):** 4–5 = satisfecho; 1–3 = no satisfecho, tal como lo establece expresamente el Word.
- **Interpretación institucional:** los rangos 0–59, 60–74, 75–89 y 90–100 se aplican a los porcentajes finales de D1–D4 y P17. Para trabajar con decimales se operacionalizan como 0–<60, 60–<75, 75–<90 y 90–100.

## Resultados principales recalculados desde el Excel

- P17 satisfacción general: **71.4% — Regular**
- D1 Calidad del proceso académico: **55.0% — Insatisfactorio**
- D2 Desempeño docente y estrategias pedagógicas: **60.5% — Regular**
- D3 Servicios y gestión educativa: **41.4% — Insatisfactorio**
- D4 Formación integral y desarrollo personal: **65.0% — Regular**

El tablero explica explícitamente por qué, por ejemplo, **P1 = 79.2%** y **D1 = 55.0%** no se contradicen: P1 es una sola pregunta, mientras que D1 clasifica a cada estudiante usando el promedio P1–P4.

## Diseño conservado

Se mantienen los semáforos 3D, la fórmula tipografiada N/D × 100, el estilo glassmorphism, las tarjetas y la distribución Likert original 1–5. P17 no se presenta como una cifra gigante que domine visualmente el tablero.

## Ejecutar

```bash
python -m streamlit run app.py
```
