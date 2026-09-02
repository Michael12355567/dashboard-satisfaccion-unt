# Dashboard UNT · Satisfacción estudiantil (Streamlit)

## Qué hace esta versión
- Carga `basededatos.xlsx` automáticamente al abrir la app.
- El archivo debe estar en la misma carpeta que `app.py`.
- El cargador de Excel queda como opción para reemplazar temporalmente la base.
- Muestra D1, D2, D3, D4 y P17.
- Incluye semáforo institucional 3D dinámico, nivel e intervalo.
- Mantiene la metodología: D1-D4 se calculan con promedio individual >= 4; P17 se evalúa directamente.

## Estructura para GitHub
```
Streamlit_UNT_3D_Pro/
├── .streamlit/
│   └── config.toml
├── app.py
├── basededatos.xlsx
├── requirements.txt
└── README.md
```

Sube la carpeta completa al repositorio. En Streamlit Community Cloud selecciona `app.py` como archivo principal.

## IMPORTANTE sobre privacidad
Si el repositorio de GitHub es público y subes `basededatos.xlsx`, el archivo también será público. Si la base contiene información que no debe difundirse, usa un repositorio/app privado o elimina el Excel del repositorio y usa el cargador de archivos de la app.

## Ejecutar en Windows
Desde la carpeta del proyecto:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
