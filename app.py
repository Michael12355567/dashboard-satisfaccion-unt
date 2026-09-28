
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils import (
    load_data, fmt_int, fmt_pct, pct, safe_unique,
    filter_mobility, filter_agreements
)

st.set_page_config(
    page_title="UNT | Estadística de Cooperación y Movilidad",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- VISUAL SYSTEM ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F4F7FB; color: #172033; }
.block-container { padding-top: 1.1rem; padding-bottom: 2rem; max-width: 1600px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1F3A 0%, #102A4D 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: #F5F8FC; }
[data-testid="stSidebar"] .stMultiSelect span,
[data-testid="stSidebar"] .stSelectbox span { color: #172033 !important; }

.hero {
    background: linear-gradient(120deg,#0B1F3A 0%,#123A66 58%,#176B87 100%);
    border-radius: 22px;
    padding: 26px 30px;
    color: white;
    box-shadow: 0 14px 34px rgba(13,37,65,.18);
    margin-bottom: 18px;
}
.hero-kicker { font-size: .78rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; opacity: .78; }
.hero h1 { margin: 4px 0 4px 0; font-size: 2rem; line-height: 1.12; }
.hero p { margin: 0; color: rgba(255,255,255,.78); font-size: .98rem; }

.section-title { font-size: 1.06rem; font-weight: 800; color: #16233B; margin: 10px 0 8px 0; }
.section-sub { color:#68758B; font-size:.85rem; margin-top:-6px; margin-bottom:12px; }

.kpi-card {
    background:#FFFFFF;
    border:1px solid #E6EBF2;
    border-radius:18px;
    padding:18px 18px 16px 18px;
    min-height:126px;
    box-shadow:0 7px 18px rgba(25,45,80,.055);
    position:relative;
    overflow:hidden;
}
.kpi-card:before {
    content:""; position:absolute; left:0; top:0; bottom:0; width:5px;
    background:linear-gradient(180deg,#176B87,#18A0AE);
}
.kpi-label { color:#66758B; font-size:.76rem; font-weight:700; text-transform:uppercase; letter-spacing:.055em; }
.kpi-value { color:#0B1F3A; font-size:2rem; font-weight:800; margin-top:7px; line-height:1; }
.kpi-foot { color:#7A8799; font-size:.76rem; margin-top:8px; line-height:1.25; }

.insight {
    background:#FFFFFF;
    border:1px solid #E5EBF3;
    border-radius:16px;
    padding:15px 17px;
    box-shadow:0 6px 16px rgba(25,45,80,.045);
}
.insight b { color:#0B1F3A; }

.panel {
    background:#FFFFFF;
    border:1px solid #E6EBF2;
    border-radius:18px;
    padding:8px 12px 4px 12px;
    box-shadow:0 7px 18px rgba(25,45,80,.05);
}
.smallnote { color:#7A8799; font-size:.78rem; }

div[data-testid="stRadio"] > div { gap: 6px; }
div[data-testid="stRadio"] label {
    background:#FFFFFF;
    border:1px solid #DFE6EF;
    border-radius:12px;
    padding:7px 13px;
}
hr { border-color:#E6EBF2; }
</style>
""", unsafe_allow_html=True)

conv, mov = load_data()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### UNT · Unidad de Estadística")
    st.caption("Sistema estadístico de cooperación y movilidad")
    st.markdown("---")
    page = st.radio(
        "Navegación",
        ["Resumen ejecutivo", "Convenios", "Movilidad académica", "Indicadores estadísticos", "Base de datos"],
        index=0
    )
    st.markdown("---")
    st.markdown("#### Filtros globales")
    years_all = sorted(set(conv["AÑO"].dropna().astype(int).tolist()) | set(mov["AÑO"].dropna().astype(int).tolist()))
    years_sel = st.multiselect("Año", years_all, default=years_all)
    st.caption("Los filtros afectan las métricas y visuales de la página activa.")

# Common theme
COLORS = ["#176B87", "#18A0AE", "#F0A33A", "#496B9A", "#8E6CB1", "#49A078", "#D36B6B"]

def style_fig(fig, height=330, legend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=12,r=12,t=54,b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", color="#27354A", size=12),
        title_font=dict(size=15, color="#17233B"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        showlegend=legend,
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    fig.update_xaxes(showgrid=False, linecolor="#E9EDF3")
    fig.update_yaxes(gridcolor="#EDF1F5", zeroline=False)
    return fig

def kpi(label, value, foot=""):
    st.markdown(
        f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-foot">{foot}</div>
        </div>""",
        unsafe_allow_html=True
    )

def hero(title, subtitle, kicker="INTELIGENCIA ESTADÍSTICA · UNT"):
    st.markdown(
        f"""<div class="hero">
        <div class="hero-kicker">{kicker}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
        </div>""", unsafe_allow_html=True
    )

conv_f = conv[conv["AÑO"].isin(years_sel)] if years_sel else conv.iloc[0:0]
mov_f = mov[mov["AÑO"].isin(years_sel)] if years_sel else mov.iloc[0:0]

# ---------- RESUMEN ----------
if page == "Resumen ejecutivo":
    hero(
        "Cooperación, convenios y movilidad académica",
        "Lectura ejecutiva de alcance institucional, internacionalización, vigencia y participación académica."
    )

    total_conv = len(conv_f)
    nac = (conv_f["ÁMBITO"] == "Nacional").sum()
    inte = (conv_f["ÁMBITO"] == "Internacional").sum()
    vig = (conv_f["ESTADO"] == "Vigente").sum()
    exp12 = (conv_f["ESTADO"] == "Vence ≤ 12 meses").sum()
    paises = conv_f.loc[conv_f["ÁMBITO"]=="Internacional","PAÍS"].nunique()

    total_mov = mov_f["TOTAL"].sum()
    int_mov = mov_f.loc[mov_f["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
    entrante = mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="INMIGRATORIA","TOTAL"].sum()
    estudiantes = mov_f.loc[mov_f["QUIÉN"].str.upper().str.contains("ESTUD"),"TOTAL"].sum()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: kpi("Convenios", fmt_int(total_conv), f"{fmt_int(nac)} nacionales · {fmt_int(inte)} internacionales")
    with c2: kpi("Convenios vigentes", fmt_int(vig), f"{fmt_int(exp12)} vencen en ≤ 12 meses")
    with c3: kpi("Países vinculados", fmt_int(paises), "Cobertura de convenios internacionales")
    with c4: kpi("Movilidades", fmt_int(total_mov), "Registros acumulados en el periodo filtrado")
    with c5: kpi("Movilidad internacional", fmt_pct(pct(int_mov,total_mov)), f"{fmt_int(int_mov)} movilidades")
    with c6: kpi("Movilidad entrante", fmt_pct(pct(entrante,total_mov)), "Participación inmigratoria")

    st.markdown('<div class="section-title">Señales estadísticas de mayor impacto</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">No solo conteos: composición, concentración, cobertura y evolución.</div>', unsafe_allow_html=True)

    # Data for visual 1
    annual = mov_f.groupby(["AÑO","MODALIDAD"], dropna=False)["TOTAL"].sum().reset_index()
    if not annual.empty:
        annual["AÑO"] = annual["AÑO"].astype(str)
    colA, colB = st.columns([1.55,1])

    with colA:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig = px.bar(
            annual, x="AÑO", y="TOTAL", color="MODALIDAD",
            barmode="stack",
            title="Movilidad académica por año y modalidad",
            color_discrete_sequence=COLORS
        )
        fig.update_traces(marker_line_width=0, hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>")
        style_fig(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        comp = mov_f.groupby("MOVILIDAD")["TOTAL"].sum().reset_index()
        fig2 = px.pie(
            comp, names="MOVILIDAD", values="TOTAL", hole=.66,
            title="Equilibrio de movilidad: saliente vs. entrante",
            color_discrete_sequence=[COLORS[0],COLORS[2],COLORS[3]]
        )
        fig2.update_traces(textposition="inside", textinfo="percent", hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>")
        style_fig(fig2, 350)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    colC,colD = st.columns(2)
    with colC:
        topc = (mov_f.groupby("CARRERA PROFESIONAL")["TOTAL"].sum().sort_values(ascending=False).head(10).sort_values()).reset_index()
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig3 = px.bar(
            topc, x="TOTAL", y="CARRERA PROFESIONAL", orientation="h",
            title="Top 10 carreras con mayor movilidad",
            color_discrete_sequence=[COLORS[0]]
        )
        fig3.update_traces(hovertemplate="<b>%{y}</b><br>Movilidad: %{x:,.0f}<extra></extra>")
        style_fig(fig3, 390, legend=False)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with colD:
        country = conv_f[conv_f["ÁMBITO"]=="Internacional"].groupby("PAÍS").size().sort_values(ascending=False).head(10).sort_values().reset_index(name="CONVENIOS")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig4 = px.bar(
            country, x="CONVENIOS", y="PAÍS", orientation="h",
            title="Países con mayor vinculación por convenios",
            color_discrete_sequence=[COLORS[2]]
        )
        fig4.update_traces(hovertemplate="<b>%{y}</b><br>Convenios: %{x}<extra></extra>")
        style_fig(fig4, 390, legend=False)
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Lectura ejecutiva automática</div>', unsafe_allow_html=True)
    female = mov_f.loc[mov_f["GÉNERO"].str.upper()=="FEMENINO","TOTAL"].sum()
    docent = mov_f.loc[mov_f["QUIÉN"].str.upper().str.contains("DOC"),"TOTAL"].sum()
    top_country = country.iloc[-1]["PAÍS"] if len(country) else "—"
    i1,i2,i3,i4 = st.columns(4)
    with i1:
        st.markdown(f'<div class="insight"><b>{fmt_pct(pct(inte,total_conv))}</b><br><span class="smallnote">de los convenios filtrados son internacionales.</span></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight"><b>{fmt_pct(pct(female,total_mov))}</b><br><span class="smallnote">de la movilidad corresponde a participación femenina.</span></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight"><b>{fmt_pct(pct(docent,total_mov))}</b><br><span class="smallnote">de la movilidad corresponde a docentes.</span></div>', unsafe_allow_html=True)
    with i4:
        st.markdown(f'<div class="insight"><b>{top_country}</b><br><span class="smallnote">aparece entre los países con mayor número de convenios.</span></div>', unsafe_allow_html=True)

# ---------- CONVENIOS ----------
elif page == "Convenios":
    hero("Convenios institucionales", "Análisis de cobertura, vigencia, tipología y concentración de convenios nacionales e internacionales.")

    f1,f2 = st.columns(2)
    with f1:
        scope = st.multiselect("Ámbito", safe_unique(conv_f["ÁMBITO"]), default=safe_unique(conv_f["ÁMBITO"]))
    with f2:
        status = st.multiselect("Estado", safe_unique(conv_f["ESTADO"]), default=safe_unique(conv_f["ESTADO"]))
    df = filter_agreements(conv_f, scope=scope, status=status)

    total=len(df); vig=(df["ESTADO"]=="Vigente").sum(); exp=(df["ESTADO"]=="Vence ≤ 12 meses").sum()
    intl=(df["ÁMBITO"]=="Internacional").sum(); countries=df.loc[df["ÁMBITO"]=="Internacional","PAÍS"].nunique()
    a,b,c,d,e = st.columns(5)
    with a: kpi("Convenios filtrados",fmt_int(total),"Base consolidada")
    with b: kpi("Vigentes",fmt_int(vig),fmt_pct(pct(vig,total))+" del total")
    with c: kpi("Vence ≤ 12 meses",fmt_int(exp),"Seguimiento prioritario")
    with d: kpi("Internacionales",fmt_int(intl),fmt_pct(pct(intl,total))+" del total")
    with e: kpi("Países",fmt_int(countries),"Cobertura internacional")

    left,right = st.columns([1.35,1])
    with left:
        yearly = df.groupby(["AÑO","ÁMBITO"]).size().reset_index(name="CONVENIOS")
        yearly["AÑO"]=yearly["AÑO"].astype(str)
        fig=px.bar(yearly,x="AÑO",y="CONVENIOS",color="ÁMBITO",barmode="group",
                   title="Registro de convenios por año y ámbito",color_discrete_sequence=COLORS)
        style_fig(fig,360)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with right:
        stat=df.groupby("ESTADO").size().reset_index(name="CONVENIOS")
        fig=px.pie(stat,names="ESTADO",values="CONVENIOS",hole=.62,title="Estado de vigencia",
                   color_discrete_sequence=COLORS)
        fig.update_traces(textinfo="percent",textposition="inside")
        style_fig(fig,360)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    l2,r2 = st.columns(2)
    with l2:
        types=(df.groupby("TIPO").size().sort_values(ascending=False).head(8).sort_values()).reset_index(name="CONVENIOS")
        fig=px.bar(types,x="CONVENIOS",y="TIPO",orientation="h",title="Tipos de convenio más frecuentes",
                   color_discrete_sequence=[COLORS[0]])
        style_fig(fig,380,legend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r2:
        countries=(df[df["ÁMBITO"]=="Internacional"].groupby("PAÍS").size().sort_values(ascending=False).head(10).sort_values()).reset_index(name="CONVENIOS")
        fig=px.bar(countries,x="CONVENIOS",y="PAÍS",orientation="h",title="Top países por convenios internacionales",
                   color_discrete_sequence=[COLORS[2]])
        style_fig(fig,380,legend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    st.markdown('<div class="section-title">Detalle de convenios</div>',unsafe_allow_html=True)
    show=df[["AÑO","ÁMBITO","INSTITUCIÓN","PAÍS","TIPO","INICIO","VENCE","ESTADO","RESOLUCIÓN"]].copy()
    show["INICIO"]=show["INICIO"].dt.strftime("%d/%m/%Y")
    show["VENCE"]=show["VENCE"].dt.strftime("%d/%m/%Y")
    st.dataframe(show,use_container_width=True,height=430,hide_index=True)

# ---------- MOVILIDAD ----------
elif page == "Movilidad académica":
    hero("Movilidad académica", "Perfil estadístico de participación, modalidad, flujo, género, carreras y destinos.")

    f1,f2,f3 = st.columns(3)
    with f1:
        mod = st.multiselect("Modalidad",safe_unique(mov_f["MODALIDAD"]),default=safe_unique(mov_f["MODALIDAD"]))
    with f2:
        who = st.multiselect("Participante",safe_unique(mov_f["QUIÉN"]),default=safe_unique(mov_f["QUIÉN"]))
    with f3:
        flow = st.multiselect("Flujo",safe_unique(mov_f["MOVILIDAD"]),default=safe_unique(mov_f["MOVILIDAD"]))
    df = mov_f[mov_f["MODALIDAD"].isin(mod) & mov_f["QUIÉN"].isin(who) & mov_f["MOVILIDAD"].isin(flow)]

    total=df["TOTAL"].sum()
    intl=df.loc[df["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
    inb=df.loc[df["MOVILIDAD"].str.upper()=="INMIGRATORIA","TOTAL"].sum()
    female=df.loc[df["GÉNERO"].str.upper()=="FEMENINO","TOTAL"].sum()
    careers=df["CARRERA PROFESIONAL"].replace("nan",np.nan).nunique()
    a,b,c,d,e = st.columns(5)
    with a:kpi("Movilidades",fmt_int(total),"Periodo filtrado")
    with b:kpi("Internacionales",fmt_pct(pct(intl,total)),f"{fmt_int(intl)} registros")
    with c:kpi("Entrantes",fmt_pct(pct(inb,total)),f"{fmt_int(inb)} registros")
    with d:kpi("Participación femenina",fmt_pct(pct(female,total)),f"{fmt_int(female)} registros")
    with e:kpi("Carreras con movilidad",fmt_int(careers),"Cobertura observada")

    yearly=df.groupby(["AÑO","MODALIDAD"])["TOTAL"].sum().reset_index()
    yearly["AÑO"]=yearly["AÑO"].astype(str)
    left,right=st.columns([1.5,1])
    with left:
        fig=px.bar(yearly,x="AÑO",y="TOTAL",color="MODALIDAD",barmode="stack",
                   title="Evolución anual de la movilidad",color_discrete_sequence=COLORS)
        style_fig(fig,360)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with right:
        g=df.groupby("GÉNERO")["TOTAL"].sum().reset_index()
        fig=px.pie(g,names="GÉNERO",values="TOTAL",hole=.64,title="Participación por género",
                   color_discrete_sequence=COLORS)
        fig.update_traces(textinfo="percent",textposition="inside")
        style_fig(fig,360)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    c1,c2=st.columns(2)
    with c1:
        carr=(df.groupby("CARRERA PROFESIONAL")["TOTAL"].sum().sort_values(ascending=False).head(12).sort_values()).reset_index()
        fig=px.bar(carr,x="TOTAL",y="CARRERA PROFESIONAL",orientation="h",
                   title="Carreras con mayor movilidad",color_discrete_sequence=[COLORS[0]])
        style_fig(fig,430,legend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        dest=(df.groupby("REGIÓN / PAÍS")["TOTAL"].sum().sort_values(ascending=False).head(12).sort_values()).reset_index()
        fig=px.bar(dest,x="TOTAL",y="REGIÓN / PAÍS",orientation="h",
                   title="Principales regiones / países",color_discrete_sequence=[COLORS[2]])
        style_fig(fig,430,legend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    st.markdown('<div class="section-title">Detalle de movilidad</div>',unsafe_allow_html=True)
    cols=["AÑO","PERÍODO","MOVILIDAD","MODALIDAD","QUIÉN","REGIÓN / PAÍS","CARRERA PROFESIONAL",
          "UNIVERSIDAD DE ORIGEN","UNIVERSIDAD DE DESTINO","GÉNERO","TOTAL"]
    st.dataframe(df[cols],use_container_width=True,height=420,hide_index=True)

# ---------- INDICADORES ----------
elif page == "Indicadores estadísticos":
    hero("Indicadores estadísticos", "Medidas derivadas para interpretar internacionalización, equilibrio de flujos, cobertura y concentración.")

    total_mov=mov_f["TOTAL"].sum()
    total_conv=len(conv_f)
    international=mov_f.loc[mov_f["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
    incoming=mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="INMIGRATORIA","TOTAL"].sum()
    outgoing=mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="EMIGRATORIA","TOTAL"].sum()
    intl_conv=(conv_f["ÁMBITO"]=="Internacional").sum()
    countries=conv_f.loc[conv_f["ÁMBITO"]=="Internacional","PAÍS"].nunique()
    careers=mov_f["CARRERA PROFESIONAL"].replace("nan",np.nan).nunique()

    # concentration top 5 destinations
    dest=mov_f.groupby("REGIÓN / PAÍS")["TOTAL"].sum().sort_values(ascending=False)
    top5=dest.head(5).sum()
    concentration=pct(top5,total_mov)
    ratio=(outgoing/incoming) if incoming else np.nan

    a,b,c,d = st.columns(4)
    with a:kpi("Índice de internacionalización",fmt_pct(pct(international,total_mov)),"Movilidad internacional / movilidad total")
    with b:kpi("Índice de movilidad entrante",fmt_pct(pct(incoming,total_mov)),"Movilidad inmigratoria / movilidad total")
    with c:kpi("Peso de convenios internacionales",fmt_pct(pct(intl_conv,total_conv)),"Convenios internacionales / total")
    with d:kpi("Concentración Top 5 destinos",fmt_pct(concentration),"Participación de los cinco destinos principales")

    st.markdown('<div class="section-title">Indicadores complementarios</div>',unsafe_allow_html=True)
    x1,x2,x3,x4=st.columns(4)
    with x1:
        val="—" if pd.isna(ratio) else f"{ratio:.1f} : 1"
        kpi("Razón saliente / entrante",val,"Cuántas salidas existen por cada entrada")
    with x2:kpi("Cobertura internacional",fmt_int(countries),"Países con convenios internacionales")
    with x3:kpi("Carreras observadas",fmt_int(careers),"Programas con registros de movilidad")
    with x4:kpi("Convenios próximos a vencer",fmt_int((conv_f["ESTADO"]=="Vence ≤ 12 meses").sum()),"Ventana de seguimiento: 12 meses")

    st.info(
        "Para incorporar tasas por cada 1 000 matriculados —un indicador comparativo más sólido— "
        "se requiere agregar la base anual de matrícula por carrera/sede. La estructura del tablero ya puede ampliarse para ello."
    )

    # Scorecard by year
    annual_m=mov_f.groupby("AÑO")["TOTAL"].sum()
    annual_int=mov_f[mov_f["MODALIDAD"].str.upper()=="INTERNACIONAL"].groupby("AÑO")["TOTAL"].sum()
    annual_in=mov_f[mov_f["MOVILIDAD"].str.upper()=="INMIGRATORIA"].groupby("AÑO")["TOTAL"].sum()
    years=sorted(mov_f["AÑO"].dropna().astype(int).unique())
    rows=[]
    for y in years:
        t=float(annual_m.get(y,0))
        rows.append({
            "Año":y,
            "Movilidad total":int(t),
            "% internacional":pct(annual_int.get(y,0),t),
            "% entrante":pct(annual_in.get(y,0),t),
        })
    score=pd.DataFrame(rows)
    if not score.empty:
        fig=go.Figure()
        fig.add_trace(go.Bar(x=score["Año"].astype(str),y=score["% internacional"],name="% internacional",marker_color=COLORS[0]))
        fig.add_trace(go.Bar(x=score["Año"].astype(str),y=score["% entrante"],name="% entrante",marker_color=COLORS[2]))
        fig.update_layout(barmode="group",title="Comparación anual de indicadores porcentuales")
        style_fig(fig,390)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        st.dataframe(
            score.style.format({"% internacional":"{:.1f}%","% entrante":"{:.1f}%"}),
            use_container_width=True,hide_index=True
        )

# ---------- DATABASE ----------
else:
    hero("Base de datos", "Consulta operativa y exportable de los registros que alimentan el tablero.")
    tab1,tab2=st.tabs(["Convenios","Movilidad académica"])
    with tab1:
        query=st.text_input("Buscar en convenios",placeholder="Institución, país, resolución, tipo...")
        df=conv_f.copy()
        if query:
            mask=df.astype(str).apply(lambda c:c.str.contains(query,case=False,na=False)).any(axis=1)
            df=df[mask]
        st.dataframe(df,use_container_width=True,height=520,hide_index=True)
        st.download_button(
            "Descargar convenios filtrados (CSV)",
            df.to_csv(index=False).encode("utf-8-sig"),
            "convenios_filtrados.csv","text/csv",use_container_width=True
        )
    with tab2:
        query2=st.text_input("Buscar en movilidad",placeholder="Carrera, país, universidad, modalidad...")
        df2=mov_f.copy()
        if query2:
            mask=df2.astype(str).apply(lambda c:c.str.contains(query2,case=False,na=False)).any(axis=1)
            df2=df2[mask]
        st.dataframe(df2,use_container_width=True,height=520,hide_index=True)
        st.download_button(
            "Descargar movilidad filtrada (CSV)",
            df2.to_csv(index=False).encode("utf-8-sig"),
            "movilidad_filtrada.csv","text/csv",use_container_width=True
        )

st.markdown("---")
st.caption("Universidad Nacional de Trujillo · Unidad de Estadística · Dashboard de cooperación y movilidad académica")
