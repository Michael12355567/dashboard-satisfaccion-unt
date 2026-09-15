# SIG UNT V3 FIX

Corrección del error de Deck.gl:
`Unexpected ":" at character 4`.

La causa era el uso de un Data URI (`data:image/...`) dentro de BitmapLayer.
La V3 elimina ese raster de la escena PyDeck y conserva el plano en la pestaña
de georreferenciación mediante Folium.

## Streamlit Cloud
Subir:
- app.py
- requirements.txt

## Nota
Para que se parezca realmente a ArcGIS Indoors se requieren:
1. DXF/CAD vectorial del campus.
2. Planos arquitectónicos por piso de al menos un pabellón.
3. Red de rutas peatonales/interiores.
4. Para mayor realismo 3D: alturas reales o BIM/Revit.
