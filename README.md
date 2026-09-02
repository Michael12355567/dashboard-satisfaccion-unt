# Dashboard UNT · Streamlit NEO

## Ejecutar localmente
Desde la carpeta que contiene este proyecto:

```powershell
C:\Users\LENOVO\AppData\Local\Programs\Python\Python314\python.exe -m pip install -r Streamlit_UNT_NEO\requirements.txt
C:\Users\LENOVO\AppData\Local\Programs\Python\Python314\python.exe -m streamlit run Streamlit_UNT_NEO\app.py
```

## Publicar en GitHub / Streamlit Community Cloud
Sube juntos `app.py`, `basededatos.xlsx`, `requirements.txt` y la carpeta `.streamlit`.
Si `basededatos.xlsx` está junto a `app.py`, la aplicación lo carga automáticamente y el visitante no necesita subir el Excel.

## Estructura
- `app.py`: aplicación.
- `basededatos.xlsx`: base incluida.
- `requirements.txt`: dependencias.
- `.streamlit/config.toml`: tema visual.
