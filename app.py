
from pathlib import Path
import math
import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.raster_layers import ImageOverlay
import plotly.graph_objects as go

try:
    import pydeck as pdk
except Exception:
    pdk = None

BASE = Path(__file__).resolve().parent
PLAN = BASE / "assets" / "plano_campus_unt_referencia.png"
REF = BASE / "assets" / "referencia_arcgis_indoors.png"
EDIF = BASE / "data" / "edificios_demo.csv"
ROOMS = BASE / "data" / "ambientes_demo.csv"
GCP = BASE / "data" / "puntos_control_provisionales.csv"

# Coordenada pública de referencia del campus (centro aproximado).
CAMPUS_LAT = -8.114656
CAMPUS_LON = -79.038595

# BBOX PROVISIONAL. Reemplazar por control topográfico / DWG georreferenciado.
DEFAULT_BOUNDS = {
    "sur": -8.11730,
    "norte": -8.11205,
    "oeste": -79.04195,
    "este": -79.03525,
}

st.set_page_config(page_title="SIG UNT | Prototipo", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1rem; padding-bottom: 2rem;}
.small-note {font-size:.86rem; color:#5f6b76;}
.demo-badge {display:inline-block; padding:.2rem .55rem; border-radius:999px; background:#fff3cd; color:#664d03; font-weight:700; font-size:.8rem;}
div[data-testid="stMetricValue"] {font-size: 1.7rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv(EDIF), pd.read_csv(ROOMS), pd.read_csv(GCP)

edificios, ambientes, gcps = load_data()

def meter_offsets(lat):
    m_per_deg_lat = 111_320.0
    m_per_deg_lon = 111_320.0 * math.cos(math.radians(lat))
    return m_per_deg_lat, m_per_deg_lon

def rotated_rect(lat, lon, width_m, height_m, angle_deg=0):
    # Devuelve [lon,lat] para Deck.gl y Folium.
    mlat, mlon = meter_offsets(lat)
    halfx, halfy = width_m/2, height_m/2
    a = math.radians(angle_deg)
    pts = []
    for x,y in [(-halfx,-halfy),(halfx,-halfy),(halfx,halfy),(-halfx,halfy)]:
        xr = x*math.cos(a)-y*math.sin(a)
        yr = x*math.sin(a)+y*math.cos(a)
        pts.append([lon + xr/mlon, lat + yr/mlat])
    return pts

def rgba_for_type(t):
    return {
        "Facultad":[52, 125, 184, 190],
        "Biblioteca":[76, 175, 80, 205],
        "Posgrado":[123, 104, 238, 195],
        "Servicio":[255, 167, 38, 195],
        "Deporte":[38, 166, 154, 185],
    }.get(t, [120,120,120,190])

def folium_color(t):
    return {
        "Facultad":"#347db8",
        "Biblioteca":"#4caf50",
        "Posgrado":"#7b68ee",
        "Servicio":"#ffa726",
        "Deporte":"#26a69a",
    }.get(t, "#777777")

def prepare_buildings(df):
    items=[]
    for _,r in df.iterrows():
        poly = rotated_rect(r.lat,r.lon,r.ancho_m,r.largo_m,r.angulo)
        items.append({
            **r.to_dict(),
            "polygon": poly,
            "color": rgba_for_type(r.tipo),
            "label": r.nombre.replace(" (DEMO)",""),
        })
    return items

bitems = prepare_buildings(edificios)
by_name = {x["nombre"]:x for x in bitems}

st.title("SIG UNT — prototipo georreferenciado + interiores")
st.caption("Demo para Streamlit. La ubicación general usa una coordenada real de referencia; las geometrías de edificios y la georreferenciación del plano son PROVISIONALES hasta reemplazarlas con DWG/DXF o puntos topográficos oficiales.")
st.markdown('<span class="demo-badge">PROTOTIPO — NO USAR COMO CATASTRO OFICIAL</span>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🧭 Control")
    edificio_sel = st.selectbox("Edificio / Facultad", edificios["nombre"].tolist(), index=0)
    start_name = st.selectbox("Origen de ruta", edificios["nombre"].tolist(), index=1)
    dest_name = st.selectbox("Destino de ruta", edificios["nombre"].tolist(), index=0)
    piso = st.selectbox("Piso interior", [1,2,3], index=0)

    st.divider()
    st.subheader("Georreferencia del plano")
    st.caption("Ajusta estas 4 coordenadas cuando tengas puntos de control reales.")
    sur = st.number_input("Sur", value=float(DEFAULT_BOUNDS["sur"]), format="%.6f")
    norte = st.number_input("Norte", value=float(DEFAULT_BOUNDS["norte"]), format="%.6f")
    oeste = st.number_input("Oeste", value=float(DEFAULT_BOUNDS["oeste"]), format="%.6f")
    este = st.number_input("Este", value=float(DEFAULT_BOUNDS["este"]), format="%.6f")
    opacidad = st.slider("Opacidad del plano", 0.05, 1.0, 0.48, 0.05)

selected = by_name[edificio_sel]
start = by_name[start_name]
dest = by_name[dest_name]

route_path = [[start["lon"], start["lat"]], [dest["lon"], dest["lat"]]]

m1,m2,m3,m4 = st.columns(4)
m1.metric("Edificio seleccionado", selected["label"])
m2.metric("Aulas", int(selected["aulas"]))
m3.metric("Laboratorios", int(selected["laboratorios"]))
m4.metric("Capacidad referencial", f'{int(selected["capacidad"]):,}')

tabs = st.tabs(["🏙️ Campus 3D", "🗺️ Plano georreferenciado", "🏢 Interiores", "📊 Indicadores", "🎯 Calibración"])

with tabs[0]:
    st.subheader("Vista 3D tipo campus")
    st.write("Los bloques se extruyen por altura y pueden vincularse a una ficha estadística. La línea representa una ruta demostrativa.")

    if pdk is None:
        st.warning("Falta pydeck. Ejecuta: pip install pydeck")
    else:
        layers = [
            pdk.Layer(
                "PolygonLayer",
                data=bitems,
                get_polygon="polygon",
                get_fill_color="color",
                get_line_color=[35,35,35,160],
                line_width_min_pixels=1,
                extruded=True,
                get_elevation="altura_m",
                elevation_scale=1,
                pickable=True,
                auto_highlight=True,
            ),
            pdk.Layer(
                "TextLayer",
                data=bitems,
                get_position="[lon, lat]",
                get_text="label",
                get_size=12,
                get_color=[20,20,20,220],
                get_angle=0,
                get_text_anchor="'middle'",
                get_alignment_baseline="'center'",
                billboard=True,
                pickable=False,
            ),
            pdk.Layer(
                "PathLayer",
                data=[{"path": route_path}],
                get_path="path",
                get_width=5,
                width_min_pixels=5,
                get_color=[0, 92, 230, 235],
                pickable=False,
            ),
        ]
        view = pdk.ViewState(
            latitude=CAMPUS_LAT,
            longitude=CAMPUS_LON,
            zoom=16.5,
            pitch=52,
            bearing=-18,
        )
        deck = pdk.Deck(
            layers=layers,
            initial_view_state=view,
            map_provider="carto",
            map_style="light",
            tooltip={
                "html":"<b>{label}</b><br/>Tipo: {tipo}<br/>Pisos: {pisos}<br/>Aulas: {aulas}<br/>Labs: {laboratorios}<br/>Capacidad: {capacidad}",
                "style":{"backgroundColor":"#ffffff","color":"#111111"}
            }
        )
        st.pydeck_chart(deck, use_container_width=True, height=680)

    st.info("Para que el 3D coincida exactamente con la UNT, el siguiente paso es sustituir estos polígonos demo por geometrías extraídas del DWG/DXF oficial.")

with tabs[1]:
    st.subheader("Plano de campus superpuesto sobre mapa")
    st.write("Aquí sí estás viendo el concepto de **georreferenciación**: una imagen/plano se coloca dentro de coordenadas reales.")

    fmap = folium.Map(
        location=[CAMPUS_LAT, CAMPUS_LON],
        zoom_start=17,
        control_scale=True,
        tiles="OpenStreetMap"
    )
    try:
        ImageOverlay(
            image=str(PLAN),
            bounds=[[sur,oeste],[norte,este]],
            opacity=opacidad,
            interactive=True,
            cross_origin=False,
            zindex=1,
            name="Plano UNT (provisional)"
        ).add_to(fmap)
    except Exception as e:
        st.warning(f"No se pudo cargar el overlay del plano: {e}")

    for item in bitems:
        latlon_poly = [[p[1],p[0]] for p in item["polygon"]]
        popup = (
            f"<b>{item['label']}</b><br>"
            f"Tipo: {item['tipo']}<br>"
            f"Pisos: {int(item['pisos'])}<br>"
            f"Aulas: {int(item['aulas'])}<br>"
            f"Laboratorios: {int(item['laboratorios'])}<br>"
            f"Capacidad: {int(item['capacidad'])}"
        )
        folium.Polygon(
            locations=latlon_poly,
            color=folium_color(item["tipo"]),
            fill=True,
            fill_opacity=0.18,
            weight=2,
            popup=folium.Popup(popup, max_width=300),
            tooltip=item["label"]
        ).add_to(fmap)

    folium.PolyLine(
        locations=[[start["lat"],start["lon"]],[dest["lat"],dest["lon"]]],
        color="#005ce6",
        weight=6,
        opacity=0.9,
        tooltip=f"Ruta DEMO: {start['label']} → {dest['label']}"
    ).add_to(fmap)
    folium.Marker([start["lat"],start["lon"]], tooltip="Origen", icon=folium.Icon(color="green", icon="play")).add_to(fmap)
    folium.Marker([dest["lat"],dest["lon"]], tooltip="Destino", icon=folium.Icon(color="red", icon="flag")).add_to(fmap)

    folium.LayerControl(collapsed=False).add_to(fmap)
    components.html(fmap.get_root().render(), height=720)

    st.caption("IMPORTANTE: el ajuste actual se hace con un rectángulo de 4 esquinas. Para precisión institucional, hay que usar puntos de control medidos o un DWG/DXF ya georreferenciado.")

with tabs[2]:
    st.subheader(f"Plano interior — {selected['label']} — Piso {piso}")
    piso_df = ambientes[ambientes["piso"]==piso].copy()

    type_fill = {
        "Aula":"rgba(65,105,225,0.28)",
        "Laboratorio":"rgba(0,150,136,0.30)",
        "Oficina":"rgba(255,167,38,0.28)",
        "Servicio":"rgba(156,39,176,0.25)",
        "Circulación":"rgba(120,120,120,0.18)",
        "Auditorio":"rgba(229,57,53,0.24)",
        "Acceso":"rgba(46,125,50,0.30)",
    }

    fig = go.Figure()
    # corredor principal
    fig.add_shape(type="rect", x0=0,y0=30,x1=82,y1=34, line=dict(color="gray",width=1), fillcolor="rgba(180,180,180,0.14)")
    fig.add_annotation(x=41,y=32,text="PASILLO",showarrow=False,font=dict(size=11,color="gray"))

    for _,r in piso_df.iterrows():
        fill = type_fill.get(r.tipo,"rgba(100,100,100,0.2)")
        fig.add_shape(type="rect", x0=r.x0,y0=r.y0,x1=r.x1,y1=r.y1,
                      line=dict(color="#333",width=1.5), fillcolor=fill)
        cap = f"<br>{int(r.capacidad)} pers." if r.capacidad and r.capacidad>0 else ""
        fig.add_annotation(
            x=(r.x0+r.x1)/2, y=(r.y0+r.y1)/2,
            text=f"<b>{r.codigo}</b><br>{r.ambiente}{cap}",
            showarrow=False, align="center", font=dict(size=11)
        )
    # demo route: entry -> corridor -> selected laboratory/aula
    target = piso_df[piso_df["tipo"].isin(["Laboratorio","Aula"])].iloc[-1]
    tx,ty = (target.x0+target.x1)/2,(target.y0+target.y1)/2
    fig.add_trace(go.Scatter(
        x=[9,9,41,tx], y=[4,32,32,ty],
        mode="lines+markers",
        line=dict(width=5, color="#005ce6"),
        marker=dict(size=8),
        name="Ruta interior DEMO",
        hovertemplate="Ruta interior<extra></extra>"
    ))
    fig.update_xaxes(visible=False, range=[-2,84])
    fig.update_yaxes(visible=False, range=[-2,55], scaleanchor="x", scaleratio=1)
    fig.update_layout(height=610, margin=dict(l=10,r=10,t=20,b=10), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

    c1,c2 = st.columns([1.2,1])
    with c1:
        st.dataframe(piso_df[["codigo","ambiente","tipo","capacidad"]], use_container_width=True, hide_index=True)
    with c2:
        st.markdown("#### Qué se puede registrar por ambiente")
        st.write("Código, facultad/escuela, piso, área m², capacidad, equipamiento, estado, responsable, horario, fotografía, accesibilidad y estadísticas de uso.")
        st.info("Para navegación interior real hay que dibujar la red de pasillos/puertas/escaleras y, si deseas el punto azul en tiempo real, incorporar IPS/Wi‑Fi/Bluetooth.")

with tabs[3]:
    st.subheader("Indicadores espaciales y de infraestructura")
    tot_aulas = int(edificios["aulas"].sum())
    tot_labs = int(edificios["laboratorios"].sum())
    tot_cap = int(edificios["capacidad"].sum())
    tot_edif = len(edificios)

    a,b,c,d = st.columns(4)
    a.metric("Edificios demo", tot_edif)
    b.metric("Aulas demo", tot_aulas)
    c.metric("Laboratorios demo", tot_labs)
    d.metric("Capacidad demo", f"{tot_cap:,}")

    chart = edificios.sort_values("capacidad", ascending=True).copy()
    chart["nombre_corto"] = chart["nombre"].str.replace(" (DEMO)","", regex=False)
    figb = go.Figure(go.Bar(
        x=chart["capacidad"], y=chart["nombre_corto"], orientation="h",
        text=chart["capacidad"], textposition="outside"
    ))
    figb.update_layout(height=560, margin=dict(l=10,r=30,t=20,b=20), xaxis_title="Capacidad referencial", yaxis_title="")
    st.plotly_chart(figb, use_container_width=True)
    st.caption("Cuando conectes la base institucional, estos indicadores dejan de ser demo y pueden actualizarse automáticamente desde PostgreSQL/PostGIS, SQL Server o APIs.")

with tabs[4]:
    st.subheader("Cómo convertir este prototipo en georreferenciación exacta")
    col1,col2 = st.columns([1,1])
    with col1:
        st.image(PLAN, caption="Plano general UNT usado como referencia visual.", use_container_width=True)
        st.dataframe(gcps, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("""
        **Este prototipo usa un BBOX provisional**, suficiente para comprobar la idea en Streamlit, pero no es una rectificación cartográfica.

        Para pasar a precisión real:

        1. Conseguir el **DWG/DXF oficial** o levantar al menos 4–8 puntos de control visibles en el plano.
        2. Registrar las coordenadas reales de esos puntos en un sistema definido (por ejemplo WGS84 / UTM 17S).
        3. Aplicar una transformación afín/proyectiva al plano.
        4. Digitalizar edificios, áreas verdes, vías y accesos.
        5. Guardar geometrías en **GeoJSON/PostGIS**.
        6. Para cada pabellón, cargar planos por piso y codificar ambientes.
        """)
        st.warning("No tomes las posiciones de las facultades de este demo como ubicación oficial. Son bloques ilustrativos para probar la interfaz.")

st.divider()
st.caption("SIG UNT — prototipo Streamlit • Python + Folium + PyDeck + Plotly • Preparado para sustituir los datos demo por cartografía oficial.")
