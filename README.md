# Dashboard UNT — Word como base, diseño conservado

Esta versión parte del `app.py` entregado por el usuario y **conserva el diseño visual existente**, especialmente:

- semáforos 3D;
- fórmula tipografiada N/D × 100 con fracción;
- glassmorphism, tarjetas, tipografía, colores y comportamiento responsive.

## Correcciones metodológicas

1. **Indicador general:** se muestra P17 como satisfacción general.
   - 4 o 5 = Satisfecho.
   - 1, 2 o 3 = No satisfecho.
2. **Dimensiones D1–D4:** satisfacción por estudiante cuando el promedio de los cuatro ítems de la dimensión es ≥4.
3. **Preguntas P1–P16:** se presentan descriptivamente como porcentaje de respuestas 4–5 y 1–3, sin inventar las categorías "Favorable / Neutral / Desfavorable".
4. **Distribución Likert:** se muestran las cinco respuestas originales 1, 2, 3, 4 y 5.
5. **Interpretación institucional:** 0–59% Insatisfactorio; 60–74% Regular; 75–89% Satisfactorio; 90–100% Muy satisfactorio.
6. Se retiró de la interfaz el bloque de **Marco documental / PEI**, porque no forma parte del cálculo de la encuesta solicitado para este tablero.
7. No se usa un promedio P1–P16 como indicador global, porque esa regla no está definida de forma explícita en el instrumento proporcionado.

## Ejecutar

```bash
python -m streamlit run app.py
```
