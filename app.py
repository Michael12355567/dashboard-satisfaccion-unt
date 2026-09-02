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

    # Reglas explícitas del documento del instrumento:
    # D1-D4: satisfecho si el promedio de sus cuatro ítems >= 4.
    for code, meta in DIMENSIONS.items():
        df[f"{code}_Prom"] = df[meta["items"]].mean(axis=1)
        df[f"{code}_Sat"] = (df[f"{code}_Prom"] >= 4).astype(float)

    # Satisfacción general: P17 = 4 o 5 => satisfecho.
    df["P17_Sat"] = (df["P17"] >= 4).astype(float)

    # Análisis complementario P1-P16: NO está definido como IND.01 global en los documentos.
    # Se conserva solo para contraste analítico y se etiqueta como no oficial.
    df["P1P16_Prom"] = df[ITEMS_16].mean(axis=1)
    df["P1P16_Sat_Analitico"] = (df["P1P16_Prom"] >= 4).astype(float)
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
GLOBAL = float(df["P17_Sat"].mean())
N_GLOBAL = int(df["P17_Sat"].sum())
GLOBAL_MEAN = float(df["P17"].mean())
INTEGRAL16 = float(df["P1P16_Sat_Analitico"].mean())
N_INTEGRAL16 = int(df["P1P16_Sat_Analitico"].sum())
INTEGRAL16_MEAN = float(df["P1P16_Prom"].mean())
DELTA_GLOBAL_INTEGRAL = GLOBAL - INTEGRAL16


def dimension_summary() -> pd.DataFrame:
    rows = []
    for code, meta in DIMENSIONS.items():
        sat = float(df[f"{code}_Sat"].mean())
        avg = float(df[f"{code}_Prom"].mean())
        n_sat = int(df[f"{code}_Sat"].sum())
        level, interval, color, state = institutional_level(sat)
        rows.append({
            "Código": code,
            "Dimensión": meta["name"],
            "Satisfacción": sat,
            "Promedio": avg,
            "N satisfechos": n_sat,
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
GLOBAL_LEVEL, GLOBAL_INTERVAL, GLOBAL_COLOR, GLOBAL_STATE = institutional_level(GLOBAL)


# ==============================================================
# HTML COMPONENTS
# ==============================================================
def top_header() -> None:
    st.markdown(
        f'''<div class="topbar">
          <div class="brand"><div class="brand-img"><img src="https://i.ibb.co/V0hydyyH/Whats-App-Image-2026-09-02-at-1-58-16-PM.jpg" alt="Identidad institucional UNT"></div><div><div class="brand-title">Tablero Ejecutivo de Satisfacción</div><div class="brand-sub">Universidad Nacional de Trujillo · OEI.01</div></div></div>
          <div class="top-meta"><div class="meta-box">Periodo analizado<b>2026</b></div><div class="meta-box">Estado PEI 2026<b>Diagnóstico / validación</b></div><div class="meta-box">Valor referencial<b>≥ 60%</b></div></div>
        </div>
        <div class="pagehead"><div><div class="kicker">Centro de control institucional</div><div class="title">Satisfacción con el proceso de formación académica</div><div class="sub">Lectura diagnóstica 2026 de la satisfacción general, análisis de las cuatro dimensiones y detalle de P1–P16. La ficha PEI señala que la medición oficial del indicador inicia a partir de 2027.</div><div class="chips"><span class="chip">IND.01 · OEI.01</span><span class="chip">👥 {N_TOTAL:,} respuestas 2026</span><span class="chip warn">⚠ 2026 no es año de medición oficial PEI</span><span class="chip">Referencia PEI: ≥60%</span></div></div><div class="basebox">Base consolidada<b>{N_TOTAL:,} estudiantes</b></div></div>''',
        unsafe_allow_html=True,
    )


def formula_html(n: int, d: int, result: float) -> str:
    return f'''<div class="formula"><div class="formula-k">Fórmula del resultado diagnóstico 2026</div><div class="formula-eq"><span>Porcentaje =</span><span class="frac"><span>N</span><span class="bar"></span><span>D</span></span><span>× 100 =</span><span class="frac"><span>{n:,}</span><span class="bar"></span><span>{d:,}</span></span><span>× 100 =</span><span class="formula-result">{pct(result)}</span></div></div>'''


def scale_html(value: float) -> str:
    level, interval, _, _ = institutional_level(value)
    levels = [
        ("Insatisfactorio", "0–59%", "#E25B68"),
        ("Regular", "60–74%", "#F2A62C"),
        ("Satisfactorio", "75–89%", "#16A878"),
        ("Muy satisfactorio", "90–100%", "#20AABD"),
    ]
    cards = []
    for name, rng, color in levels:
        active = " active" if name == level else ""
        cards.append(f'''<div class="scale-step{active}" style="--lvl:{color}"><div class="scale-dot" style="background:{color}"></div><div class="scale-name">{name}</div><div class="scale-range">{rng}</div></div>''')
    return f'''<div class="panel scale-wrap"><div class="scale-title">Escala de interpretación propuesta del instrumento · Resultado actual: <span style="color:{GLOBAL_COLOR}">{escape(level)} ({escape(interval)})</span></div><div class="scale4">{''.join(cards)}</div><div class="scale-note"><b>Importante:</b> el propio documento señala que estos rangos pueden ajustarse según lineamientos de la UNT o SUNEDU; por eso el dashboard los presenta como escala propuesta, no como norma institucional definitiva.</div></div>'''


def primary_cards_html() -> str:
    ref_delta = GLOBAL - PEI_REFERENCE
    ref_text = f"{pp(abs(ref_delta))} {'sobre' if ref_delta >= 0 else 'por debajo de'} la referencia de 60%"
    analytical_level, _, analytical_color, analytical_state = institutional_level(INTEGRAL16)
    kpis = [
        ("Estudiantes encuestados", f"{N_TOTAL:,}", "Denominador D", "👥", "#3568D4", "#EAF1FF"),
        ("Satisfechos P17", f"{N_GLOBAL:,}", "Numerador N · respuesta 4 o 5", "✓", "#16A878", "#E9F8F1"),
        ("Promedio P17", f"{GLOBAL_MEAN:.2f} / 5", "Media de satisfacción general", "◉", "#7C5CE7", "#F1ECFF"),
        ("Referencia PEI", "≥ 60%", "Valor referencial de satisfacción", "◎", "#2F66D8", "#EAF1FF"),
        ("P1–P16 analítico", pct(INTEGRAL16), "Complementario, no definido como IND.01", "∑", "#B9794E", "#FFF1E8"),
        ("Promedio P1–P16", f"{INTEGRAL16_MEAN:.2f} / 5", "Perfil conjunto de 16 ítems", "▦", "#348675", "#E9F7F3"),
    ]
    kpi_html=[]
    for i,(label,val,foot,icon,accent,soft) in enumerate(kpis):
        kpi_html.append(f'''<div class="kpi" style="--accent:{accent};--soft:{soft}"><div class="kpi-head"><div class="kpi-label">{escape(label)}</div><div class="kpi-icon">{icon}</div></div><div class="kpi-v">{escape(val)}</div><div class="kpi-f">{escape(foot)}</div><div class="spark">{spark_svg(accent,i)}</div></div>''')

    return f'''<div class="hero-grid">
      <div class="result-hero">
        <div class="result-layout">
          <div class="result-icon">◉</div>
          <div><div class="result-eyebrow">Resultado diagnóstico 2026 · satisfacción general</div><div class="result-title">P17 · percepción global del proceso de formación académica</div><div class="result-text">El documento del instrumento define P17 como satisfacción general y clasifica como satisfecho al estudiante que responde 4 o 5. El mismo sustento describe esta satisfacción general como el indicador sintético de la percepción global.</div>{formula_html(N_GLOBAL,N_TOTAL,GLOBAL)}<div class="diag-pill">⚠ Lectura diagnóstica 2026 · no constituye medición oficial PEI del año</div></div>
          <div><div class="result-score">{pct(GLOBAL)}</div><div class="result-level" style="color:#fff">{escape(GLOBAL_LEVEL)} · {escape(GLOBAL_INTERVAL)}</div><div class="signal-row"><div class="signal-copy">Escala propuesta<br><span style="color:#FFE6A9">{escape(ref_text)}</span></div>{traffic_svg(GLOBAL_STATE,48)}</div></div>
        </div>
      </div>
      <div class="panel secondary"><div class="secondary-top"><div><div class="secondary-k">Análisis complementario</div><div class="secondary-t">Perfil integral P1–P16 con promedio ≥4</div></div>{traffic_svg(analytical_state,38)}</div><div class="secondary-v">{pct(INTEGRAL16)}</div><div class="secondary-x"><b>{N_INTEGRAL16:,}</b> estudiantes alcanzan promedio P1–P16 ≥4. Este criterio es útil para contraste analítico, pero <b>los documentos compartidos no lo definen expresamente como la fórmula global oficial del IND.01</b>.</div><div class="secondary-note">Diferencia frente a P17: <b>{pp(abs(DELTA_GLOBAL_INTEGRAL))}</b>. No se interpretan como medidas idénticas: P17 es percepción global directa y P1–P16 resume 16 aspectos específicos.</div></div>
    </div><div class="kpi-grid">{''.join(kpi_html)}</div>'''


def dimension_cards_html() -> str:
    cards=[]
    for _,r in DIMS.sort_values("Código").iterrows():
        code=r["Código"]; meta=DIMENSIONS[code]; sat=float(r["Satisfacción"]); avg=float(r["Promedio"])
        level,interval,color,state=institutional_level(sat)
        gap75=max(0,.75-sat)
        gap_text="Ya está en nivel Satisfactorio" if gap75<=0 else f"A {pp(gap75)} del 75%"
        cards.append(f'''<div class="panel dim-card" style="--accent:{meta['accent']};--soft:{meta['soft']}"><div class="dim-head"><div><div class="dim-code">{meta['icon']} {code}</div><div class="dim-name">{escape(meta['name'])}</div></div>{traffic_svg(state,30)}</div><div class="dim-body"><div class="donut" style="--p:{sat*100:.2f};--accent:{meta['accent']}"><b>{pct(sat)}</b></div><div><div class="dim-level" style="color:{color}">{escape(level)}</div><div class="dim-meta"><b>{escape(interval)}</b><br>{int(r['N satisfechos']):,} estudiantes satisfechos<br>Promedio: <b>{avg:.2f}/5</b><br>{escape(gap_text)} <span style="color:#8996A5">(escala propuesta)</span></div></div></div><div class="dim-meaning"><b>Qué evalúa:</b> {escape(meta['meaning'])}</div><div class="dim-foot"><span>Criterio: promedio de 4 ítems ≥4</span><b>{', '.join(meta['items'])}</b></div></div>''')
    return '<div class="dim-grid">'+''.join(cards)+'</div>'


def insights_html() -> str:
    pri=PRIORITY_DIM; strong=STRONG_DIM; pitem=PRIORITY_ITEM; sitem=STRONG_ITEM
    none_sat = int((DIMS["Satisfacción"] >= .75).sum())
    return f'''<div class="insight-grid">
      <div class="panel insight" style="--accent:#F2A62C"><div class="insight-k">Lectura global 2026</div><div class="insight-t">P17 · {pct(GLOBAL)} · {escape(GLOBAL_LEVEL)}</div><div class="insight-x">La satisfacción global directa se ubica en <b>Regular</b> según la escala propuesta. Supera el valor referencial PEI de 60% en <b>{pp(max(0,GLOBAL-PEI_REFERENCE))}</b>, pero la ficha PEI establece que 2026 aún corresponde al diseño, estandarización y validación del instrumento.</div></div>
      <div class="panel insight" style="--accent:{DIMENSIONS[str(pri['Código'])]['accent']}"><div class="insight-k">Prioridad dimensional</div><div class="insight-t">{pri['Código']} · {pct(float(pri['Satisfacción']))} · {escape(str(pri['Nivel']))}</div><div class="insight-x"><b>{escape(str(pri['Dimensión']))}</b> presenta el menor resultado. La evidencia concentra la atención en servicios académicos, información, infraestructura y aseguramiento de la calidad.</div></div>
      <div class="panel insight" style="--accent:#E25B68"><div class="insight-k">Ítem crítico</div><div class="insight-t">{pitem['Ítem']} · {pct(float(pitem['Favorable']))} favorable</div><div class="insight-x">{escape(str(pitem['Pregunta']))} Registra <b>{pct(float(pitem['Desfavorable']))}</b> desfavorable y promedio <b>{float(pitem['Promedio']):.2f}/5</b>.</div></div>
      <div class="panel insight" style="--accent:#16A878"><div class="insight-k">Fortaleza relativa</div><div class="insight-t">{sitem['Ítem']} · {pct(float(sitem['Favorable']))} favorable</div><div class="insight-x">{escape(str(sitem['Pregunta']))} Es el aspecto con mayor valoración favorable. Aun así, <b>{none_sat} de 4</b> dimensiones alcanzan 75%, por lo que ninguna se ubica todavía en nivel Satisfactorio bajo la escala propuesta.</div></div>
    </div>'''


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
        context="El análisis cubre los 16 ítems del instrumento."
    else:
        context=f"El análisis se concentra en {selected}: {DIMENSIONS[selected]['name']}."
    return f'''<div class="insight-grid" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div class="panel insight" style="--accent:#3265CF"><div class="insight-k">Bloque analizado</div><div class="insight-t">{escape(selected)}</div><div class="insight-x">{escape(context)}</div></div><div class="panel insight" style="--accent:#E25B68"><div class="insight-k">Menor valoración favorable</div><div class="insight-t">{weak['Ítem']} · {pct(float(weak['Favorable']))}</div><div class="insight-x">{escape(str(weak['Pregunta']))}</div></div><div class="panel insight" style="--accent:#16A878"><div class="insight-k">Mayor valoración favorable</div><div class="insight-t">{strong['Ítem']} · {pct(float(strong['Favorable']))}</div><div class="insight-x">{escape(str(strong['Pregunta']))}</div></div></div>'''


# ==============================================================
# APP
# ==============================================================
top_header()

tab1, tab2, tab3 = st.tabs(["◉ Visión ejecutiva", "▦ Dimensiones e ítems", "ⓘ Método y PEI"])

with tab1:
    section_header(
        "Resultado principal",
        "Diagnóstico 2026: satisfacción general y contraste integral",
        "P17 se usa como resultado global del instrumento; P1–P16 se conserva como análisis complementario no oficial.",
    )
    st.markdown(primary_cards_html(), unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(scale_html(GLOBAL), unsafe_allow_html=True)

    section_header(
        "Diagnóstico 4D",
        "Satisfacción en las cuatro dimensiones",
        "Cada dimensión clasifica al estudiante como satisfecho si el promedio de sus cuatro ítems es ≥4. No se aplica la meta PEI de 60% a cada dimensión.",
    )
    st.markdown(dimension_cards_html(), unsafe_allow_html=True)

    section_header(
        "Interpretación ejecutiva",
        "Hallazgos que sí están sustentados por el instrumento y la ficha PEI",
        "Se diferencia diagnóstico 2026, escala propuesta del instrumento y programación oficial del PEI.",
    )
    st.markdown(insights_html(), unsafe_allow_html=True)

    section_header(
        "Contexto estratégico",
        "Ruta PEI 2026–2030",
        "2026 corresponde a preparación del instrumento; la medición efectiva y los logros esperados empiezan en 2027.",
    )
    st.markdown(pei_route_html(), unsafe_allow_html=True)

with tab2:
    section_header(
        "Explorador",
        "Dimensiones e ítems",
        "Visualizaciones estáticas y responsivas: no hay zoom, arrastre ni ejes móviles.",
    )
    selected = st.selectbox(
        "Dimensión a analizar",
        ["Todas", "D1", "D2", "D3", "D4"],
        format_func=lambda x: "Todas las dimensiones · P1–P16" if x == "Todas" else f"{x} · {DIMENSIONS[x]['name']}",
        label_visibility="collapsed",
    )

    section_header("Lectura del bloque", "Fortaleza y prioridad del conjunto seleccionado")
    st.markdown(selected_insights_html(selected), unsafe_allow_html=True)

    section_header(
        "Valoración favorable",
        "Panel de aspectos del instrumento",
        "Los ítems se muestran descriptivamente; no se les asigna un nivel institucional individual.",
    )
    st.markdown(item_cards_html(selected), unsafe_allow_html=True)

    section_header(
        "Distribución de respuesta",
        "Desfavorable · neutral · favorable",
        "1–2 = desfavorable · 3 = neutral · 4–5 = favorable.",
    )
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
    section_header("PEI", "Qué dice la ficha técnica y cómo debe usarse en 2026")
    st.markdown(
        '''<div class="method-grid">
          <div class="panel method"><div class="method-i">◎</div><div class="method-t">Fórmula PEI</div><div class="method-x">El indicador se expresa como <b>(N/D) × 100</b>, donde N es el número de estudiantes satisfechos y D el total de estudiantes encuestados.</div></div>
          <div class="panel method"><div class="method-i">⚠</div><div class="method-t">2026 no es medición oficial</div><div class="method-x">La ficha señala que durante 2026 se diseña, estandariza y valida el instrumento, sin generar aún valores medibles oficiales. La medición efectiva inicia a partir de 2027 y la frecuencia es anual.</div></div>
          <div class="panel method"><div class="method-i">🎯</div><div class="method-t">Referencia y logros esperados</div><div class="method-x">Valor referencial de satisfacción: <b>≥60%</b>. Logros esperados: <b>2027 60%</b>, <b>2028 65%</b>, <b>2029 70%</b> y <b>2030 75%</b>.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )

    section_header("Instrumento", "Reglas de cálculo que sí están escritas en la propuesta")
    st.markdown(
        f'''<div class="method-grid">
          <div class="panel method"><div class="method-i">▦</div><div class="method-t">D1–D4</div><div class="method-x">Cada dimensión contiene cuatro ítems. El estudiante se clasifica como satisfecho en la dimensión cuando el <b>promedio de sus cuatro respuestas es ≥4</b>.</div></div>
          <div class="panel method"><div class="method-i">◉</div><div class="method-t">P17 · satisfacción general</div><div class="method-x">P17 se clasifica como <b>satisfecho con respuesta 4 o 5</b> y no satisfecho con 1, 2 o 3. El sustento del documento describe la satisfacción general como el <b>indicador sintético</b> de la percepción global.</div></div>
          <div class="panel method"><div class="method-i">∑</div><div class="method-t">P1–P16 integral</div><div class="method-x">El promedio P1–P16 ≥4 se muestra solo como <b>análisis complementario</b>. La documentación compartida no especifica de forma explícita que este agregado de 16 ítems sea la regla global oficial del IND.01.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(
        '''<div class="method-alert"><b>Decisión metodológica usada en este dashboard:</b> para el <b>diagnóstico 2026</b> se presenta P17 como resultado global principal porque el instrumento lo define como satisfacción general y lo describe como indicador sintético. Las cuatro dimensiones explican dónde se concentra la satisfacción o la debilidad. El cálculo P1–P16 ≥4 se conserva únicamente como contraste analítico. Antes de convertir este tablero en reporte oficial del IND.01 a partir de 2027, la regla global debe quedar formalmente aprobada junto con la validación del instrumento.</div>''',
        unsafe_allow_html=True,
    )

    section_header("Interpretación", "Escala propuesta del instrumento")
    st.markdown(scale_html(GLOBAL), unsafe_allow_html=True)

    section_header("Resultados 2026", "Resumen técnico calculado con la base actual")
    summary = pd.DataFrame([
        ["Satisfacción general P17", pct(GLOBAL), GLOBAL_LEVEL, f"{N_GLOBAL:,} / {N_TOTAL:,}"],
        ["Análisis complementario P1–P16 ≥4", pct(INTEGRAL16), institutional_level(INTEGRAL16)[0], f"{N_INTEGRAL16:,} / {N_TOTAL:,}"],
        *[[f"{r['Código']} · {r['Dimensión']}", pct(float(r['Satisfacción'])), str(r['Nivel']), f"{int(r['N satisfechos']):,} / {N_TOTAL:,}"] for _,r in DIMS.sort_values('Código').iterrows()],
    ], columns=["Medida", "Resultado", "Lectura", "N / D"])
    st.dataframe(summary, use_container_width=True, hide_index=True)
