from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==============================================================
# CONFIGURACIÓN
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
        "color": "#2F6BFF",
        "soft": "#EAF0FF",
        "desc": "Pertinencia curricular, plan de estudios, carga académica y coherencia de las asignaturas.",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "short": "Docencia",
        "items": ["P5", "P6", "P7", "P8"],
        "color": "#6C5CE7",
        "soft": "#F0EDFF",
        "desc": "Dominio docente, metodología, participación del estudiante y retroalimentación.",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "short": "Servicios y gestión",
        "items": ["P9", "P10", "P11", "P12"],
        "color": "#D97706",
        "soft": "#FFF4E5",
        "desc": "Trámites, información académica, infraestructura, recursos y aseguramiento de la calidad.",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "short": "Formación integral",
        "items": ["P13", "P14", "P15", "P16"],
        "color": "#0F9D7A",
        "soft": "#E8F7F2",
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
        "color": "#DC2626",
        "dark": "#991B1B",
        "soft": "#FEF2F2",
        "range": "0% a <60%",
        "signal": "red",
        "icon": "●",
        "action": "Atención prioritaria",
    },
    "Regular": {
        "color": "#F59E0B",
        "dark": "#B45309",
        "soft": "#FFFBEB",
        "range": "60% a <75%",
        "signal": "amber",
        "icon": "●",
        "action": "Requiere seguimiento",
    },
    "Satisfactorio": {
        "color": "#16A34A",
        "dark": "#166534",
        "soft": "#F0FDF4",
        "range": "75% a <90%",
        "signal": "green",
        "icon": "●",
        "action": "Cumple el estándar",
    },
    "Muy satisfactorio": {
        "color": "#059669",
        "dark": "#065F46",
        "soft": "#ECFDF5",
        "range": "90% a 100%",
        "signal": "green",
        "icon": "★",
        "action": "Desempeño destacado",
    },
}

LIKERT = {
    "Desfavorable (1–2)": "#E45757",
    "Neutral (3)": "#A7B0BE",
    "Favorable (4–5)": "#1F9D78",
}


# ==============================================================
# CSS — ARQUITECTURA VISUAL NUEVA
# ==============================================================
st.html(
    """
<style>
:root{
  --ink:#132238;
  --muted:#667085;
  --line:#E7ECF2;
  --paper:#FFFFFF;
  --bg:#F4F7FB;
  --navy:#0A1E35;
  --navy2:#123B5B;
  --blue:#2F6BFF;
}
html,body,[class*="css"]{font-family:"Aptos","Segoe UI Variable","Segoe UI",Inter,Arial,sans-serif;}
.stApp{
  background:
    radial-gradient(circle at 10% -10%,rgba(47,107,255,.10),transparent 34rem),
    radial-gradient(circle at 98% 8%,rgba(15,157,122,.08),transparent 28rem),
    linear-gradient(180deg,#F9FBFE 0%,var(--bg) 100%);
  color:var(--ink);
}
.block-container{max-width:1500px;padding-top:1.15rem;padding-bottom:3.5rem;}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:rgba(249,251,254,.84);backdrop-filter:blur(12px);}

/* HERO */
.hero-shell{
  position:relative;overflow:hidden;border-radius:26px;padding:27px 30px 25px;
  background:linear-gradient(118deg,#081B30 0%,#103A59 58%,#0C6670 125%);
  color:white;border:1px solid rgba(255,255,255,.08);
  box-shadow:0 24px 60px rgba(10,30,53,.20),inset 0 1px 0 rgba(255,255,255,.10);
}
.hero-shell:before{content:"";position:absolute;right:-65px;top:-115px;width:330px;height:330px;border-radius:50%;border:58px solid rgba(255,255,255,.045);}
.hero-shell:after{content:"";position:absolute;right:190px;bottom:-145px;width:250px;height:250px;border-radius:50%;background:radial-gradient(circle,rgba(73,194,184,.18),transparent 67%);}
.hero-kicker{font-size:.72rem;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:#9ED9E2;margin-bottom:7px;}
.hero-title{font-size:2.05rem;font-weight:800;letter-spacing:-.045em;line-height:1.08;margin:0 0 8px;color:white;}
.hero-sub{font-size:.94rem;color:#D6E6EE;max-width:900px;line-height:1.5;}
.hero-meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;position:relative;z-index:1;}
.hero-chip{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14);font-size:.75rem;color:#EFF7FA;}

/* TÍTULOS */
.section-head{display:flex;align-items:end;justify-content:space-between;gap:16px;margin:1.35rem 0 .72rem;}
.section-kicker{font-size:.67rem;color:#2F6BFF;font-weight:850;text-transform:uppercase;letter-spacing:.12em;margin-bottom:3px;}
.section-title{font-size:1.22rem;font-weight:800;letter-spacing:-.025em;color:#172B3A;line-height:1.2;}
.section-note{font-size:.78rem;color:#7A8797;text-align:right;max-width:460px;}

/* TARJETAS GENERALES */
.glass-card,.metric-card,.dim-card,.insight-card,.method-card,.table-shell{
  background:linear-gradient(145deg,#FFFFFF 0%,#FBFCFE 62%,#F5F8FB 100%);
  border:1px solid var(--line);border-radius:20px;
  box-shadow:0 16px 38px rgba(19,34,56,.075),0 3px 8px rgba(19,34,56,.035),inset 0 1px 0 rgba(255,255,255,.95);
}
.metric-card,.dim-card,.insight-card{transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;}
.metric-card:hover,.dim-card:hover,.insight-card:hover{transform:translateY(-3px);box-shadow:0 24px 48px rgba(19,34,56,.105),0 5px 10px rgba(19,34,56,.045);border-color:#D7DEE8;}

/* CONTROL CENTRAL / SEMÁFORO */
.command-card{height:100%;min-height:330px;padding:20px 20px 18px;position:relative;overflow:hidden;}
.command-card:after{content:"";position:absolute;width:190px;height:190px;border-radius:50%;right:-90px;bottom:-90px;background:radial-gradient(circle,rgba(47,107,255,.08),transparent 68%);}
.command-label{font-size:.68rem;font-weight:850;letter-spacing:.12em;text-transform:uppercase;color:#718096;}
.command-title{font-size:1rem;font-weight:800;color:#1B2D40;margin-top:4px;}
.signal-stage{display:grid;grid-template-columns:112px minmax(0,1fr);gap:18px;align-items:center;margin-top:15px;padding:17px;border-radius:18px;background:linear-gradient(145deg,#0A1825,#122D43);border:1px solid rgba(255,255,255,.07);box-shadow:0 16px 30px rgba(8,24,37,.22),inset 0 1px 0 rgba(255,255,255,.07);}
.traffic-shell{width:78px;margin:auto;padding:10px 9px;border-radius:25px;background:linear-gradient(145deg,#1C2732,#080C10);border:2px solid #30404F;box-shadow:10px 12px 22px rgba(0,0,0,.32),inset 6px 6px 12px rgba(255,255,255,.045),inset -6px -7px 13px rgba(0,0,0,.48);position:relative;}
.traffic-shell:before{content:"🚦";position:absolute;font-size:1.05rem;right:-13px;top:-15px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.25));}
.lamp{width:48px;height:48px;border-radius:50%;margin:8px auto;position:relative;opacity:.18;box-shadow:inset 8px 9px 13px rgba(255,255,255,.07),inset -9px -10px 15px rgba(0,0,0,.45),0 3px 5px rgba(0,0,0,.50);}
.lamp:after{content:"";position:absolute;width:14px;height:9px;border-radius:50%;left:10px;top:7px;background:rgba(255,255,255,.30);transform:rotate(-18deg);}
.lamp.red{background:#EF4444}.lamp.amber{background:#F59E0B}.lamp.green{background:#22C55E}
.lamp.active{opacity:1;animation:pulseLamp 2.1s ease-in-out infinite;}
.lamp.red.active{box-shadow:0 0 11px #EF4444,0 0 33px rgba(239,68,68,.70),inset 8px 9px 13px rgba(255,255,255,.30),inset -9px -10px 15px rgba(80,0,0,.35);}
.lamp.amber.active{box-shadow:0 0 11px #F59E0B,0 0 33px rgba(245,158,11,.70),inset 8px 9px 13px rgba(255,255,255,.30),inset -9px -10px 15px rgba(86,51,0,.35);}
.lamp.green.active{box-shadow:0 0 11px #22C55E,0 0 33px rgba(34,197,94,.68),inset 8px 9px 13px rgba(255,255,255,.30),inset -9px -10px 15px rgba(0,68,35,.35);}
@keyframes pulseLamp{0%,100%{transform:scale(1)}50%{transform:scale(1.045)}}
.signal-copy .big-score{font-size:2.55rem;font-weight:850;color:#FFFFFF;letter-spacing:-.055em;line-height:1;}
.signal-copy .big-level{font-size:1rem;font-weight:800;margin-top:7px;}
.signal-copy .big-range{font-size:.76rem;color:#C8D8E2;margin-top:5px;line-height:1.35;}
.signal-copy .big-action{display:inline-flex;margin-top:10px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);border-radius:999px;padding:6px 9px;font-size:.71rem;color:#F3F8FA;}
.scale-zone{margin-top:14px;}
.scale-track{height:12px;border-radius:999px;display:grid;grid-template-columns:60fr 15fr 15fr 10fr;overflow:hidden;border:1px solid #E6EBF0;box-shadow:inset 0 1px 2px rgba(15,23,42,.08);}
.scale-track span:nth-child(1){background:#EF4444}.scale-track span:nth-child(2){background:#F59E0B}.scale-track span:nth-child(3){background:#22C55E}.scale-track span:nth-child(4){background:#059669}
.scale-legend{display:grid;grid-template-columns:60fr 15fr 15fr 10fr;gap:0;margin-top:5px;font-size:.61rem;color:#748195;line-height:1.15;}
.scale-legend div{padding-right:4px;}

/* MÉTRICAS */
.metric-card{padding:16px 17px;min-height:118px;position:relative;overflow:hidden;}
.metric-top{display:flex;justify-content:space-between;align-items:center;gap:8px;}
.metric-icon{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:#EEF3FF;color:#2F6BFF;font-size:1rem;box-shadow:inset 0 1px 0 rgba(255,255,255,.9);}
.metric-label{font-size:.69rem;color:#758195;font-weight:800;text-transform:uppercase;letter-spacing:.075em;margin-top:11px;}
.metric-value{font-size:1.62rem;color:#15263B;font-weight:850;letter-spacing:-.045em;margin-top:2px;line-height:1.05;}
.metric-foot{font-size:.73rem;color:#788699;margin-top:6px;line-height:1.3;}

/* DIMENSIONES */
.dim-card{padding:17px;min-height:184px;position:relative;overflow:hidden;}
.dim-card:before{content:"";position:absolute;left:0;top:0;width:100%;height:4px;background:var(--dim);}
.dim-header{display:flex;align-items:center;justify-content:space-between;gap:8px;}
.dim-code{font-size:.72rem;font-weight:900;letter-spacing:.08em;color:var(--dim);background:var(--soft);padding:5px 8px;border-radius:9px;}
.status-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 8px;border-radius:999px;background:var(--status-soft);color:var(--status-dark);font-size:.68rem;font-weight:800;border:1px solid rgba(0,0,0,.035);}
.status-led{width:8px;height:8px;border-radius:50%;background:var(--status);box-shadow:0 0 0 3px var(--status-soft);}
.dim-body{display:grid;grid-template-columns:82px minmax(0,1fr);gap:12px;align-items:center;margin-top:13px;}
.progress-ring{--p:0;--ring:#2F6BFF;width:76px;height:76px;border-radius:50%;position:relative;background:conic-gradient(var(--ring) calc(var(--p)*1%),#E9EEF5 0);display:grid;place-items:center;box-shadow:0 8px 18px rgba(19,34,56,.11),inset 0 1px 0 rgba(255,255,255,.9);}
.progress-ring:before{content:"";width:58px;height:58px;border-radius:50%;background:linear-gradient(145deg,#FFFFFF,#F6F8FB);box-shadow:inset 0 1px 2px rgba(15,23,42,.08);position:absolute;}
.progress-ring span{position:relative;z-index:1;font-size:.88rem;font-weight:850;color:#172B3A;}
.dim-name{font-size:.84rem;font-weight:800;color:#22364A;line-height:1.28;}
.dim-meta{font-size:.70rem;color:#7B8797;margin-top:6px;line-height:1.35;}
.dim-target{font-size:.69rem;font-weight:750;margin-top:6px;color:#4B5C70;}

/* MINI SEMÁFORO */
.mini-signal{display:inline-flex;gap:4px;padding:4px 6px;border-radius:999px;background:#17212B;box-shadow:inset 0 1px 2px rgba(255,255,255,.08),0 3px 8px rgba(15,23,42,.12);}
.mini-light{width:8px;height:8px;border-radius:50%;opacity:.18}.mini-light.red{background:#EF4444}.mini-light.amber{background:#F59E0B}.mini-light.green{background:#22C55E}.mini-light.on{opacity:1}.mini-light.red.on{box-shadow:0 0 8px #EF4444}.mini-light.amber.on{box-shadow:0 0 8px #F59E0B}.mini-light.green.on{box-shadow:0 0 8px #22C55E}

/* INSIGHTS */
.insight-card{padding:15px 16px;min-height:118px;border-left:4px solid var(--accent);}
.insight-kicker{font-size:.66rem;font-weight:850;text-transform:uppercase;letter-spacing:.08em;color:#7A8798;}
.insight-title{font-size:.92rem;font-weight:850;color:#1C3045;margin-top:6px;line-height:1.25;}
.insight-text{font-size:.75rem;color:#677587;margin-top:6px;line-height:1.4;}

/* TABLAS Y PANELES */
.table-shell{padding:14px 15px 12px;}
.table-title{font-size:.91rem;font-weight:850;color:#1A2E43;}
.table-sub{font-size:.73rem;color:#778496;margin-top:3px;margin-bottom:10px;}
div[data-testid="stDataFrame"]{border:1px solid #E6EBF1;border-radius:14px;overflow:hidden;}
div[data-testid="stPlotlyChart"]{background:linear-gradient(145deg,#FFFFFF,#FBFCFE);border:1px solid #E6EBF1;border-radius:18px;padding:7px 8px 2px;box-shadow:0 12px 28px rgba(19,34,56,.055);}

/* TABS */
.stTabs [data-baseweb="tab-list"]{gap:7px;background:#EDF2F7;padding:5px;border-radius:15px;width:max-content;box-shadow:inset 0 1px 2px rgba(15,23,42,.06);}
.stTabs [data-baseweb="tab"]{height:38px;border-radius:11px;padding:0 16px;color:#536273;font-weight:700;font-size:.82rem;}
.stTabs [aria-selected="true"]{background:#FFFFFF!important;color:#17304B!important;box-shadow:0 5px 12px rgba(15,23,42,.10)!important;}
.stTabs [data-baseweb="tab-highlight"]{display:none;}

/* INPUTS */
div[data-testid="stSelectbox"]>div>div,div[data-testid="stFileUploaderDropzone"]{border-radius:13px!important;}
[data-testid="stMetric"]{background:#FFFFFF;border:1px solid #E6EBF1;border-radius:16px;padding:13px 15px;box-shadow:0 8px 22px rgba(19,34,56,.05);}

/* SIDEBAR SOLO PARA DATOS */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#081B30,#10344E);border-right:1px solid rgba(255,255,255,.07);}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3{color:#FFFFFF!important;}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#D2E0E8!important;}
.data-badge{display:flex;align-items:center;gap:8px;padding:10px 11px;border-radius:12px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.11);color:#EFF7FA;font-size:.78rem;}
.data-dot{width:9px;height:9px;border-radius:50%;background:#34D399;box-shadow:0 0 12px rgba(52,211,153,.8);}

/* METODOLOGÍA */
.method-card{padding:18px;min-height:186px;}
.method-icon{font-size:1.15rem;margin-bottom:8px;}
.method-title{font-size:.91rem;font-weight:850;color:#193047;}
.method-text{font-size:.78rem;color:#687789;line-height:1.48;margin-top:7px;}
.rule-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px;}
.rule{padding:13px;border-radius:14px;border:1px solid var(--line);background:#FFFFFF;box-shadow:0 7px 18px rgba(19,34,56,.04);}
.rule-dot{width:11px;height:11px;border-radius:50%;margin-bottom:7px;box-shadow:0 0 0 4px rgba(0,0,0,.03);}
.rule-name{font-size:.77rem;font-weight:850;color:#243A4F}.rule-range{font-size:.72rem;color:#788698;margin-top:4px;}

@media(max-width:900px){
  .hero-title{font-size:1.65rem}.signal-stage{grid-template-columns:90px minmax(0,1fr)}.rule-grid{grid-template-columns:1fr 1fr}.section-note{display:none;}
}
</style>
"""
)


# ==============================================================
# LÓGICA DE DATOS
# ==============================================================
def level_for(p: float) -> str:
    if pd.isna(p):
        return "Insatisfactorio"
    if p < 0.60:
        return "Insatisfactorio"
    if p < 0.75:
        return "Regular"
    if p < 0.90:
        return "Satisfactorio"
    return "Muy satisfactorio"


def pct(p: float, digits: int = 1) -> str:
    if pd.isna(p):
        return "—"
    return f"{p * 100:.{digits}f}%"


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

    # Regla original: promedio de las cuatro preguntas >= 4 => satisfecho en la dimensión.
    for code, info in DIMENSIONS.items():
        df[f"{code}_Promedio_calc"] = df[info["items"]].mean(axis=1, skipna=True)
        df[f"{code}_Satisfecho_calc"] = (df[f"{code}_Promedio_calc"] >= 4).astype(float)

    # P17 define satisfacción general; 4–5 = satisfecho.
    df["Global_Satisfecho_calc"] = (df["P17"] >= 4).astype(float)
    return df


@st.cache_data(show_spinner=False)
def load_local(path: str, mtime: float) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=SHEET_NAME)
    return prepare_data(raw)


@st.cache_data(show_spinner=False)
def load_upload(payload: bytes) -> pd.DataFrame:
    raw = pd.read_excel(BytesIO(payload), sheet_name=SHEET_NAME)
    return prepare_data(raw)


def dim_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, info in DIMENSIONS.items():
        sat = df[f"{code}_Satisfecho_calc"].mean()
        avg = df[f"{code}_Promedio_calc"].mean()
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
            "Promedio": s.mean(),
            "Favorable": (s >= 4).mean(),
            "Neutral": (s == 3).mean(),
            "Desfavorable": (s <= 2).mean(),
        })
    return pd.DataFrame(rows)


def mini_signal(level: str) -> str:
    signal = STATUS[level]["signal"]
    rr = " on" if signal == "red" else ""
    aa = " on" if signal == "amber" else ""
    gg = " on" if signal == "green" else ""
    return (
        '<span class="mini-signal" aria-label="Semáforo">'
        f'<span class="mini-light red{rr}"></span>'
        f'<span class="mini-light amber{aa}"></span>'
        f'<span class="mini-light green{gg}"></span>'
        '</span>'
    )


def section_head(kicker: str, title: str, note: str = "") -> None:
    st.html(
        f'<div class="section-head"><div><div class="section-kicker">{escape(kicker)}</div>'
        f'<div class="section-title">{escape(title)}</div></div>'
        f'<div class="section-note">{escape(note)}</div></div>'
    )


def hero(source: str, n: int) -> None:
    st.html(
        f'''<div class="hero-shell">
          <div class="hero-kicker">Universidad Nacional de Trujillo · tablero ejecutivo</div>
          <div class="hero-title">Satisfacción estudiantil</div>
          <div class="hero-sub">Una lectura ejecutiva de satisfacción general, desempeño de las cuatro dimensiones y prioridades concretas de mejora.</div>
          <div class="hero-meta">
            <span class="hero-chip">● Base activa: {escape(source)}</span>
            <span class="hero-chip">👥 {n:,} estudiantes</span>
            <span class="hero-chip">🎯 Meta institucional: 75%</span>
          </div>
        </div>'''
    )


def traffic_command(global_sat: float) -> None:
    level = level_for(global_sat)
    meta = STATUS[level]
    red = " active" if meta["signal"] == "red" else ""
    amber = " active" if meta["signal"] == "amber" else ""
    green = " active" if meta["signal"] == "green" else ""
    st.html(
        f'''<div class="glass-card command-card">
          <div class="command-label">Estado institucional</div>
          <div class="command-title">Satisfacción general · P17</div>
          <div class="signal-stage">
            <div class="traffic-shell">
              <div class="lamp red{red}"></div>
              <div class="lamp amber{amber}"></div>
              <div class="lamp green{green}"></div>
            </div>
            <div class="signal-copy">
              <div class="big-score">{pct(global_sat)}</div>
              <div class="big-level" style="color:{meta['color']}">{escape(level)}</div>
              <div class="big-range">Intervalo: {meta['range']}<br>Regla: P17 = 4 o 5 se considera satisfecho.</div>
              <span class="big-action">{meta['icon']} {escape(meta['action'])}</span>
            </div>
          </div>
          <div class="scale-zone">
            <div class="scale-track"><span></span><span></span><span></span><span></span></div>
            <div class="scale-legend">
              <div><b>0–&lt;60</b><br>Insatisf.</div><div><b>60–&lt;75</b><br>Regular</div>
              <div><b>75–&lt;90</b><br>Satisf.</div><div><b>90–100</b><br>Muy sat.</div>
            </div>
          </div>
        </div>'''
    )


def metric_card(icon: str, label: str, value: str, foot: str) -> None:
    st.html(
        f'''<div class="metric-card">
          <div class="metric-top"><div class="metric-icon">{icon}</div></div>
          <div class="metric-label">{escape(label)}</div>
          <div class="metric-value">{escape(value)}</div>
          <div class="metric-foot">{foot}</div>
        </div>'''
    )


def dimension_card(code: str, sat: float) -> None:
    info = DIMENSIONS[code]
    level = level_for(sat)
    sm = STATUS[level]
    gap = max(0.0, TARGET - sat)
    target_text = "Meta alcanzada" if gap <= 0 else f"Faltan {gap*100:.1f} pp para 75%"
    st.html(
        f'''<div class="dim-card" style="--dim:{info['color']};--soft:{info['soft']};--status:{sm['color']};--status-dark:{sm['dark']};--status-soft:{sm['soft']};">
          <div class="dim-header">
            <span class="dim-code">{code}</span>
            <span class="status-chip"><span class="status-led"></span>{escape(level)}</span>
          </div>
          <div class="dim-body">
            <div class="progress-ring" style="--p:{sat*100:.1f};--ring:{info['color']}"><span>{pct(sat)}</span></div>
            <div>
              <div class="dim-name">{escape(info['short'])}</div>
              <div class="dim-meta">{mini_signal(level)} &nbsp; {escape(sm['range'])}</div>
              <div class="dim-target">{escape(target_text)}</div>
            </div>
          </div>
        </div>'''
    )


def insight_card(kicker: str, title: str, text: str, accent: str) -> None:
    st.html(
        f'''<div class="insight-card" style="--accent:{accent}">
          <div class="insight-kicker">{escape(kicker)}</div>
          <div class="insight-title">{escape(title)}</div>
          <div class="insight-text">{text}</div>
        </div>'''
    )


def plot_theme(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=28, t=34, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Aptos, Segoe UI, Arial", color="#566477", size=12),
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#172B3A", bordercolor="#D8E0E8"),
        legend=dict(bgcolor="rgba(255,255,255,.80)", borderwidth=0, orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig.update_xaxes(gridcolor="#EBEFF4", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", zeroline=False)
    return fig


def dimension_chart(summary: pd.DataFrame) -> go.Figure:
    d = summary.sort_values("Satisfacción", ascending=True).copy()
    d["Etiqueta"] = d["Código"] + " · " + d["Dimensión"]
    colors = [STATUS[x]["color"] for x in d["Nivel"]]
    fig = go.Figure()
    for x0, x1, color in [
        (0.00, 0.60, "rgba(239,68,68,.045)"),
        (0.60, 0.75, "rgba(245,158,11,.055)"),
        (0.75, 0.90, "rgba(34,197,94,.045)"),
        (0.90, 1.00, "rgba(5,150,105,.060)"),
    ]:
        fig.add_vrect(x0=x0, x1=x1, fillcolor=color, line_width=0, layer="below")
    fig.add_trace(go.Bar(
        x=d["Satisfacción"], y=d["Etiqueta"], orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=d["Satisfacción"].map(lambda x: f"{x*100:.1f}%"), textposition="outside",
        customdata=d[["Nivel", "Intervalo", "Promedio Likert", "Brecha a 75%"]],
        hovertemplate=(
            "<b>%{y}</b><br>Satisfacción: %{x:.2%}<br>Nivel: %{customdata[0]}"
            "<br>Intervalo: %{customdata[1]}<br>Promedio Likert: %{customdata[2]:.2f}"
            "<br>Brecha a 75%: %{customdata[3]:.2%}<extra></extra>"
        ),
    ))
    fig.add_vline(x=.75, line_dash="dash", line_width=1.5, line_color="#0F766E", annotation_text="Meta 75%", annotation_position="top")
    fig.update_xaxes(tickformat=".0%", range=[0, 1.05], title=None)
    fig.update_yaxes(title=None, tickfont=dict(size=11))
    fig.update_layout(showlegend=False)
    return plot_theme(fig, 410)


def item_bar(items: pd.DataFrame, title: str = "") -> go.Figure:
    d = items.sort_values("Favorable", ascending=True).copy()
    d["Etiqueta"] = d.apply(lambda r: f"{r['Ítem']} · {r['Pregunta'][:58]}{'…' if len(r['Pregunta'])>58 else ''}", axis=1)
    color_map = {c: DIMENSIONS[c]["color"] for c in DIMENSIONS}
    fig = go.Figure(go.Bar(
        x=d["Favorable"], y=d["Etiqueta"], orientation="h",
        marker=dict(color=[color_map.get(x, "#2F6BFF") for x in d["Dimensión"]]),
        text=d["Favorable"].map(lambda x: f"{x*100:.1f}%"), textposition="outside",
        customdata=d[["Ítem", "Dimensión", "Pregunta", "Promedio", "Neutral", "Desfavorable"]],
        hovertemplate=(
            "<b>%{customdata[0]} · %{customdata[1]}</b><br>%{customdata[2]}"
            "<br>Favorable: %{x:.2%}<br>Neutral: %{customdata[4]:.2%}"
            "<br>Desfavorable: %{customdata[5]:.2%}<br>Promedio: %{customdata[3]:.2f}<extra></extra>"
        ),
    ))
    fig.update_xaxes(tickformat=".0%", range=[0, 1.05], title="Respuestas favorables (4–5)")
    fig.update_yaxes(title=None, tickfont=dict(size=10))
    fig.update_layout(showlegend=False, title=dict(text=title, font=dict(size=14)))
    return plot_theme(fig, max(370, 42 * len(d) + 120))


def likert_chart(df: pd.DataFrame, items: list[str]) -> go.Figure:
    rows = []
    for item in items:
        s = df[item].dropna()
        total = len(s)
        if total == 0:
            continue
        rows.extend([
            {"Ítem": item, "Categoría": "Desfavorable (1–2)", "pct": (s <= 2).mean(), "Pregunta": ITEM_TEXT[item]},
            {"Ítem": item, "Categoría": "Neutral (3)", "pct": (s == 3).mean(), "Pregunta": ITEM_TEXT[item]},
            {"Ítem": item, "Categoría": "Favorable (4–5)", "pct": (s >= 4).mean(), "Pregunta": ITEM_TEXT[item]},
        ])
    d = pd.DataFrame(rows)
    fig = go.Figure()
    for cat in ["Desfavorable (1–2)", "Neutral (3)", "Favorable (4–5)"]:
        x = d[d["Categoría"] == cat]
        fig.add_trace(go.Bar(
            x=x["pct"], y=x["Ítem"], name=cat, orientation="h",
            marker_color=LIKERT[cat],
            customdata=x[["Pregunta"]],
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>" + cat + ": %{x:.2%}<extra></extra>",
        ))
    fig.update_layout(barmode="stack")
    fig.update_xaxes(tickformat=".0%", range=[0,1], title="Distribución de respuestas")
    fig.update_yaxes(title=None, autorange="reversed")
    return plot_theme(fig, max(360, 38 * len(items) + 120))


# ==============================================================
# FUENTE DE DATOS — YA NO OBLIGA A CARGAR EL EXCEL
# ==============================================================
with st.sidebar:
    st.markdown("### Datos")
    if DATA_FILE.exists():
        st.html('<div class="data-badge"><span class="data-dot"></span><span>Base incluida · carga automática</span></div>')
        st.caption("Si este Excel está en GitHub junto a app.py, el público no tiene que cargar nada.")
    else:
        st.warning("No encontré basededatos.xlsx junto a app.py.")

    with st.expander("Cambiar Excel temporalmente"):
        uploaded = st.file_uploader("Selecciona otro .xlsx", type=["xlsx"])
        st.caption("Solo reemplaza los datos durante esta sesión; no modifica el archivo del repositorio.")

if uploaded is None and not DATA_FILE.exists():
    st.error("Coloca basededatos.xlsx en la misma carpeta que app.py o carga un Excel desde la barra lateral.")
    st.stop()

try:
    if uploaded is not None:
        df = load_upload(uploaded.getvalue())
        source_name = f"{uploaded.name} · temporal"
    else:
        df = load_local(str(DATA_FILE), DATA_FILE.stat().st_mtime)
        source_name = "basededatos.xlsx"
except Exception as exc:
    st.error(f"No pude leer la base: {exc}")
    st.stop()

summary = dim_summary(df)
global_sat = df["Global_Satisfecho_calc"].mean()
items16 = item_summary(df, [f"P{i}" for i in range(1,17)])

hero(source_name, len(df))

# Navegación horizontal: no replica el menú de Shiny.
tab_resumen, tab_dim, tab_prior, tab_method = st.tabs([
    "◉  Resumen ejecutivo",
    "◫  Dimensiones",
    "⚑  Prioridades",
    "ⓘ  Metodología",
])


# ==============================================================
# RESUMEN EJECUTIVO
# ==============================================================
with tab_resumen:
    section_head("Centro de control", "Estado general de la experiencia estudiantil", "Primero la señal; después el detalle.")

    c1, c2 = st.columns([1.05, 1.95], gap="large")
    with c1:
        traffic_command(global_sat)
    with c2:
        m1, m2, m3 = st.columns(3, gap="medium")
        priority = summary.sort_values("Satisfacción").iloc[0]
        strongest = summary.sort_values("Satisfacción", ascending=False).iloc[0]
        meet = int((summary["Satisfacción"] >= TARGET).sum())
        with m1:
            metric_card("👥", "Estudiantes", f"{len(df):,}", "Registros analizados en la base activa.")
        with m2:
            metric_card("🎯", "Dimensiones en meta", f"{meet} de 4", "Meta institucional: 75% o más.")
        with m3:
            metric_card("⚠", "Prioridad", priority["Código"], f"{pct(priority['Satisfacción'])} · {escape(priority['Nivel'])}")
        st.write("")
        dcols = st.columns(4, gap="small")
        for col, code in zip(dcols, DIMENSIONS):
            sat = float(summary.loc[summary["Código"] == code, "Satisfacción"].iloc[0])
            with col:
                dimension_card(code, sat)

    section_head("Lectura ejecutiva", "Qué debería mirar primero", "Tres mensajes automáticos para orientar la discusión.")
    i1, i2, i3 = st.columns(3, gap="medium")
    with i1:
        insight_card(
            "Prioridad",
            f"{priority['Código']} · {DIMENSIONS[priority['Código']]['short']}",
            f"Registra <b>{pct(priority['Satisfacción'])}</b>. " + (f"La brecha hasta 75% es <b>{priority['Brecha a 75%']*100:.1f} pp</b>." if priority['Brecha a 75%'] > 0 else "Ya se encuentra en el estándar institucional."),
            "#DC2626" if priority["Satisfacción"] < .75 else "#16A34A",
        )
    with i2:
        insight_card(
            "Fortaleza relativa",
            f"{strongest['Código']} · {DIMENSIONS[strongest['Código']]['short']}",
            f"Es la dimensión con mayor satisfacción: <b>{pct(strongest['Satisfacción'])}</b>, nivel <b>{escape(strongest['Nivel'])}</b>.",
            "#16A34A",
        )
    with i3:
        glevel = level_for(global_sat)
        insight_card(
            "Resultado general",
            f"P17 · {glevel}",
            f"La satisfacción general alcanza <b>{pct(global_sat)}</b>. El semáforo se interpreta con el intervalo <b>{STATUS[glevel]['range']}</b>.",
            STATUS[glevel]["color"],
        )

    section_head("Mapa de desempeño", "Comparación de D1, D2, D3 y D4", "Las bandas de fondo corresponden a la escala institucional.")
    st.plotly_chart(dimension_chart(summary), use_container_width=True, config={"displayModeBar": False})

    section_head("Detalle", "Matriz de situación institucional", "El semáforo no reemplaza el porcentaje: ambos se muestran juntos.")
    table = summary.copy()
    table.insert(2, "Semáforo", table["Nivel"].map(lambda x: "🔴" if x=="Insatisfactorio" else "🟠" if x=="Regular" else "🟢"))
    table["Satisfacción"] = table["Satisfacción"].map(lambda x: f"{x*100:.2f}%")
    table["Promedio Likert"] = table["Promedio Likert"].map(lambda x: f"{x:.2f}")
    table["Brecha a 75%"] = table["Brecha a 75%"].map(lambda x: "—" if x <= 0 else f"{x*100:.2f} pp")
    st.dataframe(table, use_container_width=True, hide_index=True)


# ==============================================================
# DIMENSIONES
# ==============================================================
with tab_dim:
    section_head("Exploración", "Analizar una dimensión", "Aquí se baja del resultado global a las cuatro preguntas que lo explican.")

    selected = st.selectbox(
        "Dimensión",
        options=list(DIMENSIONS.keys()),
        format_func=lambda x: f"{x} · {DIMENSIONS[x]['name']}",
        label_visibility="collapsed",
    )
    info = DIMENSIONS[selected]
    row = summary.loc[summary["Código"] == selected].iloc[0]
    dim_items = item_summary(df, info["items"])
    low_item = dim_items.sort_values("Favorable").iloc[0]
    high_item = dim_items.sort_values("Favorable", ascending=False).iloc[0]

    a, b, c, d = st.columns(4, gap="medium")
    with a:
        dimension_card(selected, float(row["Satisfacción"]))
    with b:
        metric_card("★", "Promedio Likert", f"{row['Promedio Likert']:.2f}", "Promedio de las cuatro preguntas de la dimensión.")
    with c:
        metric_card("↓", "Aspecto más débil", low_item["Ítem"], f"{pct(low_item['Favorable'])} favorable")
    with d:
        metric_card("↑", "Aspecto más fuerte", high_item["Ítem"], f"{pct(high_item['Favorable'])} favorable")

    st.info(info["desc"], icon="ℹ️")

    left, right = st.columns([1.1, .9], gap="large")
    with left:
        section_head("Ítems", "Valoración favorable", "4–5 = favorable; se usa de forma descriptiva por pregunta.")
        st.plotly_chart(item_bar(dim_items), use_container_width=True, config={"displayModeBar": False})
    with right:
        section_head("Distribución", "Perfil Likert", "Cómo se distribuyen respuestas desfavorables, neutrales y favorables.")
        st.plotly_chart(likert_chart(df, info["items"]), use_container_width=True, config={"displayModeBar": False})

    section_head("Lectura", "Dos señales concretas", "Sirve para sustentar qué aspecto priorizar y cuál conservar.")
    r1, r2 = st.columns(2, gap="medium")
    with r1:
        insight_card(
            "Mayor oportunidad",
            f"{low_item['Ítem']} · {pct(low_item['Favorable'])} favorable",
            escape(low_item["Pregunta"]),
            "#DC2626",
        )
    with r2:
        insight_card(
            "Fortaleza del bloque",
            f"{high_item['Ítem']} · {pct(high_item['Favorable'])} favorable",
            escape(high_item["Pregunta"]),
            "#16A34A",
        )


# ==============================================================
# PRIORIDADES
# ==============================================================
with tab_prior:
    section_head("Priorización", "Ranking de los 16 aspectos", "Ordenado de menor a mayor valoración favorable.")
    ranked = items16.sort_values("Favorable", ascending=True).copy()
    st.plotly_chart(item_bar(ranked), use_container_width=True, config={"displayModeBar": False})

    section_head("Acción", "Top 5 de menor valoración", "Estos ítems ayudan a enfocar la discusión; no reemplazan el indicador oficial de la dimensión.")
    top5 = ranked.head(5).copy()
    top5["Favorable"] = top5["Favorable"].map(lambda x: f"{x*100:.2f}%")
    top5["Desfavorable"] = top5["Desfavorable"].map(lambda x: f"{x*100:.2f}%")
    top5["Promedio"] = top5["Promedio"].map(lambda x: f"{x:.2f}")
    st.dataframe(top5[["Ítem","Dimensión","Pregunta","Favorable","Desfavorable","Promedio"]], use_container_width=True, hide_index=True)

    weakest3 = ranked.head(3)
    msg = ", ".join([f"{r['Ítem']} ({r['Dimensión']})" for _, r in weakest3.iterrows()])
    st.warning(f"Prioridades descriptivas: {msg}. Revísalas junto con la satisfacción oficial de cada dimensión.", icon="⚑")


# ==============================================================
# METODOLOGÍA
# ==============================================================
with tab_method:
    section_head("Metodología", "Cómo leer el tablero", "Se conserva la lógica estadística; lo que cambia es la experiencia visual.")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.html('''<div class="method-card"><div class="method-icon">◫</div><div class="method-title">Satisfacción por dimensión</div><div class="method-text">Cada dimensión contiene 4 preguntas. Para cada estudiante se calcula el promedio de esas cuatro respuestas. Si el promedio es <b>≥ 4</b>, el estudiante se clasifica como satisfecho en esa dimensión.</div></div>''')
    with c2:
        st.html('''<div class="method-card"><div class="method-icon">◎</div><div class="method-title">Satisfacción general</div><div class="method-text">La satisfacción general se obtiene directamente de <b>P17</b>. Respuestas 4 o 5 = satisfecho; respuestas 1, 2 o 3 = no satisfecho. P17 no se obtiene promediando D1–D4.</div></div>''')
    with c3:
        st.html('''<div class="method-card"><div class="method-icon">▥</div><div class="method-title">Lectura de ítems</div><div class="method-text"><b>Desfavorable:</b> 1–2. <b>Neutral:</b> 3. <b>Favorable:</b> 4–5. Los porcentajes por ítem son descriptivos y sirven para ubicar aspectos concretos dentro de cada dimensión.</div></div>''')

    section_head("Semáforo", "Escala institucional", "El color siempre aparece acompañado de nombre e intervalo.")
    st.html('''<div class="rule-grid">
      <div class="rule"><div class="rule-dot" style="background:#EF4444"></div><div class="rule-name">Insatisfactorio</div><div class="rule-range">0% a &lt;60%</div></div>
      <div class="rule"><div class="rule-dot" style="background:#F59E0B"></div><div class="rule-name">Regular</div><div class="rule-range">60% a &lt;75%</div></div>
      <div class="rule"><div class="rule-dot" style="background:#22C55E"></div><div class="rule-name">Satisfactorio</div><div class="rule-range">75% a &lt;90%</div></div>
      <div class="rule"><div class="rule-dot" style="background:#059669"></div><div class="rule-name">Muy satisfactorio</div><div class="rule-range">90% a 100%</div></div>
    </div>''')
