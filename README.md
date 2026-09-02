# UNT · Dashboard PEI NEXUS

Versión rediseñada con una jerarquía visual más ejecutiva y menos parecida a Shiny.

## Cambios de diseño
- Cabecera convertida en **centro de control**: identidad UNT a la izquierda y estado del IND.01 a la derecha.
- Navegación renombrada a **Centro ejecutivo / Mapa 4D / Método PEI**.
- La antigua sección “Dimensiones e ítems” se reemplaza por **Mapa 4D**.
- Selector moderno por botones tipo `pills`: Vista 4D, D1, D2, D3 y D4.
- Vista general con **mapa térmico de los 16 ítems** y panel dimensional.
- Al seleccionar D1–D4 aparece un **cockpit de dimensión**, semáforo, brecha, promedio, ítem crítico e ítem fuerte.
- Los cuatro ítems de cada dimensión aparecen como tarjetas 3D compactas, con texto completo, favorable, promedio y barra visual.
- La tabla técnica queda oculta en un desplegable para evitar saturar la pantalla.
- Diseño responsive: escritorio, tablet y celular.
- Gráficos Plotly bloqueados: sin zoom, pan ni desplazamiento al tocar.
- `basededatos.xlsx` se carga automáticamente; no existe cargador de archivos.

## Lógica mantenida
- D1: P1–P4
- D2: P5–P8
- D3: P9–P12
- D4: P13–P16
- Satisfacción dimensional: promedio individual de los 4 ítems >= 4.
- P17 se conserva como satisfacción general declarada separada.
- El IND.01 integral P1–P16 permanece identificado como operacionalización analítica propuesta.

## Ejecutar
```text
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
