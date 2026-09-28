import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_config, hero, load_data, fmt_int, fmt_pct, apply_plot_style, sidebar_brand, download_csv

page_config("Movilidad académica | UNT")
sidebar_brand()
_, _, mov, _ = load_data()
hero("Movilidad académica", "Composición, evolución, destinos y participación de estudiantes y docentes")

st.sidebar.subheader("Filtros")
anios = sorted(mov["AÑO"].dropna().astype(int).unique().tolist())
anio = st.sidebar.selectbox("Año", ["Todos"] + anios)
mod = st.sidebar.selectbox("Modalidad", ["Todos"] + sorted(mov["MODALIDAD"].dropna().unique().tolist()))
quien = st.sidebar.selectbox("Participante", ["Todos"] + sorted(mov["QUIÉN"].dropna().unique().tolist()))
movtipo = st.sidebar.selectbox("Tipo de movilidad", ["Todos"] + sorted(mov["MOVILIDAD"].dropna().unique().tolist()))

f = mov.copy()
if anio != "Todos": f = f[f["AÑO"] == anio]
if mod != "Todos": f = f[f["MODALIDAD"] == mod]
if quien != "Todos": f = f[f["QUIÉN"] == quien]
if movtipo != "Todos": f = f[f["MOVILIDAD"] == movtipo]

total = f["TOTAL"].sum()
intl = f.loc[f["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
est = f.loc[f["QUIÉN"].str.upper()=="ESTUDIANTIL","TOTAL"].sum()
doc = f.loc[f["QUIÉN"].str.upper()=="DOCENTE","TOTAL"].sum()
inm = f.loc[f["MOVILIDAD"].str.upper().isin(["IMIGRATORIA","INMIGRATORIA"]),"TOTAL"].sum()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Movilidades", fmt_int(total))
c2.metric("Internacional", fmt_pct(intl/total*100 if total else 0))
c3.metric("Estudiantes", fmt_int(est))
c4.metric("Docentes", fmt_int(doc))
c5.metric("Entrante", fmt_pct(inm/total*100 if total else 0))

p1,p2 = st.columns(2)
with p1:
    anual = mov.groupby(["AÑO","MODALIDAD"], as_index=False)["TOTAL"].sum().sort_values("AÑO")
    fig = px.line(anual, x="AÑO", y="TOTAL", color="MODALIDAD", markers=True, title="Movilidad por año y modalidad")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)
with p2:
    comp = f.groupby("MOVILIDAD", as_index=False)["TOTAL"].sum()
    fig = px.pie(comp, names="MOVILIDAD", values="TOTAL", hole=.6, title="Movilidad saliente y entrante")
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)

p3,p4 = st.columns(2)
with p3:
    carreras = (f.groupby("CARRERA PROFESIONAL", as_index=False)["TOTAL"].sum().sort_values("TOTAL", ascending=False).head(12).sort_values("TOTAL"))
    fig = px.bar(carreras, x="TOTAL", y="CARRERA PROFESIONAL", orientation="h", title="Carreras con mayor movilidad")
    fig.update_yaxes(title="")
    st.plotly_chart(apply_plot_style(fig, 450), use_container_width=True)
with p4:
    destinos = (f.groupby("REGIÓN / PAÍS", as_index=False)["TOTAL"].sum().sort_values("TOTAL", ascending=False).head(12).sort_values("TOTAL"))
    fig = px.bar(destinos, x="TOTAL", y="REGIÓN / PAÍS", orientation="h", title="Principales regiones / países")
    fig.update_yaxes(title="")
    st.plotly_chart(apply_plot_style(fig, 450), use_container_width=True)

p5,p6 = st.columns(2)
with p5:
    gen = f.groupby("GÉNERO", as_index=False)["TOTAL"].sum()
    fig = px.bar(gen, x="GÉNERO", y="TOTAL", title="Participación por género")
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)
with p6:
    uni_col = "UNIVERSIDAD DE DESTINO"
    tops = (f.groupby(uni_col, as_index=False)["TOTAL"].sum().sort_values("TOTAL", ascending=False).head(10).sort_values("TOTAL"))
    fig = px.bar(tops, x="TOTAL", y=uni_col, orientation="h", title="Universidades de destino más frecuentes")
    fig.update_yaxes(title="")
    st.plotly_chart(apply_plot_style(fig, 410), use_container_width=True)

st.markdown("### Base de movilidad")
st.dataframe(f, use_container_width=True, hide_index=True, height=430)
download_csv(f, "movilidad_filtrada.csv")
