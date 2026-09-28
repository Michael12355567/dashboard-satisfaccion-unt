import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_config, hero, load_data, fmt_int, fmt_pct, apply_plot_style, sidebar_brand, download_csv

page_config("Convenios | UNT")
sidebar_brand()
_, _, _, conv = load_data()
hero("Convenios institucionales", "Análisis estadístico conjunto de convenios nacionales e internacionales")

# filtros
st.sidebar.subheader("Filtros")
ambitos = ["Todos"] + sorted(conv["Ámbito"].dropna().unique().tolist())
amb = st.sidebar.selectbox("Ámbito", ambitos)
anios = sorted(conv["Año"].dropna().astype(int).unique().tolist())
anio = st.sidebar.selectbox("Año de registro", ["Todos"] + anios)
estados = ["Todos"] + sorted(conv["Estado"].dropna().unique().tolist())
estado = st.sidebar.selectbox("Estado", estados)

f = conv.copy()
if amb != "Todos": f = f[f["Ámbito"] == amb]
if anio != "Todos": f = f[f["Año"] == anio]
if estado != "Todos": f = f[f["Estado"] == estado]

vig = (f["Estado"] == "Vigente").sum()
prox = (f["Estado"] == "Próximo a vencer").sum()
inter = (f["Ámbito"] == "Internacional").sum()
paises = f.loc[f["Ámbito"] == "Internacional", "País"].dropna().nunique()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total convenios", fmt_int(len(f)))
c2.metric("Vigentes", fmt_int(vig))
c3.metric("Próximos a vencer", fmt_int(prox))
c4.metric("Internacionales", fmt_int(inter))
c5.metric("Países", fmt_int(paises))

x1,x2 = st.columns(2)
with x1:
    est = f.groupby("Estado", as_index=False).size().rename(columns={"size":"Total"})
    fig = px.bar(est, x="Estado", y="Total", title="Estado de los convenios")
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)
with x2:
    tipo = f.groupby(["Ámbito","Tipo"], as_index=False).size().rename(columns={"size":"Total"}).sort_values("Total", ascending=False).head(12)
    fig = px.bar(tipo, x="Total", y="Tipo", color="Ámbito", orientation="h", title="Tipos de convenio más frecuentes")
    fig.update_yaxes(title="")
    st.plotly_chart(apply_plot_style(fig, 430), use_container_width=True)

x3,x4 = st.columns(2)
with x3:
    anual = f.dropna(subset=["Año"]).groupby(["Año","Ámbito"], as_index=False).size().rename(columns={"size":"Total"})
    if not anual.empty:
        anual["Año"] = anual["Año"].astype(int)
    fig = px.line(anual, x="Año", y="Total", color="Ámbito", markers=True, title="Evolución anual de convenios")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)
with x4:
    top = (f[f["Ámbito"]=="Internacional"].groupby("País", as_index=False).size().rename(columns={"size":"Total"})
           .sort_values("Total", ascending=False).head(10).sort_values("Total"))
    fig = px.bar(top, x="Total", y="País", orientation="h", title="Países con mayor número de convenios")
    fig.update_yaxes(title="")
    st.plotly_chart(apply_plot_style(fig), use_container_width=True)

st.markdown("### Base de convenios")
show = f[["Ámbito","Institución","País","Tipo","Inicio","Fin","Estado","Año","Resolución","Responsable"]].copy()
st.dataframe(show, use_container_width=True, hide_index=True, height=430)
download_csv(show, "convenios_filtrados.csv")
