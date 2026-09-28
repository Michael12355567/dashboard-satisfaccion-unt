import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_config, hero, load_data, fmt_int, fmt_pct, apply_plot_style, sidebar_brand

page_config("Indicadores | UNT")
sidebar_brand()
_, _, mov, conv = load_data()
hero("Indicadores estadísticos", "Indicadores relativos para interpretar internacionalización, cobertura y movilidad. Puede incorporar matrícula para tasas comparables.")

# Indicadores existentes
mov_total = mov["TOTAL"].sum()
intl = mov.loc[mov["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
inm = mov.loc[mov["MOVILIDAD"].str.upper().isin(["IMIGRATORIA","INMIGRATORIA"]),"TOTAL"].sum()
est = mov.loc[mov["QUIÉN"].str.upper()=="ESTUDIANTIL","TOTAL"].sum()
carreras_mov = mov["CARRERA PROFESIONAL"].replace("nan", pd.NA).dropna().nunique()
paises_conv = conv.loc[conv["Ámbito"]=="Internacional","País"].dropna().nunique()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Índice de internacionalización", fmt_pct(intl/mov_total*100))
c2.metric("Índice de movilidad entrante", fmt_pct(inm/mov_total*100))
c3.metric("Participación estudiantil", fmt_pct(est/mov_total*100))
c4.metric("Países con convenio", fmt_int(paises_conv))

st.markdown("### Tasas por matrícula")
st.info("Para calcular tasas por cada 1,000 matriculados, cargue un Excel o CSV con al menos dos columnas: **AÑO** y **MATRICULADOS**. No se modifica ninguna de las bases originales.")
upload = st.file_uploader("Cargar matrícula anual", type=["xlsx","xls","csv"])

if upload is not None:
    try:
        if upload.name.lower().endswith(".csv"):
            mat = pd.read_csv(upload)
        else:
            mat = pd.read_excel(upload)
        # normaliza nombres
        mat.columns = [str(c).strip().upper() for c in mat.columns]
        if "AÑO" not in mat.columns or "MATRICULADOS" not in mat.columns:
            st.error("El archivo debe contener las columnas AÑO y MATRICULADOS.")
        else:
            mat["AÑO"] = pd.to_numeric(mat["AÑO"], errors="coerce")
            mat["MATRICULADOS"] = pd.to_numeric(mat["MATRICULADOS"], errors="coerce")
            m_anual = mov.groupby("AÑO", as_index=False)["TOTAL"].sum().rename(columns={"TOTAL":"MOVILIDADES"})
            m_int = (mov[mov["MODALIDAD"].str.upper()=="INTERNACIONAL"].groupby("AÑO", as_index=False)["TOTAL"].sum()
                     .rename(columns={"TOTAL":"MOV_INT"}))
            rate = m_anual.merge(m_int, on="AÑO", how="left").merge(mat[["AÑO","MATRICULADOS"]], on="AÑO", how="inner")
            rate["MOV_INT"] = rate["MOV_INT"].fillna(0)
            rate["TASA_MOV_1000"] = rate["MOVILIDADES"] / rate["MATRICULADOS"] * 1000
            rate["TASA_INT_1000"] = rate["MOV_INT"] / rate["MATRICULADOS"] * 1000
            fig = px.line(rate, x="AÑO", y=["TASA_MOV_1000","TASA_INT_1000"], markers=True,
                          title="Movilidad por cada 1,000 matriculados",
                          labels={"value":"Tasa por 1,000","variable":"Indicador"})
            fig.update_xaxes(dtick=1)
            st.plotly_chart(apply_plot_style(fig), use_container_width=True)
            st.dataframe(rate.round(2), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"No se pudo procesar el archivo: {e}")
else:
    st.markdown(
        '<div class="insight"><b>Siguiente salto estadístico:</b> al incorporar matrícula anual, el tablero deja de comparar solo cantidades y puede mostrar tasas de movilidad por cada 1,000 estudiantes, permitiendo comparar años con tamaños de matrícula diferentes.</div>',
        unsafe_allow_html=True,
    )

st.markdown("### Indicadores sugeridos")
st.markdown("""
- **Tasa de movilidad estudiantil por 1,000 matriculados** = movilidades estudiantiles / matriculados × 1,000.
- **Tasa de movilidad internacional por 1,000 matriculados** = movilidades internacionales / matriculados × 1,000.
- **Índice de movilidad entrante** = movilidad entrante / movilidad total × 100.
- **Índice de internacionalización de la movilidad** = movilidad internacional / movilidad total × 100.
- **Cobertura de programas con movilidad** = programas con movilidad / total de programas × 100, cuando se incorpore el padrón oficial de programas.
- **Vigencia de convenios** = convenios vigentes / convenios con fecha válida × 100.
""")
