# Dashboard UNT — ajuste final sin rediseñar

Esta versión parte del `app.py` entregado por el usuario y conserva la apariencia anterior.

## Lo que NO se cambió
- Semáforos 3D.
- Diseño y estructura visual de la fórmula N/D × 100.
- Glassmorphism, tarjetas, donuts y jerarquía general.
- El resultado P1–P16 permanece como lectura visual principal.
- El archivo `basededatos.xlsx` no fue alterado.

## Lo que SÍ se corrigió
- P17 (71.4%) queda en segundo plano y con tipografía claramente menor.
- Se eliminó de la interfaz la sección "Marco documental / PEI".
- Se eliminaron las categorías visibles "Favorable / Neutral / Desfavorable".
- En cada P1–P16 se muestran `Respuestas 4–5`, `Respuestas 1–3` y el promedio.
- La distribución detallada muestra las cinco alternativas Likert originales: 1, 2, 3, 4 y 5.
- D1–D4 mantienen la regla del Word: promedio de los cuatro ítems >= 4.
- P17 mantiene la regla explícita del Word: 4–5 = Satisfecho; 1–3 = No satisfecho.
- Los rangos 0–59 / 60–74 / 75–89 / 90–100 se muestran como criterios de interpretación del porcentaje, no como categorías de respuesta.

## Valores verificados en la base
- N = 7,677
- Lectura integral P1–P16 (promedio individual >=4): 44.6%
- P17 (4–5): 71.4%
- D1: 55.0%
- D2: 60.5%
- D3: 41.4%
- D4: 65.0%

## Ejecución
```bash
python -m streamlit run app.py
```
