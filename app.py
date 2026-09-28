
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, fmt_int, fmt_pct, pct, safe_values

st.set_page_config(
    page_title="UNT | Cooperación y Movilidad",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
.stApp {background:#F5F7FB;}
.block-container {padding-top:.7rem; max-width:1680px;}
[data-testid="stSidebar"]{background:#071923;}
[data-testid="stSidebar"] *{color:#EAF4F8;}
[data-testid="stSidebar"] .stRadio label{padding:.28rem .4rem;border-radius:8px;}
[data-testid="stSidebar"] .stRadio label:hover{background:#0F2D3B;}
.header{
 background:linear-gradient(105deg,#0B2A44 0%,#0E4F73 62%,#0E7181 100%);
 color:white;border-radius:18px;padding:22px 26px;margin-bottom:14px;
 box-shadow:0 10px 30px rgba(10,39,62,.15);
}
.header .kicker{font-size:.72rem;letter-spacing:.16em;font-weight:800;opacity:.72;text-transform:uppercase}
.header h1{font-size:1.8rem;margin:.2rem 0 .15rem 0}
.header p{margin:0;color:rgba(255,255,255,.78);font-size:.92rem}
.filterbar{
 background:#FFFFFF;border:1px solid #E3E9F1;border-radius:14px;padding:12px 14px 2px 14px;
 box-shadow:0 6px 18px rgba(25,45,80,.05);margin-bottom:14px
}
.kpi{
 background:white;border:1px solid #E4EAF2;border-radius:15px;padding:15px 16px;
 min-height:112px;box-shadow:0 6px 18px rgba(24,48,80,.055);position:relative;overflow:hidden
}
.kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:#0F7084}
.klabel{font-size:.72rem;color:#6A788B;text-transform:uppercase;letter-spacing:.05em;font-weight:700}
.kvalue{font-size:1.9rem;font-weight:800;color:#0A2338;margin-top:8px;line-height:1}
.kfoot{font-size:.75rem;color:#7B8798;margin-top:8px}
.section{font-size:1.02rem;font-weight:800;color:#14273A;margin:14px 0 6px 0}
.note{font-size:.78rem;color:#748196}
.panel{
 background:#FFFFFF;border:1px solid #E5EAF1;border-radius:16px;padding:4px 10px 0 10px;
 box-shadow:0 6px 18px rgba(24,48,80,.05)
}
.insight{
 background:#FFFFFF;border:1px solid #E5EAF1;border-radius:14px;padding:14px 15px;
 min-height:90px;box-shadow:0 5px 15px rgba(24,48,80,.045)
}
.insight b{font-size:1.25rem;color:#0B4F69}
.stSelectbox label, .stMultiSelect label{font-weight:700!important;color:#3F5065!important;font-size:.78rem!important}
div[data-baseweb="select"] > div{border-radius:10px!important}
</style>
""", unsafe_allow_html=True)

conv, mov, mat = load_data()
COLORS=["#0F7084","#18A4A6","#E1A43A","#4F72A5","#7D65A8","#4E9B73","#CE6C6C"]

def hero(title, subtitle):
    st.markdown(f"""<div class="header">
    <div class="kicker">Universidad Nacional de Trujillo · Unidad de Estadística</div>
    <h1>{title}</h1><p>{subtitle}</p></div>""", unsafe_allow_html=True)

def kpi(label, value, foot=""):
    st.markdown(f"""<div class="kpi"><div class="klabel">{label}</div>
    <div class="kvalue">{value}</div><div class="kfoot">{foot}</div></div>""", unsafe_allow_html=True)

def figstyle(fig, h=340, legend=True):
    fig.update_layout(
        height=h, paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=12,r=12,t=55,b=24),
        font=dict(family="Inter",size=12,color="#314156"),
        title_font=dict(size=15,color="#17283B"),
        legend=dict(orientation="h",y=1.03,x=0),
        showlegend=legend,
        hoverlabel=dict(bgcolor="white",font_size=12)
    )
    fig.update_xaxes(showgrid=False,linecolor="#E7ECF2")
    fig.update_yaxes(gridcolor="#EDF1F5",zeroline=False)
    return fig

with st.sidebar:
    st.markdown("## 📊 Estadística UNT")
    st.caption("Cooperación, convenios y movilidad académica")
    st.markdown("---")
    page=st.radio(
        "Módulos",
        ["Resumen general","Convenios","Movilidad académica","Impacto e indicadores","Base de datos"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("Dashboard institucional · datos estadísticos")

# ---------- GLOBAL TOP FILTERS ----------
years_common=sorted(set(mov["AÑO"].dropna().astype(int)) & set(mat["AÑO"].dropna().astype(int)))
if not years_common:
    years_common=sorted(set(mov["AÑO"].dropna().astype(int)))

if "f_year" not in st.session_state: st.session_state.f_year="Todos"
if "f_sede" not in st.session_state: st.session_state.f_sede="Todas"
if "f_fac" not in st.session_state: st.session_state.f_fac="Todas"
if "f_car" not in st.session_state: st.session_state.f_car="Todas"
if "f_mod" not in st.session_state: st.session_state.f_mod="Todas"

def reset_filters():
    st.session_state.f_year="Todos"
    st.session_state.f_sede="Todas"
    st.session_state.f_fac="Todas"
    st.session_state.f_car="Todas"
    st.session_state.f_mod="Todas"

hero(
    "Vinculación, cooperación y movilidad académica",
    "Tablero estadístico interactivo con filtros tipo Power BI e indicadores normalizados por matrícula."
)

st.markdown('<div class="filterbar">',unsafe_allow_html=True)
fc1,fc2,fc3,fc4,fc5,fc6=st.columns([1,1.2,1.55,1.65,1.15,.9])

with fc1:
    y_options=["Todos"]+[str(y) for y in years_common]
    st.selectbox("Año",y_options,key="f_year")

# dependent filters based on matriculation
mat_base=mat.copy()
if st.session_state.f_year!="Todos":
    mat_base=mat_base[mat_base["AÑO"]==int(st.session_state.f_year)]

with fc2:
    sede_opts=["Todas"]+safe_values(mat_base["SEDE"])
    if st.session_state.f_sede not in sede_opts: st.session_state.f_sede="Todas"
    st.selectbox("Sede",sede_opts,key="f_sede")

if st.session_state.f_sede!="Todas":
    mat_base=mat_base[mat_base["SEDE"]==st.session_state.f_sede]

with fc3:
    fac_opts=["Todas"]+safe_values(mat_base["FACULTAD"])
    if st.session_state.f_fac not in fac_opts: st.session_state.f_fac="Todas"
    st.selectbox("Facultad",fac_opts,key="f_fac")

if st.session_state.f_fac!="Todas":
    mat_base=mat_base[mat_base["FACULTAD"]==st.session_state.f_fac]

career_opts=["Todas"]+safe_values(mat_base["CARRERA"])
if st.session_state.f_fac=="EDUCACION Y CIENCIAS DE LA COMUNICACION":
    if "EDUCACIÓN SECUNDARIA (TODAS)" not in career_opts:
        career_opts.insert(1,"EDUCACIÓN SECUNDARIA (TODAS)")

with fc4:
    if st.session_state.f_car not in career_opts: st.session_state.f_car="Todas"
    st.selectbox("Carrera",career_opts,key="f_car")

with fc5:
    mod_opts=["Todas"]+safe_values(mov["MODALIDAD"])
    if st.session_state.f_mod not in mod_opts: st.session_state.f_mod="Todas"
    st.selectbox("Modalidad",mod_opts,key="f_mod")

with fc6:
    st.write("")
    st.button("↺ Quitar filtros",use_container_width=True,on_click=reset_filters)

st.markdown('</div>',unsafe_allow_html=True)

# Apply filters
year = None if st.session_state.f_year=="Todos" else int(st.session_state.f_year)
sede = st.session_state.f_sede
fac = st.session_state.f_fac
car = st.session_state.f_car
mod = st.session_state.f_mod

mov_f=mov.copy()
mat_f=mat.copy()
conv_f=conv.copy()

if year:
    mov_f=mov_f[mov_f["AÑO"]==year]
    mat_f=mat_f[mat_f["AÑO"]==year]
    conv_f=conv_f[conv_f["AÑO"]==year]

if sede!="Todas":
    mat_f=mat_f[mat_f["SEDE"]==sede]

if fac!="Todas":
    mov_f=mov_f[mov_f["FACULTAD"]==fac]
    mat_f=mat_f[mat_f["FACULTAD"]==fac]

if car!="Todas":
    if car=="EDUCACIÓN SECUNDARIA (TODAS)":
        mov_f=mov_f[mov_f["CARRERA_CANON"]=="EDUCACIÓN SECUNDARIA (TODAS)"]
        mat_f=mat_f[mat_f["CARRERA"].str.upper().str.startswith("EDUCACIÓN SECUNDARIA")]
    else:
        mov_f=mov_f[mov_f["CARRERA_CANON"]==car]
        mat_f=mat_f[mat_f["CARRERA"]==car]

if mod!="Todas":
    mov_f=mov_f[mov_f["MODALIDAD"]==mod]

# If a sede is selected, mobility cannot be filtered directly because mobility file lacks sede.
# We therefore show matriculation-normalized indicators using selected sede, while raw mobility remains by year/faculty/career.
sede_warning = sede!="Todas"

# ---------- RESUMEN GENERAL ----------
if page=="Resumen general":
    total_conv=len(conv_f)
    nac=(conv_f["ÁMBITO"]=="Nacional").sum()
    inte=(conv_f["ÁMBITO"]=="Internacional").sum()
    total_mov=mov_f["TOTAL"].sum()
    int_mov=mov_f.loc[mov_f["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
    in_mov=mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="INMIGRATORIA","TOTAL"].sum()
    students=mov_f.loc[mov_f["QUIÉN"].str.upper().str.contains("ESTUD"),"TOTAL"].sum()
    enrolled=mat_f["MATRICULADOS"].sum()
    rate1000=1000*students/enrolled if enrolled else 0

    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1:kpi("Convenios",fmt_int(total_conv),f"{fmt_int(nac)} nac. · {fmt_int(inte)} int.")
    with c2:kpi("Movilidad académica",fmt_int(total_mov),"Registros del filtro actual")
    with c3:kpi("% internacional",fmt_pct(pct(int_mov,total_mov)),f"{fmt_int(int_mov)} movilidades")
    with c4:kpi("% entrante",fmt_pct(pct(in_mov,total_mov)),f"{fmt_int(in_mov)} movilidades")
    with c5:kpi("Matriculados · Periodo 1",fmt_int(enrolled),"Nunca suma Periodo 1 + Periodo 2")
    with c6:kpi("Tasa movilidad / 1 000",f"{rate1000:.1f}","Movilidad estudiantil / matriculados P1")

    if sede_warning:
        st.caption("Nota: la base de movilidad no contiene sede. El filtro Sede afecta matrícula y tasas normalizadas, no el conteo bruto de movilidad.")

    st.markdown('<div class="section">Indicadores de impacto y evolución</div>',unsafe_allow_html=True)

    a,b=st.columns([1.55,1])
    with a:
        yearly=mov.copy()
        if fac!="Todas": yearly=yearly[yearly["FACULTAD"]==fac]
        if car!="Todas":
            if car=="EDUCACIÓN SECUNDARIA (TODAS)":
                yearly=yearly[yearly["CARRERA_CANON"]=="EDUCACIÓN SECUNDARIA (TODAS)"]
            else:
                yearly=yearly[yearly["CARRERA_CANON"]==car]
        if mod!="Todas": yearly=yearly[yearly["MODALIDAD"]==mod]
        yearly=yearly.groupby(["AÑO","MODALIDAD"])["TOTAL"].sum().reset_index()
        yearly=yearly[yearly["AÑO"].isin(years_common)]
        yearly["AÑO"]=yearly["AÑO"].astype(str)
        fig=px.bar(yearly,x="AÑO",y="TOTAL",color="MODALIDAD",barmode="stack",
                   title="Evolución anual de la movilidad",color_discrete_sequence=COLORS)
        figstyle(fig,350)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with b:
        flow=mov_f.groupby("MOVILIDAD")["TOTAL"].sum().reset_index()
        fig=px.pie(flow,names="MOVILIDAD",values="TOTAL",hole=.68,
                   title="Flujo académico: saliente vs. entrante",color_discrete_sequence=COLORS)
        fig.update_traces(textinfo="percent",textposition="inside")
        figstyle(fig,350)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    a,b=st.columns(2)
    with a:
        carr=(mov_f.groupby("CARRERA CANON" if "CARRERA CANON" in mov_f.columns else "CARRERA_CANON")["TOTAL"]
              .sum().sort_values(ascending=False).head(10).sort_values()).reset_index()
        carr.columns=["Carrera","Movilidad"]
        fig=px.bar(carr,x="Movilidad",y="Carrera",orientation="h",
                   title="Top 10 carreras con mayor movilidad",color_discrete_sequence=[COLORS[0]])
        figstyle(fig,390,False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with b:
        countries=(conv_f[conv_f["ÁMBITO"]=="Internacional"].groupby("PAÍS").size()
                   .sort_values(ascending=False).head(10).sort_values()).reset_index(name="Convenios")
        fig=px.bar(countries,x="Convenios",y="PAÍS",orientation="h",
                   title="Países con mayor vinculación internacional",color_discrete_sequence=[COLORS[2]])
        figstyle(fig,390,False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# ---------- CONVENIOS ----------
elif page=="Convenios":
    total=len(conv_f); vig=(conv_f["ESTADO"]=="Vigente").sum()
    exp=(conv_f["ESTADO"]=="Vence ≤ 12 meses").sum()
    intl=(conv_f["ÁMBITO"]=="Internacional").sum()
    countries=conv_f.loc[conv_f["ÁMBITO"]=="Internacional","PAÍS"].nunique()
    a,b,c,d,e=st.columns(5)
    with a:kpi("Convenios",fmt_int(total),"Filtro actual")
    with b:kpi("Nacionales",fmt_int((conv_f["ÁMBITO"]=="Nacional").sum()),"Ámbito nacional")
    with c:kpi("Internacionales",fmt_int(intl),fmt_pct(pct(intl,total))+" del total")
    with d:kpi("Vigentes",fmt_int(vig),f"{fmt_int(exp)} vencen ≤ 12 meses")
    with e:kpi("Países",fmt_int(countries),"Cobertura internacional")

    l,r=st.columns([1.4,1])
    with l:
        yy=conv_f.groupby(["AÑO","ÁMBITO"]).size().reset_index(name="CONVENIOS")
        yy["AÑO"]=yy["AÑO"].astype(str)
        fig=px.bar(yy,x="AÑO",y="CONVENIOS",color="ÁMBITO",barmode="group",
                   title="Convenios registrados por año",color_discrete_sequence=COLORS)
        figstyle(fig,350); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r:
        ss=conv_f.groupby("ESTADO").size().reset_index(name="CONVENIOS")
        fig=px.pie(ss,names="ESTADO",values="CONVENIOS",hole=.65,title="Vigencia de convenios",
                   color_discrete_sequence=COLORS)
        fig.update_traces(textinfo="percent",textposition="inside")
        figstyle(fig,350); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    c1,c2=st.columns(2)
    with c1:
        tp=(conv_f.groupby("TIPO").size().sort_values(ascending=False).head(10).sort_values()).reset_index(name="CONVENIOS")
        fig=px.bar(tp,x="CONVENIOS",y="TIPO",orientation="h",title="Tipos de convenio",
                   color_discrete_sequence=[COLORS[0]])
        figstyle(fig,400,False); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        p=(conv_f[conv_f["ÁMBITO"]=="Internacional"].groupby("PAÍS").size()
           .sort_values(ascending=False).head(10).sort_values()).reset_index(name="CONVENIOS")
        fig=px.bar(p,x="CONVENIOS",y="PAÍS",orientation="h",title="Top países",
                   color_discrete_sequence=[COLORS[2]])
        figstyle(fig,400,False); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# ---------- MOVILIDAD ----------
elif page=="Movilidad académica":
    total=mov_f["TOTAL"].sum()
    intl=mov_f.loc[mov_f["MODALIDAD"].str.upper()=="INTERNACIONAL","TOTAL"].sum()
    incoming=mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="INMIGRATORIA","TOTAL"].sum()
    female=mov_f.loc[mov_f["GÉNERO"].str.upper()=="FEMENINO","TOTAL"].sum()
    students=mov_f.loc[mov_f["QUIÉN"].str.upper().str.contains("ESTUD"),"TOTAL"].sum()
    teachers=mov_f.loc[mov_f["QUIÉN"].str.upper().str.contains("DOC"),"TOTAL"].sum()

    a,b,c,d,e,f=st.columns(6)
    with a:kpi("Movilidad total",fmt_int(total),"Filtro actual")
    with b:kpi("Internacional",fmt_pct(pct(intl,total)),f"{fmt_int(intl)} registros")
    with c:kpi("Entrante",fmt_pct(pct(incoming,total)),f"{fmt_int(incoming)} registros")
    with d:kpi("Estudiantes",fmt_int(students),fmt_pct(pct(students,total))+" del total")
    with e:kpi("Docentes",fmt_int(teachers),fmt_pct(pct(teachers,total))+" del total")
    with f:kpi("Participación femenina",fmt_pct(pct(female,total)),f"{fmt_int(female)} registros")

    l,r=st.columns([1.45,1])
    with l:
        yy=mov_f.groupby(["AÑO","MODALIDAD"])["TOTAL"].sum().reset_index()
        yy["AÑO"]=yy["AÑO"].astype(str)
        fig=px.bar(yy,x="AÑO",y="TOTAL",color="MODALIDAD",barmode="stack",
                   title="Movilidad por año y modalidad",color_discrete_sequence=COLORS)
        figstyle(fig,350); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with r:
        gg=mov_f.groupby("GÉNERO")["TOTAL"].sum().reset_index()
        fig=px.pie(gg,names="GÉNERO",values="TOTAL",hole=.64,title="Participación por género",
                   color_discrete_sequence=COLORS)
        fig.update_traces(textinfo="percent",textposition="inside")
        figstyle(fig,350); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    c1,c2=st.columns(2)
    with c1:
        x=(mov_f.groupby("CARRERA_CANON")["TOTAL"].sum().sort_values(ascending=False).head(12).sort_values()).reset_index()
        fig=px.bar(x,x="TOTAL",y="CARRERA_CANON",orientation="h",title="Carreras con mayor movilidad",
                   color_discrete_sequence=[COLORS[0]])
        figstyle(fig,430,False); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        x=(mov_f.groupby("REGIÓN / PAÍS")["TOTAL"].sum().sort_values(ascending=False).head(12).sort_values()).reset_index()
        fig=px.bar(x,x="TOTAL",y="REGIÓN / PAÍS",orientation="h",title="Principales regiones / países",
                   color_discrete_sequence=[COLORS[2]])
        figstyle(fig,430,False); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# ---------- IMPACTO ----------
elif page=="Impacto e indicadores":
    students=mov_f.loc[mov_f["QUIÉN"].str.upper().str.contains("ESTUD"),"TOTAL"].sum()
    intl_students=mov_f.loc[
        mov_f["QUIÉN"].str.upper().str.contains("ESTUD") &
        (mov_f["MODALIDAD"].str.upper()=="INTERNACIONAL"),"TOTAL"
    ].sum()
    outgoing_students=mov_f.loc[
        mov_f["QUIÉN"].str.upper().str.contains("ESTUD") &
        (mov_f["MOVILIDAD"].str.upper()=="EMIGRATORIA"),"TOTAL"
    ].sum()
    enrolled=mat_f["MATRICULADOS"].sum()
    rate=1000*students/enrolled if enrolled else 0
    rate_int=1000*intl_students/enrolled if enrolled else 0
    rate_out=1000*outgoing_students/enrolled if enrolled else 0

    # coverage by canonical mobility careers vs current filtered matriculation careers
    mov_c=set(mov_f["CARRERA_CANON"].dropna().astype(str))
    mat_c=set(mat_f["CARRERA"].dropna().astype(str))
    if "EDUCACIÓN SECUNDARIA (TODAS)" in mov_c:
        if any(c.startswith("EDUCACIÓN SECUNDARIA") for c in mat_c):
            covered_secondary=True
        else:
            covered_secondary=False
    covered=sum(1 for c in mat_c if c in mov_c)
    if "EDUCACIÓN SECUNDARIA (TODAS)" in mov_c and covered_secondary:
        covered += sum(1 for c in mat_c if c.startswith("EDUCACIÓN SECUNDARIA"))
    coverage=pct(covered,len(mat_c)) if mat_c else 0

    a,b,c,d=st.columns(4)
    with a:kpi("Tasa de movilidad / 1 000",f"{rate:.1f}","Estudiantes en movilidad / matriculados P1")
    with b:kpi("Tasa internacional / 1 000",f"{rate_int:.1f}","Movilidad internacional estudiantil / matriculados P1")
    with c:kpi("Tasa saliente / 1 000",f"{rate_out:.1f}","Movilidad emigratoria estudiantil / matriculados P1")
    with d:kpi("Cobertura de carreras",fmt_pct(coverage),f"{covered} de {len(mat_c)} carreras con movilidad")

    total=mov_f["TOTAL"].sum()
    incoming=mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="INMIGRATORIA","TOTAL"].sum()
    outgoing=mov_f.loc[mov_f["MOVILIDAD"].str.upper()=="EMIGRATORIA","TOTAL"].sum()
    female=mov_f.loc[mov_f["GÉNERO"].str.upper()=="FEMENINO","TOTAL"].sum()
    dest=mov_f.groupby("REGIÓN / PAÍS")["TOTAL"].sum().sort_values(ascending=False)
    conc5=pct(dest.head(5).sum(),total)
    ratio=outgoing/incoming if incoming else np.nan

    a,b,c,d=st.columns(4)
    with a:kpi("Índice de movilidad entrante",fmt_pct(pct(incoming,total)),"Entrante / movilidad total")
    with b:kpi("Razón saliente : entrante","—" if pd.isna(ratio) else f"{ratio:.1f} : 1","Balance de flujos")
    with c:kpi("Participación femenina",fmt_pct(pct(female,total)),"Composición por género")
    with d:kpi("Concentración Top 5",fmt_pct(conc5),"Peso de los cinco destinos principales")

    st.markdown('<div class="section">Comparación anual normalizada</div>',unsafe_allow_html=True)
    rows=[]
    for y in years_common:
        my=mov[mov["AÑO"]==y]
        sy=my.loc[my["QUIÉN"].str.upper().str.contains("ESTUD"),"TOTAL"].sum()
        iy=my.loc[
            my["QUIÉN"].str.upper().str.contains("ESTUD") &
            (my["MODALIDAD"].str.upper()=="INTERNACIONAL"),"TOTAL"
        ].sum()
        maty=mat[mat["AÑO"]==y]
        if sede!="Todas": maty=maty[maty["SEDE"]==sede]
        if fac!="Todas": maty=maty[maty["FACULTAD"]==fac]
        if car!="Todas":
            if car=="EDUCACIÓN SECUNDARIA (TODAS)":
                maty=maty[maty["CARRERA"].str.upper().str.startswith("EDUCACIÓN SECUNDARIA")]
            else:
                maty=maty[maty["CARRERA"]==car]
        den=maty["MATRICULADOS"].sum()
        rows.append({"AÑO":str(y),"Tasa movilidad / 1000":1000*sy/den if den else 0,
                     "Tasa internacional / 1000":1000*iy/den if den else 0})
    df=pd.DataFrame(rows)
    fig=go.Figure()
    fig.add_trace(go.Bar(x=df["AÑO"],y=df["Tasa movilidad / 1000"],name="Movilidad / 1 000",marker_color=COLORS[0]))
    fig.add_trace(go.Bar(x=df["AÑO"],y=df["Tasa internacional / 1000"],name="Internacional / 1 000",marker_color=COLORS[2]))
    fig.update_layout(barmode="group",title="Tasas de movilidad por cada 1 000 matriculados · Periodo 1")
    figstyle(fig,390)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.caption("Denominador: matrícula del Periodo 1 de cada año. No se suman Periodo 1 y Periodo 2.")

# ---------- BASE ----------
else:
    t1,t2,t3=st.tabs(["Movilidad","Convenios","Matrícula · Periodo 1"])
    with t1:
        st.dataframe(mov_f,use_container_width=True,height=500,hide_index=True)
        st.download_button("Descargar movilidad filtrada",mov_f.to_csv(index=False).encode("utf-8-sig"),
                           "movilidad_filtrada.csv","text/csv")
    with t2:
        st.dataframe(conv_f,use_container_width=True,height=500,hide_index=True)
        st.download_button("Descargar convenios filtrados",conv_f.to_csv(index=False).encode("utf-8-sig"),
                           "convenios_filtrados.csv","text/csv")
    with t3:
        st.dataframe(mat_f,use_container_width=True,height=500,hide_index=True)
        st.caption("Esta tabla contiene únicamente matrícula del Periodo 1.")
        st.download_button("Descargar matrícula P1 filtrada",mat_f.to_csv(index=False).encode("utf-8-sig"),
                           "matricula_periodo1_filtrada.csv","text/csv")

st.markdown("---")
st.caption("Universidad Nacional de Trujillo · Unidad de Estadística · Dashboard estadístico interactivo")
