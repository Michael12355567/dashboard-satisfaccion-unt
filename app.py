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
    page_title="UNT | Tablero ejecutivo PEI",
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
        "accent": "#2F66D8",
        "soft": "#EAF1FF",
        "icon": "▦",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "short": "Docencia y pedagogía",
        "items": ["P5", "P6", "P7", "P8"],
        "accent": "#7C5CE7",
        "soft": "#F1ECFF",
        "icon": "✦",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "short": "Servicios y gestión",
        "items": ["P9", "P10", "P11", "P12"],
        "accent": "#F07B46",
        "soft": "#FFF0E9",
        "icon": "▣",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "short": "Formación integral",
        "items": ["P13", "P14", "P15", "P16"],
        "accent": "#12A77C",
        "soft": "#E8F8F3",
        "icon": "◆",
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

PEI_TARGETS = {2027: 0.60, 2028: 0.65, 2029: 0.70, 2030: 0.75}
REFERENCE_TARGET = PEI_TARGETS[2027]
WATCH_BAND_PP = 0.05
STATIC_PLOT = {
    "displayModeBar": False,
    "responsive": True,
    "staticPlot": True,
    "scrollZoom": False,
}

# ==============================================================
# ESTILO — inspirado en panel ejecutivo institucional
# ==============================================================
st.markdown(
    r"""
<style>
:root{
  --bg:#F3F6FB;
  --paper:#FFFFFF;
  --ink:#17304F;
  --muted:#718096;
  --line:#E5EBF4;
  --blue:#2B5CC7;
  --blue2:#376DE6;
  --navy:#183E79;
  --cyan:#12AFC0;
  --green:#16B36E;
  --amber:#F6AD36;
  --red:#E75E68;
  --shadow:0 14px 34px rgba(35,72,130,.10), 0 2px 7px rgba(35,72,130,.05);
  --shadow-hover:0 20px 42px rgba(35,72,130,.15),0 4px 12px rgba(35,72,130,.06);
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"Segoe UI Variable","Aptos","Segoe UI",Inter,Arial,sans-serif}
.stApp{background:linear-gradient(180deg,#F7F9FC 0%,#EEF3F9 100%);color:var(--ink)}
.block-container{max-width:1500px;padding:0.55rem 1rem 3rem}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:rgba(247,249,252,.88);backdrop-filter:blur(14px)}
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}

/* BARRA SUPERIOR */
.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:16px;
  min-height:64px;padding:11px 18px;border-radius:16px;
  background:linear-gradient(100deg,#244DA9 0%,#2B5CCA 52%,#376DE7 100%);
  color:#fff;box-shadow:0 12px 24px rgba(37,82,176,.22);position:relative;overflow:hidden
}
.topbar:after{content:"";position:absolute;width:260px;height:260px;border-radius:50%;right:-90px;top:-150px;border:32px solid rgba(255,255,255,.07)}
.brand{display:flex;align-items:center;gap:12px;position:relative;z-index:1}
.brandmark{width:43px;height:43px;border-radius:12px;background:linear-gradient(145deg,#fff,#EDF3FF);display:grid;place-items:center;color:#2A58C1;font-size:.78rem;font-weight:950;box-shadow:0 6px 12px rgba(10,33,89,.22),inset 0 1px 0 #fff}
.brand-title{font-size:.93rem;font-weight:900;line-height:1.1;letter-spacing:-.01em}
.brand-sub{font-size:.59rem;opacity:.80;margin-top:3px;letter-spacing:.06em;text-transform:uppercase;font-weight:750}
.top-meta{display:flex;gap:9px;flex-wrap:wrap;justify-content:flex-end;position:relative;z-index:1}
.top-pill{font-size:.61rem;font-weight:800;padding:7px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.10);backdrop-filter:blur(8px)}

/* CABECERA DE PÁGINA */
.page-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-end;margin:22px 2px 15px}
.page-kicker{font-size:.61rem;letter-spacing:.15em;text-transform:uppercase;font-weight:900;color:#3568CF}
.page-title{font-size:clamp(1.42rem,3vw,2.05rem);font-weight:950;letter-spacing:-.045em;color:#17304F;line-height:1.04;margin-top:5px}
.page-sub{font-size:.76rem;color:#78869A;margin-top:7px;line-height:1.45;max-width:900px}
.page-badge{min-width:145px;padding:11px 13px;border-radius:15px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);font-size:.61rem;color:#79879A}
.page-badge b{display:block;color:#193551;font-size:.82rem;margin-top:2px}

/* TABS */
.stTabs [data-baseweb="tab-list"]{gap:6px;background:transparent;border-bottom:1px solid #DCE5F1;padding:0;margin-top:0;overflow-x:auto;white-space:nowrap}
.stTabs [data-baseweb="tab"]{height:44px;border-radius:10px 10px 0 0;padding:0 14px;color:#68788D;font-weight:850;font-size:.75rem;flex:0 0 auto}
.stTabs [aria-selected="true"]{background:#fff!important;color:#2657BA!important;box-shadow:0 -1px 0 #fff,0 4px 16px rgba(47,95,188,.08)!important;border:1px solid #E3EAF4;border-bottom-color:#fff}
.stTabs [data-baseweb="tab-highlight"]{height:3px;background:#2F66D8;border-radius:4px 4px 0 0}

/* BANNER EJECUTIVO */
.status-banner{position:relative;overflow:hidden;display:grid;grid-template-columns:minmax(0,1.35fr) minmax(400px,.65fr);gap:18px;align-items:center;padding:21px 24px;border-radius:20px;background:linear-gradient(112deg,#1F4CA7 0%,#285BC5 53%,#376BE4 100%);color:#fff;box-shadow:0 16px 34px rgba(37,83,177,.20)}
.status-banner:after{content:"";position:absolute;width:320px;height:320px;border-radius:50%;right:-100px;top:-185px;border:28px solid rgba(255,255,255,.07)}
.status-main{display:grid;grid-template-columns:88px minmax(0,1fr);gap:17px;align-items:center;position:relative;z-index:1}
.status-icon{width:88px;height:88px;border-radius:22px;background:linear-gradient(145deg,rgba(255,255,255,.28),rgba(255,255,255,.10));border:1px solid rgba(255,255,255,.20);display:grid;place-items:center;box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 9px 20px rgba(14,42,111,.24);font-size:2rem}
.status-eyebrow{font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;font-weight:900;color:#C9DBFF}
.status-title{font-size:clamp(1.1rem,2.4vw,1.5rem);font-weight:950;letter-spacing:-.03em;margin-top:4px;line-height:1.15}
.status-text{font-size:.68rem;line-height:1.45;color:#E0E9FF;margin-top:6px;max-width:720px}
.status-side{display:grid;grid-template-columns:1fr auto;gap:15px;align-items:center;position:relative;z-index:1;border-left:1px solid rgba(255,255,255,.16);padding-left:18px}
.status-value{font-size:clamp(2.1rem,4vw,3.05rem);font-weight:950;letter-spacing:-.065em;line-height:.95}
.status-state{font-size:.69rem;font-weight:850;margin-top:6px;color:#E9F1FF}
.status-mini{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.status-mini>div{padding:8px 9px;border-radius:10px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.12)}
.status-mini .k{font-size:.49rem;text-transform:uppercase;letter-spacing:.08em;color:#C7D7FA;font-weight:900}
.status-mini .v{font-size:.74rem;font-weight:900;margin-top:2px}

/* SEMÁFORO */
.signal-shell{filter:drop-shadow(0 8px 10px rgba(10,26,40,.25))}
.signal-inline{display:inline-flex;align-items:center;gap:7px;font-size:.62rem;font-weight:850}

/* KPI */
.kpi-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:11px;margin-top:14px}
.kpi{position:relative;overflow:hidden;padding:14px 14px 12px;border-radius:16px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);min-height:126px;transition:.18s ease}
.kpi:hover{transform:translateY(-2px);box-shadow:var(--shadow-hover)}
.kpi:after{content:"";position:absolute;right:-22px;top:-25px;width:76px;height:76px;border-radius:24px;background:var(--soft);transform:rotate(18deg);opacity:.72}
.kpi-top{display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:1}
.kpi-label{font-size:.57rem;color:#7D8A9B;font-weight:850;line-height:1.25}
.kpi-icon{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;background:linear-gradient(145deg,var(--accent),color-mix(in srgb,var(--accent) 73%,#fff));color:white;font-size:1rem;font-weight:900;box-shadow:0 7px 14px color-mix(in srgb,var(--accent) 24%,transparent),inset 0 1px 0 rgba(255,255,255,.28);position:relative;z-index:2}
.kpi-value{font-size:1.35rem;font-weight:950;color:#18324F;letter-spacing:-.045em;margin-top:7px;position:relative;z-index:1}
.kpi-foot{display:flex;justify-content:space-between;gap:6px;align-items:center;margin-top:8px;font-size:.53rem;color:#7A8999;position:relative;z-index:1}
.kpi-track{height:5px;border-radius:99px;background:#EDF1F6;overflow:hidden;margin-top:8px;position:relative;z-index:1}
.kpi-track span{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 65%,#79DCE4))}

/* TITULOS DE SECCIÓN */
.section-head{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;margin:1.35rem 2px .7rem}
.section-title-wrap .k{font-size:.57rem;text-transform:uppercase;letter-spacing:.13em;font-weight:900;color:#3568CF}
.section-title-wrap .t{font-size:1.02rem;font-weight:950;color:#18324F;letter-spacing:-.02em;margin-top:3px}
.section-note{font-size:.61rem;color:#8592A2;text-align:right;max-width:540px;line-height:1.35}

/* PANELES */
.panel{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);padding:16px;position:relative;overflow:hidden}
.panel-head{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;margin-bottom:13px}
.panel-title{font-size:.76rem;font-weight:950;color:#1C3652}
.panel-sub{font-size:.56rem;color:#8995A4;margin-top:3px;line-height:1.35}
.panel-tag{font-size:.53rem;font-weight:850;padding:5px 7px;border-radius:8px;background:#F4F7FC;color:#63748A;border:1px solid #E6ECF4;white-space:nowrap}

/* DIMENSIONES SALUD */
.health-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.health-card{padding:15px 14px;border-radius:17px;background:linear-gradient(145deg,#FFFFFF 0%,#F9FBFE 100%);border:1px solid var(--line);box-shadow:var(--shadow);position:relative;overflow:hidden;min-height:220px}
.health-card:before{content:"";position:absolute;left:0;top:0;right:0;height:4px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 52%,#7DD9E1))}
.health-head{display:flex;align-items:center;justify-content:space-between;gap:9px}
.health-code{display:flex;align-items:center;gap:7px;font-size:.66rem;font-weight:950;color:var(--accent)}
.health-name{font-size:.61rem;color:#7E8C9B;line-height:1.3;margin-top:5px;min-height:2.4em}
.health-body{display:grid;grid-template-columns:105px minmax(0,1fr);align-items:center;gap:9px;margin-top:10px}
.health-ring{--p:0;--accent:#2F66D8;width:100px;height:100px;border-radius:50%;background:conic-gradient(var(--accent) calc(var(--p)*1%),#EAF0F6 0);display:grid;place-items:center;position:relative;box-shadow:0 10px 18px rgba(30,58,95,.11),inset 0 1px 0 #fff}
.health-ring:after{content:"";position:absolute;inset:11px;border-radius:50%;background:linear-gradient(145deg,#fff,#F6F9FC);box-shadow:inset 3px 3px 7px rgba(25,44,72,.05)}
.health-ring b{position:relative;z-index:1;font-size:1.14rem;color:#18324F;letter-spacing:-.04em}
.health-info .state{font-size:.59rem;font-weight:900;margin-top:6px}
.health-info .avg{font-size:.54rem;color:#7D8B9A;margin-top:5px;line-height:1.4}
.health-foot{display:flex;justify-content:space-between;align-items:center;gap:8px;border-top:1px solid #EDF1F5;margin-top:10px;padding-top:9px;font-size:.53rem;color:#7B8999}
.health-foot b{color:#2B425A}

/* GRID PRINCIPAL */
.main-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(330px,.85fr);gap:13px}

/* INSIGHTS */
.insight-stack{display:grid;gap:9px}
.insight-card{display:grid;grid-template-columns:39px 1fr auto;gap:10px;align-items:center;padding:11px;border-radius:13px;border:1px solid #E7EDF5;background:#FBFCFE}
.insight-icon{width:39px;height:39px;border-radius:11px;display:grid;place-items:center;background:var(--soft);color:var(--accent);font-weight:950}
.insight-name{font-size:.64rem;font-weight:900;color:#1F3954}
.insight-desc{font-size:.53rem;color:#8592A2;margin-top:2px;line-height:1.3}
.insight-val{font-size:.85rem;font-weight:950;color:#1C3652;text-align:right}

/* RUTA PEI */
.road{display:grid;gap:10px;margin-top:4px}
.road-row{display:grid;grid-template-columns:48px minmax(0,1fr) 58px;align-items:center;gap:9px}
.road-year{font-size:.59rem;font-weight:950;color:#38526E}
.road-track{height:11px;border-radius:99px;background:#EDF2F8;overflow:hidden;box-shadow:inset 0 2px 4px rgba(27,54,86,.07)}
.road-track span{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#2F66D8,#18A9C3)}
.road-goal{font-size:.61rem;font-weight:950;color:#244C9F;text-align:right}

/* SELECTOR */
div[data-baseweb="select"]>div{border-radius:12px!important;border-color:#DDE5EF!important;background:#fff!important;box-shadow:0 6px 15px rgba(34,67,112,.05)!important}

/* DIMENSION DETALLE */
.dimension-banner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;padding:17px 18px;border-radius:18px;background:linear-gradient(115deg,var(--soft),#fff);border:1px solid color-mix(in srgb,var(--accent) 18%,#E1E8F1);box-shadow:var(--shadow);position:relative;overflow:hidden}
.dimension-banner:after{content:"";position:absolute;right:-65px;top:-80px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--accent) 15%,transparent),transparent 68%)}
.dimension-banner .code{font-size:.59rem;text-transform:uppercase;letter-spacing:.12em;font-weight:950;color:var(--accent)}
.dimension-banner .name{font-size:1.03rem;font-weight:950;color:#18324F;margin-top:4px}
.dimension-banner .desc{font-size:.61rem;color:#738298;line-height:1.4;margin-top:5px;max-width:800px}
.dimension-banner .score{display:flex;align-items:center;gap:11px;position:relative;z-index:1}
.dimension-banner .big{font-size:1.85rem;font-weight:950;color:#18324F;letter-spacing:-.05em;text-align:right}
.dimension-banner .small{font-size:.52rem;color:#7A899A;text-align:right;margin-top:2px}

/* ITEMS */
.item-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px}
.item-card{padding:14px;border-radius:16px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);position:relative;overflow:hidden;min-height:190px}
.item-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}
.item-top{display:flex;justify-content:space-between;gap:8px;align-items:center}
.item-code{font-size:.63rem;font-weight:950;color:var(--accent);background:var(--soft);border-radius:8px;padding:4px 7px}
.item-score{font-size:1.18rem;font-weight:950;color:#18324F;letter-spacing:-.04em}
.item-question{font-size:.58rem;color:#6F7F92;line-height:1.4;margin-top:9px;min-height:4.2em}
.item-meter{height:8px;border-radius:99px;background:#EDF2F7;margin-top:10px;overflow:hidden;box-shadow:inset 0 2px 4px rgba(27,54,86,.07)}
.item-meter span{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 58%,#78D9DF))}
.item-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:10px}
.item-stat{padding:6px 5px;border-radius:8px;background:#F7F9FC;text-align:center;border:1px solid #EBF0F5}
.item-stat .k{font-size:.44rem;color:#8A96A5;text-transform:uppercase;font-weight:850}
.item-stat .v{font-size:.57rem;color:#344C65;font-weight:950;margin-top:2px}

/* MAPA DE CALOR */
.heatmap{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.heat-cell{min-height:116px;padding:12px;border-radius:15px;border:1px solid color-mix(in srgb,var(--accent) 18%,#E5EBF2);background:linear-gradient(145deg,#fff,color-mix(in srgb,var(--accent) 7%,#fff));box-shadow:0 9px 20px rgba(37,65,102,.07);position:relative;overflow:hidden}
.heat-cell:after{content:"";position:absolute;right:-28px;bottom:-32px;width:80px;height:80px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--accent) calc(var(--strength)*1%),transparent),transparent 70%)}
.heat-cell .hcode{font-size:.58rem;font-weight:950;color:var(--accent)}
.heat-cell .hpct{font-size:1.15rem;font-weight:950;color:#18324F;margin-top:5px}
.heat-cell .hq{font-size:.49rem;line-height:1.32;color:#7B8999;margin-top:5px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.heat-cell .hbar{height:5px;border-radius:99px;background:#EAEFF4;margin-top:8px;overflow:hidden}
.heat-cell .hbar span{display:block;height:100%;background:var(--accent);border-radius:99px}

/* LIKERT CARDS */
.likert-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.likert-card{padding:12px;border-radius:15px;background:#fff;border:1px solid var(--line);box-shadow:0 8px 18px rgba(37,65,102,.06)}
.likert-card .head{display:flex;justify-content:space-between;gap:8px;align-items:center}
.likert-card .head b{font-size:.61rem;color:#233E59}
.likert-card .seg{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:9px}
.likert-card .seg>div{padding:7px 4px;border-radius:9px;text-align:center}
.likert-card .seg .bad{background:#FFF0F2;color:#B84955}.likert-card .seg .neu{background:#F0F3F6;color:#657587}.likert-card .seg .good{background:#EAF8F3;color:#18815F}
.likert-card .seg .k{font-size:.43rem;text-transform:uppercase;font-weight:900}.likert-card .seg .v{font-size:.62rem;font-weight:950;margin-top:2px}

/* FORMULA */
.formula-card{display:grid;grid-template-columns:minmax(0,1fr) minmax(270px,.62fr);gap:15px;padding:18px;border-radius:18px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow)}
.formula-box{padding:15px;border-radius:15px;background:linear-gradient(145deg,#F6F9FF,#EDF3FF);border:1px solid #DDE7FA;text-align:center}
.formula-label{font-size:.57rem;text-transform:uppercase;letter-spacing:.12em;color:#6680A6;font-weight:900}
.formula-main{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:10px;color:#18324F;font-weight:950}
.frac{display:inline-grid;grid-template-rows:auto 1px auto;min-width:74px;text-align:center;font-size:1rem}.frac i{height:1px;background:#25456A;margin:4px 0}.formula-res{font-size:1.45rem;color:#2B5CCA;padding:6px 9px;border-radius:10px;background:#fff;border:1px solid #DDE6F6;box-shadow:0 6px 14px rgba(41,89,188,.08)}
.formula-defs{display:grid;gap:8px}.formula-def{padding:10px 11px;border-radius:11px;background:#F9FBFD;border:1px solid #E9EEF4;font-size:.58rem;color:#728195;line-height:1.4}.formula-def b{color:#213A55}

/* NIVEL 4 CATEGORÍAS */
.level4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.level-step{padding:11px 7px;border-radius:12px;border:1px solid #E5EBF2;background:#fff;text-align:center;opacity:.48;position:relative}
.level-step.active{opacity:1;box-shadow:0 9px 18px rgba(34,62,100,.09);transform:translateY(-1px);border-color:var(--lvl)}
.level-dot{width:11px;height:11px;border-radius:50%;margin:0 auto 6px;background:var(--lvl);box-shadow:0 2px 6px color-mix(in srgb,var(--lvl) 30%,transparent)}
.level-name{font-size:.52rem;font-weight:950;color:#3A5068}.level-range{font-size:.47rem;color:#8A96A4;margin-top:2px}

/* MÉTODO */
.method-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}
.method{padding:14px;border-radius:15px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);min-height:145px}
.method-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:#EDF3FF;color:#2F66D8;font-weight:950}
.method-title{font-size:.66rem;font-weight:950;color:#1E3853;margin-top:9px}.method-text{font-size:.56rem;color:#7B8999;line-height:1.42;margin-top:5px}
.notice{padding:12px 14px;border-radius:13px;background:#FFF9EC;border:1px solid #F5E3B8;color:#755F2A;font-size:.58rem;line-height:1.45}

/* DATAFRAME */
[data-testid="stDataFrame"]{border:1px solid #E4EAF2;border-radius:14px;overflow:hidden;box-shadow:0 8px 18px rgba(38,65,104,.05)}

/* RESPONSIVE */
@media(max-width:1180px){
  .kpi-grid{grid-template-columns:repeat(3,1fr)}
  .health-grid{grid-template-columns:repeat(2,1fr)}
  .item-grid,.heatmap,.likert-grid{grid-template-columns:repeat(2,1fr)}
  .status-banner{grid-template-columns:1fr}.status-side{border-left:0;border-top:1px solid rgba(255,255,255,.16);padding-left:0;padding-top:14px}
}
@media(max-width:760px){
  .block-container{padding:.45rem .62rem 2rem}
  .topbar{border-radius:13px;padding:9px 11px}.brandmark{width:36px;height:36px}.brand-title{font-size:.78rem}.brand-sub{font-size:.49rem}.top-meta{display:none}
  .page-head{align-items:flex-start;margin-top:16px}.page-badge{display:none}.page-title{font-size:1.36rem}.page-sub{font-size:.67rem}
  .status-banner{padding:15px;border-radius:16px}.status-main{grid-template-columns:58px 1fr;gap:11px}.status-icon{width:58px;height:58px;border-radius:15px;font-size:1.35rem}.status-side{grid-template-columns:1fr auto}.status-mini{grid-template-columns:1fr 1fr 1fr;gap:5px}.status-mini>div{padding:7px 6px}.status-value{font-size:2rem}
  .kpi-grid{grid-template-columns:repeat(2,1fr);gap:8px}.kpi{min-height:115px;padding:12px}.kpi-icon{width:33px;height:33px}.kpi-value{font-size:1.16rem}
  .health-grid{grid-template-columns:1fr}.health-card{min-height:180px}.health-body{grid-template-columns:92px 1fr}.health-ring{width:88px;height:88px}
  .main-grid{grid-template-columns:1fr}.section-note{display:none}
  .item-grid,.heatmap,.likert-grid{grid-template-columns:1fr}
  .dimension-banner{grid-template-columns:1fr}.dimension-banner .score{justify-content:space-between}.dimension-banner .big,.dimension-banner .small{text-align:left}
  .formula-card{grid-template-columns:1fr}.level4{grid-template-columns:repeat(2,1fr)}.method-grid{grid-template-columns:1fr}
  .stTabs [data-baseweb="tab"]{font-size:.67rem;padding:0 10px}
}
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================
# UTILIDADES
# ==============================================================
def pct(x: float, digits: int = 1) -> str:
    return "—" if pd.isna(x) else f"{x*100:.{digits}f}%"


def pp(x: float, digits: int = 1) -> str:
    return f"{x*100:.{digits}f} pp"


def signal_state(value: float, target: float = REFERENCE_TARGET) -> str:
    if pd.isna(value):
        return "off"
    gap = target - value
    if gap <= 0:
        return "green"
    if gap <= WATCH_BAND_PP:
        return "amber"
    return "red"


def signal_label(value: float, target: float = REFERENCE_TARGET) -> str:
    return {
        "green": "Cumple la meta",
        "amber": "En vigilancia",
        "red": "Brecha prioritaria",
        "off": "Sin dato",
    }[signal_state(value, target)]


def signal_color(state: str) -> str:
    return {"green":"#16B36E","amber":"#F6AD36","red":"#E75E68","off":"#A7B1BE"}[state]


def institutional_level(value: float) -> tuple[str, str, str, str]:
    if pd.isna(value):
        return ("Sin dato", "—", "#A7B1BE", "off")
    if value < .60:
        return ("Insatisfactorio", "0–59%", "#E75E68", "low")
    if value < .75:
        return ("Regular", "60–74%", "#F6AD36", "regular")
    if value < .90:
        return ("Satisfactorio", "75–89%", "#16B36E", "good")
    return ("Muy satisfactorio", "90–100%", "#12AFC0", "excellent")


def traffic_svg(state: str, size: int = 48) -> str:
    active = {
        "red": (1.0,.16,.16), "amber": (.16,1.0,.16), "green": (.16,.16,1.0), "off": (.16,.16,.16)
    }[state]
    return f'''<svg class="signal-shell" width="{size}" height="{int(size*1.62)}" viewBox="0 0 70 114" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="case" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#3D5061"/><stop offset=".5" stop-color="#172631"/><stop offset="1" stop-color="#070C11"/></linearGradient>
        <radialGradient id="r"><stop offset="0" stop-color="#FFABB2"/><stop offset=".45" stop-color="#FF4B5C"/><stop offset="1" stop-color="#9D1727"/></radialGradient>
        <radialGradient id="a"><stop offset="0" stop-color="#FFE4A7"/><stop offset=".45" stop-color="#FFB326"/><stop offset="1" stop-color="#A85A00"/></radialGradient>
        <radialGradient id="g"><stop offset="0" stop-color="#A3F3D2"/><stop offset=".45" stop-color="#1FC58C"/><stop offset="1" stop-color="#08724F"/></radialGradient>
        <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <rect x="8" y="3" width="54" height="106" rx="19" fill="url(#case)" stroke="#516779" stroke-width="1.4"/>
      <rect x="14" y="9" width="42" height="94" rx="14" fill="#0A1117" opacity=".86"/>
      <circle cx="35" cy="27" r="13" fill="url(#r)" opacity="{active[0]}" {'filter="url(#glow)"' if state=='red' else ''}/>
      <circle cx="35" cy="56" r="13" fill="url(#a)" opacity="{active[1]}" {'filter="url(#glow)"' if state=='amber' else ''}/>
      <circle cx="35" cy="85" r="13" fill="url(#g)" opacity="{active[2]}" {'filter="url(#glow)"' if state=='green' else ''}/>
      <ellipse cx="30" cy="22" rx="4.5" ry="2.4" fill="white" opacity=".35"/><ellipse cx="30" cy="51" rx="4.5" ry="2.4" fill="white" opacity=".35"/><ellipse cx="30" cy="80" rx="4.5" ry="2.4" fill="white" opacity=".35"/>
    </svg>'''


def level4_html(value: float) -> str:
    _, _, _, key = institutional_level(value)
    levels = [
        ("low","Insatisfactorio","0–59%","#E75E68"),
        ("regular","Regular","60–74%","#F6AD36"),
        ("good","Satisfactorio","75–89%","#16B36E"),
        ("excellent","Muy satisfactorio","90–100%","#12AFC0"),
    ]
    html=[]
    for k,name,rng,c in levels:
        active=" active" if k==key else ""
        html.append(f'<div class="level-step{active}" style="--lvl:{c}"><div class="level-dot"></div><div class="level-name">{name}</div><div class="level-range">{rng}</div></div>')
    return '<div class="level4">'+''.join(html)+'</div>'


def section_header(kicker: str, title: str, note: str = "") -> None:
    st.markdown(
        f'<div class="section-head"><div class="section-title-wrap"><div class="k">{escape(kicker)}</div><div class="t">{escape(title)}</div></div><div class="section-note">{escape(note)}</div></div>',
        unsafe_allow_html=True,
    )

# ==============================================================
# DATOS
# ==============================================================
def require_columns(df: pd.DataFrame) -> None:
    required = {f"P{i}" for i in range(1,18)}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError("Faltan columnas obligatorias: "+", ".join(missing))


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy(); require_columns(df)
    for c in [f"P{i}" for i in range(1,18)]:
        df[c]=pd.to_numeric(df[c],errors="coerce")
    # Misma lógica analítica ya acordada: P1–P16 integral y P17 separado.
    df["PEI_Promedio_P1_P16_calc"] = df[ITEMS].mean(axis=1,skipna=True)
    df["PEI_Satisfecho_calc"] = (df["PEI_Promedio_P1_P16_calc"]>=4).astype(float)
    df["P17_Satisfecho_calc"] = (df["P17"]>=4).astype(float)
    for code,meta in DIMENSIONS.items():
        df[f"{code}_Promedio_calc"] = df[meta["items"]].mean(axis=1,skipna=True)
        df[f"{code}_Satisfecho_calc"] = (df[f"{code}_Promedio_calc"]>=4).astype(float)
    return df


@st.cache_data(show_spinner=False)
def load_data(path: str, mtime: float) -> pd.DataFrame:
    return prepare_data(pd.read_excel(path,sheet_name=SHEET_NAME))


def dimension_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for code,meta in DIMENSIONS.items():
        sat=float(df[f"{code}_Satisfecho_calc"].mean())
        avg=float(df[f"{code}_Promedio_calc"].mean())
        rows.append({"Código":code,"Dimensión":meta["name"],"Satisfacción":sat,"Promedio":avg,"Brecha":max(0,REFERENCE_TARGET-sat)})
    return pd.DataFrame(rows)


def item_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for i in range(1,17):
        item=f"P{i}"; s=df[item].dropna(); code=f"D{((i-1)//4)+1}"
        rows.append({
            "Ítem":item,"Dimensión":code,"Pregunta":ITEM_TEXT[item],"Promedio":float(s.mean()),
            "Favorable":float((s>=4).mean()),"Neutral":float((s==3).mean()),"Desfavorable":float((s<=2).mean())
        })
    return pd.DataFrame(rows)


if not DATA_FILE.exists():
    st.error("No se encontró basededatos.xlsx junto a app.py.")
    st.stop()
try:
    df=load_data(str(DATA_FILE),DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"No pude leer basededatos.xlsx: {exc}")
    st.stop()

N_TOTAL=int(len(df)); N_PEI=int(df["PEI_Satisfecho_calc"].sum())
PEI=float(df["PEI_Satisfecho_calc"].mean()); P17=float(df["P17_Satisfecho_calc"].mean())
PEI_AVG=float(df["PEI_Promedio_P1_P16_calc"].mean())
DIMS=dimension_summary(df); ITEMS_SUM=item_summary(df)
PRIORITY_DIM=DIMS.sort_values("Satisfacción").iloc[0]
STRONG_DIM=DIMS.sort_values("Satisfacción",ascending=False).iloc[0]
PRIORITY_ITEM=ITEMS_SUM.sort_values("Favorable").iloc[0]
STRONG_ITEM=ITEMS_SUM.sort_values("Favorable",ascending=False).iloc[0]

# ==============================================================
# COMPONENTES HTML
# ==============================================================
def topbar() -> str:
    return '''<div class="topbar"><div class="brand"><div class="brandmark">UNT</div><div><div class="brand-title">Tablero Ejecutivo de Satisfacción Académica</div><div class="brand-sub">Universidad Nacional de Trujillo · IND.01 · OEI.01</div></div></div><div class="top-meta"><span class="top-pill">PEI 2026–2030</span><span class="top-pill">Meta 2027 · 60%</span><span class="top-pill">Monitoreo institucional</span></div></div>'''


def page_header() -> str:
    return f'''<div class="page-head"><div><div class="page-kicker">Centro de control · indicador institucional</div><div class="page-title">Satisfacción con el proceso de formación académica</div><div class="page-sub">Lectura ejecutiva del IND.01, diagnóstico de las cuatro dimensiones y contraste con la percepción global de P17. El tablero utiliza el archivo institucional cargado en el repositorio.</div></div><div class="page-badge">Registros analizados<b>{N_TOTAL:,} estudiantes</b></div></div>'''


def status_banner() -> str:
    state=signal_state(PEI); gap=max(0,REFERENCE_TARGET-PEI)
    return f'''<div class="status-banner"><div class="status-main"><div class="status-icon">▥</div><div><div class="status-eyebrow">Estado del indicador · IND.01</div><div class="status-title">Porcentaje de estudiantes satisfechos con su formación académica integral</div><div class="status-text">Resultado integral calculado con P1–P16. El semáforo muestra cumplimiento frente a la meta PEI 2027; el nivel institucional se interpreta por separado.</div></div></div><div class="status-side"><div><div class="status-value">{pct(PEI)}</div><div class="status-state" style="color:{signal_color(state)}">{escape(signal_label(PEI))}</div><div class="status-mini"><div><div class="k">N satisfechos</div><div class="v">{N_PEI:,}</div></div><div><div class="k">Meta 2027</div><div class="v">60.0%</div></div><div><div class="k">Brecha</div><div class="v">{pp(gap)}</div></div></div></div>{traffic_svg(state,58)}</div></div>'''


def kpi_cards() -> str:
    gap=max(0,REFERENCE_TARGET-PEI); p17_state=signal_state(P17)
    cards=[
        ("Estudiantes analizados",f"{N_TOTAL:,}","👥","#2F66D8","#EAF1FF",1.0,"Base institucional"),
        ("Estudiantes satisfechos",f"{N_PEI:,}","✓","#16B36E","#EAF8F1",PEI,"Numerador N"),
        ("Promedio integral",f"{PEI_AVG:.2f} / 5","∑","#7C5CE7","#F1ECFF",PEI_AVG/5,"P1–P16"),
        ("Meta PEI 2027","60.0%","◎","#12AFC0","#E8F8FA",.60,"Referencia"),
        ("Brecha actual",pp(gap),"!","#F07B46","#FFF0E9",min(1,gap/.60 if .60 else 0),"Hasta la meta"),
        ("P17 · global",pct(P17),"◉","#7C5CE7","#F1ECFF",P17,signal_label(P17)),
    ]
    html=[]
    for label,value,icon,accent,soft,progress,foot in cards:
        html.append(f'''<div class="kpi" style="--accent:{accent};--soft:{soft}"><div class="kpi-top"><div class="kpi-label">{escape(label)}</div><div class="kpi-icon">{icon}</div></div><div class="kpi-value">{escape(value)}</div><div class="kpi-track"><span style="width:{max(0,min(100,progress*100)):.1f}%"></span></div><div class="kpi-foot"><span>{escape(foot)}</span><span>IND.01</span></div></div>''')
    return '<div class="kpi-grid">'+''.join(html)+'</div>'


def health_cards() -> str:
    html=[]
    for _,r in DIMS.sort_values("Código").iterrows():
        code=r["Código"]; meta=DIMENSIONS[code]; sat=float(r["Satisfacción"]); avg=float(r["Promedio"]); state=signal_state(sat); gap=max(0,REFERENCE_TARGET-sat)
        level,interval,levelcolor,_=institutional_level(sat)
        html.append(f'''<div class="health-card" style="--accent:{meta['accent']};--soft:{meta['soft']}"><div class="health-head"><div><div class="health-code">{meta['icon']} {code}</div><div class="health-name">{escape(meta['name'])}</div></div>{traffic_svg(state,29)}</div><div class="health-body"><div class="health-ring" style="--p:{sat*100:.2f};--accent:{meta['accent']}"><b>{pct(sat)}</b></div><div class="health-info"><div class="state" style="color:{signal_color(state)}">{escape(signal_label(sat))}</div><div class="avg"><b style="color:{levelcolor}">{escape(level)}</b> · {interval}<br>Promedio Likert: <b>{avg:.2f}/5</b><br>{'Meta alcanzada' if gap<=0 else 'Brecha: '+pp(gap)}</div></div></div><div class="health-foot"><span>{', '.join(meta['items'])}</span><b>Meta 60%</b></div></div>''')
    return '<div class="health-grid">'+''.join(html)+'</div>'


def insights_html() -> str:
    p=PRIORITY_DIM; s=STRONG_DIM; i=PRIORITY_ITEM
    return f'''<div class="insight-stack"><div class="insight-card" style="--accent:#E75E68;--soft:#FFF0F2"><div class="insight-icon">!</div><div><div class="insight-name">Prioridad dimensional · {p['Código']}</div><div class="insight-desc">{escape(p['Dimensión'])}</div></div><div class="insight-val">{pct(float(p['Satisfacción']))}</div></div><div class="insight-card" style="--accent:#16B36E;--soft:#EAF8F1"><div class="insight-icon">✓</div><div><div class="insight-name">Fortaleza relativa · {s['Código']}</div><div class="insight-desc">{escape(s['Dimensión'])}</div></div><div class="insight-val">{pct(float(s['Satisfacción']))}</div></div><div class="insight-card" style="--accent:#F07B46;--soft:#FFF0E9"><div class="insight-icon">◉</div><div><div class="insight-name">Ítem con menor valoración · {i['Ítem']}</div><div class="insight-desc">{escape(i['Pregunta'])}</div></div><div class="insight-val">{pct(float(i['Favorable']))}</div></div></div>'''


def route_html() -> str:
    rows=[]
    for year,goal in PEI_TARGETS.items():
        rows.append(f'<div class="road-row"><div class="road-year">{year}</div><div class="road-track"><span style="width:{goal*100:.0f}%"></span></div><div class="road-goal">{goal*100:.0f}%</div></div>')
    return '<div class="road">'+''.join(rows)+'</div>'


def radar_fig(labels: list[str], values: list[float], colors: list[str], title: str) -> go.Figure:
    # Un único perfil; color principal tomado del primer elemento.
    c=colors[0] if colors else "#2F66D8"
    vals=values+[values[0]]; labs=labels+[labels[0]]
    fig=go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals,theta=labs,fill='toself',mode='lines+markers',line=dict(color=c,width=3),marker=dict(size=8,color=c,line=dict(color='white',width=2)),fillcolor="rgba(47,102,216,.16)",hoverinfo='skip'))
    fig.update_layout(
        height=330,showlegend=False,margin=dict(l=38,r=38,t=35,b=30),paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Segoe UI, Arial',color='#62758A',size=11),
        polar=dict(bgcolor='rgba(0,0,0,0)',radialaxis=dict(range=[0,1],tickvals=[.25,.5,.6,.75,1],ticktext=['25%','50%','60%','75%','100%'],gridcolor='#E3EAF2',linecolor='#D9E2EC',angle=90),angularaxis=dict(gridcolor='#E5EBF2',linecolor='#D9E2EC')),
        title=dict(text=title,font=dict(size=13,color='#18324F'),x=.02,y=.98)
    )
    return fig


def dimension_banner(code: str) -> str:
    meta=DIMENSIONS[code]; r=DIMS[DIMS['Código']==code].iloc[0]; sat=float(r['Satisfacción']); avg=float(r['Promedio']); state=signal_state(sat); gap=max(0,REFERENCE_TARGET-sat)
    return f'''<div class="dimension-banner" style="--accent:{meta['accent']};--soft:{meta['soft']}"><div><div class="code">{meta['icon']} {code} · {', '.join(meta['items'])}</div><div class="name">{escape(meta['name'])}</div><div class="desc">Diagnóstico de satisfacción dimensional. Un estudiante se clasifica como satisfecho cuando el promedio de sus cuatro ítems es ≥4.</div></div><div class="score"><div><div class="big">{pct(sat)}</div><div class="small">Promedio {avg:.2f}/5 · {'meta alcanzada' if gap<=0 else 'brecha '+pp(gap)}</div></div>{traffic_svg(state,41)}</div></div>'''


def item_cards(code: str) -> str:
    meta=DIMENSIONS[code]; d=ITEMS_SUM[ITEMS_SUM['Dimensión']==code].copy(); d['_n']=d['Ítem'].str.extract(r'(\d+)')[0].astype(int); d=d.sort_values('_n')
    html=[]
    for _,r in d.iterrows():
        fav=float(r['Favorable']); neu=float(r['Neutral']); bad=float(r['Desfavorable'])
        html.append(f'''<div class="item-card" style="--accent:{meta['accent']};--soft:{meta['soft']}"><div class="item-top"><span class="item-code">{r['Ítem']}</span><span class="item-score">{pct(fav)}</span></div><div class="item-question">{escape(str(r['Pregunta']))}</div><div class="item-meter"><span style="width:{fav*100:.1f}%"></span></div><div class="item-stats"><div class="item-stat"><div class="k">1–2</div><div class="v">{pct(bad)}</div></div><div class="item-stat"><div class="k">3</div><div class="v">{pct(neu)}</div></div><div class="item-stat"><div class="k">4–5</div><div class="v">{pct(fav)}</div></div></div></div>''')
    return '<div class="item-grid">'+''.join(html)+'</div>'


def heatmap_html() -> str:
    html=[]
    dheat=ITEMS_SUM.copy(); dheat['_n']=dheat['Ítem'].str.extract(r'(\d+)')[0].astype(int); dheat=dheat.sort_values(['Dimensión','_n'])
    for _,r in dheat.iterrows():
        code=str(r['Dimensión']); meta=DIMENSIONS[code]; fav=float(r['Favorable']); strength=max(5,min(22,int(fav*22)))
        html.append(f'''<div class="heat-cell" style="--accent:{meta['accent']};--strength:{strength}"><div class="hcode">{r['Ítem']} · {code}</div><div class="hpct">{pct(fav)}</div><div class="hq">{escape(str(r['Pregunta']))}</div><div class="hbar"><span style="width:{fav*100:.1f}%"></span></div></div>''')
    return '<div class="heatmap">'+''.join(html)+'</div>'


def likert_cards(code: str) -> str:
    meta=DIMENSIONS[code]; d=ITEMS_SUM[ITEMS_SUM['Dimensión']==code].copy(); d['_n']=d['Ítem'].str.extract(r'(\d+)')[0].astype(int); d=d.sort_values('_n')
    html=[]
    for _,r in d.iterrows():
        html.append(f'''<div class="likert-card"><div class="head"><b>{r['Ítem']}</b><span style="font-size:.49rem;color:{meta['accent']}">Prom. {float(r['Promedio']):.2f}/5</span></div><div class="seg"><div class="bad"><div class="k">Desfav.</div><div class="v">{pct(float(r['Desfavorable']))}</div></div><div class="neu"><div class="k">Neutral</div><div class="v">{pct(float(r['Neutral']))}</div></div><div class="good"><div class="k">Favorable</div><div class="v">{pct(float(r['Favorable']))}</div></div></div></div>''')
    return '<div class="likert-grid">'+''.join(html)+'</div>'


def formula_html() -> str:
    return f'''<div class="formula-card"><div class="formula-box"><div class="formula-label">Fórmula del indicador</div><div class="formula-main"><span>IND.01 =</span><span class="frac"><span>N</span><i></i><span>D</span></span><span>× 100 =</span><span class="frac"><span>{N_PEI:,}</span><i></i><span>{N_TOTAL:,}</span></span><span>× 100 =</span><span class="formula-res">{pct(PEI)}</span></div></div><div class="formula-defs"><div class="formula-def"><b>N</b> = número de estudiantes clasificados como satisfechos con su formación académica integral.</div><div class="formula-def"><b>D</b> = total de estudiantes de pregrado encuestados analizados.</div><div class="formula-def"><b>Criterio operativo del tablero:</b> promedio P1–P16 ≥4 para ingresar al numerador N.</div></div></div>'''

# ==============================================================
# APP
# ==============================================================
st.markdown(topbar(),unsafe_allow_html=True)
st.markdown(page_header(),unsafe_allow_html=True)

tab1,tab2,tab3=st.tabs(["▣ Panel ejecutivo","▦ Dimensiones e ítems","ⓘ Método PEI"])

with tab1:
    st.markdown(status_banner(),unsafe_allow_html=True)
    st.markdown(kpi_cards(),unsafe_allow_html=True)

    section_header("Monitoreo dimensional","Salud de las cuatro dimensiones","Anillos de satisfacción + semáforo de cumplimiento frente a la meta 2027 de 60%.")
    st.markdown(health_cards(),unsafe_allow_html=True)

    section_header("Lectura ejecutiva","Perfil y prioridades","Visualización de gestión: perfil 4D, hallazgos y ruta de metas PEI.")
    c1,c2=st.columns([1.12,.88],gap="medium")
    with c1:
        st.markdown('<div class="panel"><div class="panel-head"><div><div class="panel-title">Perfil 4D de satisfacción</div><div class="panel-sub">Forma del desempeño de D1–D4. La escala radial incluye la referencia de 60%.</div></div><div class="panel-tag">Diagnóstico 4D</div></div>',unsafe_allow_html=True)
        fig=radar_fig(DIMS.sort_values('Código')['Código'].tolist(),DIMS.sort_values('Código')['Satisfacción'].tolist(),["#2F66D8"],"")
        st.plotly_chart(fig,use_container_width=True,config=STATIC_PLOT)
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><div class="panel-head"><div><div class="panel-title">Alertas y fortalezas</div><div class="panel-sub">Lectura automática para priorizar decisiones.</div></div><div class="panel-tag">Acción</div></div>'+insights_html()+'</div>',unsafe_allow_html=True)
        st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="panel-head"><div><div class="panel-title">Ruta PEI 2027–2030</div><div class="panel-sub">Metas anuales de la ficha técnica.</div></div><div class="panel-tag">Ascendente</div></div>'+route_html()+'</div>',unsafe_allow_html=True)

    section_header("Interpretación","Nivel institucional del resultado integral","Cuatro niveles de satisfacción; el semáforo sigue siendo de tres luces porque mide cumplimiento de meta.")
    st.markdown(level4_html(PEI),unsafe_allow_html=True)

with tab2:
    section_header("Explorador","Dimensiones e ítems","Sin gráficos que se arrastren: radar estático, tarjetas de ítems y composición Likert compacta.")
    selected=st.selectbox("Dimensión",["Todas","D1","D2","D3","D4"],format_func=lambda x:"Vista general · P1–P16" if x=="Todas" else f"{x} · {DIMENSIONS[x]['name']}",label_visibility="collapsed")

    if selected=="Todas":
        st.markdown(health_cards(),unsafe_allow_html=True)
        section_header("Mapa de diagnóstico","Matriz visual de los 16 ítems","Cada tarjeta muestra valoración favorable (4–5) sin convertir la página en una lista de barras.")
        st.markdown(heatmap_html(),unsafe_allow_html=True)
        section_header("Prioridades","Lectura automática de los extremos")
        st.markdown(insights_html(),unsafe_allow_html=True)
    else:
        st.markdown(dimension_banner(selected),unsafe_allow_html=True)
        section_header("Ítems de la dimensión","Cuatro indicadores específicos","Porcentaje favorable, composición 1–2 / 3 / 4–5 y promedio Likert.")
        st.markdown(item_cards(selected),unsafe_allow_html=True)
        section_header("Perfil interno","Radar de los cuatro ítems","Gráfico estático: no hace zoom, no se desplaza y no cambia al tocarlo.")
        d=ITEMS_SUM[ITEMS_SUM['Dimensión']==selected].copy(); d['_n']=d['Ítem'].str.extract(r'(\d+)')[0].astype(int); d=d.sort_values('_n')
        meta=DIMENSIONS[selected]
        c1,c2=st.columns([1.05,.95],gap="medium")
        with c1:
            st.markdown('<div class="panel">',unsafe_allow_html=True)
            fig=radar_fig(d['Ítem'].tolist(),d['Favorable'].tolist(),[meta['accent']],f"{selected} · valoración favorable")
            st.plotly_chart(fig,use_container_width=True,config=STATIC_PLOT)
            st.markdown('</div>',unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="panel"><div class="panel-head"><div><div class="panel-title">Composición de respuestas</div><div class="panel-sub">Lectura compacta por ítem, sin barras apiladas gigantes.</div></div><div class="panel-tag">Likert</div></div>'+likert_cards(selected)+'</div>',unsafe_allow_html=True)

    with st.expander("Ver detalle técnico de P1–P16"):
        t=ITEMS_SUM.copy() if selected=="Todas" else ITEMS_SUM[ITEMS_SUM['Dimensión']==selected].copy()
        t=t[["Ítem","Dimensión","Pregunta","Favorable","Neutral","Desfavorable","Promedio"]]
        for c in ["Favorable","Neutral","Desfavorable"]: t[c]=t[c].map(lambda x:f"{x*100:.1f}%")
        t["Promedio"]=t["Promedio"].map(lambda x:f"{x:.2f}")
        st.dataframe(t,use_container_width=True,hide_index=True,height=min(620,45+36*len(t)))

with tab3:
    section_header("Ficha técnica","Fórmula e interpretación")
    st.markdown(formula_html(),unsafe_allow_html=True)
    section_header("Criterios","Nivel institucional de satisfacción")
    st.markdown(level4_html(PEI),unsafe_allow_html=True)

    section_header("Estructura","Cómo se organiza el instrumento")
    methods=[]
    for code,meta in DIMENSIONS.items():
        methods.append(f'''<div class="method"><div class="method-icon">{meta['icon']}</div><div class="method-title">{code} · {escape(meta['short'])}</div><div class="method-text">{', '.join(meta['items'])}. Un estudiante se clasifica como satisfecho en la dimensión cuando el promedio de sus cuatro respuestas es ≥4.</div></div>''')
    methods.append(f'''<div class="method"><div class="method-icon">∑</div><div class="method-title">IND.01 integral · P1–P16</div><div class="method-text">Promedio integral por estudiante. Criterio operativo del tablero: promedio ≥4. Resultado actual: <b>{pct(PEI)}</b>.</div></div>''')
    methods.append(f'''<div class="method"><div class="method-icon">◉</div><div class="method-title">P17 · satisfacción global</div><div class="method-text">Pregunta directa complementaria. Respuesta 4 o 5 = satisfecho. Resultado actual: <b>{pct(P17)}</b>.</div></div>''')
    st.markdown('<div class="method-grid">'+''.join(methods)+'</div>',unsafe_allow_html=True)
    st.markdown('<div style="height:12px"></div><div class="notice"><b>Nota metodológica:</b> se conserva la lógica analítica ya definida en la versión anterior. Esta actualización cambia la presentación visual, no los cálculos. El semáforo de tres luces representa cumplimiento de la meta PEI; la escala de cuatro categorías representa nivel de satisfacción.</div>',unsafe_allow_html=True)
