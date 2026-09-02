# UNT · Dashboard PEI de satisfacción — Visual 3D Pro

## Esta versión parte de “Refinado Visual”
No cambia la lógica ni la estructura principal del dashboard. Se rediseñaron únicamente las visualizaciones que se veían demasiado básicas.

### Visualizaciones nuevas
- **Perfil 4D:** las barras planas D1–D4 se reemplazan por torres 3D estáticas con línea de referencia PEI 2027 (60%).
- **Ruta PEI 2027–2030:** la línea simple se reemplaza por una trayectoria visual con hitos 60%, 65%, 70% y 75%.
- **Ítems P1–P16:** el ranking de barras se reemplaza por un muro diagnóstico 4D. Cada dimensión conserva sus cuatro ítems y cada tarjeta muestra valoración favorable, promedio y pregunta.
- **Distribución Likert:** las barras apiladas se reemplazan por cápsulas 3D estáticas para 1–2, 3 y 4–5.
- **Sin movimiento:** las nuevas visualizaciones son HTML/CSS, por lo que no hacen pan, zoom ni se desplazan al tocar.
- **Responsive:** PC, tablet y celular.

## Se mantiene
- Carga automática de `basededatos.xlsx`.
- IND.01 integral propuesto y P17 separados.
- D1, D2, D3 y D4.
- Semáforos 3D.
- Fórmula N/D × 100.
- Escala institucional de cuatro niveles.
- Selector por dimensión y tabla técnica.

## Ejecutar
```text
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
