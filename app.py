from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==============================================================
# CONFIGURACIÓN GENERAL
# ==============================================================
st.set_page_config(
    page_title="UNT | Satisfacción estudiantil",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path(__file__).resolve().parent / "basededatos.xlsx"
SHEET_NAME = "Base_Encuesta"
TARGET = 0.75

DIMENSIONS = {
    "D1": {
        "name": "Calidad del proceso académico",
        "short": "Proceso académico",
        "items": ["P1", "P2", "P3", "P4"],
        "color": "#3157D5",
        "soft": "#EEF2FF",
        "icon": "📘",
        "desc": "Pertinencia curricular, plan de estudios, carga académica y coherencia de las asignaturas.",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "short": "Docencia y pedagogía",
        "items": ["P5", "P6", "P7", "P8"],
        "color": "#6D4CC7",
        "soft": "#F3EFFF",
        "icon": "🎓",
        "desc": "Dominio docente, metodología, participación del estudiante y retroalimentación.",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "short": "Servicios y gestión",
        "items": ["P9", "P10", "P11", "P12"],
        "color": "#B7791F",
        "soft": "#FFF7E8",
        "icon": "🏛️",
        "desc": "Trámites, información académica, infraestructura, recursos y aseguramiento de la calidad.",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "short": "Formación integral",
        "items": ["P13", "P14", "P15", "P16"],
        "color": "#16836B",
        "soft": "#ECF8F4",
        "icon": "🌱",
        "desc": "Competencias profesionales, valores, desarrollo personal y preparación para el ejercicio profesional.",
    },
}

ITEM_TEXT = {
    "P1": "Los contenidos de las asignaturas que curso son pertinentes para mi formación profesional.",
    "P2": "El plan de estudios de mi carrera está actualizado y responde a las demandas del entorno profesional.",
    "P3": "La carga académica por semestre es adecuada para lograr un buen aprendizaje.",
    "P4": "Existe coherencia entre los objetivos de las asignaturas y los contenidos desarrollados.",
    "P5": "Los docentes demuestran dominio de los temas que imparten.",
    "P6": "Los docentes utilizan metodologías de enseñanza que facilitan mi aprendizaje.",
    "P7": "Los docentes promueven la participación activa de los estudiantes en clase.",
    "P8": "La retroalimentación brindada por los docentes contribuye a mejorar mi desempeño académico.",
    "P9": "Los servicios académicos (matrícula, registros, trámites) funcionan de manera eficiente.",
    "P10": "La universidad brinda información clara y oportuna sobre los procesos académicos.",
    "P11": "La infraestructura y los recursos educativos son adecuados para el aprendizaje.",
    "P12": "La universidad promueve acciones orientadas al aseguramiento de la calidad educativa.",
    "P13": "Mi formación universitaria contribuye al desarrollo de mis competencias profesionales.",
    "P14": "La universidad fomenta valores éticos y responsabilidad social en los estudiantes.",
    "P15": "Las actividades académicas y extracurriculares contribuyen a mi desarrollo personal y ciudadano.",
    "P16": "Me siento preparado(a) para afrontar los retos del ejercicio profesional futuro.",
    "P17": "En general, me siento satisfecho(a) con el proceso de formación académica que recibo en la Universidad Nacional de Trujillo.",
}

STATUS = {
    "Insatisfactorio": {
        "color": "#D9363E",
        "dark": "#8F1F25",
        "soft": "#FFF0F1",
        "range": "0% a <60%",
        "signal": "red",
        "emoji": "🔴",
        "action": "Atención prioritaria",
    },
    "Regular": {
        "color": "#E59A18",
        "dark": "#9A6209",
        "soft": "#FFF7E6",
        "range": "60% a <75%",
        "signal": "amber",
        "emoji": "🟠",
        "action": "Requiere seguimiento",
    },
    "Satisfactorio": {
        "color": "#1C9B62",
        "dark": "#126540",
        "soft": "#ECF9F2",
        "range": "75% a <90%",
        "signal": "green",
        "emoji": "🟢",
        "action": "Cumple el estándar",
    },
    "Muy satisfactorio": {
        "color": "#087A57",
        "dark": "#07513C",
        "soft": "#E7F7F0",
        "range": "90% a 100%",
        "signal": "green",
        "emoji": "🟢",
        "action": "Desempeño destacado",
    },
}

LIKERT = {
    "Desfavorable (1–2)": "#D9595F",
    "Neutral (3)": "#AAB3C0",
    "Favorable (4–5)": "#248B70",
}

PLOT_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": False,
    "doubleClick": False,
}


# ==============================================================
# ESTILO RESPONSIVE — COMPUTADORA, TABLET Y CELULAR
# ==============================================================
st.html(
    """
<style>
:root{
  --ink:#172033;
  --muted:#6D788A;
  --line:#E6EAF0;
  --paper:#FFFFFF;
  --bg:#F5F7FB;
  --navy:#0D1F35;
  --navy2:#163D5C;
  --blue:#3157D5;
  --shadow:0 16px 38px rgba(25,39,62,.08),0 3px 8px rgba(25,39,62,.035);
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"Aptos","Segoe UI Variable","Segoe UI",Inter,Arial,sans-serif;}
.stApp{
  background:
    radial-gradient(circle at 8% -6%,rgba(49,87,213,.09),transparent 34rem),
    radial-gradient(circle at 98% 4%,rgba(22,131,107,.08),transparent 30rem),
    linear-gradient(180deg,#FAFBFD 0%,var(--bg) 100%);
  color:var(--ink);
}
.block-container{max-width:1420px;padding:1rem 1.5rem 3rem;}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:rgba(250,251,253,.86);backdrop-filter:blur(12px);}
section[data-testid="stSidebar"]{display:none!important;}
[data-testid="stSidebarCollapsedControl"]{display:none!important;}

/* HERO */
.hero{
  position:relative;overflow:hidden;border-radius:28px;padding:28px 30px;
  background:linear-gradient(120deg,#0A1C31 0%,#113C5C 62%,#0D6C70 130%);
  color:#fff;border:1px solid rgba(255,255,255,.08);
  box-shadow:0 26px 62px rgba(13,31,53,.20),inset 0 1px 0 rgba(255,255,255,.10);
}
.hero:before{content:"";position:absolute;right:-85px;top:-130px;width:360px;height:360px;border-radius:50%;border:64px solid rgba(255,255,255,.045)}
.hero-kicker{font-size:.72rem;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:#A8DDE3;margin-bottom:8px}
.hero-title{font-size:clamp(1.65rem,4vw,2.45rem);font-weight:850;letter-spacing:-.045em;line-height:1.05;margin:0;color:white}
.hero-sub{font-size:clamp(.83rem,1.5vw,.98rem);color:#D8E7EE;line-height:1.5;max-width:920px;margin-top:9px}
.hero-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px;position:relative;z-index:1}
.hero-chip{padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14);font-size:.74rem;color:#F2F8FA}

/* SECCIONES */
.section-head{display:flex;align-items:end;justify-content:space-between;gap:14px;margin:1.45rem 0 .72rem}
.section-kicker{font-size:.67rem;color:#3157D5;font-weight:850;text-transform:uppercase;letter-spacing:.12em;margin-bottom:3px}
.section-title{font-size:clamp(1.05rem,2.3vw,1.3rem);font-weight:850;letter-spacing:-.025em;color:#17263A;line-height:1.2}
.section-note{font-size:.77rem;color:#7A8797;text-align:right;max-width:460px}

/* GRIDS RESPONSIVE */
.top-grid{display:grid;grid-template-columns:minmax(300px,.92fr) minmax(0,1.65fr);gap:18px;align-items:stretch}
.kpi-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:12px}
.dim-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.insight-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.method-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.rule-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}

/* TARJETAS */
.card,.metric-card,.dim-card,.insight-card,.method-card,.rule-card{
  background:linear-gradient(145deg,#FFFFFF 0%,#FBFCFE 66%,#F5F7FA 100%);
  border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);
}
.metric-card,.dim-card,.insight-card{transition:transform .18s ease,box-shadow .18s ease}
.metric-card:hover,.dim-card:hover,.insight-card:hover{transform:translateY(-2px);box-shadow:0 22px 48px rgba(25,39,62,.11)}

/* SEMÁFORO 3D GLOBAL */
.signal-card{padding:20px;min-height:336px;position:relative;overflow:hidden}
.signal-label{font-size:.66rem;font-weight:850;text-transform:uppercase;letter-spacing:.12em;color:#718096}
.signal-title{font-size:1.02rem;font-weight:850;color:#1A2E43;margin-top:5px}
.signal-stage{margin-top:15px;padding:17px;border-radius:20px;background:linear-gradient(145deg,#091520,#122B3E);border:1px solid rgba(255,255,255,.08);box-shadow:0 16px 30px rgba(8,24,37,.23),inset 0 1px 0 rgba(255,255,255,.07);display:grid;grid-template-columns:105px minmax(0,1fr);gap:18px;align-items:center}
.traffic-wrap{display:flex;justify-content:center}
.traffic{
  width:80px;padding:10px 9px;border-radius:26px;background:linear-gradient(145deg,#26333F,#080C10);
  border:2px solid #344656;box-shadow:11px 13px 22px rgba(0,0,0,.34),inset 6px 6px 12px rgba(255,255,255,.045),inset -7px -8px 14px rgba(0,0,0,.5);position:relative
}
.traffic:before{content:"🚦";position:absolute;font-size:1.15rem;right:-16px;top:-17px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.25))}
.lamp{width:49px;height:49px;border-radius:50%;margin:8px auto;opacity:.16;position:relative;box-shadow:inset 8px 9px 13px rgba(255,255,255,.07),inset -9px -10px 15px rgba(0,0,0,.45),0 3px 5px rgba(0,0,0,.5)}
.lamp:after{content:"";position:absolute;width:14px;height:9px;border-radius:50%;left:10px;top:7px;background:rgba(255,255,255,.30);transform:rotate(-18deg)}
.lamp.red{background:#EF4444}.lamp.amber{background:#F59E0B}.lamp.green{background:#22C55E}
.lamp.on{opacity:1;animation:glow 2s ease-in-out infinite}
.lamp.red.on{box-shadow:0 0 11px #EF4444,0 0 34px rgba(239,68,68,.72),inset 8px 9px 13px rgba(255,255,255,.30),inset -9px -10px 15px rgba(80,0,0,.35)}
.lamp.amber.on{box-shadow:0 0 11px #F59E0B,0 0 34px rgba(245,158,11,.72),inset 8px 9px 13px rgba(255,255,255,.30),inset -9px -10px 15px rgba(86,51,0,.35)}
.lamp.green.on{box-shadow:0 0 11px #22C55E,0 0 34px rgba(34,197,94,.70),inset 8px 9px 13px rgba(255,255,255,.30),inset -9px -10px 15px rgba(0,68,35,.35)}
@keyframes glow{0%,100%{transform:scale(1)}50%{transform:scale(1.055)}}
.signal-score{font-size:clamp(2.25rem,5vw,3rem);font-weight:900;letter-spacing:-.06em;color:#fff;line-height:1}
.signal-level{font-size:1rem;font-weight:850;margin-top:8px}
.signal-range{font-size:.75rem;color:#CAD9E2;margin-top:5px;line-height:1.42}
.signal-action{display:inline-flex;margin-top:10px;border-radius:999px;padding:6px 9px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);font-size:.7rem;color:#F4F8FA}
.scale{height:10px;border-radius:999px;display:grid;grid-template-columns:60fr 15fr 15fr 10fr;overflow:hidden;margin-top:15px;border:1px solid #E4E9F0}
.scale span:nth-child(1){background:#D9363E}.scale span:nth-child(2){background:#E59A18}.scale span:nth-child(3){background:#1C9B62}.scale span:nth-child(4){background:#087A57}
.scale-labels{display:grid;grid-template-columns:60fr 15fr 15fr 10fr;margin-top:5px;font-size:.59rem;color:#7D8999;line-height:1.2}

/* KPIs */
.metric-card{padding:16px;min-height:116px}
.metric-icon{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:#EEF2FF;font-size:1.02rem;box-shadow:inset 0 1px 0 #fff}
.metric-label{font-size:.65rem;color:#7A8697;font-weight:850;text-transform:uppercase;letter-spacing:.075em;margin-top:10px}
.metric-value{font-size:1.55rem;color:#17263A;font-weight:900;letter-spacing:-.045em;margin-top:2px}
.metric-foot{font-size:.71rem;color:#788699;margin-top:5px;line-height:1.35}

/* SATISFACCIÓN DE LAS 4 DIMENSIONES */
.dim-card{padding:17px;min-height:210px;position:relative;overflow:hidden}
.dim-card:before{content:"";position:absolute;left:0;top:0;width:100%;height:4px;background:var(--dim)}
.dim-head{display:flex;align-items:center;justify-content:space-between;gap:8px}
.dim-id{display:flex;align-items:center;gap:7px}
.dim-icon{font-size:1rem}
.dim-code{font-size:.7rem;font-weight:900;color:var(--dim);background:var(--soft);padding:5px 8px;border-radius:9px}
.status-badge{display:flex;align-items:center;gap:5px;padding:5px 7px;border-radius:999px;background:var(--status-soft);color:var(--status-dark);font-size:.64rem;font-weight:850;white-space:nowrap}
.dim-score-row{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:17px}
.dim-score{font-size:clamp(1.75rem,3vw,2.15rem);font-weight:900;color:#17263A;letter-spacing:-.055em;line-height:1}
.dim-caption{font-size:.66rem;color:#7B8797;font-weight:750;margin-top:4px;text-transform:uppercase;letter-spacing:.04em}
.mini-traffic{display:flex;gap:4px;padding:6px 7px;border-radius:999px;background:linear-gradient(145deg,#273440,#10161C);box-shadow:4px 5px 10px rgba(15,23,42,.18),inset 0 1px 0 rgba(255,255,255,.08)}
.mini-light{width:10px;height:10px;border-radius:50%;opacity:.16;box-shadow:inset 1px 1px 2px rgba(255,255,255,.24)}
.mini-light.red{background:#EF4444}.mini-light.amber{background:#F59E0B}.mini-light.green{background:#22C55E}
.mini-light.on{opacity:1}.mini-light.red.on{box-shadow:0 0 9px rgba(239,68,68,.85)}.mini-light.amber.on{box-shadow:0 0 9px rgba(245,158,11,.85)}.mini-light.green.on{box-shadow:0 0 9px rgba(34,197,94,.85)}
.dim-name{font-size:.82rem;font-weight:850;color:#25384D;line-height:1.32;margin-top:14px;min-height:2.15em}
.dim-foot{display:flex;justify-content:space-between;gap:8px;align-items:end;margin-top:12px;padding-top:10px;border-top:1px solid #EDF0F4}
.dim-range{font-size:.67rem;color:#758294}.dim-gap{font-size:.67rem;color:#4D5D70;font-weight:750;text-align:right}

/* INSIGHTS */
.insight-card{padding:16px;border-left:4px solid var(--accent);min-height:116px}
.insight-kicker{font-size:.64rem;font-weight:850;text-transform:uppercase;letter-spacing:.08em;color:#7A8798}
.insight-title{font-size:.9rem;font-weight:850;color:#1D3044;margin-top:6px;line-height:1.25}
.insight-text{font-size:.74rem;color:#687688;margin-top:6px;line-height:1.42}

/* PLOTS / TABLAS */
div[data-testid="stPlotlyChart"]{background:linear-gradient(145deg,#FFFFFF,#FBFCFE);border:1px solid #E6EAF0;border-radius:19px;padding:7px 7px 1px;box-shadow:0 12px 28px rgba(25,39,62,.055);overflow:hidden}
div[data-testid="stDataFrame"]{border:1px solid #E6EAF0;border-radius:15px;overflow:hidden}
[data-testid="stMetric"]{background:#fff;border:1px solid #E6EAF0;border-radius:16px;padding:12px 14px;box-shadow:0 8px 20px rgba(25,39,62,.05)}

/* TABS: scroll horizontal en móvil, sin cortar */
.stTabs [data-baseweb="tab-list"]{gap:7px;background:#EDF1F6;padding:5px;border-radius:15px;width:100%;overflow-x:auto;white-space:nowrap;scrollbar-width:thin}
.stTabs [data-baseweb="tab"]{height:39px;border-radius:11px;padding:0 15px;color:#536273;font-weight:750;font-size:.8rem;flex:0 0 auto}
.stTabs [aria-selected="true"]{background:#fff!important;color:#17304B!important;box-shadow:0 5px 12px rgba(15,23,42,.10)!important}
.stTabs [data-baseweb="tab-highlight"]{display:none}

/* SELECT */
div[data-testid="stSelectbox"]{max-width:760px}
div[data-testid="stSelectbox"]>div>div{border-radius:14px!important}

/* METODOLOGÍA */
.method-card{padding:18px;min-height:180px}
.method-icon{font-size:1.15rem;margin-bottom:8px}.method-title{font-size:.9rem;font-weight:850;color:#193047}.method-text{font-size:.76rem;color:#687789;line-height:1.48;margin-top:7px}
.rule-card{padding:13px}.rule-dot{width:12px;height:12px;border-radius:50%;margin-bottom:7px}.rule-name{font-size:.75rem;font-weight:850;color:#243A4F}.rule-range{font-size:.7rem;color:#788698;margin-top:4px}

/* TABLET */
@media(max-width:1100px){
  .top-grid{grid-template-columns:1fr}
  .dim-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .signal-card{min-height:0}
}

/* CELULAR */
@media(max-width:700px){
  .block-container{padding:.65rem .72rem 2.2rem}
  .hero{border-radius:20px;padding:20px 17px}
  .hero-chip{font-size:.67rem;padding:6px 8px}
  .section-head{align-items:flex-start;margin:1.15rem 0 .62rem}
  .section-note{display:none}
  .kpi-grid,.dim-grid,.insight-grid,.method-grid,.rule-grid{grid-template-columns:1fr}
  .signal-stage{grid-template-columns:84px minmax(0,1fr);gap:12px;padding:14px 12px}
  .traffic{width:67px;padding:8px 7px;border-radius:22px}
  .lamp{width:40px;height:40px;margin:7px auto}
  .signal-card{padding:15px}
  .scale-labels{font-size:.53rem}
  .dim-card{min-height:0}
  .dim-name{min-height:0}
  .stTabs [data-baseweb="tab"]{padding:0 12px;font-size:.75rem}
  div[data-testid="stPlotlyChart"]{border-radius:15px;padding:3px 2px 0}
}
</style>
"""
)


# ==============================================================
# LÓGICA ESTADÍSTICA
# ==============================================================
def level_for(p: float) -> str:
    if pd.isna(p) or p < 0.60:
        return "Insatisfactorio"
    if p < 0.75:
        return "Regular"
    if p < 0.90:
        return "Satisfactorio"
    return "Muy satisfactorio"


def pct(p: float, digits: int = 1) -> str:
    return "—" if pd.isna(p) else f"{p * 100:.{digits}f}%"


def require_columns(df: pd.DataFrame) -> None:
    required = {f"P{i}" for i in range(1, 18)}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(missing))


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    require_columns(df)
    for i in range(1, 18):
        df[f"P{i}"] = pd.to_numeric(df[f"P{i}"], errors="coerce")

    # Misma lógica estadística del instrumento:
    # promedio de las 4 preguntas de la dimensión >= 4 => satisfecho.
    for code, info in DIMENSIONS.items():
        avg_col = f"{code}_Promedio_calc"
        sat_col = f"{code}_Satisfecho_calc"
        df[avg_col] = df[info["items"]].mean(axis=1, skipna=True)
        df[sat_col] = (df[avg_col] >= 4).astype(float)

    # P17 es satisfacción general independiente.
    df["Global_Satisfecho_calc"] = (df["P17"] >= 4).astype(float)
    return df


@st.cache_data(show_spinner=False)
def load_data(path: str, mtime: float) -> pd.DataFrame:
    return prepare_data(pd.read_excel(path, sheet_name=SHEET_NAME))


def dim_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, info in DIMENSIONS.items():
        sat = float(df[f"{code}_Satisfecho_calc"].mean())
        avg = float(df[f"{code}_Promedio_calc"].mean())
        level = level_for(sat)
        rows.append({
            "Código": code,
            "Dimensión": info["name"],
            "Satisfacción": sat,
            "Promedio Likert": avg,
            "Nivel": level,
            "Intervalo": STATUS[level]["range"],
            "Brecha a 75%": max(0.0, TARGET - sat),
        })
    return pd.DataFrame(rows)


def item_summary(df: pd.DataFrame, items: list[str]) -> pd.DataFrame:
    rows = []
    for item in items:
        s = df[item].dropna()
        code = "D" + str(((int(item[1:]) - 1) // 4) + 1) if item != "P17" else "P17"
        rows.append({
            "Ítem": item,
            "Dimensión": code,
            "Pregunta": ITEM_TEXT[item],
            "Promedio": float(s.mean()),
            "Favorable": float((s >= 4).mean()),
            "Neutral": float((s == 3).mean()),
            "Desfavorable": float((s <= 2).mean()),
        })
    return pd.DataFrame(rows)


# ==============================================================
# COMPONENTES HTML
# ==============================================================
def section_head(kicker: str, title: str, note: str = "") -> None:
    st.html(
        f'<div class="section-head"><div><div class="section-kicker">{escape(kicker)}</div>'
        f'<div class="section-title">{escape(title)}</div></div>'
        f'<div class="section-note">{escape(note)}</div></div>'
    )


def hero(n: int) -> None:
    st.html(
        f'''<div class="hero">
          <div class="hero-kicker">Universidad Nacional de Trujillo · tablero ejecutivo</div>
          <div class="hero-title">Satisfacción estudiantil</div>
          <div class="hero-sub">Panel responsive para lectura rápida de la satisfacción general, las cuatro dimensiones y los aspectos prioritarios de mejora.</div>
          <div class="hero-row">
            <span class="hero-chip">● Base institucional integrada</span>
            <span class="hero-chip">👥 {n:,} estudiantes</span>
            <span class="hero-chip">🎯 Meta institucional 75%</span>
            <span class="hero-chip">📱 Adaptable a celular, tablet y PC</span>
          </div>
        </div>'''
    )


def traffic_html(value: float) -> str:
    level = level_for(value)
    meta = STATUS[level]
    signal = meta["signal"]
    return f'''<div class="card signal-card">
      <div class="signal-label">Estado institucional</div>
      <div class="signal-title">Satisfacción general · P17</div>
      <div class="signal-stage">
        <div class="traffic-wrap"><div class="traffic" aria-label="Semáforo institucional">
          <div class="lamp red{' on' if signal == 'red' else ''}"></div>
          <div class="lamp amber{' on' if signal == 'amber' else ''}"></div>
          <div class="lamp green{' on' if signal == 'green' else ''}"></div>
        </div></div>
        <div>
          <div class="signal-score">{pct(value)}</div>
          <div class="signal-level" style="color:{meta['color']}">{meta['emoji']} {escape(level)}</div>
          <div class="signal-range">Intervalo: {escape(meta['range'])}<br>P17 = 4 o 5 se considera satisfecho.</div>
          <div class="signal-action">{escape(meta['action'])}</div>
        </div>
      </div>
      <div class="scale"><span></span><span></span><span></span><span></span></div>
      <div class="scale-labels"><div>0–&lt;60<br>Insatisf.</div><div>60–&lt;75<br>Regular</div><div>75–&lt;90<br>Satisf.</div><div>90–100<br>Muy sat.</div></div>
    </div>'''


def metric_html(icon: str, label: str, value: str, foot: str) -> str:
    return f'''<div class="metric-card">
      <div class="metric-icon">{icon}</div>
      <div class="metric-label">{escape(label)}</div>
      <div class="metric-value">{escape(value)}</div>
      <div class="metric-foot">{foot}</div>
    </div>'''


def mini_traffic(level: str) -> str:
    signal = STATUS[level]["signal"]
    return f'''<span class="mini-traffic" aria-label="{escape(level)}">
      <span class="mini-light red{' on' if signal == 'red' else ''}"></span>
      <span class="mini-light amber{' on' if signal == 'amber' else ''}"></span>
      <span class="mini-light green{' on' if signal == 'green' else ''}"></span>
    </span>'''


def dimension_html(code: str, sat: float) -> str:
    info = DIMENSIONS[code]
    level = level_for(sat)
    meta = STATUS[level]
    gap = max(0.0, TARGET - sat)
    gap_text = "Meta alcanzada" if gap == 0 else f"Faltan {gap * 100:.1f} pp para 75%"
    return f'''<div class="dim-card" style="--dim:{info['color']};--soft:{info['soft']};--status-soft:{meta['soft']};--status-dark:{meta['dark']}">
      <div class="dim-head">
        <div class="dim-id"><span class="dim-icon">{info['icon']}</span><span class="dim-code">{code}</span></div>
        <div class="status-badge">{meta['emoji']} {escape(level)}</div>
      </div>
      <div class="dim-score-row">
        <div><div class="dim-score">{pct(sat)}</div><div class="dim-caption">Satisfacción de la dimensión</div></div>
        {mini_traffic(level)}
      </div>
      <div class="dim-name">{escape(info['name'])}</div>
      <div class="dim-foot"><div class="dim-range">{escape(meta['range'])}</div><div class="dim-gap">{escape(gap_text)}</div></div>
    </div>'''


def insight_html(kicker: str, title: str, text: str, accent: str) -> str:
    return f'''<div class="insight-card" style="--accent:{accent}">
      <div class="insight-kicker">{escape(kicker)}</div>
      <div class="insight-title">{escape(title)}</div>
      <div class="insight-text">{text}</div>
    </div>'''


# ==============================================================
# GRÁFICOS RESPONSIVE
# ==============================================================
def base_plot(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=28, b=34),
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Aptos, Segoe UI, Arial", color="#566477", size=11),
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#172B3A", bordercolor="#D8E0E8"),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0, bgcolor="rgba(255,255,255,.75)"),
    )
    fig.update_xaxes(automargin=True, gridcolor="#EBEFF4", zeroline=False)
    fig.update_yaxes(automargin=True, gridcolor="rgba(0,0,0,0)", zeroline=False)
    return fig


def dimension_chart(summary: pd.DataFrame) -> go.Figure:
    d = summary.sort_values("Código").copy()
    colors = [STATUS[x]["color"] for x in d["Nivel"]]
    fig = go.Figure()
    fig.add_hrect(y0=0.00, y1=0.60, fillcolor="rgba(217,54,62,.045)", line_width=0, layer="below")
    fig.add_hrect(y0=0.60, y1=0.75, fillcolor="rgba(229,154,24,.055)", line_width=0, layer="below")
    fig.add_hrect(y0=0.75, y1=0.90, fillcolor="rgba(28,155,98,.045)", line_width=0, layer="below")
    fig.add_hrect(y0=0.90, y1=1.00, fillcolor="rgba(8,122,87,.060)", line_width=0, layer="below")
    fig.add_trace(go.Bar(
        x=d["Código"], y=d["Satisfacción"], marker_color=colors,
        text=d["Satisfacción"].map(lambda x: f"{x*100:.1f}%"), textposition="outside",
        customdata=d[["Dimensión", "Nivel", "Intervalo", "Promedio Likert", "Brecha a 75%"]],
        hovertemplate=(
            "<b>%{x} · %{customdata[0]}</b><br>Satisfacción: %{y:.2%}<br>Nivel: %{customdata[1]}"
            "<br>Intervalo: %{customdata[2]}<br>Promedio Likert: %{customdata[3]:.2f}"
            "<br>Brecha a 75%: %{customdata[4]:.2%}<extra></extra>"
        ),
    ))
    fig.add_hline(y=.75, line_dash="dash", line_width=1.5, line_color="#0F766E")
    fig.add_annotation(x=3.45, y=.765, text="Meta 75%", showarrow=False, font=dict(size=10, color="#0F766E"))
    fig.update_yaxes(tickformat=".0%", range=[0,1.06], title=None)
    fig.update_xaxes(title=None, tickfont=dict(size=12))
    fig.update_layout(showlegend=False)
    return base_plot(fig, 390)


def item_bar(items: pd.DataFrame, height: int | None = None) -> go.Figure:
    d = items.sort_values("Favorable", ascending=True).copy()
    color_map = {c: DIMENSIONS[c]["color"] for c in DIMENSIONS}
    fig = go.Figure(go.Bar(
        x=d["Favorable"], y=d["Ítem"], orientation="h",
        marker_color=[color_map.get(x, "#3157D5") for x in d["Dimensión"]],
        text=d["Favorable"].map(lambda x: f"{x*100:.1f}%"), textposition="outside",
        customdata=d[["Dimensión", "Pregunta", "Promedio", "Neutral", "Desfavorable"]],
        hovertemplate=(
            "<b>%{y} · %{customdata[0]}</b><br>%{customdata[1]}"
            "<br>Favorable: %{x:.2%}<br>Neutral: %{customdata[3]:.2%}"
            "<br>Desfavorable: %{customdata[4]:.2%}<br>Promedio: %{customdata[2]:.2f}<extra></extra>"
        ),
    ))
    fig.update_xaxes(tickformat=".0%", range=[0,1.08], title=None)
    fig.update_yaxes(title=None, tickfont=dict(size=11))
    fig.update_layout(showlegend=False)
    return base_plot(fig, height or max(330, 33 * len(d) + 110))


def likert_chart(df: pd.DataFrame, items: list[str]) -> go.Figure:
    rows = []
    for item in items:
        s = df[item].dropna()
        if len(s) == 0:
            continue
        rows.extend([
            {"Ítem": item, "Categoría": "Desfavorable (1–2)", "pct": float((s <= 2).mean()), "Pregunta": ITEM_TEXT[item]},
            {"Ítem": item, "Categoría": "Neutral (3)", "pct": float((s == 3).mean()), "Pregunta": ITEM_TEXT[item]},
            {"Ítem": item, "Categoría": "Favorable (4–5)", "pct": float((s >= 4).mean()), "Pregunta": ITEM_TEXT[item]},
        ])
    d = pd.DataFrame(rows)
    fig = go.Figure()
    for cat in ["Desfavorable (1–2)", "Neutral (3)", "Favorable (4–5)"]:
        x = d[d["Categoría"] == cat]
        fig.add_trace(go.Bar(
            x=x["pct"], y=x["Ítem"], name=cat, orientation="h",
            marker_color=LIKERT[cat], customdata=x[["Pregunta"]],
            hovertemplate=f"<b>%{{y}}</b><br>%{{customdata[0]}}<br>{cat}: %{{x:.2%}}<extra></extra>",
        ))
    fig.update_layout(barmode="stack")
    fig.update_xaxes(tickformat=".0%", range=[0,1], title=None)
    fig.update_yaxes(title=None, autorange="reversed")
    return base_plot(fig, max(330, 37 * len(items) + 110))


# ==============================================================
# CARGA AUTOMÁTICA — NO HAY BOTÓN PARA SUBIR EXCEL
# ==============================================================
if not DATA_FILE.exists():
    st.error("No se encontró 'basededatos.xlsx'. Debe estar en la misma carpeta que app.py.")
    st.stop()

try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"No pude leer basededatos.xlsx: {exc}")
    st.stop()

summary = dim_summary(df)
global_sat = float(df["Global_Satisfecho_calc"].mean())
items16 = item_summary(df, [f"P{i}" for i in range(1, 17)])
priority = summary.sort_values("Satisfacción").iloc[0]
strongest = summary.sort_values("Satisfacción", ascending=False).iloc[0]
meet = int((summary["Satisfacción"] >= TARGET).sum())

hero(len(df))

# Navegación horizontal. En celular se desplaza horizontalmente sin cortar contenido.
tab_resumen, tab_dim, tab_prior, tab_method = st.tabs([
    "◉ Resumen",
    "▦ Dimensiones",
    "⚑ Prioridades",
    "ⓘ Metodología",
])


# ==============================================================
# 1. RESUMEN EJECUTIVO
# ==============================================================
with tab_resumen:
    section_head("Panorama", "Estado general", "Una lectura clara antes de entrar al detalle.")

    top_html = '<div class="top-grid">' + traffic_html(global_sat) + '<div>'
    top_html += '<div class="kpi-grid">'
    top_html += metric_html("👥", "Estudiantes", f"{len(df):,}", "Registros analizados en la base institucional.")
    top_html += metric_html("🎯", "Dimensiones en meta", f"{meet} de 4", "Meta institucional: satisfacción ≥ 75%.")
    top_html += metric_html("⚠️", "Prioridad", str(priority["Código"]), f"{pct(priority['Satisfacción'])} · {escape(str(priority['Nivel']))}")
    top_html += '</div>'
    top_html += '<div class="insight-card" style="--accent:#3157D5"><div class="insight-kicker">Lectura inmediata</div>'
    top_html += f'<div class="insight-title">La satisfacción general es {pct(global_sat)}</div>'
    top_html += f'<div class="insight-text">El resultado P17 se ubica en nivel <b>{escape(level_for(global_sat))}</b>. La dimensión que requiere atención primero es <b>{escape(str(priority["Código"]))}</b>.</div></div>'
    top_html += '</div></div>'
    st.html(top_html)

    # Esta sección muestra explícitamente la satisfacción de D1, D2, D3 y D4.
    section_head("Satisfacción dimensional", "Las cuatro dimensiones", "Cada tarjeta muestra porcentaje, nivel, semáforo e intervalo.")
    dims_html = '<div class="dim-grid">'
    for code in DIMENSIONS:
        sat = float(summary.loc[summary["Código"] == code, "Satisfacción"].iloc[0])
        dims_html += dimension_html(code, sat)
    dims_html += '</div>'
    st.html(dims_html)

    section_head("Lectura ejecutiva", "Tres mensajes para la toma de decisiones", "Priorización, fortaleza y satisfacción general.")
    insight_grid = '<div class="insight-grid">'
    insight_grid += insight_html(
        "Prioridad",
        f"{priority['Código']} · {DIMENSIONS[str(priority['Código'])]['short']}",
        f"Satisfacción: <b>{pct(priority['Satisfacción'])}</b>. " + (f"Brecha hasta 75%: <b>{priority['Brecha a 75%']*100:.1f} pp</b>." if priority["Brecha a 75%"] > 0 else "Ya alcanza la meta institucional."),
        "#D9363E" if priority["Satisfacción"] < TARGET else "#1C9B62",
    )
    insight_grid += insight_html(
        "Fortaleza relativa",
        f"{strongest['Código']} · {DIMENSIONS[str(strongest['Código'])]['short']}",
        f"Es la dimensión con mayor satisfacción: <b>{pct(strongest['Satisfacción'])}</b>, nivel <b>{escape(str(strongest['Nivel']))}</b>.",
        "#1C9B62",
    )
    glevel = level_for(global_sat)
    insight_grid += insight_html(
        "Satisfacción general",
        f"P17 · {glevel}",
        f"Resultado institucional: <b>{pct(global_sat)}</b>. Intervalo del semáforo: <b>{STATUS[glevel]['range']}</b>.",
        STATUS[glevel]["color"],
    )
    insight_grid += '</div>'
    st.html(insight_grid)

    section_head("Comparación", "D1, D2, D3 y D4", "Gráfico compacto para no cortar textos en pantallas pequeñas.")
    st.plotly_chart(dimension_chart(summary), use_container_width=True, config=PLOT_CONFIG)

    section_head("Detalle compacto", "Matriz de situación", "En móvil la tabla puede desplazarse horizontalmente sin romper el dashboard.")
    compact = summary[["Código", "Satisfacción", "Nivel", "Intervalo", "Brecha a 75%"]].copy()
    compact.insert(1, "Semáforo", compact["Nivel"].map(lambda x: STATUS[x]["emoji"]))
    compact["Satisfacción"] = compact["Satisfacción"].map(lambda x: f"{x*100:.1f}%")
    compact["Brecha a 75%"] = compact["Brecha a 75%"].map(lambda x: "—" if x <= 0 else f"{x*100:.1f} pp")
    st.dataframe(compact, use_container_width=True, hide_index=True)


# ==============================================================
# 2. DIMENSIONES
# ==============================================================
with tab_dim:
    section_head("Exploración", "Profundizar en una dimensión", "Seleccione D1, D2, D3 o D4; los gráficos usan códigos cortos para verse bien en celular.")

    selected = st.selectbox(
        "Dimensión",
        list(DIMENSIONS.keys()),
        format_func=lambda x: f"{x} · {DIMENSIONS[x]['name']}",
        label_visibility="collapsed",
    )
    info = DIMENSIONS[selected]
    row = summary.loc[summary["Código"] == selected].iloc[0]
    dim_items = item_summary(df, info["items"])
    low_item = dim_items.sort_values("Favorable").iloc[0]
    high_item = dim_items.sort_values("Favorable", ascending=False).iloc[0]

    detail_html = '<div class="dim-grid">'
    detail_html += dimension_html(selected, float(row["Satisfacción"]))
    detail_html += metric_html("★", "Promedio Likert", f"{row['Promedio Likert']:.2f}", "Promedio de las cuatro preguntas de la dimensión.")
    detail_html += metric_html("↓", "Aspecto más débil", str(low_item["Ítem"]), f"{pct(low_item['Favorable'])} favorable")
    detail_html += metric_html("↑", "Aspecto más fuerte", str(high_item["Ítem"]), f"{pct(high_item['Favorable'])} favorable")
    detail_html += '</div>'
    st.html(detail_html)
    st.info(info["desc"], icon="ℹ️")

    section_head("Ítems", "Valoración favorable", "En el eje solo aparece P1, P2… para evitar cortes; la pregunta completa aparece al tocar o pasar el cursor.")
    st.plotly_chart(item_bar(dim_items, 350), use_container_width=True, config=PLOT_CONFIG)

    qtable = dim_items[["Ítem", "Pregunta", "Favorable", "Neutral", "Desfavorable"]].copy()
    for col in ["Favorable", "Neutral", "Desfavorable"]:
        qtable[col] = qtable[col].map(lambda x: f"{x*100:.1f}%")
    st.dataframe(qtable, use_container_width=True, hide_index=True)

    section_head("Distribución Likert", "Desfavorable, neutral y favorable", "El gráfico usa P1–P4, P5–P8, etc.; el texto completo queda en la interacción.")
    st.plotly_chart(likert_chart(df, info["items"]), use_container_width=True, config=PLOT_CONFIG)


# ==============================================================
# 3. PRIORIDADES
# ==============================================================
with tab_prior:
    section_head("Priorización", "Ranking de P1 a P16", "Sin textos largos en el eje: en celular no se corta y la pregunta completa aparece en el tooltip.")
    ranked = items16.sort_values("Favorable", ascending=True).copy()
    st.plotly_chart(item_bar(ranked, 660), use_container_width=True, config=PLOT_CONFIG)

    section_head("Top 5", "Aspectos con menor valoración favorable", "Para discutir prioridades concretas sin confundirlas con la satisfacción oficial de la dimensión.")
    top5 = ranked.head(5).copy()
    top5["Favorable"] = top5["Favorable"].map(lambda x: f"{x*100:.1f}%")
    top5["Desfavorable"] = top5["Desfavorable"].map(lambda x: f"{x*100:.1f}%")
    top5["Promedio"] = top5["Promedio"].map(lambda x: f"{x:.2f}")
    st.dataframe(top5[["Ítem", "Dimensión", "Pregunta", "Favorable", "Desfavorable", "Promedio"]], use_container_width=True, hide_index=True)


# ==============================================================
# 4. METODOLOGÍA
# ==============================================================
with tab_method:
    section_head("Metodología", "Cómo se calcula", "Se conserva la lógica estadística del instrumento; solo cambia la experiencia visual.")
    st.html('''<div class="method-grid">
      <div class="method-card"><div class="method-icon">▦</div><div class="method-title">Satisfacción D1–D4</div><div class="method-text">Cada dimensión contiene <b>4 preguntas</b>. Para cada estudiante se calcula el promedio de sus cuatro respuestas. Si el promedio es <b>≥ 4</b>, se clasifica como satisfecho en esa dimensión.</div></div>
      <div class="method-card"><div class="method-icon">◎</div><div class="method-title">Satisfacción general P17</div><div class="method-text">P17 se interpreta de forma independiente. Respuesta <b>4 o 5 = satisfecho</b>; respuestas 1, 2 o 3 = no satisfecho. P17 no se obtiene promediando D1–D4.</div></div>
      <div class="method-card"><div class="method-icon">▥</div><div class="method-title">Ítems P1–P16</div><div class="method-text"><b>Desfavorable:</b> 1–2. <b>Neutral:</b> 3. <b>Favorable:</b> 4–5. Los porcentajes por ítem se usan para identificar aspectos concretos de mejora.</div></div>
    </div>''')

    section_head("Semáforo", "Escala institucional", "El color siempre aparece acompañado del nivel y del intervalo.")
    st.html('''<div class="rule-grid">
      <div class="rule-card"><div class="rule-dot" style="background:#D9363E;box-shadow:0 0 10px rgba(217,54,62,.45)"></div><div class="rule-name">🔴 Insatisfactorio</div><div class="rule-range">0% a &lt;60%</div></div>
      <div class="rule-card"><div class="rule-dot" style="background:#E59A18;box-shadow:0 0 10px rgba(229,154,24,.45)"></div><div class="rule-name">🟠 Regular</div><div class="rule-range">60% a &lt;75%</div></div>
      <div class="rule-card"><div class="rule-dot" style="background:#1C9B62;box-shadow:0 0 10px rgba(28,155,98,.45)"></div><div class="rule-name">🟢 Satisfactorio</div><div class="rule-range">75% a &lt;90%</div></div>
      <div class="rule-card"><div class="rule-dot" style="background:#087A57;box-shadow:0 0 10px rgba(8,122,87,.45)"></div><div class="rule-name">🟢 Muy satisfactorio</div><div class="rule-range">90% a 100%</div></div>
    </div>''')
