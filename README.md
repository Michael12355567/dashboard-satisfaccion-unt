# Portal de Información Estadística UNT — prototipo Streamlit

## Inicio rápido (Windows)
1. Instala Python 3.11 o 3.12 de https://www.python.org/downloads/ y habilita "Add Python to PATH".
2. Extrae completamente este ZIP en una carpeta.
3. Haz doble clic en `INICIAR_WINDOWS.bat`.
4. Abre la dirección local que aparezca en pantalla (normalmente http://localhost:8501).

En terminal también puedes ejecutar:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Módulos
- **Panorama:** totales anuales, indicadores y gráficos interactivos.
- **Explorador:** filtros de facultad, carrera, sede, año, indicador; descarga CSV.
- **Informes:** Word editable y PDF con portada institucional, tablas y notas.
- **Proyecciones:** extrapolación lineal ilustrativa, sin fingir precisión predictiva.
- **Consultas guiadas:** texto libre con patrones de indicadores y años; no requiere API ni envía información externa.
- **Otros indicadores:** consulta 47 tablas institucionales adicionales, sin asignarlas erróneamente a facultades.
- **Administración:** importación de CSV validada en sesión; no modifica datos base.

## Origen y cobertura
El sistema fue construido con las 47 tablas del catálogo `UNT_EN_CIFRAS_2021_2026_INFORME_INSTITUCIONAL_CORREGIDO.docx` disponible en la conversación. Se extrajeron los registros de seis indicadores académicos: vacantes (2022–2026), postulantes, ingresantes y matrícula (2021–2026), bachilleres y titulados (2021–2025). Las demás tablas se ofrecen en una sección institucional de lectura. Esto permite generar reportes genuinos por facultad y carrera para los indicadores con desglose, pero **no** afirma que todos los indicadores estén desglosados ni que los periodos faltantes sean cero.

## Limitaciones para producción
- No hay autenticación, usuarios, roles ni servidor institucional configurado.
- Las consultas en lenguaje natural son reglas deterministas, **no** una IA entrenada.
- Las proyecciones son orientativas y no sustituyen análisis de series temporales validado.
- La plantilla Word/PDF reproduce el estilo general azul/dorado y fotografía de UNT, pero no copia exactamente la carátula histórica o todas las composiciones APA 7.
- No procesa información personal ni debe publicarse sin autorización.
- Las series derivan del catálogo y requieren reconciliación con las fuentes administrativas oficiales antes de difusión pública.

## Flujo sugerido de producción
1. Base PostgreSQL con catálogos maestros de facultad, carrera, sede e indicador.
2. ETL validado, fechas de corte, control de duplicados y conciliación de totales.
3. Autenticación SSO institucional y perfiles de acceso.
4. Cola para informes largos; versionado y auditoría de descargas.
5. Motor IA opcional que solo consulta vistas autorizadas y cita datos.
