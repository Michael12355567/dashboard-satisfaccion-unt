# Dashboard UNT — versión estilo Power BI

## Qué incluye
- Filtros superiores tipo Power BI: Año, Sede, Facultad, Carrera y Modalidad.
- Botón "Quitar filtros".
- Filtros dependientes: Facultad -> Carrera.
- KPI, gráficos y tablas se recalculan automáticamente.
- Matrícula: SOLO Periodo 1. No se suma con Periodo 2.
- Indicadores normalizados por cada 1 000 matriculados.
- Convenios nacionales e internacionales.
- Movilidad académica.
- Base de datos exportable.

## Publicación
Sube TODO el contenido de esta carpeta a GitHub y usa `app.py` como Main file path.

Si ya tenías una versión anterior:
1. Reemplaza `app.py`, `utils.py`, `requirements.txt`.
2. Reemplaza completa la carpeta `data/`.
3. Reemplaza `.streamlit/config.toml`.
4. En Streamlit Cloud: Manage app -> Reboot app.

## Importante sobre Sede
La base de movilidad entregada no tiene campo sede. Por eso el filtro Sede afecta matrícula y las tasas
normalizadas, pero no puede filtrar el conteo bruto de movilidad sin inventar información.
