# Dashboard UNT — Satisfacción con la formación académica integral

Versión corregida para que el tablero siga la metodología del instrumento proporcionado.

## Criterios aplicados

- Escala Likert: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Totalmente de acuerdo.
- Por pregunta: **Satisfecho = 4 o 5**; **No satisfecho = 1, 2 o 3**.
- D1 (P1–P4), D2 (P5–P8), D3 (P9–P12), D4 (P13–P16): un estudiante es satisfecho en la dimensión si su **promedio de los cuatro ítems es >= 4**.
- Satisfacción general: **P17**, satisfecho si responde 4 o 5.
- Fórmula de porcentaje: **(N / D) × 100**.
- Escala interpretativa propuesta: 0–59% Insatisfactorio; 60–74% Regular; 75–89% Satisfactorio; 90–100% Muy satisfactorio.

## Resultado observado en la base incluida

- P17 satisfacción general: **71.4%** (5,482 de 7,677).
- D1: **55.0%**.
- D2: **60.5%**.
- D3: **41.4%**.
- D4: **65.0%**.
- Pregunta con menor satisfacción entre P1–P16: **P11 = 47.5%**.
- Pregunta con mayor satisfacción entre P1–P16: **P13 = 80.5%**.

## Cambios principales del tablero

- P17 pasa a ser la lectura global principal.
- Se elimina el uso de categorías adicionales para la satisfacción por pregunta.
- Cada tarjeta de pregunta muestra **Satisfechos 4–5**, **No satisfechos 1–3** y promedio.
- La distribución por pregunta conserva las **cinco alternativas Likert originales**.
- Se incluye P17 dentro del explorador de preguntas.
- Las dimensiones mantienen la regla de promedio individual >= 4.
- Se conserva el diseño visual institucional y responsivo.

## Ejecución

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Los archivos `app.py` y `basededatos.xlsx` deben permanecer en la misma carpeta.
