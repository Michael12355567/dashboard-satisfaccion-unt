# Dashboard UNT auditado contra el Word y el Excel

Esta versión reconstruye el indicador directamente desde P1–P17 y elimina interpretaciones que no pertenecen a la regla operativa del instrumento.

## Reglas aplicadas

- **Satisfacción general:** P17.
  - Satisfecho = respuesta 4 o 5.
  - No satisfecho = respuesta 1, 2 o 3.
- **D1:** promedio individual P1–P4 >= 4.
- **D2:** promedio individual P5–P8 >= 4.
- **D3:** promedio individual P9–P12 >= 4.
- **D4:** promedio individual P13–P16 >= 4.
- **Por pregunta:** 4–5 = satisfecho; 1–3 = no satisfecho.
- **Fórmula:** (N de satisfechos / D de respuestas válidas) x 100.

## Criterios de interpretación del porcentaje

La propuesta del instrumento incluye:

- 0–59%: Insatisfactorio
- 60–74%: Regular
- 75–89%: Satisfactorio
- 90–100%: Muy satisfactorio

En el código se implementan como intervalos continuos para porcentajes con decimales: <60%, 60–<75%, 75–<90%, >=90%.

Estos rangos clasifican **el porcentaje de satisfacción**, no las respuestas individuales. No se utilizan categorías “favorable / neutral / desfavorable”.

## Resultados verificados en basededatos.xlsx

Base: 7,677 estudiantes; 0 respuestas faltantes P1–P17; 0 valores fuera de 1–5.

- P17 satisfacción general: 5,482 / 7,677 = **71.4% (Regular)**
- D1: 4,222 / 7,677 = **55.0% (Insatisfactorio)**
- D2: 4,647 / 7,677 = **60.5% (Regular)**
- D3: 3,182 / 7,677 = **41.4% (Insatisfactorio)**
- D4: 4,989 / 7,677 = **65.0% (Regular)**

Las columnas calculadas presentes en el Excel (promedios y dicotomías D1–D4, Global_Satisfecho y Categoria_Global) fueron contrastadas contra las respuestas originales y coinciden.

## Qué se eliminó

- “Favorable / Neutral / Desfavorable”.
- “Marco documental / Referencia PEI”.
- El promedio P1–P16 como supuesto indicador global.
- Pruebas inferenciales y psicométricas del tablero principal, porque no forman parte de la fórmula operativa del indicador.

## Ejecutar

```bash
python -m streamlit run app.py
```
