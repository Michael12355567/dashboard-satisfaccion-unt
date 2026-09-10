# Dashboard UNT — revisión metodológica final

Esta versión parte del `app.py` visual anterior y conserva el diseño general, los semáforos 3D y la fórmula tipografiada N/D × 100. Los cambios se concentran en la lógica y en la interpretación para que el tablero siga el documento del instrumento y la base `basededatos.xlsx`.

## Regla aplicada

- Escala original: 1 Totalmente en desacuerdo, 2 En desacuerdo, 3 Ni de acuerdo ni en desacuerdo, 4 De acuerdo, 5 Totalmente de acuerdo.
- D1 = P1–P4, D2 = P5–P8, D3 = P9–P12, D4 = P13–P16.
- Para D1–D4: por cada estudiante se calcula el promedio de los cuatro ítems. Promedio >= 4 = satisfecho; promedio < 4 = no satisfecho.
- Satisfacción general: P17. Respuesta 4–5 = satisfecho; 1–3 = no satisfecho.
- El porcentaje de satisfacción se calcula como N de estudiantes satisfechos / D de estudiantes válidos × 100.
- Los rangos del Word se aplican al porcentaje final de cada dimensión y de P17: 0–59 Insatisfactorio, 60–74 Regular, 75–89 Satisfactorio, 90–100 Muy satisfactorio. En el código se operacionalizan con límites continuos: <60, 60–<75, 75–<90, >=90, antes de redondear.

## Qué NO se hace

- No se construye un indicador global P1–P16 porque el Word no define esa regla global.
- No se usa “Favorable / Neutral / Desfavorable”.
- No se convierte el 3 en una tercera categoría del indicador.
- No se suman 1–3 de los cuatro ítems para decidir la satisfacción de una dimensión. La clasificación dimensional depende del promedio individual de los cuatro ítems.
- No se asigna Insatisfactorio/Regular/Satisfactorio/Muy satisfactorio a P1–P16 como si fueran indicadores institucionales independientes. Por ítem se reporta la distribución 1–5, el porcentaje 4–5, el porcentaje 1–3 y una lectura descriptiva dentro de su dimensión.
- No se muestra el bloque “Marco documental / PEI”.

## Resultados verificados en la base actual (7,677 estudiantes)

- P17 satisfacción general: 5,482 / 7,677 = 71.4% → Regular.
- D1 Calidad del proceso académico: 4,222 / 7,677 = 55.0% → Insatisfactorio.
- D2 Desempeño docente y estrategias pedagógicas: 4,647 / 7,677 = 60.5% → Regular.
- D3 Servicios y gestión educativa: 3,182 / 7,677 = 41.4% → Insatisfactorio.
- D4 Formación integral y desarrollo personal: 4,989 / 7,677 = 65.0% → Regular.

Las columnas calculadas ya presentes en el Excel (`D1_Promedio`–`D4_Promedio`, `D1_Satisfecho`–`D4_Satisfecho` y `Global_Satisfecho`) fueron contrastadas con las reglas anteriores y no presentan diferencias en la base actual.

## Calidad estadística

El tablero mantiene el alfa de Cronbach como análisis complementario de consistencia interna, porque el Word lo señala como siguiente paso. En esta base: alfa P1–P16 ≈ 0.968; D1 ≈ 0.917; D2 ≈ 0.942; D3 ≈ 0.913; D4 ≈ 0.942. El alfa no prueba validez. La V de Aiken no puede calcularse con la base de estudiantes; requiere una matriz de evaluación de jueces expertos.

Los intervalos de confianza al 95% se presentan solo como complemento técnico. Su interpretación inferencial para toda la población requiere un diseño de selección que justifique esa inferencia.

## Ejecución

```bash
python -m streamlit run app.py
```
