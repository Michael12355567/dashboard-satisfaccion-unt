from __future__ import annotations

from html import escape
from pathlib import Path
import math

import pandas as pd
import streamlit as st


# ==============================================================
# CONFIGURACIÓN
# ==============================================================
st.set_page_config(
    page_title="UNT | Diagnóstico 2026 de satisfacción académica",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "basededatos.xlsx"
SHEET_NAME = "Base_Encuesta"

ITEMS_16 = [f"P{i}" for i in range(1, 17)]
ALL_ITEMS = [f"P{i}" for i in range(1, 18)]

DIMENSIONS = {
    "D1": {
        "name": "Calidad del proceso académico",
        "short": "Proceso académico",
        "items": ["P1", "P2", "P3", "P4"],
        "accent": "#3573A3",
        "soft": "#EAF3FA",
        "icon": "▥",
        "meaning": "Pertinencia curricular, actualización del plan de estudios, carga académica y coherencia entre objetivos y contenidos.",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "short": "Docencia y pedagogía",
        "items": ["P5", "P6", "P7", "P8"],
        "accent": "#7767A0",
        "soft": "#F1EEFA",
        "icon": "✦",
        "meaning": "Dominio docente, metodologías de enseñanza, participación estudiantil y retroalimentación pedagógica.",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "short": "Servicios y gestión",
        "items": ["P9", "P10", "P11", "P12"],
        "accent": "#B9794E",
        "soft": "#FFF1E8",
        "icon": "⌂",
        "meaning": "Servicios académicos, información, infraestructura, recursos educativos y aseguramiento de la calidad.",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "short": "Formación integral",
        "items": ["P13", "P14", "P15", "P16"],
        "accent": "#348675",
        "soft": "#E9F7F3",
        "icon": "◇",
        "meaning": "Competencias profesionales, valores, responsabilidad social, desarrollo personal y preparación para el ejercicio profesional.",
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

# Ficha técnica PEI compartida por el usuario:
# - 2026: diseño, estandarización y validación; sin valor medible oficial.
# - medición efectiva a partir de 2027.
# - valor referencial del indicador de satisfacción: >=60%.
# - logros esperados 2027-2030: 60%, 65%, 70%, 75%.
PEI_REFERENCE = 0.60
PEI_TARGETS = {2027: 0.60, 2028: 0.65, 2029: 0.70, 2030: 0.75}


# ==============================================================
# CSS — SISTEMA INSTITUCIONAL + PROFUNDIDAD / RESPONSIVE
# ==============================================================
st.markdown(
    r"""
<style>
:root{
  --bg:#F3F6FA; --paper:#FFFFFF; --ink:#112B48; --muted:#718197; --line:#E1E9F2;
  --blue:#2E5EC8; --blue2:#3B71EA; --deep:#153C82; --cyan:#18A9C0;
  --red:#E25B68; --amber:#F2A62C; --green:#16A878; --excellent:#20AABD;
  --shadow:0 14px 34px rgba(31,68,121,.10),0 3px 9px rgba(31,68,121,.05);
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"Segoe UI Variable","Aptos","Segoe UI",Inter,Arial,sans-serif}
.stApp{background:linear-gradient(180deg,#FAFCFF 0%,var(--bg) 100%);color:var(--ink)}
.block-container{max-width:1540px;padding:.55rem 1rem 3rem}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:rgba(250,252,255,.80);backdrop-filter:blur(16px)}
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}

/* TOPBAR */
.topbar{min-height:60px;border-radius:0 0 17px 17px;background:linear-gradient(105deg,#234EA8 0%,#2E5FCB 53%,#3B6FE8 100%);display:flex;align-items:center;justify-content:space-between;gap:14px;padding:9px 17px;color:#fff;box-shadow:0 11px 25px rgba(31,75,165,.22);position:relative;overflow:hidden}
.topbar:after{content:"";position:absolute;width:260px;height:260px;border:30px solid rgba(255,255,255,.065);border-radius:50%;right:-90px;top:-170px}
.brand{display:flex;align-items:center;gap:10px;position:relative;z-index:1;min-width:0}.brand-img{height:43px;max-width:290px;background:#fff;border-radius:11px;padding:4px 7px;box-shadow:0 7px 16px rgba(10,31,80,.22);display:flex;align-items:center}.brand-img img{height:100%;width:auto;max-width:100%;object-fit:contain}.brand-title{font-size:.82rem;font-weight:950;line-height:1.08}.brand-sub{font-size:.50rem;opacity:.82;letter-spacing:.08em;text-transform:uppercase;margin-top:2px}
.top-meta{display:flex;gap:8px;align-items:center;position:relative;z-index:1}.meta-box{padding:7px 10px;border-radius:10px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);font-size:.50rem;line-height:1.22}.meta-box b{display:block;font-size:.65rem;color:#fff;margin-top:2px}

/* PAGE HEADER */
.pagehead{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:19px 4px 13px}.kicker{font-size:.57rem;letter-spacing:.16em;text-transform:uppercase;font-weight:950;color:#3265CF}.title{font-size:clamp(1.42rem,2.7vw,2rem);font-weight:950;letter-spacing:-.045em;color:#142E4D;margin-top:4px;line-height:1.03}.sub{font-size:.69rem;color:#76879A;margin-top:6px;line-height:1.48;max-width:960px}.basebox{min-width:160px;padding:10px 12px;border-radius:14px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);font-size:.52rem;color:#8491A2}.basebox b{display:block;color:#183650;font-size:.74rem;margin-top:2px}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}.chip{padding:6px 9px;border-radius:999px;background:#EEF4FD;border:1px solid #DCE7F6;color:#41607F;font-size:.55rem;font-weight:850}.chip.warn{background:#FFF8E9;border-color:#F2E2B8;color:#80651F}

/* TABS */
.stTabs [data-baseweb="tab-list"]{gap:7px;background:transparent;border-bottom:1px solid #DDE5F0;padding:0;border-radius:0;box-shadow:none;margin-top:0;overflow-x:auto;white-space:nowrap}.stTabs [data-baseweb="tab"]{height:46px;border-radius:11px 11px 0 0;padding:0 15px;color:#6B7B90;font-weight:900;font-size:.74rem;flex:0 0 auto}.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#2453B4,#2F66D8)!important;color:#fff!important;box-shadow:0 8px 18px rgba(44,94,198,.18)!important}.stTabs [data-baseweb="tab-highlight"]{display:none}

/* SECTION */
.section-head{display:flex;justify-content:space-between;align-items:end;gap:16px;margin:1.35rem 0 .68rem}.section-kicker{font-size:.56rem;text-transform:uppercase;letter-spacing:.14em;font-weight:950;color:#3265CF}.section-title{font-size:clamp(1.02rem,2vw,1.30rem);font-weight:950;color:#17324F;letter-spacing:-.025em;margin-top:3px}.section-note{font-size:.64rem;color:#7C8B9D;text-align:right;max-width:570px;line-height:1.42}
.panel{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow)}

/* HERO RESULT */
.hero-grid{display:grid;grid-template-columns:minmax(0,1.28fr) minmax(330px,.72fr);gap:14px}
.result-hero{padding:21px 22px;border-radius:20px;background:linear-gradient(110deg,#214BA6 0%,#2B5DC7 52%,#396DE8 100%);color:#fff;box-shadow:0 17px 36px rgba(40,85,178,.21);position:relative;overflow:hidden}.result-hero:after{content:"";position:absolute;width:320px;height:320px;border:30px solid rgba(255,255,255,.065);border-radius:50%;right:-100px;top:-190px}.result-layout{display:grid;grid-template-columns:82px minmax(0,1fr) auto;gap:17px;align-items:center;position:relative;z-index:1}.result-icon{width:82px;height:82px;border-radius:21px;background:linear-gradient(145deg,rgba(255,255,255,.28),rgba(255,255,255,.10));border:1px solid rgba(255,255,255,.18);display:grid;place-items:center;font-size:1.85rem;box-shadow:0 10px 22px rgba(15,42,105,.24),inset 0 1px 0 rgba(255,255,255,.27)}.result-eyebrow{font-size:.53rem;text-transform:uppercase;letter-spacing:.12em;font-weight:900;color:#CCDAFF}.result-title{font-size:clamp(1rem,1.8vw,1.28rem);font-weight:950;line-height:1.15;margin-top:3px}.result-text{font-size:.63rem;color:#E0E9FF;line-height:1.48;margin-top:7px;max-width:750px}.result-score{font-size:clamp(2.35rem,4.6vw,3.35rem);font-weight:950;letter-spacing:-.065em;line-height:.95;text-align:right}.result-level{font-size:.63rem;font-weight:900;text-align:right;margin-top:5px}.diag-pill{display:inline-flex;align-items:center;gap:6px;margin-top:8px;padding:6px 8px;border-radius:10px;background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.15);font-size:.52rem;font-weight:800}

/* SECONDARY ANALYTIC */
.secondary{padding:18px;display:flex;flex-direction:column;min-height:100%}.secondary-top{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.secondary-k{font-size:.53rem;letter-spacing:.11em;text-transform:uppercase;color:#7F8EA0;font-weight:950}.secondary-t{font-size:.93rem;color:#18344F;font-weight:950;line-height:1.22;margin-top:5px}.secondary-v{font-size:2.25rem;font-weight:950;color:#173451;letter-spacing:-.055em;margin-top:14px}.secondary-x{font-size:.64rem;color:#6E7F93;line-height:1.46;margin-top:6px}.secondary-note{margin-top:auto;padding-top:12px;border-top:1px solid #E9EEF4;font-size:.57rem;color:#8090A3;line-height:1.43}

/* TRAFFIC LIGHT */
.signal-shell{filter:drop-shadow(0 8px 12px rgba(10,26,40,.26))}.signal-row{display:flex;align-items:center;justify-content:flex-end;gap:9px;margin-top:8px}.signal-copy{font-size:.57rem;font-weight:900;text-align:right;line-height:1.25}

/* FORMULA */
.formula{margin-top:13px;padding:13px 14px;border-radius:15px;background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.16)}.formula-k{font-size:.47rem;text-transform:uppercase;letter-spacing:.11em;font-weight:900;color:#C9D8FA}.formula-eq{display:flex;align-items:center;justify-content:flex-start;gap:8px;flex-wrap:wrap;margin-top:7px;font-weight:900}.frac{display:inline-grid;grid-template-rows:auto 1px auto;min-width:55px;text-align:center;align-items:center;line-height:1.05}.frac .bar{height:1px;background:#fff;margin:3px 0}.formula-result{font-size:1.12rem;background:#fff;color:#2455B7;padding:5px 9px;border-radius:9px;box-shadow:0 6px 15px rgba(9,31,77,.16)}

/* KPI */
.kpi-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin-top:12px}.kpi{min-height:112px;padding:12px;border-radius:16px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);position:relative;overflow:hidden}.kpi:before{content:"";position:absolute;right:-17px;top:-21px;width:68px;height:68px;border-radius:20px;background:var(--soft);transform:rotate(18deg);opacity:.82}.kpi-head{display:flex;justify-content:space-between;gap:7px;align-items:flex-start;position:relative;z-index:1}.kpi-label{font-size:.51rem;color:#728296;font-weight:850;line-height:1.25}.kpi-icon{width:32px;height:32px;border-radius:9px;background:linear-gradient(145deg,var(--accent),color-mix(in srgb,var(--accent) 72%,#fff));display:grid;place-items:center;color:#fff;font-size:.82rem;font-weight:950;box-shadow:0 7px 14px color-mix(in srgb,var(--accent) 22%,transparent)}.kpi-v{font-size:1.2rem;font-weight:950;color:#17324F;margin-top:7px;letter-spacing:-.04em;position:relative;z-index:1}.kpi-f{font-size:.48rem;color:#8A96A5;margin-top:4px;position:relative;z-index:1}.spark{height:18px;margin-top:8px;position:relative;z-index:1}.spark svg{width:100%;height:100%;overflow:visible}

/* DIMENSIONS */
.dim-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px}.dim-card{padding:15px;min-height:255px;position:relative;overflow:hidden}.dim-card:before{content:"";position:absolute;left:0;top:0;right:0;height:4px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 55%,#77D5DC))}.dim-head{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}.dim-code{display:flex;align-items:center;gap:7px;font-size:.62rem;color:var(--accent);font-weight:950}.dim-name{font-size:.58rem;color:#7C8B9C;line-height:1.30;margin-top:4px;min-height:2.55em}.dim-body{display:grid;grid-template-columns:96px 1fr;gap:10px;align-items:center;margin-top:10px}.donut{--p:0;--accent:#2F66D8;width:94px;height:94px;border-radius:50%;background:conic-gradient(var(--accent) calc(var(--p)*1%),#EDF2F7 0);position:relative;display:grid;place-items:center;box-shadow:0 10px 18px rgba(27,54,90,.11),inset 0 1px 0 #fff}.donut:after{content:"";position:absolute;inset:11px;border-radius:50%;background:linear-gradient(145deg,#fff,#F6F9FC);box-shadow:inset 3px 3px 7px rgba(30,53,83,.05)}.donut b{position:relative;z-index:1;font-size:1.05rem;color:#18334F;letter-spacing:-.04em}.dim-level{font-size:.59rem;font-weight:950;line-height:1.25}.dim-meta{font-size:.49rem;color:#8190A1;line-height:1.47;margin-top:6px}.dim-meaning{margin-top:10px;padding-top:8px;border-top:1px dashed #E2E9F0;font-size:.54rem;color:#677A90;line-height:1.42}.dim-foot{display:flex;justify-content:space-between;gap:8px;border-top:1px solid #EDF1F5;margin-top:9px;padding-top:8px;font-size:.48rem;color:#7D8B9A}.dim-foot b{color:#2B425C}

/* SCALE */
.scale-wrap{padding:13px 14px}.scale-title{font-size:.58rem;font-weight:950;color:#1F3B57;margin-bottom:9px}.scale-note{font-size:.52rem;color:#7B8B9E;line-height:1.4;margin-top:8px}.scale4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}.scale-step{padding:9px 7px;border-radius:12px;border:1px solid #E4EBF3;background:#fff;text-align:center;opacity:.58}.scale-step.active{opacity:1;box-shadow:0 9px 18px color-mix(in srgb,var(--lvl) 17%,transparent);border:2px solid var(--lvl);transform:translateY(-1px)}.scale-dot{width:11px;height:11px;border-radius:50%;margin:0 auto 5px;box-shadow:0 3px 8px rgba(20,35,50,.14)}.scale-name{font-size:.54rem;font-weight:950;color:#405168}.scale-range{font-size:.49rem;color:#8794A3;margin-top:2px}

/* INTERPRETATION */
.insight-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.insight{padding:14px 15px;position:relative;overflow:hidden}.insight:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}.insight-k{font-size:.52rem;letter-spacing:.10em;text-transform:uppercase;color:#8290A1;font-weight:950}.insight-t{font-size:.80rem;color:#1A3551;font-weight:950;line-height:1.25;margin-top:5px}.insight-x{font-size:.60rem;color:#687B90;line-height:1.47;margin-top:6px}

/* PEI ROUTE */
.pei-card{padding:15px 16px}.pei-banner{display:flex;gap:11px;align-items:flex-start;padding:12px;border-radius:14px;background:linear-gradient(135deg,#FFF8E7,#FFFDF7);border:1px solid #F0DFB4;color:#71591E}.pei-banner .i{font-size:1.12rem}.pei-banner .t{font-size:.64rem;font-weight:950}.pei-banner .x{font-size:.56rem;line-height:1.45;margin-top:3px}.route{display:grid;grid-template-columns:1.15fr repeat(4,1fr);gap:8px;margin-top:11px}.node{padding:11px;border-radius:13px;background:linear-gradient(145deg,#fff,#F7FAFE);border:1px solid var(--line);box-shadow:0 8px 18px rgba(31,70,126,.06);position:relative;overflow:hidden}.node:before{content:"";position:absolute;left:0;top:0;right:0;height:3px;background:var(--accent)}.node-y{font-size:.49rem;color:#8190A1;text-transform:uppercase;font-weight:900}.node-v{font-size:1rem;font-weight:950;color:#214DA6;margin-top:4px}.node-c{font-size:.47rem;color:#8A97A7;margin-top:3px;line-height:1.35}.node.diag .node-v{font-size:.74rem;color:#82651F;line-height:1.2}

/* SELECT */
div[data-baseweb="select"] > div{background:#fff!important;border:1px solid #D8E4EB!important;border-radius:13px!important;min-height:44px!important;box-shadow:0 7px 18px rgba(30,57,77,.05)!important}div[data-baseweb="select"] span{color:#26445A!important;font-weight:750!important}

/* ITEM CARDS */
.item-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.item{padding:13px;position:relative;overflow:hidden}.item:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}.item-top{display:flex;justify-content:space-between;gap:8px;align-items:center}.item-code{font-size:.56rem;font-weight:950;color:var(--accent);padding:4px 7px;border-radius:8px;background:var(--soft)}.item-score{font-size:1rem;font-weight:950;color:#17324F}.item-q{font-size:.52rem;color:#6F8093;line-height:1.42;margin-top:8px;min-height:4.4em}.meter{height:7px;border-radius:99px;background:#EDF2F7;overflow:hidden;margin-top:9px}.meter span{height:100%;display:block;border-radius:99px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 58%,#78D9DF))}.item-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:9px}.item-meta>div{padding:6px 4px;border-radius:8px;background:#F7F9FC;border:1px solid #EBF0F5;text-align:center}.item-meta .k{font-size:.40rem;color:#8B97A5;text-transform:uppercase;font-weight:850}.item-meta .v{font-size:.53rem;color:#334B64;font-weight:950;margin-top:1px}

/* LIKERT CAPSULES */
.likert{padding:15px 16px}.likert-row{display:grid;grid-template-columns:46px minmax(0,1fr);gap:10px;align-items:center;padding:7px 0}.likert-code{font-size:.56rem;font-weight:950;color:#48627E}.likert-pill{height:24px;border-radius:999px;overflow:hidden;display:flex;background:#EDF2F7;box-shadow:inset 0 2px 4px rgba(28,50,78,.08)}.seg{height:100%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:.43rem;font-weight:900;white-space:nowrap;overflow:hidden}.bad{background:linear-gradient(180deg,#DB6B77,#C75563)}.neutral{background:linear-gradient(180deg,#BCC6D0,#9EABB8)}.good{background:linear-gradient(180deg,#4AA28D,#348873)}

/* TECHNICAL */
.method-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.method{padding:15px;min-height:175px}.method-i{font-size:1.1rem}.method-t{font-size:.78rem;font-weight:950;color:#1C334B;margin-top:6px}.method-x{font-size:.60rem;color:#68798C;line-height:1.50;margin-top:6px}.method-alert{padding:14px 15px;border-radius:16px;background:linear-gradient(135deg,#FFF9EA,#FFFDF7);border:1px solid #F1E2B9;color:#6D5720;font-size:.62rem;line-height:1.5;box-shadow:0 9px 22px rgba(85,69,22,.06)}
div[data-testid="stDataFrame"]{border:1px solid #E5EAF0;border-radius:15px;overflow:hidden;box-shadow:0 9px 22px rgba(33,53,82,.05)}

@media(max-width:1120px){
  .hero-grid{grid-template-columns:1fr}.kpi-grid{grid-template-columns:repeat(3,1fr)}.dim-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.item-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.insight-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.route{grid-template-columns:repeat(3,1fr)}.route .diag{grid-column:span 3}.method-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:700px){
  .block-container{padding:.35rem .55rem 2rem}.topbar{height:auto;min-height:54px;padding:9px 11px}.brand-img{height:38px;max-width:165px}.brand-title{font-size:.66rem}.brand-sub,.top-meta{display:none}.pagehead{padding:13px 2px 9px;align-items:flex-start}.basebox{display:none}.title{font-size:1.45rem}.chips{gap:5px}.chip{font-size:.49rem;padding:5px 7px}.section-note{display:none}.result-layout{grid-template-columns:55px 1fr;gap:10px}.result-icon{width:55px;height:55px;border-radius:14px;font-size:1.25rem}.result-layout>div:last-child{grid-column:1/-1}.result-score{text-align:left;font-size:2.35rem}.result-level{text-align:left}.signal-row{justify-content:flex-start}.formula-eq{justify-content:center}.kpi-grid{grid-template-columns:1fr 1fr}.dim-grid,.item-grid,.insight-grid,.method-grid{grid-template-columns:1fr}.dim-card{min-height:0}.scale4{grid-template-columns:1fr 1fr}.route{grid-template-columns:1fr 1fr}.route .diag{grid-column:1/-1}.likert-row{grid-template-columns:36px minmax(0,1fr)}.likert-pill{height:22px}.seg{font-size:.39rem}.stTabs [data-baseweb="tab"]{padding:0 10px;font-size:.67rem}
}

/* === CAPA METODOLÓGICA FINAL 2026 === */
.pei-official{padding:18px;display:flex;flex-direction:column;min-height:100%;background:linear-gradient(155deg,#FFFFFF 0%,#F7FAFE 100%)}
.pei-official-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.pei-official-k{font-size:.52rem;letter-spacing:.11em;text-transform:uppercase;color:#7D8DA1;font-weight:950}
.pei-official-t{font-size:.94rem;color:#17334F;font-weight:950;line-height:1.22;margin-top:5px}
.pei-official-status{margin-top:14px;padding:12px 13px;border-radius:14px;background:linear-gradient(135deg,#EEF4FF,#F8FBFF);border:1px solid #DCE7FA}
.pei-official-status .big{font-size:1.22rem;font-weight:950;color:#2B5EC7;letter-spacing:-.03em}
.pei-official-status .small{font-size:.58rem;color:#6E8095;line-height:1.45;margin-top:4px}
.pei-official-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.pei-official-mini{padding:9px 10px;border-radius:11px;background:#fff;border:1px solid #E7EDF5}
.pei-official-mini .k{font-size:.45rem;text-transform:uppercase;letter-spacing:.07em;color:#8795A6;font-weight:900}
.pei-official-mini .v{font-size:.72rem;color:#203C58;font-weight:950;margin-top:2px}
.pei-official-note{margin-top:auto;padding-top:11px;border-top:1px solid #E8EEF5;font-size:.57rem;color:#76889B;line-height:1.45}
.ref-badge{display:inline-flex;align-items:center;gap:7px;margin-top:8px;padding:7px 9px;border-radius:10px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.19);font-size:.54rem;font-weight:850;color:#ECF4FF}
.ref-badge b{color:#BFF3DC}
.quality-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.quality-card{padding:14px 15px;position:relative;overflow:hidden}.quality-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}
.quality-k{font-size:.50rem;letter-spacing:.10em;text-transform:uppercase;color:#8392A4;font-weight:950}.quality-v{font-size:1.22rem;color:#173550;font-weight:950;letter-spacing:-.04em;margin-top:5px}.quality-x{font-size:.58rem;color:#6C7F94;line-height:1.46;margin-top:5px}
.quality-warning{margin-top:10px;padding:12px 13px;border-radius:14px;background:linear-gradient(135deg,#FFF8E9,#FFFDF7);border:1px solid #F0E0B7;color:#705A24;font-size:.59rem;line-height:1.5}
.interpret-banner{padding:13px 15px;border-radius:16px;background:linear-gradient(135deg,#EDF4FF,#F8FBFF);border:1px solid #DCE7F6;color:#31516F;font-size:.60rem;line-height:1.5;margin-top:10px}.interpret-banner b{color:#173C5C}
@media(max-width:980px){.quality-grid{grid-template-columns:1fr 1fr}}@media(max-width:700px){.pei-official-grid,.quality-grid{grid-template-columns:1fr}.ref-badge{font-size:.50rem}}

</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================
# AJUSTE VISUAL FINAL — FONDO BLANCO / MAYOR LEGIBILIDAD
# ==============================================================
st.markdown(
    r"""
<style>
:root{--bg:#FFFFFF!important;--line:#DDE6F0!important;--shadow:0 10px 28px rgba(25,55,95,.08),0 2px 6px rgba(25,55,95,.035)!important}
.stApp{background:#FFFFFF!important}
header[data-testid="stHeader"]{background:rgba(255,255,255,.96)!important}
.block-container{max-width:1580px!important;padding:.65rem 1.15rem 3rem!important}
.pagehead{background:#FFFFFF!important}
.topbar{background:linear-gradient(100deg,#123B78 0%,#1D52A2 58%,#2865C5 100%)!important}
.title{font-size:clamp(1.75rem,3vw,2.35rem)!important}.sub{font-size:.84rem!important;line-height:1.58!important;max-width:1120px!important}
.kicker{font-size:.68rem!important}.chip{font-size:.66rem!important;padding:7px 11px!important}.basebox{font-size:.64rem!important}.basebox b{font-size:.88rem!important}
.stTabs [data-baseweb="tab"]{font-size:.86rem!important;height:50px!important}
.section-title{font-size:clamp(1.25rem,2.2vw,1.55rem)!important}.section-kicker{font-size:.66rem!important}.section-note{font-size:.77rem!important;max-width:680px!important}
.panel{background:#FFFFFF!important;border-color:#DDE6F0!important}
.main-reading-grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(330px,.55fr);gap:16px;align-items:stretch}
.integral-hero{border-radius:22px;background:linear-gradient(128deg,#0E3268 0%,#164A96 52%,#1F5DB6 100%);color:#fff;padding:25px 26px;box-shadow:0 18px 38px rgba(24,72,145,.18);position:relative;overflow:hidden}
.integral-hero:after{content:"";position:absolute;width:360px;height:360px;border:42px solid rgba(255,255,255,.055);border-radius:50%;right:-120px;top:-210px}
.integral-top,.integral-core,.integral-bottom{position:relative;z-index:1}.integral-top{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.integral-eyebrow,.side-kicker{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;font-weight:900}.integral-eyebrow{color:#C9D9FA}.integral-title{font-size:clamp(1.55rem,2.7vw,2.2rem);font-weight:950;letter-spacing:-.04em;margin-top:5px}.integral-text{font-size:.82rem;line-height:1.58;color:#E7EEFC;max-width:980px;margin-top:9px}.integral-core{display:grid;grid-template-columns:250px minmax(0,1fr);gap:20px;align-items:center;margin-top:18px}.integral-score{font-size:clamp(3.3rem,6.3vw,5.2rem);font-weight:950;letter-spacing:-.07em;line-height:.92}.integral-level{font-size:.88rem;font-weight:900;margin-top:8px}.integral-level span{font-size:.70rem;color:#DDE7F8;font-weight:700;margin-left:4px}.integral-formula .formula{margin-top:0;background:rgba(255,255,255,.10);border-color:rgba(255,255,255,.17)}.integral-bottom{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}.integral-bottom>div{padding:11px 12px;border-radius:13px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14)}.integral-bottom b{display:block;font-size:.64rem;color:#C8D8F6}.integral-bottom span{display:block;font-size:.89rem;font-weight:900;margin-top:3px}.integral-signal{position:relative;z-index:1}
.formula-k{font-size:.62rem!important}.formula-eq{font-size:.91rem!important;gap:10px!important}.formula-result{font-size:1.35rem!important}.diag-pill,.ref-badge{font-size:.66rem!important;line-height:1.45!important}
.side-stack{display:grid;grid-template-rows:auto auto;gap:12px}.p17-card,.pei-mini{padding:18px 19px}.p17-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.side-kicker{color:#6C7D91}.p17-title,.pei-mini-title{font-size:1.05rem;font-weight:950;color:#183651;line-height:1.25;margin-top:5px}.p17-score{font-size:2.9rem;font-weight:950;color:#183651;letter-spacing:-.06em;margin-top:14px}.p17-level{font-size:.78rem;font-weight:900}.p17-copy,.pei-mini-note{font-size:.72rem;line-height:1.52;color:#66798E;margin-top:9px}.pei-mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}.pei-mini-grid>div{padding:10px 11px;border-radius:12px;background:#F7F9FC;border:1px solid #E5EBF2}.pei-mini-grid b{display:block;font-size:.86rem;color:#1D3D60}.pei-mini-grid span{display:block;font-size:.60rem;color:#8491A0;margin-top:3px}.pei-mini-note{border-top:1px solid #E8EDF3;padding-top:10px}
.kpi{min-height:128px!important;padding:14px!important}.kpi-label{font-size:.66rem!important}.kpi-icon{width:36px!important;height:36px!important;font-size:.95rem!important}.kpi-v{font-size:1.42rem!important}.kpi-f{font-size:.60rem!important}.stat-footnote{font-size:.64rem;color:#7C8998;line-height:1.5;margin-top:8px}
.dim-card{min-height:285px!important;padding:17px!important}.dim-code{font-size:.72rem!important}.dim-name{font-size:.70rem!important;min-height:2.35em!important}.donut{width:102px!important;height:102px!important}.donut b{font-size:1.18rem!important}.dim-level{font-size:.72rem!important}.dim-meta{font-size:.61rem!important}.dim-meaning{font-size:.64rem!important}.dim-foot{font-size:.58rem!important}.scale-title{font-size:.72rem!important}.scale-name{font-size:.66rem!important}.scale-range,.scale-note{font-size:.60rem!important}
.insight-k{font-size:.62rem!important}.insight-t{font-size:.92rem!important}.insight-x{font-size:.70rem!important}.interpret-banner{font-size:.70rem!important}.method-t{font-size:.90rem!important}.method-x,.method-alert{font-size:.70rem!important}.quality-k{font-size:.60rem!important}.quality-v{font-size:1.42rem!important}.quality-x,.quality-warning{font-size:.68rem!important}
div[data-testid="stDataFrame"]{font-size:.78rem!important}
@media(max-width:1050px){.main-reading-grid{grid-template-columns:1fr}.side-stack{grid-template-columns:1fr 1fr;grid-template-rows:auto}.integral-core{grid-template-columns:220px 1fr}}
@media(max-width:700px){.block-container{padding:.45rem .65rem 2rem!important}.title{font-size:1.62rem!important}.sub{font-size:.78rem!important}.main-reading-grid{grid-template-columns:1fr}.side-stack{grid-template-columns:1fr}.integral-hero{padding:19px 17px;border-radius:18px}.integral-top{display:grid;grid-template-columns:1fr auto}.integral-title{font-size:1.52rem}.integral-text{font-size:.76rem}.integral-core{grid-template-columns:1fr;gap:12px}.integral-score{font-size:3.25rem}.integral-bottom{grid-template-columns:1fr 1fr}.integral-bottom>div:last-child{grid-column:1/-1}.p17-score{font-size:2.45rem}.kpi-grid{grid-template-columns:1fr 1fr!important}.section-title{font-size:1.26rem!important}.section-kicker{font-size:.60rem!important}.formula-eq{justify-content:flex-start!important}}
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================
# CAPA VISUAL PARA EXPOSICIÓN — BLANCO / JERARQUÍA / LETRA MAYOR
# ==============================================================
st.markdown(
    r"""
<style>
:root{
  --page:#FFFFFF;--navy:#12345B;--navy2:#1B4E87;--blue:#2F66C8;--blue-soft:#EEF4FC;
  --ink:#152D47;--muted:#63768A;--line:#DCE5EF;--soft:#F7F9FC;
  --shadow:0 12px 32px rgba(25,55,90,.08),0 2px 7px rgba(25,55,90,.035);
}
.stApp{background:#FFFFFF!important;color:var(--ink)!important}
header[data-testid="stHeader"]{background:rgba(255,255,255,.97)!important}
.block-container{max-width:1600px!important;padding:.65rem 1.2rem 3.2rem!important}
.pagehead{padding:22px 4px 15px!important}
.title{font-size:clamp(1.95rem,3.2vw,2.7rem)!important;color:#102D4C!important}
.sub{font-size:.95rem!important;line-height:1.62!important;color:#60758B!important;max-width:1180px!important}
.kicker{font-size:.72rem!important}.chip{font-size:.72rem!important;padding:8px 12px!important}
.section-title{font-size:clamp(1.35rem,2.35vw,1.72rem)!important}.section-kicker{font-size:.70rem!important}
.section-note{font-size:.82rem!important;line-height:1.5!important;max-width:720px!important}
.stTabs [data-baseweb="tab"]{font-size:.92rem!important;height:52px!important}
.panel{background:#FFFFFF!important;border:1px solid var(--line)!important;box-shadow:var(--shadow)!important}
.main-reading-grid{display:grid!important;grid-template-columns:minmax(0,1.62fr) minmax(315px,.48fr)!important;gap:16px!important;align-items:stretch!important}
.integral-hero{background:#FFFFFF!important;color:var(--ink)!important;border:1px solid #D8E4F0!important;border-radius:22px!important;padding:26px 28px!important;box-shadow:0 18px 42px rgba(21,56,95,.10)!important;position:relative!important;overflow:hidden!important}
.integral-hero:before{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;background:linear-gradient(180deg,#173E72,#2F6CC8)}
.integral-hero:after{content:"";position:absolute;width:330px;height:330px;border-radius:50%;right:-150px;top:-200px;background:radial-gradient(circle,rgba(47,102,200,.09),transparent 70%);border:0!important}
.integral-eyebrow{color:#2F66C8!important;font-size:.76rem!important}.integral-title{color:#122F50!important;font-size:clamp(1.7rem,2.8vw,2.35rem)!important;line-height:1.08!important}
.integral-text{color:#5D7288!important;font-size:.92rem!important;line-height:1.62!important;max-width:1080px!important}
.integral-core{grid-template-columns:265px minmax(0,1fr)!important;gap:24px!important;margin-top:20px!important}.integral-score{color:#184D91!important;font-size:clamp(4rem,7vw,6.1rem)!important}
.integral-level{font-size:1rem!important}.integral-level span{color:#75879A!important;font-size:.78rem!important}
.integral-formula .formula{background:#F4F8FD!important;border:1px solid #D9E6F4!important;color:#173A60!important;box-shadow:inset 0 1px 0 #fff!important}
.integral-formula .formula-k{color:#668099!important}.integral-formula .formula-eq{color:#173A60!important;font-size:1rem!important}.integral-formula .formula-result{background:#FFFFFF!important;color:#215DB0!important;border:1px solid #D8E4F1!important}
.integral-bottom>div{background:#F7F9FC!important;border:1px solid #E1E8F0!important}.integral-bottom b{font-size:.72rem!important;color:#718196!important}.integral-bottom span{font-size:1rem!important;color:#173650!important}
.integral-signal{padding:7px 12px;border-radius:15px;background:#F7F9FC;border:1px solid #E2E9F0}
.human-box{margin-top:16px;padding:14px 16px;border-radius:15px;background:linear-gradient(135deg,#F5F9FE,#FBFCFE);border:1px solid #DDE8F4;color:#4F667D;font-size:.84rem;line-height:1.58}
.human-box b{color:#173B62}.human-box .headline{font-size:.92rem;font-weight:950;color:#163A60;margin-bottom:4px}
.side-stack{grid-template-rows:auto auto!important}.p17-card,.pei-mini{padding:17px 18px!important}.p17-card{background:#FAFBFD!important}.side-kicker{font-size:.66rem!important;color:#7B8998!important}
.p17-title,.pei-mini-title{font-size:1.02rem!important}.p17-score{font-size:2.35rem!important;color:#425469!important;margin-top:10px!important}.p17-level{font-size:.76rem!important}.p17-copy,.pei-mini-note{font-size:.73rem!important;line-height:1.55!important}
.pei-mini{background:#FCFDFE!important}.pei-mini-grid b{font-size:.84rem!important}
.kpi{min-height:132px!important}.kpi-label{font-size:.70rem!important}.kpi-v{font-size:1.48rem!important}.kpi-f{font-size:.65rem!important}
.dim-card{min-height:300px!important;padding:18px!important}.dim-code{font-size:.77rem!important}.dim-name{font-size:.76rem!important}.dim-level{font-size:.78rem!important}.dim-meta{font-size:.67rem!important;line-height:1.55!important}.dim-meaning{font-size:.70rem!important;line-height:1.52!important}.dim-foot{font-size:.64rem!important}
.insight-k{font-size:.68rem!important}.insight-t{font-size:1rem!important}.insight-x{font-size:.77rem!important;line-height:1.56!important}.interpret-banner{font-size:.78rem!important;line-height:1.55!important}
.scale-title{font-size:.80rem!important}.scale-name{font-size:.72rem!important}.scale-range,.scale-note{font-size:.66rem!important}.method-t{font-size:.96rem!important}.method-x,.method-alert{font-size:.76rem!important;line-height:1.58!important}
.quality-k{font-size:.66rem!important}.quality-v{font-size:1.48rem!important}.quality-x,.quality-warning{font-size:.73rem!important}.item-q{font-size:.66rem!important;line-height:1.52!important}.item-code{font-size:.66rem!important}.item-score{font-size:1.12rem!important}
.item-meta .k{font-size:.50rem!important}.item-meta .v{font-size:.63rem!important}
@media(max-width:1080px){.main-reading-grid{grid-template-columns:1fr!important}.side-stack{grid-template-columns:1fr 1fr!important;grid-template-rows:auto!important}.integral-core{grid-template-columns:230px 1fr!important}}
@media(max-width:700px){.block-container{padding:.48rem .68rem 2.2rem!important}.title{font-size:1.72rem!important}.sub{font-size:.84rem!important}.main-reading-grid{grid-template-columns:1fr!important}.side-stack{grid-template-columns:1fr!important}.integral-hero{padding:20px 18px!important}.integral-top{display:grid!important;grid-template-columns:1fr auto!important}.integral-title{font-size:1.55rem!important}.integral-text{font-size:.80rem!important}.integral-core{grid-template-columns:1fr!important}.integral-score{font-size:3.65rem!important}.integral-bottom{grid-template-columns:1fr 1fr!important}.integral-bottom>div:last-child{grid-column:1/-1!important}.p17-score{font-size:2.1rem!important}.section-title{font-size:1.35rem!important}.section-note{display:none!important}.kpi-grid{grid-template-columns:1fr 1fr!important}}
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
    return "—" if pd.isna(x) else f"{x*100:.{digits}f} pp"


def institutional_level(value: float) -> tuple[str, str, str, str]:
    """Escala PROPUESTA en el documento del instrumento, no asumida como norma UNT aprobada."""
    if pd.isna(value):
        return "Sin dato", "—", "#9AA7B5", "off"
    if value < .60:
        return "Insatisfactorio", "0–59%", "#E25B68", "red"
    if value < .75:
        return "Regular", "60–74%", "#F2A62C", "amber"
    if value < .90:
        return "Satisfactorio", "75–89%", "#16A878", "green"
    return "Muy satisfactorio", "90–100%", "#20AABD", "green"


def traffic_svg(state: str, size: int = 50) -> str:
    active = {
        "red": (1.0, .15, .15),
        "amber": (.15, 1.0, .15),
        "green": (.15, .15, 1.0),
        "off": (.15, .15, .15),
    }[state]
    return f'''<svg class="signal-shell" width="{size}" height="{int(size*1.62)}" viewBox="0 0 70 114" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Semáforo {state}">
      <defs>
        <linearGradient id="case{size}" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#344A5B"/><stop offset=".48" stop-color="#172531"/><stop offset="1" stop-color="#070C11"/></linearGradient>
        <radialGradient id="r{size}"><stop offset="0" stop-color="#FFAAB2"/><stop offset=".45" stop-color="#FF4758"/><stop offset="1" stop-color="#9C1726"/></radialGradient>
        <radialGradient id="a{size}"><stop offset="0" stop-color="#FFE6A9"/><stop offset=".45" stop-color="#FFB020"/><stop offset="1" stop-color="#A85A00"/></radialGradient>
        <radialGradient id="g{size}"><stop offset="0" stop-color="#A3F5D5"/><stop offset=".45" stop-color="#22C997"/><stop offset="1" stop-color="#08724F"/></radialGradient>
        <filter id="glow{size}"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <rect x="8" y="3" width="54" height="106" rx="19" fill="url(#case{size})" stroke="#465C6D" stroke-width="1.5"/>
      <rect x="14" y="9" width="42" height="94" rx="14" fill="#0B1117" opacity=".84"/>
      <circle cx="35" cy="27" r="13" fill="url(#r{size})" opacity="{active[0]}" {'filter="url(#glow'+str(size)+')"' if state=='red' else ''}/>
      <circle cx="35" cy="56" r="13" fill="url(#a{size})" opacity="{active[1]}" {'filter="url(#glow'+str(size)+')"' if state=='amber' else ''}/>
      <circle cx="35" cy="85" r="13" fill="url(#g{size})" opacity="{active[2]}" {'filter="url(#glow'+str(size)+')"' if state=='green' else ''}/>
      <ellipse cx="30" cy="22" rx="4.5" ry="2.5" fill="white" opacity=".34"/><ellipse cx="30" cy="51" rx="4.5" ry="2.5" fill="white" opacity=".34"/><ellipse cx="30" cy="80" rx="4.5" ry="2.5" fill="white" opacity=".34"/>
    </svg>'''


def section_header(kicker: str, title: str, note: str = "") -> None:
    st.markdown(
        f'''<div class="section-head"><div><div class="section-kicker">{escape(kicker)}</div><div class="section-title">{escape(title)}</div></div><div class="section-note">{escape(note)}</div></div>''',
        unsafe_allow_html=True,
    )


def spark_svg(color: str, variant: int = 0) -> str:
    paths = [
        "M2 15 L24 10 L45 13 L67 8 L94 10",
        "M2 13 L24 15 L45 9 L67 13 L94 7",
        "M2 12 L24 8 L45 11 L67 15 L94 9",
        "M2 15 L24 12 L45 7 L67 11 L94 8",
    ]
    p = paths[variant % len(paths)]
    return f'<svg viewBox="0 0 96 20" preserveAspectRatio="none"><path d="{p}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/><circle cx="94" cy="{[10,7,9,8][variant%4]}" r="2" fill="{color}"/></svg>'


# ==============================================================
# DATOS
# ==============================================================
def require_columns(df: pd.DataFrame) -> None:
    missing = [c for c in ALL_ITEMS if c not in df.columns]
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(missing))


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    require_columns(df)
    for c in ALL_ITEMS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Reglas explícitas de la propuesta del instrumento.
    for code, meta in DIMENSIONS.items():
        df[f"{code}_Prom"] = df[meta["items"]].mean(axis=1)
        df[f"{code}_Sat"] = (df[f"{code}_Prom"] >= 4).astype(float)

    # Estimación integral P1-P16 para seguimiento analítico del IND.01:
    # se extiende al conjunto de los 16 ítems la misma lógica usada en las dimensiones:
    # promedio individual >= 4 => estudiante satisfecho.
    # Esta operacionalización NO aparece formulada de manera literal en la ficha PEI;
    # debe validarse institucionalmente antes de usarla como regla oficial del IND.01.
    df["Integral_P1P16_Prom"] = df[ITEMS_16].mean(axis=1)
    df["Integral_P1P16_Sat"] = (df["Integral_P1P16_Prom"] >= 4).astype(float)

    # P17: 4 o 5 = satisfecho; 1, 2 o 3 = no satisfecho.
    # Se conserva como percepción global directa y medida complementaria.
    df["P17_Sat"] = (df["P17"] >= 4).astype(float)
    return df


@st.cache_data(show_spinner=False)
def load_data(path: str, mtime: float) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=SHEET_NAME)
    return prepare_data(raw)


if not DATA_FILE.exists():
    st.error("No se encontró basededatos.xlsx. Debe estar en la misma carpeta que app.py.")
    st.stop()

try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"No pude leer basededatos.xlsx: {exc}")
    st.stop()

N_TOTAL = int(len(df))

# Resultado integral P1-P16 (operacionalización analítica para seguimiento).
INTEGRAL = float(df["Integral_P1P16_Sat"].mean())
N_INTEGRAL = int(df["Integral_P1P16_Sat"].sum())
INTEGRAL_MEAN = float(df["Integral_P1P16_Prom"].mean())

# P17: percepción global directa, complementaria al análisis integral.
GLOBAL = float(df["P17_Sat"].mean())
N_GLOBAL = int(df["P17_Sat"].sum())
GLOBAL_MEAN = float(df["P17"].mean())
REFERENCE_DELTA = GLOBAL - PEI_REFERENCE
GAP_TO_SATISFACTORY = max(0.0, 0.75 - GLOBAL)

MISSING_RESPONSES = int(df[ALL_ITEMS].isna().sum().sum())
INVALID_RESPONSES = int((~df[ALL_ITEMS].isin([1, 2, 3, 4, 5]) & df[ALL_ITEMS].notna()).sum().sum())
UNIFORM_MASK = df[ALL_ITEMS].nunique(axis=1, dropna=True) == 1
UNIFORM_N = int(UNIFORM_MASK.sum())
UNIFORM_PCT = UNIFORM_N / N_TOTAL if N_TOTAL else float("nan")

def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """IC de Wilson para una proporción binomial.

    Solo debe interpretarse como inferencia poblacional estricta cuando el diseño
    de selección sea probabilístico o razonablemente equivalente.
    """
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + (z**2) / n
    center = (p + (z**2)/(2*n)) / den
    half = z * math.sqrt((p*(1-p)/n) + (z**2)/(4*n*n)) / den
    return (center-half, center+half)


def spearman_corr(a: pd.Series, b: pd.Series) -> float:
    x = pd.concat([pd.to_numeric(a, errors="coerce"), pd.to_numeric(b, errors="coerce")], axis=1).dropna()
    if len(x) < 3:
        return float("nan")
    return float(x.iloc[:,0].rank(method="average").corr(x.iloc[:,1].rank(method="average")))


def cronbach_alpha(cols: list[str]) -> float:
    x = df[cols].dropna()
    k = len(cols)
    if k < 2 or len(x) < 2:
        return float("nan")
    item_var = x.var(axis=0, ddof=1).sum()
    total_var = x.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return float("nan")
    return float((k / (k - 1)) * (1 - item_var / total_var))

ALPHA_P1_P16 = cronbach_alpha(ITEMS_16)
ALPHA_DIMS = {code: cronbach_alpha(meta["items"]) for code, meta in DIMENSIONS.items()}
INTEGRAL_CI_LOW, INTEGRAL_CI_HIGH = wilson_interval(N_INTEGRAL, N_TOTAL)
GLOBAL_CI_LOW, GLOBAL_CI_HIGH = wilson_interval(N_GLOBAL, N_TOTAL)
P1P16_MEAN = df[ITEMS_16].mean(axis=1)
RHO_P17_P1P16 = spearman_corr(df["P17"], P1P16_MEAN)
DATE_START = pd.to_datetime(df["Fecha"], errors="coerce").min() if "Fecha" in df.columns else pd.NaT
DATE_END = pd.to_datetime(df["Fecha"], errors="coerce").max() if "Fecha" in df.columns else pd.NaT


def dimension_summary() -> pd.DataFrame:
    rows = []
    for code, meta in DIMENSIONS.items():
        sat = float(df[f"{code}_Sat"].mean())
        avg = float(df[f"{code}_Prom"].mean())
        n_sat = int(df[f"{code}_Sat"].sum())
        level, interval, color, state = institutional_level(sat)
        ci_low, ci_high = wilson_interval(n_sat, N_TOTAL)
        rows.append({
            "Código": code,
            "Dimensión": meta["name"],
            "Satisfacción": sat,
            "Promedio": avg,
            "N satisfechos": n_sat,
            "IC95 inferior": ci_low,
            "IC95 superior": ci_high,
            "Nivel": level,
            "Intervalo": interval,
            "Color": color,
            "Semáforo": state,
        })
    return pd.DataFrame(rows)


def item_summary() -> pd.DataFrame:
    rows = []
    for i in range(1, 17):
        item = f"P{i}"
        s = df[item].dropna()
        code = f"D{((i-1)//4)+1}"
        rows.append({
            "Número": i,
            "Ítem": item,
            "Dimensión": code,
            "Pregunta": ITEM_TEXT[item],
            "Promedio": float(s.mean()),
            "Favorable": float((s >= 4).mean()),
            "Neutral": float((s == 3).mean()),
            "Desfavorable": float((s <= 2).mean()),
        })
    return pd.DataFrame(rows)


DIMS = dimension_summary()
ITEMS_SUM = item_summary()
PRIORITY_DIM = DIMS.sort_values("Satisfacción").iloc[0]
STRONG_DIM = DIMS.sort_values("Satisfacción", ascending=False).iloc[0]
PRIORITY_ITEM = ITEMS_SUM.sort_values("Favorable").iloc[0]
STRONG_ITEM = ITEMS_SUM.sort_values("Favorable", ascending=False).iloc[0]
INTEGRAL_LEVEL, INTEGRAL_INTERVAL, INTEGRAL_COLOR, INTEGRAL_STATE = institutional_level(INTEGRAL)
GLOBAL_LEVEL, GLOBAL_INTERVAL, GLOBAL_COLOR, GLOBAL_STATE = institutional_level(GLOBAL)


# ==============================================================
# HTML COMPONENTS
# ==============================================================
def top_header() -> None:
    period = "11–31 ago 2026" if pd.notna(DATE_START) and pd.notna(DATE_END) else "2026"
    st.markdown(
        f'''<div class="topbar">
          <div class="brand"><div class="brand-img"><img src="https://i.ibb.co/V0hydyyH/Whats-App-Image-2026-09-02-at-1-58-16-PM.jpg" alt="Identidad institucional UNT"></div><div><div class="brand-title">Tablero Ejecutivo de Satisfacción</div><div class="brand-sub">Universidad Nacional de Trujillo · OEI.01 · IND.01</div></div></div>
          <div class="top-meta"><div class="meta-box">Periodo de encuesta<b>{period}</b></div><div class="meta-box">Base analizada<b>{N_TOTAL:,} estudiantes</b></div><div class="meta-box">Instrumento<b>17 ítems · 4 dimensiones</b></div></div>
        </div>
        <div class="pagehead"><div><div class="kicker">Tablero ejecutivo · análisis estadístico 2026</div><div class="title">Indicador de satisfacción con el proceso de formación académica</div><div class="sub"><b>P1–P16 constituye la lectura principal del tablero</b>: reúne las cuatro dimensiones que describen el proceso de formación académica. <b>P17 se muestra en segundo plano</b> como una pregunta global de contraste. La estadística observada, la escala interpretativa propuesta y la ficha PEI se presentan por separado para evitar conclusiones confusas.</div><div class="chips"><span class="chip">👥 {N_TOTAL:,} estudiantes</span><span class="chip">▦ P1–P16 · indicador integral</span><span class="chip">D1–D4 · diagnóstico explicativo</span><span class="chip">◉ P17 · contraste complementario</span></div></div><div class="basebox">Encuesta 2026<b>{period}</b></div></div>''',
        unsafe_allow_html=True,
    )


def formula_html(n: int, d: int, result: float, caption: str = "Fórmula diagnóstica") -> str:
    return f'''<div class="formula"><div class="formula-k">{escape(caption)}</div><div class="formula-eq"><span>Porcentaje =</span><span class="frac"><span>N</span><span class="bar"></span><span>D</span></span><span>× 100 =</span><span class="frac"><span>{n:,}</span><span class="bar"></span><span>{d:,}</span></span><span>× 100 =</span><span class="formula-result">{pct(result)}</span></div></div>'''


def scale_html(value: float) -> str:
    level, interval, color_now, _ = institutional_level(value)
    levels = [("Insatisfactorio", "0–59%", "#E25B68"), ("Regular", "60–74%", "#F2A62C"), ("Satisfactorio", "75–89%", "#16A878"), ("Muy satisfactorio", "90–100%", "#20AABD")]
    cards = []
    for name, rng, color in levels:
        active = " active" if name == level else ""
        cards.append(f'<div class="scale-step{active}" style="--lvl:{color}"><div class="scale-dot" style="background:{color}"></div><div class="scale-name">{name}</div><div class="scale-range">{rng}</div></div>')
    return f'''<div class="panel scale-wrap"><div class="scale-title">Escala interpretativa PROPUESTA del instrumento · Resultado actual: <span style="color:{color_now}">{escape(level)} ({escape(interval)})</span></div><div class="scale4">{"".join(cards)}</div><div class="scale-note"><b>No confundir con el PEI:</b> la ficha técnica oficial fija un <b>valor referencial ≥60%</b>, pero no establece estas cuatro categorías. Los rangos provienen de la propuesta del instrumento y pueden ajustarse según lineamientos institucionales.</div></div>'''


def primary_cards_html() -> str:
    integral_ci = f"{pct(INTEGRAL_CI_LOW)} – {pct(INTEGRAL_CI_HIGH)}"
    p17_ci = f"{pct(GLOBAL_CI_LOW)} – {pct(GLOBAL_CI_HIGH)}"
    every100 = round(INTEGRAL * 100)
    delta = GLOBAL - INTEGRAL

    kpis = [
        ("Estudiantes analizados", f"{N_TOTAL:,}", "Denominador del análisis", "👥", "#2457B8", "#EEF4FF"),
        ("Satisfechos P1–P16", f"{N_INTEGRAL:,}", "Promedio individual ≥4", "✓", "#14846C", "#EDF8F5"),
        ("Satisfacción integral", pct(INTEGRAL), "Resultado principal", "▦", "#2457B8", "#EEF4FF"),
        ("IC 95% aprox.*", integral_ci, "Precisión estadística", "↔", "#0F7D92", "#EEF9FB"),
        ("Promedio P1–P16", f"{INTEGRAL_MEAN:.2f} / 5", "Media de los 16 ítems", "∑", "#5A6475", "#F3F5F7"),
        ("P17 · contraste", pct(GLOBAL), "Pregunta global directa", "◉", "#7A8490", "#F5F6F8"),
    ]
    kpi_html=[]
    for i,(label,val,foot,icon,accent,soft) in enumerate(kpis):
        kpi_html.append(f'<div class="kpi" style="--accent:{accent};--soft:{soft}"><div class="kpi-head"><div class="kpi-label">{escape(label)}</div><div class="kpi-icon">{icon}</div></div><div class="kpi-v">{escape(val)}</div><div class="kpi-f">{escape(foot)}</div><div class="spark">{spark_svg(accent,i)}</div></div>')

    return f'''<div class="main-reading-grid">
      <div class="integral-hero">
        <div class="integral-top">
          <div>
            <div class="integral-eyebrow">IND.01 · estimación integral para el análisis 2026</div>
            <div class="integral-title">Satisfacción integral de las 16 preguntas · P1–P16</div>
            <div class="integral-text">La lectura principal reúne las cuatro dimensiones del instrumento. Para cada estudiante se calcula su promedio en P1–P16 y se clasifica como satisfecho cuando ese promedio es <b>≥4</b>. Con esta operacionalización integral, <b>{N_INTEGRAL:,} de {N_TOTAL:,}</b> estudiantes cumplen el criterio.</div>
          </div>
          <div class="integral-signal">{traffic_svg(INTEGRAL_STATE,56)}</div>
        </div>
        <div class="integral-core">
          <div><div class="integral-score">{pct(INTEGRAL)}</div><div class="integral-level" style="color:{INTEGRAL_COLOR}">{escape(INTEGRAL_LEVEL)} · {escape(INTEGRAL_INTERVAL)} <span>escala interpretativa propuesta</span></div></div>
          <div class="integral-formula">{formula_html(N_INTEGRAL,N_TOTAL,INTEGRAL,"Cálculo integral P1–P16")}</div>
        </div>
        <div class="human-box"><div class="headline">¿Cómo explicarlo en una exposición?</div>En términos sencillos, <b>aproximadamente {every100} de cada 100 estudiantes</b> alcanzan un promedio de 4 o más cuando se evalúan conjuntamente los 16 aspectos de la formación académica. El resultado no significa que el resto esté “totalmente insatisfecho”; significa que <b>no alcanzó el criterio integral exigente de promedio ≥4 en el conjunto P1–P16</b>. Por eso las cuatro dimensiones sirven para identificar dónde se concentran las principales brechas.</div>
        <div class="integral-bottom"><div><b>IC 95% aprox.*</b><span>{integral_ci}</span></div><div><b>Promedio P1–P16</b><span>{INTEGRAL_MEAN:.2f}/5</span></div><div><b>Estructura</b><span>D1 · D2 · D3 · D4</span></div></div>
      </div>
      <div class="side-stack">
        <div class="panel p17-card"><div class="p17-head"><div><div class="side-kicker">Contraste complementario</div><div class="p17-title">P17 · satisfacción general declarada</div></div>{traffic_svg(GLOBAL_STATE,29)}</div><div class="p17-score">{pct(GLOBAL)}</div><div class="p17-level" style="color:{GLOBAL_COLOR}">{escape(GLOBAL_LEVEL)} · {escape(GLOBAL_INTERVAL)}</div><div class="p17-copy"><b>{N_GLOBAL:,} de {N_TOTAL:,}</b> estudiantes respondieron 4 o 5. IC 95% aprox.: <b>{p17_ci}</b>. P17 es una sola pregunta global y se usa aquí <b>como contraste</b>, no como sustituto de la lectura integral P1–P16.</div></div>
        <div class="panel pei-mini"><div class="side-kicker">Cómo interpretar la diferencia</div><div class="pei-mini-title">P17 es {pp(delta)} mayor que P1–P16</div><div class="pei-mini-note">Esto no es una contradicción. Una pregunta global recoge una valoración general, mientras que el criterio P1–P16 exige desempeño favorable sostenido en 16 aspectos. En esta base ambas medidas están fuertemente asociadas (<b>ρ de Spearman = {RHO_P17_P1P16:.3f}</b>), pero no son equivalentes.</div></div>
      </div>
    </div><div class="kpi-grid">{"".join(kpi_html)}</div><div class="stat-footnote">* IC 95% de Wilson. Se interpreta como inferencia poblacional estricta solo si el diseño de selección de estudiantes es probabilístico o razonablemente equivalente; de lo contrario, funciona como referencia de precisión de la proporción observada.</div>'''

def dimension_cards_html() -> str:
    cards=[]
    for _,r in DIMS.sort_values("Código").iterrows():
        code=r["Código"]; meta=DIMENSIONS[code]; sat=float(r["Satisfacción"]); avg=float(r["Promedio"])
        level,interval,color,state=institutional_level(sat)
        ci_low=float(r["IC95 inferior"]); ci_high=float(r["IC95 superior"])
        cards.append(f'''<div class="panel dim-card" style="--accent:{meta['accent']};--soft:{meta['soft']}"><div class="dim-head"><div><div class="dim-code">{meta['icon']} {code}</div><div class="dim-name">{escape(meta['name'])}</div></div>{traffic_svg(state,30)}</div><div class="dim-body"><div class="donut" style="--p:{sat*100:.2f};--accent:{meta['accent']}"><b>{pct(sat)}</b></div><div><div class="dim-level" style="color:{color}">{escape(level)}</div><div class="dim-meta"><b>{escape(interval)}</b> · escala propuesta<br>{int(r['N satisfechos']):,} de {N_TOTAL:,} estudiantes<br>IC 95% aprox.*: <b>{pct(ci_low)}–{pct(ci_high)}</b><br>Promedio: <b>{avg:.2f}/5</b></div></div></div><div class="dim-meaning"><b>Qué evalúa:</b> {escape(meta['meaning'])}</div><div class="dim-foot"><span>Regla documental: promedio de 4 ítems ≥4</span><b>{', '.join(meta['items'])}</b></div></div>''')
    return '<div class="dim-grid">'+''.join(cards)+'</div>'

def insights_html() -> str:
    pri=PRIORITY_DIM; pitem=PRIORITY_ITEM; strong_dim=STRONG_DIM; strong_item=STRONG_ITEM
    delta_p17 = GLOBAL - INTEGRAL
    return f'''<div class="insight-grid">
      <div class="panel insight" style="--accent:#2457B8"><div class="insight-k">Qué significa el resultado integral</div><div class="insight-t">{pct(INTEGRAL)} · {N_INTEGRAL:,} estudiantes</div><div class="insight-x">El criterio integral exige que el promedio personal de las 16 respuestas sea ≥4. Por ello, el {pct(INTEGRAL)} debe leerse como la proporción que alcanza un nivel favorable <b>de manera conjunta</b> en el proceso formativo, no como el promedio simple de porcentajes favorables de cada pregunta.</div></div>
      <div class="panel insight" style="--accent:{DIMENSIONS[str(pri['Código'])]['accent']}"><div class="insight-k">Dónde está la principal dificultad</div><div class="insight-t">{pri['Código']} · {pct(float(pri['Satisfacción']))}</div><div class="insight-x"><b>{escape(str(pri['Dimensión']))}</b> es la dimensión con menor satisfacción. Dentro de ella, <b>{pitem['Ítem']}</b> registra {pct(float(pitem['Favorable']))} de valoración favorable. Esto señala como prioridad revisar los aspectos vinculados a <b>infraestructura y recursos educativos</b>, junto con los demás componentes de D3.</div></div>
      <div class="panel insight" style="--accent:{DIMENSIONS[str(strong_dim['Código'])]['accent']}"><div class="insight-k">Dónde aparece la mayor fortaleza</div><div class="insight-t">{strong_dim['Código']} · {pct(float(strong_dim['Satisfacción']))}</div><div class="insight-x"><b>{escape(str(strong_dim['Dimensión']))}</b> presenta el mejor resultado dimensional. Además, <b>{strong_item['Ítem']}</b> es el ítem con mayor valoración favorable ({pct(float(strong_item['Favorable']))}). Conviene conservar estas fortalezas mientras se atienden las brechas de D3.</div></div>
      <div class="panel insight" style="--accent:#6C7583"><div class="insight-k">Por qué P17 es más alto</div><div class="insight-t">P17 {pct(GLOBAL)} · diferencia {pp(delta_p17)}</div><div class="insight-x">La pregunta P17 recoge una impresión global y resulta más favorable que el criterio integral P1–P16. La asociación entre ambas es alta (<b>ρ={RHO_P17_P1P16:.3f}</b>), por lo que se mueven en la misma dirección, pero la diferencia muestra que <b>una percepción general positiva no implica que todos los componentes específicos alcancen el mismo nivel</b>.</div></div>
    </div><div class="interpret-banner"><b>Mensaje para la toma de decisiones:</b> el tablero no busca reducir la satisfacción a un solo número. El {pct(INTEGRAL)} resume la lectura integral; D1–D4 muestran <b>en qué parte del proceso</b> se originan las brechas; y P17 funciona como una comprobación de la percepción global. Esta combinación permite explicar el resultado de forma más útil y defendible.</div>'''

def pei_route_html() -> str:
    nodes=[f'''<div class="node diag" style="--accent:#D7A53B"><div class="node-y">2026</div><div class="node-v">Diseño · estandarización · validación</div><div class="node-c">La ficha PEI indica que no se generan todavía valores medibles oficiales del indicador.</div></div>''']
    for y,t in PEI_TARGETS.items():
        abs_target={2027:"8,400 / 14,000",2028:"9,100 / 14,000",2029:"9,800 / 14,000",2030:"10,500 / 14,000"}[y]
        nodes.append(f'''<div class="node" style="--accent:#2F66D8"><div class="node-y">{y}</div><div class="node-v">{pct(t,0)}</div><div class="node-c">Logro esperado · {abs_target}</div></div>''')
    return f'''<div class="panel pei-card"><div class="pei-banner"><div class="i">⚠</div><div><div class="t">Cómo debe leerse el PEI frente a estas encuestas 2026</div><div class="x">La base 2026 puede utilizarse como diagnóstico o línea base preliminar. No debe presentarse como cumplimiento oficial del PEI 2026, porque la ficha técnica señala que la medición efectiva inicia a partir de 2027. El 60% funciona como valor referencial y como logro esperado para 2027, no como meta oficial del año 2026.</div></div></div><div class="route">{''.join(nodes)}</div></div>'''


def item_cards_html(selected: str) -> str:
    d=ITEMS_SUM.copy() if selected=="Todas" else ITEMS_SUM[ITEMS_SUM["Dimensión"]==selected].copy()
    cards=[]
    for _,r in d.sort_values(["Dimensión","Número"]).iterrows():
        code=str(r["Dimensión"]); meta=DIMENSIONS[code]; fav=float(r["Favorable"]); neu=float(r["Neutral"]); bad=float(r["Desfavorable"])
        cards.append(f'''<div class="panel item" style="--accent:{meta['accent']};--soft:{meta['soft']}"><div class="item-top"><div class="item-code">{r['Ítem']} · {code}</div><div class="item-score">{pct(fav)}</div></div><div class="item-q">{escape(str(r['Pregunta']))}</div><div class="meter"><span style="width:{fav*100:.2f}%"></span></div><div class="item-meta"><div><div class="k">Favorable</div><div class="v">{pct(fav)}</div></div><div><div class="k">Neutral</div><div class="v">{pct(neu)}</div></div><div><div class="k">Promedio</div><div class="v">{float(r['Promedio']):.2f}</div></div></div></div>''')
    return '<div class="item-grid">'+''.join(cards)+'</div>'


def likert_html(selected: str) -> str:
    d=ITEMS_SUM.copy() if selected=="Todas" else ITEMS_SUM[ITEMS_SUM["Dimensión"]==selected].copy()
    rows=[]
    for _,r in d.sort_values(["Dimensión","Número"]).iterrows():
        bad=float(r["Desfavorable"]); neu=float(r["Neutral"]); fav=float(r["Favorable"])
        def label(v: float) -> str:
            return f"{v*100:.0f}%" if v >= .085 else ""
        rows.append(f'''<div class="likert-row"><div class="likert-code">{r['Ítem']}</div><div class="likert-pill"><div class="seg bad" style="width:{bad*100:.3f}%">{label(bad)}</div><div class="seg neutral" style="width:{neu*100:.3f}%">{label(neu)}</div><div class="seg good" style="width:{fav*100:.3f}%">{label(fav)}</div></div></div>''')
    return '<div class="panel likert">'+''.join(rows)+'</div>'


def selected_insights_html(selected: str) -> str:
    d=ITEMS_SUM.copy() if selected=="Todas" else ITEMS_SUM[ITEMS_SUM["Dimensión"]==selected].copy()
    weak=d.sort_values("Favorable").iloc[0]; strong=d.sort_values("Favorable",ascending=False).iloc[0]
    if selected=="Todas":
        context="El análisis cubre P1–P16 y permite localizar fortalezas y cuellos de botella del instrumento."
        action="Priorizar los ítems con menor valoración favorable y leerlos dentro de su dimensión; no convertir porcentajes por ítem en el indicador PEI."
    else:
        context=f"{selected} evalúa {DIMENSIONS[selected]['meaning'].lower()}"
        action=f"Usar estos cuatro ítems para explicar el resultado de {selected}; la clasificación dimensional se obtiene con el promedio de los cuatro ítems por estudiante."
    return f'''<div class="insight-grid" style="grid-template-columns:repeat(4,minmax(0,1fr))"><div class="panel insight" style="--accent:#3265CF"><div class="insight-k">Bloque analizado</div><div class="insight-t">{escape(selected)}</div><div class="insight-x">{escape(context)}</div></div><div class="panel insight" style="--accent:#E25B68"><div class="insight-k">Aspecto prioritario</div><div class="insight-t">{weak['Ítem']} · {pct(float(weak['Favorable']))} favorable</div><div class="insight-x">{escape(str(weak['Pregunta']))}<br><b>{pct(float(weak['Desfavorable']))}</b> desfavorable · promedio <b>{float(weak['Promedio']):.2f}/5</b>.</div></div><div class="panel insight" style="--accent:#16A878"><div class="insight-k">Fortaleza del bloque</div><div class="insight-t">{strong['Ítem']} · {pct(float(strong['Favorable']))} favorable</div><div class="insight-x">{escape(str(strong['Pregunta']))}<br>Promedio <b>{float(strong['Promedio']):.2f}/5</b>.</div></div><div class="panel insight" style="--accent:#7C5CE7"><div class="insight-k">Cómo usarlo</div><div class="insight-t">Lectura para decisión</div><div class="insight-x">{escape(action)}</div></div></div>'''


def quality_html() -> str:
    completeness = 1 - (MISSING_RESPONSES / (N_TOTAL * len(ALL_ITEMS))) if N_TOTAL else float("nan")
    valid_pct = 1 - (INVALID_RESPONSES / (N_TOTAL * len(ALL_ITEMS))) if N_TOTAL else float("nan")
    alpha_dims = " · ".join([f"{k} {v:.3f}" for k,v in ALPHA_DIMS.items()])
    return f'''<div class="quality-grid">
      <div class="panel quality-card" style="--accent:#16A878"><div class="quality-k">Completitud P1–P17</div><div class="quality-v">{pct(completeness)}</div><div class="quality-x">{MISSING_RESPONSES:,} valores faltantes en los 17 ítems.</div></div>
      <div class="panel quality-card" style="--accent:#2F66D8"><div class="quality-k">Rango de respuestas</div><div class="quality-v">{pct(valid_pct)}</div><div class="quality-x">{INVALID_RESPONSES:,} respuestas fuera de la escala 1–5.</div></div>
      <div class="panel quality-card" style="--accent:#7C5CE7"><div class="quality-k">Consistencia interna P1–P16</div><div class="quality-v">α = {ALPHA_P1_P16:.3f}</div><div class="quality-x">Alfas dimensionales: {alpha_dims}. Valores altos indican consistencia interna, no validez del instrumento.</div></div>
      <div class="panel quality-card" style="--accent:#F2A62C"><div class="quality-k">Patrones uniformes P1–P17</div><div class="quality-v">{pct(UNIFORM_PCT)}</div><div class="quality-x">{UNIFORM_N:,} estudiantes marcaron exactamente la misma alternativa en los 17 ítems.</div></div>
    </div><div class="quality-warning"><b>Advertencia estadística:</b> el alfa muy alto puede reflejar buena consistencia, pero también redundancia entre ítems o patrones de respuesta poco diferenciados. El {pct(UNIFORM_PCT)} de respuestas uniformes merece auditoría, no eliminación automática. La validez de contenido mediante <b>V de Aiken</b> requiere jueces expertos; la representatividad poblacional requiere conocer el diseño muestral, cobertura y no respuesta.</div>'''


# ==============================================================
# APP
# ==============================================================
top_header()

tab1, tab2, tab3 = st.tabs(["◉ Visión ejecutiva", "▦ Dimensiones e ítems", "ⓘ Método, PEI y calidad"])

with tab1:
    section_header(
        "Indicador principal",
        "Satisfacción integral P1–P16",
        "Resultado principal construido con las 16 preguntas de las cuatro dimensiones; P17 se presenta únicamente como contraste complementario.",
    )
    st.markdown(primary_cards_html(), unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(scale_html(INTEGRAL), unsafe_allow_html=True)

    section_header(
        "Diagnóstico 4D",
        "Satisfacción en las cuatro dimensiones",
        "Cada dimensión se estima con la regla documental promedio ≥4; el semáforo solo traduce la escala propuesta y no constituye una prueba estadística.",
    )
    st.markdown(dimension_cards_html(), unsafe_allow_html=True)

    section_header(
        "Interpretación ejecutiva",
        "Qué dicen los resultados y qué decisiones sugieren",
        "Lectura descriptiva con precisión estadística aproximada, confiabilidad y asociación exploratoria.",
    )
    st.markdown(insights_html(), unsafe_allow_html=True)

    section_header(
        "Marco documental",
        "Referencia de la ficha PEI",
        "Esta sección contextualiza el indicador; no modifica ni determina estadísticamente los resultados observados de la encuesta.",
    )
    st.markdown(pei_route_html(), unsafe_allow_html=True)

with tab2:
    section_header("Explorador", "Dimensiones e ítems", "Visualizaciones estáticas y responsivas: no hay zoom, arrastre ni ejes móviles.")
    selected = st.selectbox(
        "Dimensión a analizar",
        ["Todas", "D1", "D2", "D3", "D4"],
        format_func=lambda x: "Todas las dimensiones · P1–P16" if x == "Todas" else f"{x} · {DIMENSIONS[x]['name']}",
        label_visibility="collapsed",
    )
    section_header("Lectura del bloque", "Qué destaca y qué requiere atención")
    st.markdown(selected_insights_html(selected), unsafe_allow_html=True)
    section_header("Valoración favorable", "Panel de aspectos del instrumento", "4–5 = favorable. Los ítems explican las dimensiones; no se reportan como indicadores PEI individuales.")
    st.markdown(item_cards_html(selected), unsafe_allow_html=True)
    section_header("Distribución de respuesta", "Desfavorable · neutral · favorable", "1–2 = desfavorable · 3 = neutral · 4–5 = favorable.")
    st.markdown(likert_html(selected), unsafe_allow_html=True)
    with st.expander("Ver detalle técnico de los ítems"):
        dshow = ITEMS_SUM.copy() if selected == "Todas" else ITEMS_SUM[ITEMS_SUM["Dimensión"] == selected].copy()
        dshow = dshow.sort_values(["Dimensión", "Número"])
        table = dshow[["Ítem", "Dimensión", "Pregunta", "Favorable", "Neutral", "Desfavorable", "Promedio"]].copy()
        for c in ["Favorable", "Neutral", "Desfavorable"]:
            table[c] = table[c].map(lambda x: f"{x*100:.1f}%")
        table["Promedio"] = table["Promedio"].map(lambda x: f"{x:.2f}")
        st.dataframe(table, use_container_width=True, hide_index=True, height=min(600, 45 + 36*len(table)))

with tab3:
    section_header("PEI oficial", "Qué establece la ficha técnica IND.01")
    st.markdown(
        '''<div class="method-grid">
          <div class="panel method"><div class="method-i">◎</div><div class="method-t">Indicador y fórmula</div><div class="method-x"><b>IND.01:</b> porcentaje de estudiantes de pregrado satisfechos con su proceso de formación académica. Fórmula oficial: <b>(N/D) × 100</b>.</div></div>
          <div class="panel method"><div class="method-i">⚠</div><div class="method-t">Situación 2026</div><div class="method-x">La ficha indica diseño, estandarización y validación del instrumento durante 2026, <b>sin generar todavía valores medibles oficiales</b>. La medición efectiva inicia en 2027.</div></div>
          <div class="panel method"><div class="method-i">🎯</div><div class="method-t">Referencia documental, no corte estadístico</div><div class="method-x">La ficha consigna un valor referencial <b>≥60%</b> y logros esperados 2027–2030. Ese 60% es un criterio de planeamiento; <b>no se deriva de los datos</b> y no define por sí mismo si el resultado es estadísticamente bueno o malo.</div></div>
        </div>''', unsafe_allow_html=True)

    section_header("Instrumento propuesto", "Qué reglas de cálculo están explícitamente definidas")
    st.markdown(
        '''<div class="method-grid">
          <div class="panel method"><div class="method-i">▦</div><div class="method-t">Cómo se obtiene el resultado integral P1–P16</div><div class="method-x">Cada dimensión contiene cuatro preguntas y el documento usa <b>promedio ≥4</b> para clasificar al estudiante como satisfecho en esa dimensión. Para obtener una lectura integral del conjunto P1–P16, este tablero aplica la misma lógica al promedio de las 16 preguntas. Así se obtiene un único estado por estudiante y luego se calcula <b>N/D × 100</b>. La adopción oficial de esta regla global debe formalizarse institucionalmente.</div></div>
          <div class="panel method"><div class="method-i">◉</div><div class="method-t">P17 · contraste global</div><div class="method-x">P17: respuesta <b>4 o 5 = satisfecho</b>; 1, 2 o 3 = no satisfecho. Se muestra como percepción global directa y complementaria para contrastar la lectura integral P1–P16.</div></div>
          <div class="panel method"><div class="method-i">🚦</div><div class="method-t">Escala propuesta, no clasificación estadística</div><div class="method-x"><b>0–59%</b> Insatisfactorio · <b>60–74%</b> Regular · <b>75–89%</b> Satisfactorio · <b>90–100%</b> Muy satisfactorio. Estos rangos provienen de la propuesta del instrumento y pueden ajustarse; el semáforo es solo una ayuda visual.</div></div>
        </div>''', unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('''<div class="method-alert"><b>Criterio estadístico usado en este tablero:</b> la lectura principal P1–P16 es una <b>estimación operativa integral</b> construida aplicando promedio individual ≥4; P17 se presenta como contraste global. Ambas proporciones se acompañan de IC 95% aproximados de Wilson. La ficha PEI y su valor referencial se mantienen separados. <b>La regla global P1–P16 debe validarse institucionalmente antes de utilizarse como cálculo oficial del IND.01.</b></div>''', unsafe_allow_html=True)

    section_header("Calidad de datos", "Controles que conviene revisar antes del informe oficial")
    st.markdown(quality_html(), unsafe_allow_html=True)

    section_header("Resultados diagnósticos 2026", "Resumen técnico de la base actual")
    summary = pd.DataFrame([
        ["Integral P1–P16 · estimación operativa", pct(INTEGRAL), f"{pct(INTEGRAL_CI_LOW)}–{pct(INTEGRAL_CI_HIGH)}", INTEGRAL_LEVEL, f"{N_INTEGRAL:,} / {N_TOTAL:,}", "Promedio P1–P16 ≥4 (regla analítica)"],
        ["P17 · satisfacción general directa", pct(GLOBAL), f"{pct(GLOBAL_CI_LOW)}–{pct(GLOBAL_CI_HIGH)}", GLOBAL_LEVEL, f"{N_GLOBAL:,} / {N_TOTAL:,}", "P17 = 4 o 5"],
        *[[f"{r['Código']} · {r['Dimensión']}", pct(float(r['Satisfacción'])), f"{pct(float(r['IC95 inferior']))}–{pct(float(r['IC95 superior']))}", str(r['Nivel']), f"{int(r['N satisfechos']):,} / {N_TOTAL:,}", "Promedio de 4 ítems ≥4"] for _,r in DIMS.sort_values('Código').iterrows()],
    ], columns=["Medida", "Resultado", "IC 95% aprox.*", "Escala propuesta", "N / D", "Regla"])
    st.dataframe(summary, use_container_width=True, hide_index=True)
