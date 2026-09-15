# SIG UNT — Prototipo Streamlit

Este proyecto es un prototipo funcional para demostrar:
- campus 3D con edificios extruidos;
- plano general superpuesto a coordenadas reales de referencia;
- selección de edificio/facultad;
- rutas demostrativas entre edificios;
- plano interior por pisos;
- ambientes (aulas, laboratorios, oficinas, servicios);
- indicadores de infraestructura.

## Importante
Las geometrías de edificios y las cuatro esquinas usadas para el plano son **PROVISIONALES / DEMO**.
No deben emplearse como catastro oficial ni para mediciones.

La Ciudad Universitaria de la UNT se ubica en Av. Juan Pablo II s/n, Trujillo.
La app usa como centro de referencia: latitud -8.114656, longitud -79.038595.

## Instalación en Windows

1. Descomprimir la carpeta.
2. Abrir CMD o PowerShell dentro de la carpeta.
3. Crear entorno virtual (recomendado):

    python -m venv .venv
    .venv\Scripts\activate

4. Instalar dependencias:

    pip install -r requirements.txt

5. Ejecutar:

    streamlit run app.py

6. Abrir la dirección que aparece, normalmente:

    http://localhost:8501

## Para convertirlo en SIG real de la UNT

Reemplazar:
- `data/edificios_demo.csv` por geometrías reales del DWG/DXF;
- `data/puntos_control_provisionales.csv` por puntos medidos;
- `data/ambientes_demo.csv` por inventario oficial de ambientes;
- `assets/plano_campus_unt_referencia.png` por raster georreferenciado o capas vectoriales.

Lo más recomendable para producción es:
PostgreSQL/PostGIS + Python/FastAPI + Streamlit o frontend web + ArcGIS/QGIS para edición cartográfica.

## Próxima versión sugerida
1. Importar DXF real.
2. Convertir capas a GeoJSON.
3. Crear códigos únicos de edificio/piso/ambiente.
4. Agregar red peatonal y rutas.
5. Vincular estadísticas institucionales.
