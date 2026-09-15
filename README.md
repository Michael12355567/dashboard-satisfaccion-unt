# SIG UNT Streamlit V2

Versión visual mejorada, inspirada en ArcGIS Indoors.

## Subir a GitHub / Streamlit Cloud
- app.py
- requirements.txt

La app es autocontenida: el plano y los polígonos aproximados están embebidos.

## Ejecutar
pip install -r requirements.txt
streamlit run app.py

## Importante
La geometría V2 fue inferida visualmente desde el plano del campus para mejorar el prototipo.
No es todavía cartografía oficial.

El DWG recibido es AutoCAD 2007/2008/2009.
Para la siguiente etapa, exportarlo a DXF permitirá leer la geometría CAD real.
