from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title='UNT | Convenios e Internacionalización',
    page_icon='🎓',
    layout='wide',
    initial_sidebar_state='expanded'
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
TODAY = pd.Timestamp(date.today())

# ------------------------------
# ESTILO
# ------------------------------
st.markdown('''
<style>
:root {
  --navy:#0b1830;
  --navy2:#13294b;
  --violet:#6558f5;
  --cyan:#14b8a6;
  --ink:#172033;
  --muted:#667085;
  --line:#e7eaf0;
  --bg:#f5f7fb;
  --card:#ffffff;
}
html, body, [class*="css"]  { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.stApp { background: var(--bg); }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #081426 0%, #101d35 100%); }
section[data-testid="stSidebar"] * { color: #f7f9fc !important; }
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 10px; border-radius: 10px; margin: 2px 0;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(255,255,255,.08); }
.block-container { padding-top: 1.4rem; padding-bottom: 2.5rem; max-width: 1550px; }
.hero {
    background: linear-gradient(125deg, #5a50ee 0%, #4958f4 45%, #19a9dc 100%);
    border-radius: 20px; padding: 26px 30px; color: white; margin-bottom: 18px;
    box-shadow: 0 14px 34px rgba(64,83,220,.16);
}
.hero h1 { margin: 0 0 6px 0; font-size: 2rem; line-height: 1.15; }
.hero p { margin: 0; opacity: .9; font-size: .98rem; }
.section-title { font-size: 1.08rem; font-weight: 800; color: var(--ink); margin: 8px 0 10px; }
.kpi {
    background: var(--card); border:1px solid var(--line); border-radius:16px;
    padding:18px 18px 14px 18px; min-height:118px; box-shadow:0 7px 22px rgba(17,24,39,.045);
}
.kpi .label { color:#697386; font-size:.83rem; font-weight:700; margin-bottom:8px; }
.kpi .value { color:#111827; font-size:1.85rem; font-weight:850; letter-spacing:-.03em; line-height:1; }
.kpi .note { color:#98a2b3; font-size:.76rem; margin-top:10px; }
.badge { display:inline-block; padding:4px 9px; border-radius:999px; background:#eef2ff; color:#5145cd; font-size:.72rem; font-weight:800; }
.insight {
    background:#fff; border:1px solid var(--line); border-left:4px solid #6558f5;
    border-radius:14px; padding:14px 16px; color:#344054; font-size:.9rem;
    box-shadow:0 6px 18px rgba(17,24,39,.035); margin-top:7px;
}
.filterbox { background:#fff; border:1px solid var(--line); border-radius:16px; padding:10px 14px 2px 14px; margin-bottom:14px; }
.small-muted { color:#7b8495; font-size:.8rem; }
hr { border-color:#eef0f5 !important; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; }
div[data-testid="stPlotlyChart"] { background:#fff; border:1px solid var(--line); border-radius:16px; padding:4px; box-shadow:0 6px 18px rgba(17,24,39,.035); }
</style>
''', unsafe_allow_html=True)

# ------------------------------
# DATOS
# ------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    nat = pd.read_excel(DATA_DIR / 'CONVENIOS_NACIONALES_.xlsx')
    intl = pd.read_excel(DATA_DIR / 'CONVENIOS_INTERNACIONALES.xlsx', sheet_name='Convenios')
    mov = pd.read_excel(DATA_DIR / 'MOVILIDAD_ACADEMICA.xlsx', sheet_name='Movilidad')
    mat = pd.read_csv(DATA_DIR / 'MATRICULADOS_PERIODO1_AGREGADO.csv')

    # Nacionales
    nat.columns = [str(c).strip() for c in nat.columns]
    nat['Año_Registro'] = pd.to_numeric(nat['Año_Registro'], errors='coerce').astype('Int64')
    nat['Fecha_Inicio'] = pd.to_datetime(nat['Fecha_Inicio'], errors='coerce')
    nat['Fecha_Término'] = pd.to_datetime(nat['Fecha_Término'], errors='coerce')
    nat['Institución'] = nat['Institución'].astype(str).str.strip()
    nat['Tipo_Convenio'] = nat['Tipo_Convenio'].astype(str).str.strip()

    def clasif_tipo_nat(x):
        t = str(x).lower()
        if 'marco' in t: return 'Marco'
        if 'espec' in t: return 'Específico'
        if 'docente' in t or 'asistencial' in t: return 'Docente-asistencial'
        if 'cultural' in t or 'lingü' in t: return 'Cultural / lingüístico'
        if 'administr' in t: return 'Administración'
        if 'cooper' in t: return 'Cooperación'
        return 'Otros'
    nat['Tipo_Analítico'] = nat['Tipo_Convenio'].apply(clasif_tipo_nat)

    # Internacionales
    intl.columns = [str(c).strip() for c in intl.columns]
    intl['AÑO'] = pd.to_numeric(intl['AÑO'], errors='coerce').astype('Int64')
    intl['INICIO'] = pd.to_datetime(intl['INICIO'], errors='coerce')
    intl['VENCE'] = pd.to_datetime(intl['VENCE'], errors='coerce')
    intl['INSTITUCIÓN'] = intl['INSTITUCIÓN'].astype(str).str.strip()
    intl['PAÍS'] = intl['PAÍS'].astype(str).str.strip()
    intl['TIPO'] = intl['TIPO'].astype(str).str.strip().str.title()

    # Estado de vigencia
    def estado(fecha_fin):
        if pd.isna(fecha_fin): return 'Sin fecha de término'
        if fecha_fin < TODAY: return 'Vencido'
        if fecha_fin <= TODAY + pd.Timedelta(days=180): return 'Por vencer ≤ 180 días'
        return 'Vigente'
    nat['Estado'] = nat['Fecha_Término'].apply(estado)
    intl['Estado'] = intl['VENCE'].apply(estado)

    # Movilidad
    mov.columns = [str(c).strip() for c in mov.columns]
    for c in ['AÑO', 'TOTAL']:
        mov[c] = pd.to_numeric(mov[c], errors='coerce')
    mov['TOTAL'] = mov['TOTAL'].fillna(0)
    for c in ['MOVILIDAD','PERÍODO','MODALIDAD','QUIÉN','REGIÓN / PAÍS','CARRERA PROFESIONAL',
              'UNIVERSIDAD DE ORIGEN','UNIVERSIDAD DE DESTINO','GÉNERO']:
        mov[c] = mov[c].astype(str).str.strip().str.upper()

    # Matrícula
    mat.columns = [str(c).strip() for c in mat.columns]
    mat['AÑO'] = pd.to_numeric(mat['AÑO'], errors='coerce')
    mat['MATRICULADOS'] = pd.to_numeric(mat['MATRICULADOS'], errors='coerce').fillna(0)
    for c in ['SEDE','FACULTAD','CARRERA','SEXO']:
        mat[c] = mat[c].astype(str).str.strip()
    return nat, intl, mov, mat

nat, intl, mov, mat = load_data()

# ------------------------------
# HELPERS VISUALES
# ------------------------------
COLORS = ['#6558F5','#18A6D9','#14B8A6','#F59E0B','#EF6A8A','#7C8AA5','#2F80ED']


def chart_layout(fig, height=340, legend=True):
    fig.update_layout(
        height=height, margin=dict(l=22,r=18,t=48,b=24),
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter, Arial', color='#344054', size=12),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0) if legend else dict(visible=False),
        hoverlabel=dict(bgcolor='white', font_size=12)
    )
    fig.update_xaxes(showgrid=False, linecolor='#e9edf4')
    fig.update_yaxes(gridcolor='#edf0f5', zeroline=False)
    return fig


def kpi(label, value, note=''):
    st.markdown(f'''<div class="kpi"><div class="label">{label}</div><div class="value">{value}</div><div class="note">{note}</div></div>''', unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight"><b>Interpretación.</b> {text}</div>', unsafe_allow_html=True)


def pct(x, total):
    return 0 if total == 0 else 100*x/total


def top_label_bar(df, x, y, title, horizontal=False, height=350):
    if df.empty:
        st.info('No hay registros para los filtros seleccionados.')
        return
    if horizontal:
        fig = px.bar(df, x=x, y=y, orientation='h', text=x, title=title, color_discrete_sequence=COLORS)
        fig.update_traces(textposition='outside', cliponaxis=False)
        fig.update_yaxes(categoryorder='total ascending')
    else:
        fig = px.bar(df, x=x, y=y, text=y, title=title, color_discrete_sequence=COLORS)
        fig.update_traces(textposition='outside', cliponaxis=False)
    st.plotly_chart(chart_layout(fig, height=height, legend=False), use_container_width=True, config={'displayModeBar':False})

# ------------------------------
# SIDEBAR
# ------------------------------
with st.sidebar:
    st.markdown('''
    <div style="padding:8px 4px 18px 4px">
      <div style="font-size:1.35rem;font-weight:900;letter-spacing:.02em">UNT · ANALYTICS</div>
      <div style="font-size:.78rem;opacity:.65;margin-top:4px">Convenios e Internacionalización</div>
    </div>
    ''', unsafe_allow_html=True)
    page = st.radio('Navegación', [
        'Resumen ejecutivo',
        'Convenios nacionales',
        'Convenios internacionales',
        'Movilidad académica',
        'Matrícula e indicador relativo',
        'Ficha técnica'
    ], label_visibility='collapsed')
    st.markdown('<hr>', unsafe_allow_html=True)
    st.caption('Datos disponibles: convenios nacionales e internacionales, movilidad académica y matrícula agregada.')

# ------------------------------
# HERO
# ------------------------------
page_sub = {
    'Resumen ejecutivo':'Lectura directiva de cooperación e internacionalización universitaria.',
    'Convenios nacionales':'Seguimiento exclusivo de cooperación nacional. No se mezcla con internacionalización.',
    'Convenios internacionales':'Cobertura internacional por país, vigencia y tipo de convenio.',
    'Movilidad académica':'Flujos entrantes y salientes, nacionales e internacionales, de estudiantes y docentes.',
    'Matrícula e indicador relativo':'Contexto institucional y tasa de movilidad por cada 1,000 matriculados.',
    'Ficha técnica':'Definiciones, fórmulas y criterios usados por el tablero.'
}
st.markdown(f'''<div class="hero"><span class="badge">UNIVERSIDAD NACIONAL DE TRUJILLO</span><h1>{page}</h1><p>{page_sub[page]}</p></div>''', unsafe_allow_html=True)

# ------------------------------
# RESUMEN EJECUTIVO
# ------------------------------
if page == 'Resumen ejecutivo':
    st.markdown('<div class="section-title">Cooperación nacional</div>', unsafe_allow_html=True)
    n_total = len(nat)
    n_vig = (nat['Estado']=='Vigente').sum()
    n_vence = (nat['Estado']=='Por vencer ≤ 180 días').sum()
    n_inst = nat['Institución'].nunique()
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi('Convenios nacionales registrados', f'{n_total:,}', 'Base nacional; no incluye convenios internacionales.')
    with c2: kpi('Convenios nacionales vigentes', f'{n_vig:,}', f'{pct(n_vig,n_total):.1f}% del total nacional')
    with c3: kpi('Por vencer en ≤ 180 días', f'{n_vence:,}', 'Alerta de gestión para seguimiento de vigencia')
    with c4: kpi('Instituciones nacionales vinculadas', f'{n_inst:,}', 'Instituciones distintas registradas')

    st.markdown('<div class="section-title" style="margin-top:18px">Internacionalización</div>', unsafe_allow_html=True)
    i_total = len(intl)
    i_vig = (intl['Estado']=='Vigente').sum()
    i_countries = intl['PAÍS'].replace('NAN',np.nan).nunique()
    mov_int = int(mov.loc[mov['MODALIDAD']=='INTERNACIONAL','TOTAL'].sum())
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi('Convenios internacionales', f'{i_total:,}', 'Instrumentos internacionales registrados')
    with c2: kpi('Países con convenio', f'{i_countries:,}', 'Cobertura geográfica de cooperación internacional')
    with c3: kpi('Convenios internacionales vigentes', f'{i_vig:,}', f'{pct(i_vig,i_total):.1f}% del total internacional')
    with c4: kpi('Movilidades internacionales', f'{mov_int:,}', 'Suma de participantes registrados en movilidad internacional')

    left,right = st.columns([1.05,.95])
    with left:
        reg_nat = nat.groupby('Año_Registro', dropna=True).size().reset_index(name='Convenios')
        fig = px.area(reg_nat, x='Año_Registro', y='Convenios', markers=True,
                      title='Evolución de registros de convenios nacionales', color_discrete_sequence=['#6558F5'])
        fig.update_traces(text=reg_nat['Convenios'], textposition='top center', mode='lines+markers+text')
        st.plotly_chart(chart_layout(fig, 360, False), use_container_width=True, config={'displayModeBar':False})
        if len(reg_nat):
            peak = reg_nat.loc[reg_nat['Convenios'].idxmax()]
            insight(f'La mayor cantidad de registros nacionales se observa en {int(peak["Año_Registro"])} con {int(peak["Convenios"])} convenios. Esta lectura corresponde a registros por año y no debe interpretarse como total de convenios vigentes.')
    with right:
        reg_int = intl.groupby('AÑO', dropna=True).size().reset_index(name='Convenios')
        fig = px.bar(reg_int, x='AÑO', y='Convenios', text='Convenios',
                     title='Evolución de registros de convenios internacionales', color_discrete_sequence=['#14B8A6'])
        fig.update_traces(textposition='outside')
        st.plotly_chart(chart_layout(fig, 360, False), use_container_width=True, config={'displayModeBar':False})
        if len(reg_int):
            peak = reg_int.loc[reg_int['Convenios'].idxmax()]
            insight(f'En convenios internacionales, el mayor volumen de registros corresponde a {int(peak["AÑO"])} con {int(peak["Convenios"])}. Se mantiene separado del componente nacional para evitar mezclar dimensiones distintas de gestión.')

    st.markdown('<div class="section-title" style="margin-top:18px">Movilidad académica: lectura estratégica</div>', unsafe_allow_html=True)
    m_year = mov.groupby(['AÑO','MOVILIDAD'], as_index=False)['TOTAL'].sum()
    fig = px.line(m_year, x='AÑO', y='TOTAL', color='MOVILIDAD', markers=True, text='TOTAL',
                  title='Movilidad académica por dirección', color_discrete_sequence=['#6558F5','#14B8A6'])
    fig.update_traces(textposition='top center')
    st.plotly_chart(chart_layout(fig, 380, True), use_container_width=True, config={'displayModeBar':False})

    out_total = int(mov.loc[mov['MOVILIDAD']=='EMIGRATORIA','TOTAL'].sum())
    in_total = int(mov.loc[mov['MOVILIDAD']=='IMIGRATORIA','TOTAL'].sum())
    who_top = mov.groupby('QUIÉN')['TOTAL'].sum().sort_values(ascending=False)
    insight(f'La base registra {out_total} movilidades emigratorias y {in_total} inmigratorias. El grupo con mayor participación es {who_top.index[0].title()} con {int(who_top.iloc[0])} registros. El sexo no se usa como indicador principal porque el objetivo del tablero es monitorear cooperación e internacionalización, no caracterización demográfica.')

# ------------------------------
# CONVENIOS NACIONALES
# ------------------------------
elif page == 'Convenios nacionales':
    with st.container():
        st.markdown('<div class="filterbox">', unsafe_allow_html=True)
        f1,f2,f3 = st.columns(3)
        years = sorted([int(x) for x in nat['Año_Registro'].dropna().unique()], reverse=True)
        with f1: sel_years = st.multiselect('Año de registro', years, default=years)
        with f2: sel_tipos = st.multiselect('Clasificación analítica', sorted(nat['Tipo_Analítico'].dropna().unique()), default=sorted(nat['Tipo_Analítico'].dropna().unique()))
        with f3: sel_estado = st.multiselect('Estado de vigencia', ['Vigente','Por vencer ≤ 180 días','Vencido','Sin fecha de término'], default=['Vigente','Por vencer ≤ 180 días','Vencido','Sin fecha de término'])
        st.markdown('</div>', unsafe_allow_html=True)
    d = nat[nat['Año_Registro'].isin(sel_years) & nat['Tipo_Analítico'].isin(sel_tipos) & nat['Estado'].isin(sel_estado)].copy()
    total=len(d); vig=(d['Estado']=='Vigente').sum(); vence=(d['Estado']=='Por vencer ≤ 180 días').sum(); inst=d['Institución'].nunique()
    c1,c2,c3,c4=st.columns(4)
    with c1:kpi('Convenios filtrados',f'{total:,}','Resultado de los filtros activos')
    with c2:kpi('Vigentes',f'{vig:,}',f'{pct(vig,total):.1f}% de la selección')
    with c3:kpi('Por vencer ≤ 180 días',f'{vence:,}','Prioridad de seguimiento')
    with c4:kpi('Instituciones vinculadas',f'{inst:,}','Instituciones distintas')

    a,b=st.columns(2)
    with a:
        g=d.groupby('Año_Registro').size().reset_index(name='Convenios')
        top_label_bar(g,'Año_Registro','Convenios','Convenios nacionales por año de registro')
    with b:
        g=d.groupby('Tipo_Analítico').size().reset_index(name='Convenios').sort_values('Convenios',ascending=False)
        top_label_bar(g,'Convenios','Tipo_Analítico','Composición por tipo analítico',horizontal=True)
    if total:
        top_tipo=d['Tipo_Analítico'].value_counts().idxmax(); topn=d['Tipo_Analítico'].value_counts().max()
        insight(f'En la selección actual predominan los convenios clasificados como {top_tipo}, con {topn} registros. Esta clasificación es analítica y agrupa variantes de redacción del campo “Tipo_Convenio” para facilitar el seguimiento gerencial.')

    st.markdown('<div class="section-title">Agenda de vigencia</div>', unsafe_allow_html=True)
    agenda=d[['Institución','Tipo_Analítico','Fecha_Inicio','Fecha_Término','Estado','N_Resolución']].sort_values('Fecha_Término', na_position='last')
    st.dataframe(agenda, use_container_width=True, hide_index=True, column_config={
        'Fecha_Inicio':st.column_config.DateColumn('Inicio',format='DD/MM/YYYY'),
        'Fecha_Término':st.column_config.DateColumn('Término',format='DD/MM/YYYY')
    })

# ------------------------------
# CONVENIOS INTERNACIONALES
# ------------------------------
elif page == 'Convenios internacionales':
    with st.container():
        st.markdown('<div class="filterbox">', unsafe_allow_html=True)
        f1,f2,f3=st.columns(3)
        years=sorted([int(x) for x in intl['AÑO'].dropna().unique()], reverse=True)
        countries=sorted([x for x in intl['PAÍS'].dropna().unique() if x and x.upper()!='NAN'])
        types=sorted(intl['TIPO'].dropna().unique())
        with f1: sy=st.multiselect('Año de registro',years,default=years)
        with f2: sc=st.multiselect('País',countries,default=countries)
        with f3: stypes=st.multiselect('Tipo',types,default=types)
        st.markdown('</div>', unsafe_allow_html=True)
    d=intl[intl['AÑO'].isin(sy)&intl['PAÍS'].isin(sc)&intl['TIPO'].isin(stypes)].copy()
    total=len(d); countries_n=d['PAÍS'].nunique(); vig=(d['Estado']=='Vigente').sum(); vence=(d['Estado']=='Por vencer ≤ 180 días').sum()
    c1,c2,c3,c4=st.columns(4)
    with c1:kpi('Convenios internacionales',f'{total:,}','Selección actual')
    with c2:kpi('Países representados',f'{countries_n:,}','Cobertura geográfica')
    with c3:kpi('Vigentes',f'{vig:,}',f'{pct(vig,total):.1f}% de la selección')
    with c4:kpi('Por vencer ≤ 180 días',f'{vence:,}','Alertas de vigencia')

    a,b=st.columns([1.05,.95])
    with a:
        g=d.groupby('PAÍS').size().reset_index(name='Convenios').sort_values('Convenios',ascending=False).head(12)
        top_label_bar(g,'Convenios','PAÍS','Países con mayor número de convenios',horizontal=True, height=430)
    with b:
        g=d.groupby('TIPO').size().reset_index(name='Convenios')
        fig=px.pie(g,names='TIPO',values='Convenios',hole=.62,title='Tipo de convenio internacional',color_discrete_sequence=['#6558F5','#14B8A6'])
        fig.update_traces(textposition='outside',textinfo='label+percent+value')
        st.plotly_chart(chart_layout(fig,430,True),use_container_width=True,config={'displayModeBar':False})
    if total:
        pc=d['PAÍS'].value_counts();
        insight(f'La cobertura internacional alcanza {countries_n} países en la selección. {pc.index[0]} concentra {int(pc.iloc[0])} convenios. Este módulo representa cooperación internacional formal; la movilidad académica se analiza por separado como resultado o flujo de internacionalización.')

    st.markdown('<div class="section-title">Detalle internacional</div>', unsafe_allow_html=True)
    detail=d[['INSTITUCIÓN','PAÍS','TIPO','INICIO','VENCE','Estado','RESOLUCIÓN']].sort_values(['PAÍS','VENCE'])
    st.dataframe(detail,use_container_width=True,hide_index=True,column_config={
        'INICIO':st.column_config.DateColumn('Inicio',format='DD/MM/YYYY'),
        'VENCE':st.column_config.DateColumn('Vence',format='DD/MM/YYYY')
    })

# ------------------------------
# MOVILIDAD
# ------------------------------
elif page == 'Movilidad académica':
    with st.container():
        st.markdown('<div class="filterbox">', unsafe_allow_html=True)
        a,b,c,dcol=st.columns(4)
        years=sorted([int(x) for x in mov['AÑO'].dropna().unique()], reverse=True)
        mods=sorted(mov['MODALIDAD'].dropna().unique())
        dirs=sorted(mov['MOVILIDAD'].dropna().unique())
        who=sorted(mov['QUIÉN'].dropna().unique())
        with a: sy=st.multiselect('Año',years,default=years)
        with b: sm=st.multiselect('Modalidad',mods,default=mods)
        with c: sd=st.multiselect('Dirección',dirs,default=dirs)
        with dcol: sw=st.multiselect('Participante',who,default=who)
        st.markdown('</div>', unsafe_allow_html=True)
    f=mov[mov['AÑO'].isin(sy)&mov['MODALIDAD'].isin(sm)&mov['MOVILIDAD'].isin(sd)&mov['QUIÉN'].isin(sw)].copy()
    total=int(f['TOTAL'].sum()); out=int(f.loc[f['MOVILIDAD']=='EMIGRATORIA','TOTAL'].sum()); inc=int(f.loc[f['MOVILIDAD']=='IMIGRATORIA','TOTAL'].sum()); intl_n=int(f.loc[f['MODALIDAD']=='INTERNACIONAL','TOTAL'].sum())
    c1,c2,c3,c4=st.columns(4)
    with c1:kpi('Participaciones registradas',f'{total:,}','Suma del campo TOTAL')
    with c2:kpi('Movilidad saliente',f'{out:,}',f'{pct(out,total):.1f}% de la selección')
    with c3:kpi('Movilidad entrante',f'{inc:,}',f'{pct(inc,total):.1f}% de la selección')
    with c4:kpi('Movilidad internacional',f'{intl_n:,}',f'{pct(intl_n,total):.1f}% de la selección')

    a,b=st.columns(2)
    with a:
        g=f.groupby(['AÑO','MOVILIDAD'],as_index=False)['TOTAL'].sum()
        fig=px.bar(g,x='AÑO',y='TOTAL',color='MOVILIDAD',barmode='group',text='TOTAL',title='Flujo de movilidad por año y dirección',color_discrete_sequence=['#6558F5','#14B8A6'])
        fig.update_traces(textposition='outside')
        st.plotly_chart(chart_layout(fig,370,True),use_container_width=True,config={'displayModeBar':False})
    with b:
        g=f.groupby(['MODALIDAD','QUIÉN'],as_index=False)['TOTAL'].sum()
        fig=px.bar(g,x='MODALIDAD',y='TOTAL',color='QUIÉN',barmode='group',text='TOTAL',title='Modalidad por tipo de participante',color_discrete_sequence=['#18A6D9','#F59E0B'])
        fig.update_traces(textposition='outside')
        st.plotly_chart(chart_layout(fig,370,True),use_container_width=True,config={'displayModeBar':False})

    a,b=st.columns([.9,1.1])
    with a:
        g=f.groupby('REGIÓN / PAÍS',as_index=False)['TOTAL'].sum().sort_values('TOTAL',ascending=False).head(12)
        top_label_bar(g,'TOTAL','REGIÓN / PAÍS','Principales regiones / países asociados',horizontal=True,height=430)
    with b:
        g=f.groupby('CARRERA PROFESIONAL',as_index=False)['TOTAL'].sum().sort_values('TOTAL',ascending=False).head(12)
        top_label_bar(g,'TOTAL','CARRERA PROFESIONAL','Carreras con mayor movilidad registrada',horizontal=True,height=430)
    if total:
        direction='saliente' if out>inc else ('entrante' if inc>out else 'equilibrada')
        top_place=f.groupby('REGIÓN / PAÍS')['TOTAL'].sum().sort_values(ascending=False)
        insight(f'El patrón de la selección es principalmente {direction}. El principal territorio asociado es {top_place.index[0].title()} con {int(top_place.iloc[0])} participaciones. Este análisis se basa en flujos de movilidad y no utiliza sexo como KPI de desempeño.')

# ------------------------------
# MATRÍCULA + INDICADOR RELATIVO
# ------------------------------
elif page == 'Matrícula e indicador relativo':
    years=sorted([int(x) for x in mat['AÑO'].dropna().unique()])
    sel=st.select_slider('Año de matrícula', options=years, value=years[-1])
    d=mat[mat['AÑO']==sel].copy()
    total=int(d['MATRICULADOS'].sum()); sedes=d['SEDE'].nunique(); fac=d['FACULTAD'].nunique(); car=d['CARRERA'].nunique()
    c1,c2,c3,c4=st.columns(4)
    with c1:kpi('Matriculados',f'{total:,}',f'Periodo 1 · {sel}')
    with c2:kpi('Sedes registradas',f'{sedes:,}','Cobertura de la base de matrícula')
    with c3:kpi('Facultades',f'{fac:,}','Facultades con matrícula registrada')
    with c4:kpi('Carreras',f'{car:,}','Programas/carreras registrados')

    a,b=st.columns(2)
    with a:
        g=mat.groupby('AÑO',as_index=False)['MATRICULADOS'].sum()
        fig=px.line(g,x='AÑO',y='MATRICULADOS',markers=True,text='MATRICULADOS',title='Evolución de matrícula agregada',color_discrete_sequence=['#6558F5'])
        fig.update_traces(textposition='top center')
        st.plotly_chart(chart_layout(fig,370,False),use_container_width=True,config={'displayModeBar':False})
    with b:
        g=d.groupby('SEDE',as_index=False)['MATRICULADOS'].sum().sort_values('MATRICULADOS',ascending=False)
        top_label_bar(g,'MATRICULADOS','SEDE',f'Matrícula por sede · {sel}',horizontal=True,height=370)

    # indicador relativo por 1,000 matriculados usando años comunes
    m_yr=mov.groupby('AÑO',as_index=False)['TOTAL'].sum().rename(columns={'TOTAL':'Movilidad'})
    e_yr=mat.groupby('AÑO',as_index=False)['MATRICULADOS'].sum()
    rate=m_yr.merge(e_yr,on='AÑO',how='inner')
    rate['Movilidad_por_1000']=np.where(rate['MATRICULADOS']>0,rate['Movilidad']/rate['MATRICULADOS']*1000,0)
    fig=px.bar(rate,x='AÑO',y='Movilidad_por_1000',text=rate['Movilidad_por_1000'].round(1),title='Indicador relativo: movilidades por cada 1,000 matriculados',color_discrete_sequence=['#14B8A6'])
    fig.update_traces(textposition='outside')
    st.plotly_chart(chart_layout(fig,390,False),use_container_width=True,config={'displayModeBar':False})
    if len(rate):
        last=rate.sort_values('AÑO').iloc[-1]
        insight(f'Para {int(last["AÑO"])}, la base registra aproximadamente {last["Movilidad_por_1000"]:.1f} movilidades por cada 1,000 matriculados. Este indicador permite dimensionar la movilidad respecto del tamaño de la población estudiantil; no mide por sí solo calidad ni cumplimiento de una meta institucional.')

# ------------------------------
# FICHA TÉCNICA
# ------------------------------
else:
    st.markdown('### Definiciones de indicadores')
    tech = pd.DataFrame([
        ['Convenios nacionales registrados','Conteo de registros de la base nacional','CONVENIOS_NACIONALES_.xlsx'],
        ['Convenios internacionales','Conteo de registros de la hoja Convenios','CONVENIOS_INTERNACIONALES.xlsx'],
        ['Vigente','Fecha de término posterior a 180 días desde la fecha de consulta','Bases de convenios'],
        ['Por vencer ≤ 180 días','Fecha de término entre hoy y los próximos 180 días','Bases de convenios'],
        ['Movilidad saliente','Registros con MOVILIDAD = EMIGRATORIA','MOVILIDAD_ACADEMICA.xlsx'],
        ['Movilidad entrante','Registros con MOVILIDAD = IMIGRATORIA','MOVILIDAD_ACADEMICA.xlsx'],
        ['Movilidad internacional','Registros con MODALIDAD = INTERNACIONAL','MOVILIDAD_ACADEMICA.xlsx'],
        ['Movilidad por 1,000 matriculados','Movilidad total del año / matrícula total del año × 1,000','Movilidad + matrícula']
    ],columns=['Indicador','Definición / fórmula','Fuente'])
    st.dataframe(tech,use_container_width=True,hide_index=True)
    st.markdown('### Criterios de diseño y lectura')
    st.markdown('''
- **Cooperación nacional** e **internacionalización** se presentan en módulos separados. Un convenio nacional no se suma a un convenio internacional como si fueran la misma dimensión estratégica.
- En movilidad, la dirección **EMIGRATORIA** se interpreta como salida desde la UNT y **IMIGRATORIA** como ingreso hacia la UNT, de acuerdo con la codificación de la base.
- La variable **sexo/género** permanece en la fuente, pero no se usa como KPI principal del tablero porque no representa por sí sola un indicador de desempeño de internacionalización.
- La clasificación de convenios nacionales en “Marco”, “Específico”, “Docente-asistencial”, etc. es una **clasificación analítica** construida a partir del texto original de `Tipo_Convenio` para reducir variantes de escritura.
- Las interpretaciones automáticas describen los datos filtrados y evitan convertir una cifra descriptiva en una evaluación de desempeño sin una meta oficial.
''')
    st.info('El tablero no incluye botones de descarga. Está orientado a consulta, seguimiento y lectura directiva.')
