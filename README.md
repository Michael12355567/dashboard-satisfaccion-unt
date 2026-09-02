# UNT · Dashboard PEI de satisfacción

## Qué cambia en esta versión
- No existe botón para subir Excel: `basededatos.xlsx` se lee automáticamente.
- Se separan dos resultados globales:
  - **IND.01 integral propuesto**: promedio P1–P16 por estudiante; satisfecho si promedio >= 4; luego N/D x 100.
  - **P17**: satisfacción general declarada, mostrada como medida complementaria.
- D1, D2, D3 y D4 aparecen como diagnóstico dimensional.
- Semáforos 3D vectoriales (SVG) sin archivos de imagen externos.
- Diseño responsive para PC, tablet y celular.
- Gráficos Plotly bloqueados: sin zoom, pan ni desplazamiento al tocar.
- Metas PEI mostradas: 2027 60%, 2028 65%, 2029 70%, 2030 75%.

## Nota metodológica
La ficha PEI compartida define el indicador N/D x 100 y el criterio “satisfecho”, pero la imagen no especifica el algoritmo exacto para agregar múltiples ítems. Por ello, la regla `promedio P1-P16 >= 4` se presenta como **operacionalización analítica propuesta** y debe validarse institucionalmente antes de usarla como resultado PEI oficial.

## Ejecutar
```text
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
