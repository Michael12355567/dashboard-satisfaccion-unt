import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_config, hero, load_data, fmt_int, fmt_pct, apply_plot_style, sidebar_brand

page_config("Resumen estadístico | UNT")
sidebar_brand()

nac, inte, mov, conv = load_data()
hero("Resumen estadístico institucional", "Convenios nacionales e internacionales y movilidad académica de la Universidad Nacional de Trujillo")

# Filtro de año
anios = sorted(set(conv["Año"].dropna().astype(int).tolist()) | set(mov["AÑO"].dropna().astype(int).tolist()))
sel_anio = st.sidebar.selectbox("Año", ["Todos"] + anios, index=0)

conv_f = conv.copy()
mov_f = mov.copy()
if sel_anio != "Todos":
    conv_f = conv_f[conv_f["Año"] == sel_anio]
    mov_f = mov_f[mov_f["AÑO"] == sel_anio]

# KPIs
conv_total = len(conv_f)
conv_vig = int((conv_f["Estado"] == "Vigente").sum())
mov_total = mov_f["TOTAL"].sum()
mov_int = mov_f.loc[mov_f["MODALIDAD"].str.upper() == "INTERNACIONAL", "TOTAL"].sum()
mov_in = mov_f.loc[mov_f["MOVILIDAD"].str.upper().str.contains("MIGRATORIA") & ~mov_f["MOVILIDAD"].str.upper().str.startswith("E"), "TOTAL"].sum()
# robusto ante IMIGRATORIA / INMIGRATORIA
if mov_in == 0:
    mov_in = mov_f.loc[mov_f["MOVILIDAD"].str.upper().isin(["IMIGRATORIA","INMIGRATORIA"]), "TOTAL"].sum()
paises = conv_f.loc[conv_f["Ámbito"] == "Internacional", "País"].replace({"Méxcio":"México"}).dropna().nunique()

pct_int = (mov_int / mov_total * 100) if mov_total else 0
pct_in = (mov_in / mov_total * 100) if mov_total else 0

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Convenios", fmt_int(conv_total))
c2.metric("Convenios vigentes", fmt_int(conv_vig))
c3.metric("Movilidades", fmt_int(mov_total))
c4.metric("Movilidad internacional", fmt_pct(pct_int))
c5.metric("Países vinculados", fmt_int(paises))
c6.metric("Movilidad entrante", fmt_pct(pct_in))

st.markdown('<div class="section-title">Indicadores que explican el alcance institucional</div>', unsafe_allow_html=True)

col1,col2 = st.columns([1.25,1])
with col1:
    annual = mov.groupby("AÑO", as_index=False)["TOTAL"].sum().sort_values("AÑO")
    fig = px.line(annual, x="AÑO", y="TOTAL", markers=True, title="Evolución de la movilidad académica")
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_yaxes(title="Movilidades")
    fig.update_xaxes(title="Año", dtick=1)
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)
with col2:
    comp = mov_f.groupby("MODALIDAD", as_index=False)["TOTAL"].sum()
    fig = px.pie(comp, names="MODALIDAD", values="TOTAL", hole=.62, title="Composición de la movilidad")
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)

col3,col4 = st.columns(2)
with col3:
    cy = conv.groupby(["Año","Ámbito"], as_index=False).size().rename(columns={"size":"Convenios"}).dropna()
    cy["Año"] = cy["Año"].astype(int)
    fig = px.bar(cy, x="Año", y="Convenios", color="Ámbito", barmode="group", title="Convenios registrados por año y ámbito")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)
with col4:
    top = (mov_f.groupby("REGIÓN / PAÍS", as_index=False)["TOTAL"].sum()
           .sort_values("TOTAL", ascending=False).head(10).sort_values("TOTAL"))
    fig = px.bar(top, x="TOTAL", y="REGIÓN / PAÍS", orientation="h", title="Principales regiones / países de movilidad")
    fig.update_xaxes(title="Movilidades")
    fig.update_yaxes(title="")
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)

# Lectura automática
est = mov_f.loc[mov_f["QUIÉN"].str.upper() == "ESTUDIANTIL", "TOTAL"].sum()
pct_est = est / mov_total * 100 if mov_total else 0
st.markdown(
    f'<div class="insight"><b>Lectura estadística:</b> {fmt_pct(pct_int)} de la movilidad seleccionada es internacional, '
    f'{fmt_pct(pct_est)} corresponde a estudiantes y {fmt_pct(pct_in)} es movilidad entrante. '
    'Estos indicadores permiten observar internacionalización, composición y capacidad de atracción, no solo conteos.</div>',
    unsafe_allow_html=True,
)

st.markdown("### Ir al detalle")
a,b,c = st.columns(3)
with a:
    st.page_link("pages/1_Convenios.py", label="🤝 Abrir Convenios", use_container_width=True)
with b:
    st.page_link("pages/2_Movilidad.py", label="✈️ Abrir Movilidad", use_container_width=True)
with c:
    st.page_link("pages/3_Indicadores.py", label="📈 Abrir Indicadores", use_container_width=True)

st.caption("Nota: 2026 puede contener información parcial. La vigencia de convenios se calcula con la fecha actual del servidor.")
