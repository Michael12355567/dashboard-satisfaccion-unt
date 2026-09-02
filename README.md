# Dashboard UNT — Streamlit Responsive Pro

## Archivos
- `app.py`: aplicación Streamlit.
- `basededatos.xlsx`: base que se carga automáticamente.
- `requirements.txt`: dependencias.
- `.streamlit/config.toml`: tema.

## Ejecutar en Windows
Desde la carpeta del proyecto:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

No existe cargador de Excel en la interfaz. La aplicación siempre lee `basededatos.xlsx` desde la misma carpeta de `app.py`.

## Publicar
Sube estos archivos al mismo repositorio de GitHub y despliega `app.py` en Streamlit Community Cloud.
