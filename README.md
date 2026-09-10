# Dashboard UNT — metodología alineada al Word y al Excel

Esta versión conserva el diseño visual, los semáforos y la fórmula tipografiada, pero corrige la lectura metodológica para que el dashboard siga el instrumento y las variables ya calculadas en `basededatos.xlsx`.

## Reglas aplicadas

- **Ítems P1–P16:** lectura descriptiva por pregunta. Respuestas 4–5 se presentan como satisfechos en el ítem y 1–3 como no satisfechos en el ítem. Esta lectura no sustituye el cálculo de la dimensión.
- **D1–D4:** se utiliza el promedio de los cuatro ítems de cada dimensión por estudiante. Promedio >= 4 = Satisfecho; promedio < 4 = No satisfecho.
- **P17:** satisfacción general. Respuesta 4 o 5 = Satisfecho; respuesta 1, 2 o 3 = No satisfecho.
- **Interpretación institucional:** 0–59% Insatisfactorio; 60–74% Regular; 75–89% Satisfactorio; 90–100% Muy satisfactorio. Se aplica al porcentaje final de satisfacción de D1–D4 y P17, no a cada alternativa Likert.
- Se retiró del dashboard el porcentaje global construido con promedio P1–P16, porque esa regla no está definida en el Word como indicador global.

## Resultados de la base Excel

- P17: 5,482 / 7,677 = 71.4% — Regular
- D1: 4,222 / 7,677 = 55.0% — Insatisfactorio
- D2: 4,647 / 7,677 = 60.5% — Regular
- D3: 3,182 / 7,677 = 41.4% — Insatisfactorio
- D4: 4,989 / 7,677 = 65.0% — Regular

## Verificación técnica

- `app.py` compila correctamente.
- Se ejecutó una prueba completa con un stub de Streamlit para verificar que no queden `NameError`/`KeyError` en la lógica principal.
- La aplicación usa las columnas calculadas del Excel (`D1_Promedio`–`D4_Promedio`, `D1_Satisfecho`–`D4_Satisfecho`, `Global_Satisfecho`) cuando están disponibles y tiene cálculo de respaldo si faltan.

Ejecutar con:

```bash
python -m streamlit run app.py
```
