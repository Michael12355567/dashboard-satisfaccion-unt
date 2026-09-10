# Dashboard UNT — versión Word + Excel auditada

Esta versión toma el **Word como base metodológica** y el **Excel como base de datos**.

## Lógica implementada

- **Satisfacción general:** P17.
  - Satisfecho: respuesta 4 o 5.
  - No satisfecho: respuesta 1, 2 o 3.
- **Dimensiones D1–D4:** se calcula el promedio individual de los 4 ítems de cada dimensión.
  - Satisfecho en la dimensión: promedio >= 4.
- **Preguntas P1–P16:** se muestran de forma descriptiva como respuestas 4–5 y respuestas 1–3.
  - No se crea una categoría "Neutral".
  - No se usa "Favorable / Neutral / Desfavorable" como clasificación del indicador.
- **Criterios de interpretación del porcentaje:**
  - 0–59% Insatisfactorio
  - 60–74% Regular
  - 75–89% Satisfactorio
  - 90–100% Muy satisfactorio
- Estos niveles se aplican al **porcentaje ya calculado**, no a las respuestas individuales 1–5.
- Se eliminó de la interfaz el bloque de **Marco documental / PEI**.

## Control del Excel

El tablero recalcula los resultados desde P1–P17 y contrasta las columnas derivadas del Excel cuando existen.

## Ejecutar

```bash
python -m streamlit run app.py
```
