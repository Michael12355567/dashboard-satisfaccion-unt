from __future__ import annotations

from html import escape
from pathlib import Path
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==============================================================
# CONFIGURACIÓN
# ==============================================================
st.set_page_config(
    page_title="UNT | Indicador PEI de satisfacción",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "basededatos.xlsx"
SHEET_NAME = "Base_Encuesta"

ITEMS = [f"P{i}" for i in range(1, 17)]
DIMENSIONS = {
    "D1": {
        "name": "Calidad del proceso académico",
        "short": "Proceso académico",
        "items": ["P1", "P2", "P3", "P4"],
        "accent": "#5B7CFA",
        "icon": "◫",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "short": "Docencia y pedagogía",
        "items": ["P5", "P6", "P7", "P8"],
        "accent": "#9B6CF5",
        "icon": "✦",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "short": "Servicios y gestión",
        "items": ["P9", "P10", "P11", "P12"],
        "accent": "#F59E63",
        "icon": "⌂",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "short": "Formación integral",
        "items": ["P13", "P14", "P15", "P16"],
        "accent": "#33B69A",
        "icon": "◇",
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

# Metas mostradas en la ficha técnica PEI compartida por el usuario.
PEI_TARGETS = {2027: 0.60, 2028: 0.65, 2029: 0.70, 2030: 0.75}
REFERENCE_TARGET = PEI_TARGETS[2027]

# Semáforo VISUAL de gestión (no es una escala normativa del PEI):
# verde = cumple la meta seleccionada; ámbar = queda a <=5 pp; rojo = >5 pp por debajo.
WATCH_BAND_PP = 0.05

LOCKED_PLOT_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": False,
    "doubleClick": False,
    "showTips": False,
}


# ==============================================================
# CSS — DISEÑO FUTURISTA / RESPONSIVE
# ==============================================================
st.markdown(
    r"""
<style>
:root{
  --bg:#F3F6FA;
  --paper:rgba(255,255,255,.86);
  --ink:#172336;
  --muted:#6D7B8E;
  --line:rgba(113,129,152,.16);
  --navy:#071A2B;
  --navy2:#0C3651;
  --cyan:#32D3E2;
  --blue:#5B7CFA;
  --green:#2AD49B;
  --amber:#FFB648;
  --red:#FF5C6C;
  --shadow:0 20px 55px rgba(33,53,82,.12), 0 4px 12px rgba(33,53,82,.05);
  --shadow3d:0 18px 38px rgba(19,35,58,.14), inset 0 1px 0 rgba(255,255,255,.9);
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"Segoe UI Variable","Aptos","Segoe UI",Inter,Arial,sans-serif;}
.stApp{
  background:
    radial-gradient(circle at 8% 0%,rgba(91,124,250,.10),transparent 32rem),
    radial-gradient(circle at 96% 9%,rgba(50,211,226,.08),transparent 28rem),
    linear-gradient(180deg,#FBFCFE 0%,var(--bg) 100%);
  color:var(--ink);
}
.block-container{max-width:1480px;padding:1rem 1.35rem 3.2rem;}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:rgba(248,250,253,.74);backdrop-filter:blur(16px)}
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}

/* HERO */
.neo-hero{
  position:relative;overflow:hidden;border-radius:30px;padding:30px 32px 28px;
  background:linear-gradient(128deg,#071827 0%,#0B304A 52%,#095661 106%);
  color:white;border:1px solid rgba(255,255,255,.09);
  box-shadow:0 30px 68px rgba(9,33,52,.23),inset 0 1px 0 rgba(255,255,255,.10);
  isolation:isolate;
}
.neo-hero:before{content:"";position:absolute;width:440px;height:440px;border-radius:50%;right:-150px;top:-235px;border:72px solid rgba(50,211,226,.065);z-index:-1}
.neo-hero:after{content:"";position:absolute;width:240px;height:240px;border-radius:50%;right:120px;bottom:-160px;background:radial-gradient(circle,rgba(91,124,250,.25),transparent 68%);z-index:-1}
.neo-kicker{font-size:.69rem;letter-spacing:.17em;text-transform:uppercase;font-weight:850;color:#88E7EF}
.neo-title{margin-top:7px;font-size:clamp(1.75rem,4vw,2.75rem);font-weight:900;letter-spacing:-.055em;line-height:1.03}
.neo-sub{max-width:960px;margin-top:10px;color:#D7E7ED;font-size:clamp(.82rem,1.4vw,.98rem);line-height:1.5}
.neo-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:17px}
.neo-chip{font-size:.69rem;font-weight:700;color:#EAF7FA;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.075);border-radius:999px;padding:7px 10px;backdrop-filter:blur(12px)}

/* TABS */
.stTabs [data-baseweb="tab-list"]{gap:7px;background:#EAF0F5;padding:5px;border-radius:16px;width:100%;overflow-x:auto;white-space:nowrap;scrollbar-width:thin;margin-top:6px}
.stTabs [data-baseweb="tab"]{height:41px;border-radius:12px;padding:0 16px;color:#607084;font-weight:800;font-size:.79rem;flex:0 0 auto}
.stTabs [aria-selected="true"]{background:white!important;color:#102B43!important;box-shadow:0 6px 16px rgba(24,47,72,.11)!important}
.stTabs [data-baseweb="tab-highlight"]{display:none}

/* SECTION */
.section-head{display:flex;justify-content:space-between;align-items:end;gap:16px;margin:1.5rem 0 .75rem}
.section-kicker{font-size:.65rem;text-transform:uppercase;letter-spacing:.14em;font-weight:900;color:#4A6EF2}
.section-title{font-size:clamp(1.05rem,2vw,1.32rem);font-weight:900;color:#182A40;letter-spacing:-.025em;margin-top:3px}
.section-note{font-size:.72rem;color:#7D8B9C;text-align:right;max-width:520px;line-height:1.42}

/* GLASS / 3D */
.glass{
  background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(248,251,254,.82));
  border:1px solid rgba(126,145,168,.16);border-radius:22px;box-shadow:var(--shadow3d);backdrop-filter:blur(18px);
}

/* DUAL CORE */
.core-grid{display:grid;grid-template-columns:minmax(0,1.22fr) minmax(0,.78fr);gap:16px}
.primary-core{padding:22px;position:relative;overflow:hidden;min-height:315px}
.primary-core:after{content:"";position:absolute;right:-120px;bottom:-145px;width:310px;height:310px;border-radius:50%;background:radial-gradient(circle,rgba(91,124,250,.12),transparent 68%)}
.core-top{display:flex;justify-content:space-between;gap:15px;align-items:flex-start}
.core-label{font-size:.64rem;text-transform:uppercase;letter-spacing:.13em;font-weight:900;color:#718096}
.core-name{font-size:clamp(1rem,2vw,1.35rem);font-weight:900;color:#172D45;margin-top:5px;max-width:720px;line-height:1.25}
.core-tag{font-size:.65rem;font-weight:850;color:#27406A;background:#EEF2FF;padding:7px 9px;border-radius:999px;white-space:nowrap;border:1px solid #DEE5FF}
.core-main{display:grid;grid-template-columns:155px minmax(0,1fr);gap:22px;align-items:center;margin-top:19px}
.ring{--p:0;--ring:#5B7CFA;width:145px;height:145px;border-radius:50%;background:conic-gradient(var(--ring) calc(var(--p)*1%),#E8EDF4 0);position:relative;box-shadow:10px 14px 24px rgba(25,44,75,.15),inset 0 1px 0 #fff;display:grid;place-items:center}
.ring:before{content:"";position:absolute;inset:13px;border-radius:50%;background:linear-gradient(145deg,#FFFFFF,#F3F7FA);box-shadow:inset 5px 6px 12px rgba(31,51,79,.06),inset -5px -6px 12px rgba(255,255,255,.95)}
.ring-value{position:relative;z-index:1;font-size:1.8rem;font-weight:950;letter-spacing:-.055em;color:#172B42}
.ring-label{position:relative;z-index:1;font-size:.59rem;font-weight:800;color:#7A8797;text-transform:uppercase;letter-spacing:.06em;margin-top:-37px}
.core-score{font-size:clamp(2.35rem,5vw,3.45rem);font-weight:950;letter-spacing:-.065em;color:#11253A;line-height:.95}
.core-desc{font-size:.79rem;color:#68788C;line-height:1.5;margin-top:9px;max-width:650px}
/* FORMULA / ESCALA INSTITUCIONAL */
.core-formula{display:none}
.formula-panel{margin-top:14px;padding:15px 16px;border-radius:18px;background:linear-gradient(145deg,#F7FAFD,#EEF4F9);border:1px solid #DFE7EF;box-shadow:inset 0 1px 0 #fff,0 10px 22px rgba(32,54,82,.06)}
.formula-kicker{font-size:.58rem;font-weight:900;text-transform:uppercase;letter-spacing:.12em;color:#76879A;margin-bottom:8px}
.formula-equation{display:flex;align-items:center;gap:10px;flex-wrap:wrap;color:#132A42;font-weight:900}
.formula-id{font-size:.88rem;letter-spacing:.03em;color:#4E6380}
.formula-eq{font-size:1.15rem;color:#60738A}
.formula-frac{display:inline-grid;grid-template-rows:auto 1px auto;min-width:58px;text-align:center;align-items:center;font-size:1rem;line-height:1.1}
.formula-frac .bar{height:1px;background:#243D59;margin:4px 0}
.formula-times{font-size:1rem}
.formula-result{font-size:1.24rem;color:#0B6572;background:linear-gradient(135deg,#E9FBFC,#F1FBFF);border:1px solid #CFECEF;border-radius:12px;padding:6px 10px;box-shadow:0 8px 18px rgba(23,105,119,.08)}
.formula-defs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:11px}
.formula-def{padding:9px 10px;border-radius:12px;background:rgba(255,255,255,.78);border:1px solid #E4EAF0;font-size:.63rem;color:#6A7A8E;line-height:1.35}
.formula-def b{color:#213951}
.scale4-wrap{margin-top:14px;padding:13px 14px;border-radius:17px;background:#F8FAFC;border:1px solid #E5EAF1}
.scale4-title{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:9px}
.scale4-title .a{font-size:.59rem;text-transform:uppercase;letter-spacing:.1em;font-weight:900;color:#7A899A}
.scale4-title .b{font-size:.68rem;font-weight:900;color:#233A52}
.scale4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
.scale4-step{position:relative;padding:8px 6px;border-radius:11px;text-align:center;border:1px solid transparent;opacity:.52;filter:saturate(.72);transition:.18s ease;background:#fff}
.scale4-step .dot{width:10px;height:10px;border-radius:50%;margin:0 auto 5px;box-shadow:inset 0 1px 1px rgba(255,255,255,.8),0 3px 8px rgba(20,35,50,.14)}
.scale4-step .name{font-size:.56rem;font-weight:900;line-height:1.15;color:#405168}
.scale4-step .range{font-size:.52rem;color:#8794A3;margin-top:3px}
.scale4-step.active{opacity:1;filter:none;transform:translateY(-2px);box-shadow:0 10px 20px rgba(34,52,76,.10)}
.scale4-step.active:after{content:"";position:absolute;inset:-2px;border-radius:13px;border:2px solid var(--lvl);pointer-events:none}
.signal-caption{font-size:.57rem;text-transform:uppercase;letter-spacing:.09em;font-weight:900;color:#8290A1;margin-bottom:5px}
.core-mini{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:18px}
.mini-stat{padding:12px;border-radius:15px;background:rgba(247,250,253,.86);border:1px solid #E6EBF1}
.mini-stat .k{font-size:.58rem;color:#8090A1;font-weight:850;text-transform:uppercase;letter-spacing:.06em}
.mini-stat .v{font-size:1rem;font-weight:900;color:#17304A;margin-top:3px}
.mini-stat .s{font-size:.61rem;color:#8190A0;margin-top:2px}

/* SECONDARY CORE */
.secondary-core{padding:20px;min-height:315px;display:flex;flex-direction:column}
.secondary-head{display:flex;justify-content:space-between;align-items:start;gap:10px}
.secondary-title{font-size:1.05rem;font-weight:900;color:#172E46}
.secondary-sub{font-size:.7rem;color:#7A8798;margin-top:4px;line-height:1.4}
.secondary-value{font-size:2.45rem;font-weight:950;letter-spacing:-.06em;color:#17304A;margin-top:16px}
.delta-pill{display:inline-flex;align-items:center;gap:6px;width:max-content;margin-top:7px;padding:6px 9px;border-radius:999px;background:#FFF4E8;color:#9A641D;border:1px solid #FFE3BE;font-size:.66rem;font-weight:850}
.secondary-bottom{margin-top:auto;padding-top:16px;border-top:1px solid #E9EDF2;font-size:.7rem;color:#697A8E;line-height:1.45}

/* TRAFFIC SIGNAL SVG */
.signal-badge{display:flex;align-items:center;gap:8px;font-size:.65rem;font-weight:850;color:#546579}
.signal-shell{filter:drop-shadow(0 8px 12px rgba(10,26,40,.24))}

/* FOUR DIMENSIONS */
.dim-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px}
.dim-card{padding:17px;position:relative;overflow:hidden;min-height:216px;transition:transform .18s ease,box-shadow .18s ease}
.dim-card:hover{transform:translateY(-3px);box-shadow:0 24px 48px rgba(23,42,66,.13)}
.dim-card:before{content:"";position:absolute;left:0;top:0;width:100%;height:4px;background:var(--accent)}
.dim-head{display:flex;justify-content:space-between;align-items:center;gap:10px}
.dim-code{display:inline-flex;align-items:center;gap:7px;font-size:.7rem;font-weight:900;color:var(--accent);background:color-mix(in srgb,var(--accent) 10%,white);padding:6px 9px;border-radius:10px}
.dim-name{font-size:.83rem;font-weight:900;color:#24394F;line-height:1.28;margin-top:13px;min-height:2.15em}
.dim-middle{display:flex;justify-content:space-between;align-items:end;gap:10px;margin-top:17px}
.dim-score{font-size:2.05rem;font-weight:950;letter-spacing:-.055em;color:#172B42;line-height:1}
.dim-score-label{font-size:.59rem;color:#8491A0;text-transform:uppercase;font-weight:850;letter-spacing:.05em;margin-top:4px}
.dim-progress{height:8px;border-radius:99px;background:#E9EEF4;overflow:hidden;margin-top:13px;box-shadow:inset 0 2px 4px rgba(18,34,52,.05)}
.dim-progress span{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 60%,#32D3E2));box-shadow:0 0 12px color-mix(in srgb,var(--accent) 28%,transparent)}
.dim-foot{display:flex;justify-content:space-between;gap:8px;border-top:1px solid #EDF1F5;margin-top:13px;padding-top:10px}
.dim-foot .a{font-size:.64rem;color:#718196;line-height:1.35}
.dim-foot .b{font-size:.64rem;color:#354A60;font-weight:850;text-align:right;line-height:1.35}

/* SIGNAL LEGEND */
.legend-card{padding:14px 16px;display:grid;grid-template-columns:auto 1fr;gap:13px;align-items:center;margin-top:12px}
.legend-lights{display:flex;gap:7px;align-items:center}
.legend-dot{width:12px;height:12px;border-radius:50%;box-shadow:0 3px 8px rgba(0,0,0,.12)}
.legend-text{font-size:.67rem;color:#6E7E91;line-height:1.45}

/* INSIGHTS */
.insight-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.insight{padding:16px;border-left:4px solid var(--accent);min-height:120px}
.insight .k{font-size:.61rem;color:#8290A1;font-weight:900;text-transform:uppercase;letter-spacing:.09em}
.insight .t{font-size:.9rem;color:#1B334C;font-weight:900;line-height:1.25;margin-top:6px}
.insight .x{font-size:.72rem;color:#67788B;line-height:1.45;margin-top:6px}

/* METHOD */
.method-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.method{padding:17px;min-height:185px}
.method .i{font-size:1.18rem}.method .t{font-size:.86rem;font-weight:900;color:#1C334B;margin-top:7px}.method .x{font-size:.72rem;color:#68798C;line-height:1.5;margin-top:7px}
.notice{padding:14px 16px;border-radius:18px;background:linear-gradient(145deg,#FFF9EC,#FFFDF8);border:1px solid #F3E5BE;color:#6F5A27;font-size:.72rem;line-height:1.48;box-shadow:0 10px 26px rgba(96,74,21,.06)}

/* PLOTS */
div[data-testid="stPlotlyChart"]{background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(248,251,254,.87));border:1px solid rgba(126,145,168,.16);border-radius:21px;padding:7px 6px 1px;box-shadow:0 14px 34px rgba(33,53,82,.07);overflow:hidden;touch-action:pan-y!important}
div[data-testid="stDataFrame"]{border:1px solid #E5EAF0;border-radius:17px;overflow:hidden;box-shadow:0 10px 24px rgba(33,53,82,.055)}

/* TABLET */
@media(max-width:1100px){
  .core-grid{grid-template-columns:1fr}
  .dim-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}

/* PHONE */
@media(max-width:700px){
  .block-container{padding:.58rem .68rem 2.2rem}
  .neo-hero{padding:21px 17px;border-radius:21px}
  .neo-title{font-size:1.75rem}
  .neo-chip{font-size:.63rem;padding:6px 8px}
  .section-head{align-items:flex-start;margin:1.15rem 0 .6rem}
  .section-note{display:none}
  .core-main{grid-template-columns:1fr;justify-items:center;text-align:center;gap:13px}
  .core-top{display:block}.core-tag{display:inline-flex;margin-top:9px}
  .core-mini{grid-template-columns:1fr 1fr}.core-mini .mini-stat:last-child{grid-column:1/-1}
  .formula-defs{grid-template-columns:1fr}
  .scale4{grid-template-columns:1fr 1fr}
  .formula-equation{justify-content:center}
  .primary-core,.secondary-core{padding:16px;border-radius:19px;min-height:0}
  .dim-grid,.insight-grid,.method-grid{grid-template-columns:1fr}
  .dim-card{min-height:0}
  .dim-name{min-height:0}
  .stTabs [data-baseweb="tab"]{font-size:.72rem;padding:0 12px}
  div[data-testid="stPlotlyChart"]{border-radius:16px;padding:3px 2px 0}
}
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================
# UTILIDADES
# ==============================================================
def pct(x: float, digits: int = 1) -> str:
    if pd.isna(x):
        return "—"
    return f"{x * 100:.{digits}f}%"


def pp(x: float, digits: int = 1) -> str:
    return f"{x * 100:.{digits}f} pp"


def signal_state(value: float, target: float) -> str:
    """Semáforo operativo: cumple / cerca (<=5 pp) / lejos (>5 pp)."""
    if pd.isna(value):
        return "off"
    gap = target - value
    if gap <= 0:
        return "green"
    if gap <= WATCH_BAND_PP:
        return "amber"
    return "red"


def signal_label(value: float, target: float) -> str:
    state = signal_state(value, target)
    return {
        "green": "Cumple la meta",
        "amber": "En vigilancia",
        "red": "Brecha prioritaria",
        "off": "Sin dato",
    }[state]


def signal_color(state: str) -> str:
    return {"green": "#22C997", "amber": "#FFB648", "red": "#FF5C6C", "off": "#A7B1BE"}[state]


def institutional_level(value: float) -> tuple[str, str, str, str]:
    """Clasificación institucional del instrumento: 4 niveles.

    Los colores son una decisión visual del dashboard; los rangos provienen del instrumento.
    """
    if pd.isna(value):
        return ("Sin dato", "—", "#A7B1BE", "none")
    if value < 0.60:
        return ("Insatisfactorio", "0–59%", "#FF5C6C", "low")
    if value < 0.75:
        return ("Regular", "60–74%", "#FFB648", "regular")
    if value < 0.90:
        return ("Satisfactorio", "75–89%", "#2AD49B", "good")
    return ("Muy satisfactorio", "90–100%", "#22B8CF", "excellent")


def institutional_scale_html(value: float) -> str:
    name, interval, color, key = institutional_level(value)
    levels = [
        ("low", "Insatisfactorio", "0–59%", "#FF5C6C"),
        ("regular", "Regular", "60–74%", "#FFB648"),
        ("good", "Satisfactorio", "75–89%", "#2AD49B"),
        ("excellent", "Muy satisfactorio", "90–100%", "#22B8CF"),
    ]
    boxes = []
    for k, label, rng, c in levels:
        active = " active" if k == key else ""
        boxes.append(
            f'<div class="scale4-step{active}" style="--lvl:{c}"><div class="dot" style="background:{c}"></div><div class="name">{label}</div><div class="range">{rng}</div></div>'
        )
    return f'<div class="scale4-wrap"><div class="scale4-title"><span class="a">Nivel institucional · 4 categorías</span><span class="b" style="color:{color}">{name} · {interval}</span></div><div class="scale4">{"".join(boxes)}</div></div>'


def formula_html(n: int, d: int, result: float) -> str:
    return f'''<div class="formula-panel">
      <div class="formula-kicker">Fórmula del indicador</div>
      <div class="formula-equation">
        <span class="formula-id">IND.01</span><span class="formula-eq">=</span>
        <span class="formula-frac"><span>N</span><span class="bar"></span><span>D</span></span>
        <span class="formula-times">× 100</span><span class="formula-eq">=</span>
        <span class="formula-frac"><span>{n:,}</span><span class="bar"></span><span>{d:,}</span></span>
        <span class="formula-times">× 100</span><span class="formula-eq">=</span>
        <span class="formula-result">{pct(result)}</span>
      </div>
      <div class="formula-defs">
        <div class="formula-def"><b>N</b> = estudiantes clasificados como satisfechos.</div>
        <div class="formula-def"><b>D</b> = total de estudiantes encuestados analizados.</div>
      </div>
    </div>'''


def traffic_svg(state: str, size: int = 58) -> str:
    # SVG propio, sin imágenes externas. Luces con relieve y brillo selectivo.
    active = {
        "red": (1.0, 0.16, 0.16),
        "amber": (0.16, 1.0, 0.16),
        "green": (0.16, 0.16, 1.0),
        "off": (0.16, 0.16, 0.16),
    }[state]
    return f'''<svg class="signal-shell" width="{size}" height="{int(size*1.62)}" viewBox="0 0 70 114" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Semáforo {state}">
      <defs>
        <linearGradient id="case" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#344A5B"/><stop offset=".48" stop-color="#172531"/><stop offset="1" stop-color="#070C11"/></linearGradient>
        <radialGradient id="r"><stop offset="0" stop-color="#FF9AA4"/><stop offset=".45" stop-color="#FF4758"/><stop offset="1" stop-color="#9C1726"/></radialGradient>
        <radialGradient id="a"><stop offset="0" stop-color="#FFE09C"/><stop offset=".45" stop-color="#FFB020"/><stop offset="1" stop-color="#A85A00"/></radialGradient>
        <radialGradient id="g"><stop offset="0" stop-color="#9AF2CE"/><stop offset=".45" stop-color="#22C997"/><stop offset="1" stop-color="#08724F"/></radialGradient>
        <filter id="glowR"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="glowA"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="glowG"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <rect x="8" y="3" width="54" height="106" rx="19" fill="url(#case)" stroke="#465C6D" stroke-width="1.5"/>
      <rect x="14" y="9" width="42" height="94" rx="14" fill="#0B1117" opacity=".82"/>
      <circle cx="35" cy="27" r="13" fill="url(#r)" opacity="{active[0]}" {'filter="url(#glowR)"' if state=='red' else ''}/>
      <circle cx="35" cy="56" r="13" fill="url(#a)" opacity="{active[1]}" {'filter="url(#glowA)"' if state=='amber' else ''}/>
      <circle cx="35" cy="85" r="13" fill="url(#g)" opacity="{active[2]}" {'filter="url(#glowG)"' if state=='green' else ''}/>
      <ellipse cx="30" cy="22" rx="4.5" ry="2.5" fill="white" opacity=".33"/>
      <ellipse cx="30" cy="51" rx="4.5" ry="2.5" fill="white" opacity=".33"/>
      <ellipse cx="30" cy="80" rx="4.5" ry="2.5" fill="white" opacity=".33"/>
    </svg>'''


def section_header(kicker: str, title: str, note: str = "") -> None:
    st.markdown(
        f'''<div class="section-head"><div><div class="section-kicker">{escape(kicker)}</div><div class="section-title">{escape(title)}</div></div><div class="section-note">{escape(note)}</div></div>''',
        unsafe_allow_html=True,
    )


def hero(n: int) -> None:
    st.markdown(
        f'''<div class="neo-hero">
          <div class="neo-kicker">Universidad Nacional de Trujillo · tablero ejecutivo PEI</div>
          <div class="neo-title">Satisfacción con el proceso de formación académica</div>
          <div class="neo-sub">Lectura integral del IND. 01, diagnóstico de las cuatro dimensiones y contraste con la satisfacción general declarada en P17. Diseño responsive para computadora, tablet y celular.</div>
          <div class="neo-chips">
            <span class="neo-chip">IND. 01 · OEI.01</span>
            <span class="neo-chip">👥 {n:,} estudiantes analizados</span>
            <span class="neo-chip">◉ P1–P16 · medición integral propuesta</span>
            <span class="neo-chip">P17 · percepción global complementaria</span>
            <span class="neo-chip">🎯 Meta PEI 2027 · 60%</span>
          </div>
        </div>''',
        unsafe_allow_html=True,
    )


# ==============================================================
# DATOS Y CÁLCULO
# ==============================================================
def require_columns(df: pd.DataFrame) -> None:
    required = {f"P{i}" for i in range(1, 18)}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(missing))


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    require_columns(df)
    for c in [f"P{i}" for i in range(1, 18)]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Operacionalización analítica PROPUESTA para el dashboard:
    # 1) promedio integral del estudiante en P1-P16;
    # 2) estudiante satisfecho si promedio >= 4 (nivel satisfecho o superior);
    # 3) IND.01 = N satisfechos / D encuestados * 100.
    df["PEI_Promedio_P1_P16_calc"] = df[ITEMS].mean(axis=1, skipna=True)
    df["PEI_Satisfecho_calc"] = (df["PEI_Promedio_P1_P16_calc"] >= 4).astype(float)

    # P17 se mantiene separado: percepción global declarada.
    df["P17_Satisfecho_calc"] = (df["P17"] >= 4).astype(float)

    # Diagnóstico por dimensión: promedio de sus 4 ítems >=4.
    for code, meta in DIMENSIONS.items():
        df[f"{code}_Promedio_calc"] = df[meta["items"]].mean(axis=1, skipna=True)
        df[f"{code}_Satisfecho_calc"] = (df[f"{code}_Promedio_calc"] >= 4).astype(float)
    return df


@st.cache_data(show_spinner=False)
def load_data(path: str, mtime: float) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=SHEET_NAME)
    return prepare_data(raw)


def dimension_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for code, meta in DIMENSIONS.items():
        sat = float(df[f"{code}_Satisfecho_calc"].mean())
        avg = float(df[f"{code}_Promedio_calc"].mean())
        out.append({
            "Código": code,
            "Dimensión": meta["name"],
            "Satisfacción": sat,
            "Promedio Likert": avg,
            "Brecha a 60%": max(0.0, REFERENCE_TARGET - sat),
            "Estado": signal_label(sat, REFERENCE_TARGET),
            "Semáforo": signal_state(sat, REFERENCE_TARGET),
        })
    return pd.DataFrame(out)


def item_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i in range(1, 17):
        item = f"P{i}"
        s = df[item].dropna()
        code = f"D{((i - 1) // 4) + 1}"
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


if not DATA_FILE.exists():
    st.error("No se encontró basededatos.xlsx. El archivo debe estar en la misma carpeta que app.py.")
    st.stop()

try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"No pude leer basededatos.xlsx: {exc}")
    st.stop()

N_TOTAL = int(len(df))
N_PEI = int(df["PEI_Satisfecho_calc"].sum())
PEI = float(df["PEI_Satisfecho_calc"].mean())
P17 = float(df["P17_Satisfecho_calc"].mean())
PEI_AVG = float(df["PEI_Promedio_P1_P16_calc"].mean())
DELTA_P17 = P17 - PEI
DIMS = dimension_summary(df)
ITEMS_SUM = item_summary(df)
PRIORITY_DIM = DIMS.sort_values("Satisfacción").iloc[0]
STRONG_DIM = DIMS.sort_values("Satisfacción", ascending=False).iloc[0]
PRIORITY_ITEM = ITEMS_SUM.sort_values("Favorable").iloc[0]
STRONG_ITEM = ITEMS_SUM.sort_values("Favorable", ascending=False).iloc[0]


# ==============================================================
# TARJETAS HTML
# ==============================================================
def core_cards() -> str:
    state = signal_state(PEI, REFERENCE_TARGET)
    p17_state = signal_state(P17, REFERENCE_TARGET)
    gap = max(0.0, REFERENCE_TARGET - PEI)
    return f'''
    <div class="core-grid">
      <div class="glass primary-core">
        <div class="core-top">
          <div><div class="core-label">IND. 01 · resultado integral</div><div class="core-name">Porcentaje de estudiantes satisfechos con su proceso de formación académica</div></div>
          <div class="core-tag">Cálculo operativo P1–P16</div>
        </div>
        <div class="core-main">
          <div class="ring" style="--p:{PEI*100:.2f};--ring:{signal_color(state)}"><div class="ring-value">{pct(PEI)}</div><div class="ring-label">satisfacción</div></div>
          <div>
            <div class="core-score">{pct(PEI)}</div>
            <div class="signal-caption">Semáforo de cumplimiento de la meta PEI 2027</div>
            <div class="signal-badge">{traffic_svg(state, 44)} <span style="color:{signal_color(state)}">{escape(signal_label(PEI,REFERENCE_TARGET))}</span></div>
            <div class="core-desc">{N_PEI:,} de {N_TOTAL:,} estudiantes alcanzan un promedio integral P1–P16 de 4 o más. Frente a la meta PEI 2027 de 60%, la brecha es de <b>{pp(gap)}</b>.</div>
            {formula_html(N_PEI, N_TOTAL, PEI)}
            {institutional_scale_html(PEI)}
          </div>
        </div>
        <div class="core-mini">
          <div class="mini-stat"><div class="k">Promedio integral</div><div class="v">{PEI_AVG:.2f} / 5</div><div class="s">Media de P1–P16</div></div>
          <div class="mini-stat"><div class="k">Meta 2027</div><div class="v">60.0%</div><div class="s">Referencia PEI</div></div>
          <div class="mini-stat"><div class="k">Brecha</div><div class="v">{pp(gap)}</div><div class="s">Para alcanzar 60%</div></div>
        </div>
      </div>
      <div class="glass secondary-core">
        <div class="secondary-head"><div><div class="core-label">medida complementaria</div><div class="secondary-title">P17 · satisfacción general declarada</div><div class="secondary-sub">Pregunta directa de percepción global. Se muestra separada del IND.01 integral.</div></div>{traffic_svg(p17_state, 52)}</div>
        <div class="secondary-value">{pct(P17)}</div>
        <div class="signal-caption">Comparación visual frente a la meta 2027</div>
        <div class="signal-badge"><span style="color:{signal_color(p17_state)}">{escape(signal_label(P17,REFERENCE_TARGET))}</span></div>
        {institutional_scale_html(P17)}
        <div class="delta-pill">↔ Diferencia frente al integral: {pp(abs(DELTA_P17))}</div>
        <div class="secondary-bottom"><b>Lectura:</b> P17 es {"mayor" if DELTA_P17>=0 else "menor"} que la medición integral. Esto sugiere distinguir la percepción global espontánea del desempeño conjunto de los 16 aspectos específicos.</div>
      </div>
    </div>
    '''


def dimension_cards() -> str:
    cards = []
    for _, r in DIMS.sort_values("Código").iterrows():
        code = r["Código"]
        meta = DIMENSIONS[code]
        sat = float(r["Satisfacción"])
        avg = float(r["Promedio Likert"])
        gap = max(0.0, REFERENCE_TARGET - sat)
        state = signal_state(sat, REFERENCE_TARGET)
        gap_txt = "Referencia alcanzada" if gap <= 0 else f"Brecha {pp(gap)}"
        cards.append(f'''
        <div class="glass dim-card" style="--accent:{meta['accent']}">
          <div class="dim-head"><div class="dim-code">{meta['icon']} {code}</div>{traffic_svg(state, 34)}</div>
          <div class="dim-name">{escape(meta['name'])}</div>
          <div class="dim-middle"><div><div class="dim-score">{pct(sat)}</div><div class="dim-score-label">estudiantes satisfechos</div></div><div style="font-size:.65rem;font-weight:850;color:{signal_color(state)};text-align:right">{escape(signal_label(sat,REFERENCE_TARGET))}</div></div>
          <div class="dim-progress"><span style="width:{min(100,sat*100):.1f}%"></span></div>
          <div class="dim-foot"><div class="a">Promedio Likert<br><b>{avg:.2f} / 5</b></div><div class="b">{escape(gap_txt)}<br>vs. 60%</div></div>
        </div>''')
    return '<div class="dim-grid">' + ''.join(cards) + '</div>'


def insight_cards() -> str:
    priority = PRIORITY_DIM
    strong = STRONG_DIM
    return f'''
    <div class="insight-grid">
      <div class="glass insight" style="--accent:#FF5C6C"><div class="k">Prioridad dimensional</div><div class="t">{priority['Código']} · {escape(priority['Dimensión'])}</div><div class="x">Registra {pct(float(priority['Satisfacción']))}. Es la dimensión con menor proporción de estudiantes satisfechos.</div></div>
      <div class="glass insight" style="--accent:#2AD49B"><div class="k">Fortaleza relativa</div><div class="t">{strong['Código']} · {escape(strong['Dimensión'])}</div><div class="x">Obtiene {pct(float(strong['Satisfacción']))}, el resultado dimensional más alto del conjunto.</div></div>
      <div class="glass insight" style="--accent:#5B7CFA"><div class="k">Aspecto crítico</div><div class="t">{PRIORITY_ITEM['Ítem']} · {escape(PRIORITY_ITEM['Dimensión'])}</div><div class="x">{escape(PRIORITY_ITEM['Pregunta'])}<br><b>{pct(float(PRIORITY_ITEM['Favorable']))}</b> de valoración favorable.</div></div>
    </div>
    '''


# ==============================================================
# GRÁFICOS BLOQUEADOS (NO PAN / NO ZOOM)
# ==============================================================
def lock_figure(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        height=height,
        autosize=True,
        dragmode=False,
        clickmode="none",
        margin=dict(l=12, r=16, t=34, b=36),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Arial", color="#617185", size=11),
        hoverlabel=dict(bgcolor="white", font_color="#172B42", bordercolor="#D8E1EA"),
    )
    fig.update_xaxes(fixedrange=True, automargin=True, zeroline=False, gridcolor="#EAF0F5")
    fig.update_yaxes(fixedrange=True, automargin=True, zeroline=False, gridcolor="rgba(0,0,0,0)")
    return fig


def dimension_chart() -> go.Figure:
    d = DIMS.sort_values("Código")
    colors = [DIMENSIONS[c]["accent"] for c in d["Código"]]
    fig = go.Figure(go.Bar(
        x=d["Código"], y=d["Satisfacción"], marker_color=colors,
        text=d["Satisfacción"].map(lambda x: f"{x*100:.1f}%"), textposition="outside",
        customdata=d[["Dimensión", "Promedio Likert", "Brecha a 60%"]],
        hovertemplate="<b>%{x}</b><br>%{customdata[0]}<br>Satisfacción: %{y:.1%}<br>Promedio: %{customdata[1]:.2f}<br>Brecha a 60%: %{customdata[2]:.1%}<extra></extra>",
    ))
    fig.add_hline(y=REFERENCE_TARGET, line_dash="dash", line_width=1.5, line_color="#334E68")
    fig.add_annotation(x=3.25, y=REFERENCE_TARGET+0.018, text="Referencia 60%", showarrow=False, font=dict(size=10, color="#334E68"))
    fig.update_yaxes(tickformat=".0%", range=[0, max(.78, float(d["Satisfacción"].max()) + .10)], title=None)
    fig.update_xaxes(title=None, tickfont=dict(size=12))
    fig.update_layout(showlegend=False)
    return lock_figure(fig, 390)


def targets_chart() -> go.Figure:
    years = list(PEI_TARGETS.keys())
    goals = list(PEI_TARGETS.values())
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=goals, mode="lines+markers+text", name="Meta PEI",
        line=dict(width=4, color="#5B7CFA", shape="spline"), marker=dict(size=10, color="#5B7CFA"),
        text=[f"{v*100:.0f}%" for v in goals], textposition="top center",
        hovertemplate="Año %{x}<br>Meta PEI: %{y:.0%}<extra></extra>",
    ))
    fig.add_hline(y=PEI, line_dash="dot", line_width=2, line_color="#FF5C6C")
    fig.add_annotation(x=2030, y=PEI+0.012, text=f"Diagnóstico integral actual {pct(PEI)}", showarrow=False, font=dict(size=10, color="#C83D4C"), xanchor="right")
    fig.update_yaxes(tickformat=".0%", range=[max(0, PEI-.08), .82], title=None)
    fig.update_xaxes(dtick=1, title=None)
    fig.update_layout(showlegend=False)
    return lock_figure(fig, 360)


def item_chart(selected_dim: str = "Todas") -> go.Figure:
    d = ITEMS_SUM.copy()
    if selected_dim != "Todas":
        d = d[d["Dimensión"] == selected_dim]
    d = d.sort_values("Favorable", ascending=True)
    colors = [DIMENSIONS[c]["accent"] for c in d["Dimensión"]]
    fig = go.Figure(go.Bar(
        x=d["Favorable"], y=d["Ítem"], orientation="h", marker_color=colors,
        text=d["Favorable"].map(lambda x: f"{x*100:.1f}%"), textposition="outside",
        customdata=d[["Dimensión", "Pregunta", "Promedio", "Neutral", "Desfavorable"]],
        hovertemplate="<b>%{y} · %{customdata[0]}</b><br>%{customdata[1]}<br>Favorable: %{x:.1%}<br>Neutral: %{customdata[3]:.1%}<br>Desfavorable: %{customdata[4]:.1%}<br>Promedio: %{customdata[2]:.2f}<extra></extra>",
    ))
    fig.update_xaxes(tickformat=".0%", range=[0, 1.10], title=None)
    fig.update_yaxes(title=None, tickfont=dict(size=11))
    fig.update_layout(showlegend=False)
    return lock_figure(fig, max(330, 34 * len(d) + 100))


def likert_chart(selected_dim: str = "Todas") -> go.Figure:
    item_list = ITEMS if selected_dim == "Todas" else DIMENSIONS[selected_dim]["items"]
    rows = []
    for item in item_list:
        s = df[item].dropna()
        rows += [
            {"Ítem": item, "cat": "Desfavorable (1–2)", "p": float((s <= 2).mean())},
            {"Ítem": item, "cat": "Neutral (3)", "p": float((s == 3).mean())},
            {"Ítem": item, "cat": "Favorable (4–5)", "p": float((s >= 4).mean())},
        ]
    d = pd.DataFrame(rows)
    palette = {"Desfavorable (1–2)": "#FF6877", "Neutral (3)": "#B7C1CD", "Favorable (4–5)": "#27B48E"}
    fig = go.Figure()
    for cat in ["Desfavorable (1–2)", "Neutral (3)", "Favorable (4–5)"]:
        x = d[d["cat"] == cat]
        fig.add_trace(go.Bar(x=x["p"], y=x["Ítem"], orientation="h", name=cat, marker_color=palette[cat], hovertemplate=f"<b>%{{y}}</b><br>{cat}: %{{x:.1%}}<extra></extra>"))
    fig.update_layout(barmode="stack", legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=10)))
    fig.update_xaxes(tickformat=".0%", range=[0,1], title=None)
    fig.update_yaxes(autorange="reversed", title=None)
    return lock_figure(fig, max(330, 34 * len(item_list) + 105))


# ==============================================================
# APP
# ==============================================================
hero(N_TOTAL)

tab1, tab2, tab3 = st.tabs(["◉ Visión ejecutiva", "▦ Dimensiones e ítems", "ⓘ Método PEI"])

with tab1:
    section_header("Indicador principal", "Dos lecturas globales, claramente separadas", "El IND.01 integral se calcula con P1–P16; P17 permanece como percepción global complementaria.")
    st.markdown(core_cards(), unsafe_allow_html=True)

    section_header("Diagnóstico 4D", "Satisfacción en las cuatro dimensiones", "Cada dimensión clasifica al estudiante como satisfecho si su promedio de cuatro ítems es ≥4.")
    st.markdown(dimension_cards(), unsafe_allow_html=True)
    st.markdown(
        f'''<div class="glass legend-card"><div class="legend-lights">{traffic_svg('green',28)}{traffic_svg('amber',28)}{traffic_svg('red',28)}</div><div class="legend-text"><b>Dos lecturas distintas:</b> el semáforo conserva <b>3 luces</b> (verde, ámbar y rojo) porque representa el cumplimiento de la meta PEI. La <b>escala institucional</b> se muestra aparte con <b>4 categorías</b>: Insatisfactorio, Regular, Satisfactorio y Muy satisfactorio. Así no se mezclan meta y nivel de satisfacción.</div></div>''',
        unsafe_allow_html=True,
    )

    section_header("Lectura automática", "Qué requiere atención y qué funciona mejor")
    st.markdown(insight_cards(), unsafe_allow_html=True)

    c1, c2 = st.columns([1.08, .92], gap="medium")
    with c1:
        section_header("Comparación", "Resultado por dimensión")
        st.plotly_chart(dimension_chart(), use_container_width=True, config=LOCKED_PLOT_CONFIG)
    with c2:
        section_header("Ruta estratégica", "Metas PEI 2027–2030")
        st.plotly_chart(targets_chart(), use_container_width=True, config=LOCKED_PLOT_CONFIG)

with tab2:
    section_header("Explorador", "Dimensiones e ítems sin gráficos que se desplacen", "Los ejes están bloqueados: tocar o arrastrar no hace zoom ni mueve el gráfico.")
    selected = st.selectbox(
        "Dimensión a analizar",
        ["Todas", "D1", "D2", "D3", "D4"],
        format_func=lambda x: "Todas las dimensiones · P1–P16" if x == "Todas" else f"{x} · {DIMENSIONS[x]['name']}",
        label_visibility="collapsed",
    )

    section_header("Valoración favorable", "Aspectos ordenados de menor a mayor", "En celular se muestran solo códigos P1–P16; el texto completo aparece al tocar el dato, sin mover el gráfico.")
    st.plotly_chart(item_chart(selected), use_container_width=True, config=LOCKED_PLOT_CONFIG)

    section_header("Distribución Likert", "Desfavorable · neutral · favorable")
    st.plotly_chart(likert_chart(selected), use_container_width=True, config=LOCKED_PLOT_CONFIG)

    dshow = ITEMS_SUM.copy() if selected == "Todas" else ITEMS_SUM[ITEMS_SUM["Dimensión"] == selected].copy()
    dshow = dshow.sort_values("Favorable")
    table = dshow[["Ítem", "Dimensión", "Pregunta", "Favorable", "Neutral", "Desfavorable", "Promedio"]].copy()
    table["Favorable"] = table["Favorable"].map(lambda x: f"{x*100:.1f}%")
    table["Neutral"] = table["Neutral"].map(lambda x: f"{x*100:.1f}%")
    table["Desfavorable"] = table["Desfavorable"].map(lambda x: f"{x*100:.1f}%")
    table["Promedio"] = table["Promedio"].map(lambda x: f"{x:.2f}")
    st.dataframe(table, use_container_width=True, hide_index=True, height=min(620, 45 + 36*len(table)))

with tab3:
    section_header("Ficha PEI", "Cómo está interpretado el indicador en este dashboard")
    st.markdown(
        '''<div class="method-grid">
          <div class="glass method"><div class="i">◎</div><div class="t">Definición oficial</div><div class="x">IND. 01: porcentaje de estudiantes de pregrado satisfechos con su proceso de formación académica. Fórmula: <b>(N/D) × 100</b>.</div></div>
          <div class="glass method"><div class="i">∑</div><div class="t">Operacionalización propuesta</div><div class="x">Para convertir P1–P16 en N, el dashboard calcula el promedio integral de los 16 ítems por estudiante y lo clasifica como satisfecho cuando el promedio es <b>≥4</b>.</div></div>
          <div class="glass method"><div class="i">↔</div><div class="t">P17 queda separado</div><div class="x">P17 es una pregunta directa de satisfacción general. Se usa para contraste y validación de percepción, no se mezcla automáticamente con el IND.01 integral.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown(
        '''<div class="notice"><b>Importante metodológicamente:</b> la ficha técnica compartida define N, D y el nivel “satisfecho”, pero no especifica en la imagen el algoritmo exacto para combinar varios ítems de la encuesta. Por eso, <b>promedio P1–P16 ≥4</b> se presenta aquí como una <b>operacionalización analítica propuesta</b>. Antes de reportarlo como resultado PEI oficial, conviene dejar este criterio aprobado en el protocolo, resolución o ficha metodológica del instrumento.</div>''',
        unsafe_allow_html=True,
    )

    section_header("Estructura del instrumento", "Qué aporta cada bloque")
    method_cards = []
    for code, meta in DIMENSIONS.items():
        method_cards.append(f'''<div class="glass method"><div class="i">{meta['icon']}</div><div class="t">{code} · {escape(meta['short'])}</div><div class="x">{', '.join(meta['items'])}. Diagnóstico dimensional del proceso formativo. Un estudiante se clasifica como satisfecho en la dimensión si el promedio de sus cuatro respuestas es ≥4.</div></div>''')
    st.markdown('<div class="method-grid">' + ''.join(method_cards[:3]) + '</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:12px"></div><div class="method-grid">' + method_cards[3] + f'''<div class="glass method"><div class="i">◉</div><div class="t">IND.01 integral · P1–P16</div><div class="x">Promedio del estudiante en los 16 ítems. Si es ≥4, ingresa al numerador N. Resultado actual del archivo: <b>{pct(PEI)}</b>.</div></div><div class="glass method"><div class="i">●</div><div class="t">P17 · satisfacción declarada</div><div class="x">Pregunta global complementaria. Resultado actual: <b>{pct(P17)}</b>. Se reporta aparte para no confundir dos constructos de medición.</div></div></div>''', unsafe_allow_html=True)

    section_header("Metas", "Línea esperada de logro PEI")
    targets_df = pd.DataFrame({"Año": list(PEI_TARGETS.keys()), "Meta": [f"{v*100:.0f}%" for v in PEI_TARGETS.values()]})
    st.dataframe(targets_df, use_container_width=True, hide_index=True)

