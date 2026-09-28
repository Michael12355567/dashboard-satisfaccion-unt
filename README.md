# Dashboard Streamlit UNT

Aplicación lista para ejecutar con Streamlit. Usa tres bases incluidas en `data/`:

- Convenios nacionales
- Convenios internacionales
- Movilidad académica

## Ejecutar en RStudio / terminal local

Aunque la app está hecha en Python + Streamlit, puede ejecutarse desde una terminal del equipo:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá normalmente en `http://localhost:8501`.

## Publicar en Streamlit Community Cloud

1. Suba **toda esta carpeta** a un repositorio de GitHub.
2. Ingrese a Streamlit Community Cloud.
3. Cree una app nueva y seleccione el repositorio.
4. Como archivo principal indique `app.py`.
5. Despliegue.

No cambie los nombres de los archivos dentro de `data/` sin actualizar `utils.py`.

## Estructura

- `app.py`: Resumen general.
- `pages/1_Convenios.py`: dashboard de convenios.
- `pages/2_Movilidad.py`: dashboard de movilidad.
- `pages/3_Indicadores.py`: indicadores relativos y carga opcional de matrícula.
- `utils.py`: carga, limpieza, estilos y funciones comunes.
- `.streamlit/config.toml`: tema visual.
- `requirements.txt`: dependencias.

## Nota metodológica

2026 puede ser un año parcial. Las comparaciones interanuales deben interpretarse considerando la fecha de corte. La condición de vigencia se calcula con la fecha del servidor al ejecutar la app.
