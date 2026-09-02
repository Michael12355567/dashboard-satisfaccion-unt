from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================================================
# CONFIGURACIÓN GENERAL
# ==============================================================
st.set_page_config(
    page_title="UNT | Satisfacción Estudiantil",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Identidad visual: institucional, sobria y de alto contraste.
NAVY = "#0B1F33"
NAVY_2 = "#12324A"
INK = "#172B3A"
MUTED = "#667085"
BORDER = "#E4E7EC"
SURFACE = "#FFFFFF"
BG = "#F5F7FA"
BLUE = "#2563EB"
TEAL = "#0E7490"

COLORS_DIM = {
    "D1": "#315B7D",  # azul acero
    "D2": "#5B5F97",  # índigo sobrio
    "D3": "#A66A2C",  # cobre
    "D4": "#2E7668",  # verde mineral
}

LEVEL_META = {
    "Insatisfactorio": {
        "color": "#B42318",
        "bg": "#FEF3F2",
        "border": "#FECDCA",
        "interval": "0% a <60%",
        "short": "Bajo el mínimo",
    },
    "Regular": {
        "color": "#B54708",
        "bg": "#FFFAEB",
        "border": "#FEDF89",
        "interval": "60% a <75%",
        "short": "En observación",
    },
    "Satisfactorio": {
        "color": "#027A48",
        "bg": "#ECFDF3",
        "border": "#ABEFC6",
        "interval": "75% a <90%",
        "short": "Cumple estándar",
    },
    "Muy satisfactorio": {
        "color": "#065F46",
        "bg": "#E8F8F2",
        "border": "#9ED8C2",
        "interval": "90% a 100%",
        "short": "Desempeño alto",
    },
    "Sin dato": {
        "color": "#667085",
        "bg": "#F2F4F7",
        "border": "#D0D5DD",
        "interval": "Sin dato",
        "short": "Sin información",
    },
}

LIKERT_COLORS = {
    "Desfavorable (1–2)": "#C2413A",
    "Neutral (3)": "#98A2B3",
    "Favorable (4–5)": "#23836F",
}


# ==============================================================
# ESTILO VISUAL
# ==============================================================
st.markdown(
    f"""
    <style>
    :root {{
        --navy:{NAVY};
        --navy2:{NAVY_2};
        --ink:{INK};
        --muted:{MUTED};
        --border:{BORDER};
        --surface:{SURFACE};
        --bg:{BG};
        --blue:{BLUE};
        --teal:{TEAL};
    }}

    html, body, [class*="css"] {{
        font-family: "Segoe UI Variable", "Segoe UI", Inter, Arial, sans-serif;
    }}

    .stApp {{
        background:
          radial-gradient(circle at 88% 2%, rgba(49,91,125,.065), transparent 23rem),
          linear-gradient(180deg, #F8FAFC 0%, var(--bg) 100%);
        color: var(--ink);
    }}

    .block-container {{
        padding-top: 1.15rem;
        padding-bottom: 3rem;
        max-width: 1480px;
    }}

    h1, h2, h3, h4 {{
        color: var(--ink);
        letter-spacing: -.025em;
    }}

    h1 {{ font-size: 2.05rem !important; font-weight: 750 !important; }}
    h2 {{ font-size: 1.42rem !important; font-weight: 720 !important; }}
    h3 {{ font-size: 1.08rem !important; font-weight: 700 !important; }}

    .hero {{
        background: linear-gradient(118deg, #0B1F33 0%, #143B54 56%, #176075 100%);
        border-radius: 22px;
        padding: 24px 28px 22px 28px;
        color: white;
        box-shadow: 0 18px 44px rgba(11,31,51,.16);
        margin-bottom: 18px;
        position: relative;
        overflow: hidden;
    }}
    .hero:after {{
        content:"";
        position:absolute;
        right:-78px;
        top:-85px;
        width:260px;
        height:260px;
        border-radius:50%;
        border:48px solid rgba(255,255,255,.055);
    }}
    .hero-kicker {{
        font-size:.76rem;
        font-weight:750;
        letter-spacing:.12em;
        text-transform:uppercase;
        color:#CDE6F0;
        margin-bottom:7px;
    }}
    .hero-title {{
        font-size:2rem;
        font-weight:760;
        letter-spacing:-.035em;
        line-height:1.08;
        margin:0 0 7px 0;
        color:#FFFFFF;
    }}
    .hero-sub {{
        font-size:.96rem;
        color:#D6E4EB;
        max-width:850px;
        line-height:1.55;
    }}
    .hero-chip {{
        display:inline-flex;
        align-items:center;
        gap:7px;
        background:rgba(255,255,255,.10);
        border:1px solid rgba(255,255,255,.18);
        border-radius:999px;
        padding:6px 10px;
        margin-top:13px;
        font-size:.78rem;
        color:#EDF7FA;
        backdrop-filter: blur(8px);
    }}

    .section-title {{
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:12px;
        margin: 1.15rem 0 .7rem 0;
    }}
    .section-title h3 {{ margin:0; }}
    .section-note {{ color:var(--muted); font-size:.82rem; }}

    .kpi-card {{
        background:var(--surface);
        border:1px solid var(--border);
        border-radius:16px;
        padding:17px 18px 15px 18px;
        min-height:128px;
        box-shadow:0 5px 18px rgba(16,24,40,.045);
    }}
    .kpi-label {{
        font-size:.77rem;
        font-weight:700;
        color:#667085;
        text-transform:uppercase;
        letter-spacing:.055em;
        margin-bottom:8px;
    }}
    .kpi-value {{
        font-size:1.78rem;
        line-height:1.05;
        font-weight:760;
        letter-spacing:-.035em;
        color:#101828;
        margin-bottom:8px;
    }}
    .kpi-foot {{ font-size:.80rem; color:#667085; line-height:1.35; }}
    .kpi-accent {{
        width:34px;
        height:4px;
        border-radius:99px;
        background:var(--accent, #315B7D);
        margin-bottom:12px;
    }}

    .dim-card {{
        background:var(--surface);
        border:1px solid var(--border);
        border-radius:16px;
        padding:17px 17px 15px 17px;
        min-height:166px;
        box-shadow:0 5px 18px rgba(16,24,40,.04);
        position:relative;
        overflow:hidden;
    }}
    .dim-card:before {{
        content:"";
        position:absolute;
        left:0; top:0; bottom:0;
        width:4px;
        background:var(--dim-color);
    }}
    .dim-head {{ display:flex; align-items:center; justify-content:space-between; gap:8px; }}
    .dim-code {{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-width:38px;
        height:28px;
        border-radius:8px;
        background:color-mix(in srgb, var(--dim-color) 11%, white);
        color:var(--dim-color);
        font-size:.78rem;
        font-weight:800;
        letter-spacing:.05em;
    }}
    .dim-value {{
        font-size:1.72rem;
        font-weight:760;
        letter-spacing:-.035em;
        color:#101828;
        margin:13px 0 5px 0;
    }}
    .dim-name {{
        font-size:.83rem;
        line-height:1.35;
        color:#475467;
        min-height:38px;
    }}
    .dim-foot {{
        margin-top:10px;
        display:flex;
        align-items:center;
        gap:7px;
        flex-wrap:wrap;
    }}

    .status-pill {{
        display:inline-flex;
        align-items:center;
        gap:6px;
        border-radius:999px;
        padding:4px 8px;
        font-size:.72rem;
        font-weight:700;
        line-height:1.1;
        border:1px solid var(--status-border);
        color:var(--status-color);
        background:var(--status-bg);
        white-space:nowrap;
    }}
    .status-dot {{
        width:8px;
        height:8px;
        border-radius:50%;
        background:var(--status-color);
        box-shadow:0 0 0 3px color-mix(in srgb, var(--status-color) 12%, transparent);
        display:inline-block;
    }}
    .interval-label {{ font-size:.72rem; color:#667085; font-weight:600; }}

    .panel {{
        background:#FFFFFF;
        border:1px solid var(--border);
        border-radius:17px;
        padding:17px 18px;
        box-shadow:0 5px 18px rgba(16,24,40,.04);
    }}
    .panel-title {{ font-size:.95rem; font-weight:750; color:#1D2939; margin-bottom:3px; }}
    .panel-sub {{ font-size:.78rem; color:#667085; margin-bottom:11px; }}

    .traffic-row {{
        display:grid;
        grid-template-columns:minmax(0,1fr) auto;
        align-items:center;
        gap:12px;
        padding:11px 0;
        border-bottom:1px solid #F0F2F5;
    }}
    .traffic-row:last-child {{ border-bottom:none; }}
    .traffic-left {{ display:flex; align-items:flex-start; gap:10px; min-width:0; }}
    .traffic-name {{ font-size:.82rem; font-weight:700; color:#344054; }}
    .traffic-desc {{ font-size:.73rem; color:#667085; margin-top:2px; line-height:1.25; }}
    .traffic-value {{ text-align:right; }}
    .traffic-value strong {{ display:block; font-size:.96rem; color:#101828; }}
    .traffic-value span {{ font-size:.70rem; color:#667085; }}

    .scale-wrap {{ margin-top:11px; }}
    .scale-bar {{
        width:100%;
        height:13px;
        display:flex;
        overflow:hidden;
        border-radius:999px;
        border:1px solid rgba(16,24,40,.06);
    }}
    .scale-segment {{ height:100%; }}
    .scale-labels {{
        display:grid;
        grid-template-columns:60fr 15fr 15fr 10fr;
        margin-top:6px;
        font-size:.64rem;
        color:#667085;
        line-height:1.15;
    }}
    .scale-labels > div {{ padding-right:5px; }}

    .finding {{
        background:#FFFFFF;
        border:1px solid var(--border);
        border-left:4px solid #315B7D;
        border-radius:13px;
        padding:13px 14px;
        margin-bottom:9px;
        color:#344054;
        line-height:1.45;
        box-shadow:0 4px 14px rgba(16,24,40,.035);
        font-size:.84rem;
    }}
    .finding.alert {{ border-left-color:#B42318; }}
    .finding.good {{ border-left-color:#027A48; }}
    .finding.warn {{ border-left-color:#B54708; }}
    .finding b {{ color:#1D2939; }}

    .method-card {{
        background:#FFFFFF;
        border:1px solid var(--border);
        border-radius:16px;
        padding:18px;
        min-height:205px;
        box-shadow:0 5px 18px rgba(16,24,40,.035);
    }}
    .method-card h3 {{ margin-top:0; }}
    .method-card p {{ color:#475467; font-size:.88rem; line-height:1.5; }}

    .level-card {{
        border:1px solid var(--level-border);
        background:var(--level-bg);
        border-radius:14px;
        padding:14px 14px 13px 14px;
        min-height:145px;
    }}
    .level-card .level-name {{
        font-size:.82rem;
        color:var(--level-color);
        font-weight:800;
        margin-bottom:6px;
    }}
    .level-card .level-range {{
        font-size:1.12rem;
        font-weight:760;
        color:#101828;
        margin-bottom:7px;
    }}
    .level-card .level-help {{ font-size:.77rem; color:#667085; line-height:1.35; }}

    .priority-legend {{
        background:#F8FAFC;
        border:1px solid #EAECF0;
        border-radius:12px;
        padding:10px 12px;
        color:#667085;
        font-size:.78rem;
        margin-bottom:10px;
    }}

    .upload-intro {{
        background:#FFFFFF;
        border:1px solid var(--border);
        border-radius:17px;
        padding:22px;
        box-shadow:0 6px 20px rgba(16,24,40,.045);
    }}

    div[data-testid="stDataFrame"] {{
        border:1px solid #EAECF0;
        border-radius:14px;
        overflow:hidden;
    }}

    div[data-testid="stPlotlyChart"] {{
        background:#FFFFFF;
        border:1px solid #EAECF0;
        border-radius:16px;
        padding:6px 8px 3px 8px;
        box-shadow:0 4px 16px rgba(16,24,40,.03);
    }}

    section[data-testid="stSidebar"] {{
        background:linear-gradient(180deg, #0B1F33 0%, #102C42 100%);
        border-right:1px solid rgba(255,255,255,.06);
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{ color:#FFFFFF !important; }}
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{ color:#D0DCE3 !important; }}
    section[data-testid="stSidebar"] hr {{ border-color:rgba(255,255,255,.12); }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        border-radius:10px;
        padding:5px 6px;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background:rgba(255,255,255,.06);
    }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
        background:#FFFFFF;
        border:1px dashed #B8C7D1;
        border-radius:12px;
    }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{
        color:#344054 !important;
    }}

    .sidebar-brand {{
        padding:6px 2px 2px 2px;
        margin-bottom:4px;
    }}
    .sidebar-brand .sb-kicker {{ color:#8FB8C9; font-size:.68rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; }}
    .sidebar-brand .sb-title {{ color:#FFFFFF; font-size:1.15rem; font-weight:750; margin-top:4px; }}
    .sidebar-brand .sb-sub {{ color:#B9CBD4; font-size:.76rem; line-height:1.35; margin-top:4px; }}

    #MainMenu {{visibility:hidden;}}
    footer {{visibility:hidden;}}

    @media (max-width: 900px) {{
        .hero-title {{ font-size:1.6rem; }}
        .hero {{ padding:20px; }}
        .scale-labels {{ font-size:.58rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================
# CATÁLOGO DEL INSTRUMENTO
# ==============================================================
QUESTION_TEXT = {
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
    "P11": "La infraestructura y los recursos educativos (aulas, bibliotecas, laboratorios) son adecuados para el aprendizaje.",
    "P12": "La universidad promueve acciones orientadas al aseguramiento de la calidad educativa.",
    "P13": "Mi formación universitaria contribuye al desarrollo de mis competencias profesionales.",
    "P14": "La universidad fomenta valores éticos y responsabilidad social en los estudiantes.",
    "P15": "Las actividades académicas y extracurriculares contribuyen a mi desarrollo personal y ciudadano.",
    "P16": "Me siento preparado(a) para afrontar los retos del ejercicio profesional futuro.",
    "P17": "En general, me siento satisfecho(a) con el proceso de formación académica que recibo en la Universidad Nacional de Trujillo.",
}

DIMENSIONS = {
    "D1": {
        "name": "Calidad del proceso académico",
        "items": ["P1", "P2", "P3", "P4"],
        "description": "Pertinencia curricular, plan de estudios, carga académica y coherencia de asignaturas.",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "items": ["P5", "P6", "P7", "P8"],
        "description": "Dominio docente, metodología, participación y retroalimentación.",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "items": ["P9", "P10", "P11", "P12"],
        "description": "Trámites académicos, información, infraestructura y aseguramiento de la calidad.",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "items": ["P13", "P14", "P15", "P16"],
        "description": "Competencias profesionales, valores, desarrollo personal y preparación profesional.",
    },
}


# ==============================================================
# CÁLCULOS
# ==============================================================
def nivel_inst(p: float) -> str:
    if pd.isna(p):
        return "Sin dato"
    if p < 0.60:
        return "Insatisfactorio"
    if p < 0.75:
        return "Regular"
    if p < 0.90:
        return "Satisfactorio"
    return "Muy satisfactorio"


def pct(p: float, decimals: int = 1) -> str:
    return "—" if pd.isna(p) else f"{p * 100:.{decimals}f}%"


def level_html(level: str, include_interval: bool = False) -> str:
    m = LEVEL_META[level]
    interval = f'<span class="interval-label">{m["interval"]}</span>' if include_interval else ""
    return (
        f'<span class="status-pill" style="--status-color:{m["color"]};'
        f'--status-bg:{m["bg"]};--status-border:{m["border"]};">'
        f'<span class="status-dot"></span>{escape(level)}</span>{interval}'
    )


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    required = [f"P{i}" for i in range(1, 18)]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Faltan columnas obligatorias en el Excel: " + ", ".join(missing))

    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for code, info in DIMENSIONS.items():
        prom_col = f"{code}_Promedio"
        sat_col = f"{code}_Satisfecho"
        df[prom_col] = df[info["items"]].mean(axis=1)
        df[sat_col] = (df[prom_col] >= 4).astype(int)

    df["Global_Satisfecho"] = (df["P17"] >= 4).astype(int)
    df["Categoria_Global"] = df["Global_Satisfecho"].map({1: "Satisfecho", 0: "No satisfecho"})
    df["Promedio_P1_P16"] = df[[f"P{i}" for i in range(1, 17)]].mean(axis=1)
    return df


def read_excel(source) -> pd.DataFrame:
    try:
        return pd.read_excel(source, sheet_name="Base_Encuesta", engine="openpyxl")
    except ValueError as exc:
        raise ValueError("No encuentro la hoja 'Base_Encuesta'. Revisa el nombre de la hoja.") from exc


@st.cache_data(show_spinner=False)
def load_uploaded_excel(file_bytes: bytes) -> pd.DataFrame:
    return prepare_data(read_excel(BytesIO(file_bytes)))


def dimension_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, info in DIMENSIONS.items():
        sat = df[f"{code}_Satisfecho"].mean()
        avg = df[f"{code}_Promedio"].mean()
        level = nivel_inst(sat)
        rows.append(
            {
                "Código": code,
                "Dimensión": info["name"],
                "Preguntas": f"{info['items'][0]}–{info['items'][-1]}",
                "Satisfacción": sat,
                "Promedio Likert": avg,
                "Nivel": level,
                "Intervalo": LEVEL_META[level]["interval"],
                "Brecha a 75%": max(0, 0.75 - sat),
            }
        )
    return pd.DataFrame(rows)


def item_summary(df: pd.DataFrame, items: list[str]) -> pd.DataFrame:
    rows = []
    for item in items:
        s = df[item].dropna()
        code = next(c for c, info in DIMENSIONS.items() if item in info["items"])
        rows.append(
            {
                "Ítem": item,
                "Número": int(item[1:]),
                "Dimensión": code,
                "Texto": QUESTION_TEXT[item],
                "Promedio": s.mean(),
                "Favorable": (s >= 4).mean(),
                "Neutral": (s == 3).mean(),
                "Desfavorable": (s <= 2).mean(),
            }
        )
    return pd.DataFrame(rows)


# ==============================================================
# COMPONENTES DE PRESENTACIÓN
# ==============================================================
def hero(title: str, subtitle: str, kicker: str = "Universidad Nacional de Trujillo") -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-kicker">{escape(kicker)}</div>
          <div class="hero-title">{escape(title)}</div>
          <div class="hero-sub">{escape(subtitle)}</div>
          <div class="hero-chip">● Sistema de seguimiento · Escala institucional D1–D4 + P17</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, note: str | None = None) -> None:
    note_html = f'<div class="section-note">{escape(note)}</div>' if note else ""
    st.markdown(
        f'<div class="section-title"><h3>{escape(title)}</h3>{note_html}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, foot: str, accent: str = COLORS_DIM["D1"]) -> None:
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent};">
          <div class="kpi-accent"></div>
          <div class="kpi-label">{escape(label)}</div>
          <div class="kpi-value">{escape(value)}</div>
          <div class="kpi-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dim_card(code: str, value: float) -> None:
    info = DIMENSIONS[code]
    level = nivel_inst(value)
    color = COLORS_DIM[code]
    st.markdown(
        f"""
        <div class="dim-card" style="--dim-color:{color};">
          <div class="dim-head">
            <span class="dim-code">{code}</span>
            {level_html(level)}
          </div>
          <div class="dim-value">{pct(value)}</div>
          <div class="dim-name">{escape(info['name'])}</div>
          <div class="dim-foot"><span class="interval-label">Intervalo: {LEVEL_META[level]['interval']}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def semaforo_scale() -> str:
    return """
    <div class="scale-wrap">
      <div class="scale-bar" aria-label="Escala institucional">
        <div class="scale-segment" style="width:60%;background:#B42318"></div>
        <div class="scale-segment" style="width:15%;background:#D97706"></div>
        <div class="scale-segment" style="width:15%;background:#16A34A"></div>
        <div class="scale-segment" style="width:10%;background:#047857"></div>
      </div>
      <div class="scale-labels">
        <div><b>0–&lt;60</b><br>Insatisfactorio</div>
        <div><b>60–&lt;75</b><br>Regular</div>
        <div><b>75–&lt;90</b><br>Satisfactorio</div>
        <div><b>90–100</b><br>Muy satisf.</div>
      </div>
    </div>
    """


def traffic_panel(summary_dim: pd.DataFrame, global_sat: float) -> None:
    rows = []
    for _, r in summary_dim.sort_values("Código").iterrows():
        level = r["Nivel"]
        meta = LEVEL_META[level]
        rows.append(
            f"""
            <div class="traffic-row">
              <div class="traffic-left">
                <span class="status-dot" style="--status-color:{meta['color']};margin-top:5px"></span>
                <div>
                  <div class="traffic-name">{r['Código']} · {escape(r['Dimensión'])}</div>
                  <div class="traffic-desc">{escape(level)} · {meta['interval']}</div>
                </div>
              </div>
              <div class="traffic-value"><strong>{pct(r['Satisfacción'])}</strong><span>{meta['short']}</span></div>
            </div>
            """
        )

    global_level = nivel_inst(global_sat)
    gm = LEVEL_META[global_level]
    rows.append(
        f"""
        <div class="traffic-row">
          <div class="traffic-left">
            <span class="status-dot" style="--status-color:{gm['color']};margin-top:5px"></span>
            <div>
              <div class="traffic-name">P17 · Satisfacción general</div>
              <div class="traffic-desc">{escape(global_level)} · {gm['interval']}</div>
            </div>
          </div>
          <div class="traffic-value"><strong>{pct(global_sat)}</strong><span>{gm['short']}</span></div>
        </div>
        """
    )

    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-title">Semáforo institucional</div>
          <div class="panel-sub">Color + texto + intervalo para una lectura ejecutiva rápida.</div>
          {''.join(rows)}
          {semaforo_scale()}
        </div>
        """,
        unsafe_allow_html=True,
    )


def plot_layout(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=28, t=32, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Arial", color="#475467", size=12),
        hoverlabel=dict(bgcolor="white", font_color="#101828", bordercolor="#D0D5DD"),
        legend=dict(bgcolor="rgba(255,255,255,.75)", borderwidth=0),
    )
    fig.update_xaxes(gridcolor="#EAECF0", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", zeroline=False)
    return fig


def dimension_bar_chart(summary_dim: pd.DataFrame) -> go.Figure:
    chart_df = summary_dim.sort_values("Satisfacción", ascending=True).copy()
    chart_df["Color"] = chart_df["Nivel"].map(lambda x: LEVEL_META[x]["color"])
    chart_df["Etiqueta"] = chart_df.apply(lambda r: f"{r['Código']} · {r['Dimensión']}", axis=1)

    fig = go.Figure()
    # Bandas institucionales de fondo: el "semáforo" también aparece en el gráfico.
    for x0, x1, color in [
        (0.00, 0.60, "rgba(180,35,24,.055)"),
        (0.60, 0.75, "rgba(217,119,6,.070)"),
        (0.75, 0.90, "rgba(22,163,74,.060)"),
        (0.90, 1.00, "rgba(4,120,87,.075)"),
    ]:
        fig.add_vrect(x0=x0, x1=x1, fillcolor=color, line_width=0, layer="below")

    fig.add_trace(
        go.Bar(
            x=chart_df["Satisfacción"],
            y=chart_df["Etiqueta"],
            orientation="h",
            marker=dict(color=chart_df["Color"], line=dict(width=0)),
            text=chart_df["Satisfacción"].map(lambda x: f"{x*100:.1f}%"),
            textposition="outside",
            textfont=dict(size=12, color="#344054"),
            customdata=chart_df[["Código", "Dimensión", "Nivel", "Intervalo", "Promedio Likert", "Brecha a 75%"]],
            hovertemplate=(
                "<b>%{customdata[0]} · %{customdata[1]}</b><br>"
                "Satisfacción: %{x:.2%}<br>"
                "Nivel: %{customdata[2]}<br>"
                "Intervalo: %{customdata[3]}<br>"
                "Promedio Likert: %{customdata[4]:.2f}<br>"
                "Brecha a 75%: %{customdata[5]:.2%}<extra></extra>"
            ),
        )
    )
    fig.add_vline(x=0.60, line_width=1, line_dash="dot", line_color="#D97706")
    fig.add_vline(x=0.75, line_width=1.4, line_dash="dash", line_color="#15803D")
    fig.add_vline(x=0.90, line_width=1, line_dash="dot", line_color="#047857")
    fig.update_xaxes(tickformat=".0%", range=[0, 1.04], title="% de estudiantes satisfechos")
    fig.update_yaxes(title=None, tickfont=dict(size=11))
    fig.update_layout(showlegend=False)
    return plot_layout(fig, 430)


# ==============================================================
# SIDEBAR + CARGA DEL EXCEL
# ==============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
          <div class="sb-kicker">Dashboard ejecutivo</div>
          <div class="sb-title">UNT · Satisfacción estudiantil</div>
          <div class="sb-sub">Lectura institucional de D1–D4 y satisfacción general P17.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    uploaded = st.file_uploader(
        "Archivo de datos",
        type=["xlsx"],
        help="Selecciona el Excel que contiene la hoja Base_Encuesta.",
    )

    use_local = False
    local_file = Path("basededatos.xlsx")
    if local_file.exists():
        use_local = st.checkbox(
            "Usar basededatos.xlsx de esta carpeta",
            value=False,
            help="Útil al ejecutar la app localmente.",
        )

    st.markdown("---")
    page = st.radio(
        "Navegación",
        [
            "Panorama institucional",
            "Explorar dimensiones",
            "Prioridades de mejora",
            "Metodología",
        ],
    )


if uploaded is None and not use_local:
    hero(
        "Dashboard de satisfacción estudiantil",
        "Carga el archivo Excel para generar automáticamente los indicadores institucionales, el semáforo D1–D4 y P17, y el ranking de prioridades.",
    )
    st.markdown(
        """
        <div class="upload-intro">
          <h3 style="margin-top:0">Carga de datos</h3>
          <p style="color:#475467;line-height:1.55;margin-bottom:6px">
            Usa <b>Archivo de datos</b> en la barra izquierda y selecciona <code>basededatos.xlsx</code>.
            El archivo no se pega dentro del código: se selecciona desde esta misma aplicación.
          </p>
          <p style="color:#667085;font-size:.82rem;margin-bottom:0">
            Requisito: hoja <b>Base_Encuesta</b> y columnas P1 a P17. D1–D4 se recalculan automáticamente.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    section_title("Qué verás", "Diseño ejecutivo con lectura por nivel e intervalo")
    c1, c2, c3, c4 = st.columns(4)
    preview = [
        ("D1", "Calidad del proceso académico"),
        ("D2", "Desempeño docente"),
        ("D3", "Servicios y gestión"),
        ("D4", "Formación integral"),
    ]
    for col, (code, name) in zip([c1, c2, c3, c4], preview):
        with col:
            st.markdown(
                f'<div class="dim-card" style="--dim-color:{COLORS_DIM[code]};min-height:120px">'
                f'<div class="dim-code">{code}</div><div class="dim-name" style="margin-top:13px"><b>{escape(name)}</b></div>'
                f'<div class="dim-foot"><span class="interval-label">Se calcula al cargar el Excel</span></div></div>',
                unsafe_allow_html=True,
            )
    st.stop()


try:
    if uploaded is not None:
        df = load_uploaded_excel(uploaded.getvalue())
        source_name = uploaded.name
    else:
        df = prepare_data(read_excel(local_file))
        source_name = local_file.name
except Exception as exc:
    st.error(f"No pude leer el archivo: {exc}")
    st.stop()

summary_dim = dimension_summary(df)
all_items = [f"P{i}" for i in range(1, 17)]
global_sat = df["Global_Satisfecho"].mean()

with st.sidebar:
    st.markdown("---")
    st.success(f"Datos cargados · {source_name}")
    st.caption(f"{len(df):,} registros analizados")


# ==============================================================
# 1) PANORAMA INSTITUCIONAL
# ==============================================================
if page == "Panorama institucional":
    hero(
        "Panorama institucional",
        "Una lectura ejecutiva de la satisfacción general, el desempeño de D1–D4 y las brechas respecto del umbral satisfactorio de 75%.",
    )

    worst = summary_dim.sort_values("Satisfacción").iloc[0]
    best = summary_dim.sort_values("Satisfacción", ascending=False).iloc[0]
    meets = int((summary_dim["Satisfacción"] >= 0.75).sum())
    gl = nivel_inst(global_sat)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Estudiantes encuestados", f"{len(df):,}", "Registros válidos cargados en la base", COLORS_DIM["D1"])
    with c2:
        gm = LEVEL_META[gl]
        kpi_card(
            "Satisfacción general · P17",
            pct(global_sat),
            f'{level_html(gl)} <span class="interval-label">&nbsp;{gm["interval"]}</span>',
            gm["color"],
        )
    with c3:
        kpi_card("Cumplimiento dimensional", f"{meets} de 4", "Dimensiones con satisfacción ≥ 75%", "#027A48" if meets == 4 else "#B54708")
    with c4:
        wm = LEVEL_META[worst["Nivel"]]
        kpi_card("Prioridad dimensional", worst["Código"], f'{escape(worst["Dimensión"])} · <b>{pct(worst["Satisfacción"])}</b>', wm["color"])

    section_title("Satisfacción por dimensión", "Cada tarjeta muestra nivel + intervalo institucional")
    cols = st.columns(4)
    for col, code in zip(cols, ["D1", "D2", "D3", "D4"]):
        with col:
            value = float(summary_dim.loc[summary_dim["Código"] == code, "Satisfacción"].iloc[0])
            render_dim_card(code, value)

    section_title("Comparación D1–D4", "Bandas de fondo = semáforo institucional")
    left, right = st.columns([1.62, 1])
    with left:
        st.plotly_chart(dimension_bar_chart(summary_dim), use_container_width=True)
    with right:
        traffic_panel(summary_dim, global_sat)

    section_title("Tablero de situación institucional", "El intervalo corresponde al nivel alcanzado")
    table = summary_dim.copy()
    table["Satisfacción"] = table["Satisfacción"].map(lambda x: pct(x, 2))
    table["Promedio Likert"] = table["Promedio Likert"].map(lambda x: f"{x:.2f}")
    table["Brecha a 75%"] = table["Brecha a 75%"].map(lambda x: f"{x*100:.2f} pp")
    table["Semáforo"] = table["Nivel"].map(
        {
            "Insatisfactorio": "🔴 Insatisfactorio",
            "Regular": "🟠 Regular",
            "Satisfactorio": "🟢 Satisfactorio",
            "Muy satisfactorio": "🟢 Muy satisfactorio",
            "Sin dato": "⚪ Sin dato",
        }
    )
    st.dataframe(
        table[["Código", "Dimensión", "Preguntas", "Satisfacción", "Promedio Likert", "Semáforo", "Intervalo", "Brecha a 75%"]],
        use_container_width=True,
        hide_index=True,
    )

    section_title("Conclusiones clave")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.markdown(
            f'<div class="finding alert"><b>Principal prioridad · {worst["Código"]}</b><br>{escape(worst["Dimensión"])} registra <b>{pct(worst["Satisfacción"])}</b>. Su nivel es <b>{escape(worst["Nivel"])}</b>.</div>',
            unsafe_allow_html=True,
        )
    with cc2:
        st.markdown(
            f'<div class="finding good"><b>Fortaleza relativa · {best["Código"]}</b><br>{escape(best["Dimensión"])} obtiene el resultado más alto: <b>{pct(best["Satisfacción"])}</b>.</div>',
            unsafe_allow_html=True,
        )
    with cc3:
        klass = "good" if meets == 4 else "warn"
        st.markdown(
            f'<div class="finding {klass}"><b>Meta institucional</b><br><b>{meets} de 4</b> dimensiones están en nivel satisfactorio o superior (≥75%).</div>',
            unsafe_allow_html=True,
        )


# ==============================================================
# 2) EXPLORAR DIMENSIONES
# ==============================================================
elif page == "Explorar dimensiones":
    hero(
        "Explorar dimensiones",
        "Profundiza en D1, D2, D3 o D4 y revisa los ítems que explican el resultado. La valoración por ítem se mantiene descriptiva y separada de la escala institucional.",
    )

    options = {
        "Todas las dimensiones": "TODAS",
        "D1 · Calidad del proceso académico": "D1",
        "D2 · Desempeño docente y estrategias pedagógicas": "D2",
        "D3 · Servicios y gestión educativa": "D3",
        "D4 · Formación integral y desarrollo personal": "D4",
    }
    label = st.selectbox("Dimensión de análisis", list(options.keys()), index=3)
    selected = options[label]

    if selected == "TODAS":
        items = all_items
        best_dim = summary_dim.sort_values("Satisfacción", ascending=False).iloc[0]
        worst_dim = summary_dim.sort_values("Satisfacción").iloc[0]
        c1, c2, c3 = st.columns(3)
        with c1:
            kpi_card("Vista activa", "D1–D4", "Comparación de los 16 ítems", COLORS_DIM["D1"])
        with c2:
            kpi_card("Mayor resultado", best_dim["Código"], f'{pct(best_dim["Satisfacción"])} · {escape(best_dim["Nivel"])}', LEVEL_META[best_dim["Nivel"]]["color"])
        with c3:
            kpi_card("Menor resultado", worst_dim["Código"], f'{pct(worst_dim["Satisfacción"])} · {escape(worst_dim["Nivel"])}', LEVEL_META[worst_dim["Nivel"]]["color"])
    else:
        info = DIMENSIONS[selected]
        items = info["items"]
        sat = df[f"{selected}_Satisfecho"].mean()
        avg = df[f"{selected}_Promedio"].mean()
        gap = max(0, 0.75 - sat)
        level = nivel_inst(sat)
        meta = LEVEL_META[level]
        st.markdown(
            f'<div class="panel" style="margin-bottom:12px"><div class="panel-title">{selected} · {escape(info["name"])}</div>'
            f'<div class="panel-sub">{escape(info["description"])}</div>{level_html(level, True)}</div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            kpi_card("Satisfacción", pct(sat), f'{level_html(level)}', meta["color"])
        with c2:
            kpi_card("Promedio Likert", f"{avg:.2f} / 5", "Promedio de las cuatro preguntas", COLORS_DIM[selected])
        with c3:
            kpi_card("Brecha a 75%", f"{gap*100:.2f} pp", "0 pp significa que ya alcanza la meta", "#027A48" if gap == 0 else "#B54708")

    items_df = item_summary(df, items).sort_values("Favorable", ascending=True)
    items_df["Etiqueta"] = items_df.apply(
        lambda r: f"{r['Ítem']} · {r['Texto'][:60]}{'…' if len(r['Texto']) > 60 else ''}", axis=1
    )

    section_title("Valoración favorable de los ítems", "4–5 = favorable · lectura descriptiva")
    fig = px.bar(
        items_df,
        x="Favorable",
        y="Etiqueta",
        orientation="h",
        color="Dimensión",
        color_discrete_map=COLORS_DIM,
        text=items_df["Favorable"].map(lambda x: f"{x*100:.1f}%"),
        custom_data=["Ítem", "Texto", "Neutral", "Desfavorable", "Promedio"],
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>"
            "Favorable: %{x:.2%}<br>"
            "Neutral: %{customdata[2]:.2%}<br>"
            "Desfavorable: %{customdata[3]:.2%}<br>"
            "Promedio Likert: %{customdata[4]:.2f}<extra></extra>"
        ),
    )
    fig.update_xaxes(tickformat=".0%", range=[0, 1.03], title="% favorable (respuestas 4–5)")
    fig.update_yaxes(title=None)
    fig.update_layout(showlegend=(selected == "TODAS"), legend_title_text="Dimensión")
    height = 700 if selected == "TODAS" else 480
    st.plotly_chart(plot_layout(fig, height), use_container_width=True)

    long_rows = []
    for item in items:
        s = df[item].dropna()
        code = next(c for c, info in DIMENSIONS.items() if item in info["items"])
        cats = {
            "Desfavorable (1–2)": (s <= 2).mean(),
            "Neutral (3)": (s == 3).mean(),
            "Favorable (4–5)": (s >= 4).mean(),
        }
        for category, value in cats.items():
            long_rows.append(
                {
                    "Ítem": item,
                    "Dimensión": code,
                    "Categoría": category,
                    "Porcentaje": value,
                    "Texto": QUESTION_TEXT[item],
                }
            )
    likert_df = pd.DataFrame(long_rows)

    section_title("Distribución de respuestas", "Desfavorable · Neutral · Favorable")
    fig2 = px.bar(
        likert_df,
        x="Porcentaje",
        y="Ítem",
        color="Categoría",
        orientation="h",
        barmode="stack",
        category_orders={
            "Categoría": ["Desfavorable (1–2)", "Neutral (3)", "Favorable (4–5)"],
            "Ítem": list(reversed(items)),
        },
        color_discrete_map=LIKERT_COLORS,
        custom_data=["Texto"],
    )
    fig2.update_traces(hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>%{fullData.name}: %{x:.2%}<extra></extra>")
    fig2.update_xaxes(tickformat=".0%", range=[0, 1], title="Distribución")
    fig2.update_yaxes(title=None)
    fig2.update_layout(legend_title_text=None, legend_orientation="h", legend_y=1.08)
    st.plotly_chart(plot_layout(fig2, height), use_container_width=True)

    worst_item = items_df.sort_values("Favorable").iloc[0]
    best_item = items_df.sort_values("Favorable", ascending=False).iloc[0]
    section_title("Lectura del filtro seleccionado")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="finding alert"><b>Menor valoración · {worst_item["Ítem"]}</b><br>{escape(worst_item["Texto"])}<br><br><b>{pct(worst_item["Favorable"])}</b> favorable · <b>{pct(worst_item["Desfavorable"])}</b> desfavorable.</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="finding good"><b>Mayor valoración · {best_item["Ítem"]}</b><br>{escape(best_item["Texto"])}<br><br><b>{pct(best_item["Favorable"])}</b> favorable.</div>',
            unsafe_allow_html=True,
        )


# ==============================================================
# 3) PRIORIDADES DE MEJORA
# ==============================================================
elif page == "Prioridades de mejora":
    hero(
        "Prioridades de mejora",
        "Ordena P1–P16 desde la menor hasta la mayor valoración favorable para focalizar la discusión en aspectos concretos del servicio educativo.",
    )

    rank = item_summary(df, all_items).sort_values("Favorable", ascending=True).copy()
    rank["Etiqueta"] = rank.apply(
        lambda r: f"{r['Ítem']} · {r['Texto'][:53]}{'…' if len(r['Texto']) > 53 else ''}", axis=1
    )
    # Colores de prioridad descriptiva; NO representan la escala institucional.
    rank["BarColor"] = "#64748B"
    rank.loc[rank.index[:3], "BarColor"] = "#B42318"
    rank.loc[rank.index[3:5], "BarColor"] = "#D97706"

    bottom = rank.iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Aspecto más crítico", bottom["Ítem"], pct(bottom["Favorable"]), "#B42318")
    with c2:
        kpi_card("Dimensión asociada", bottom["Dimensión"], DIMENSIONS[bottom["Dimensión"]]["name"], COLORS_DIM[bottom["Dimensión"]])
    with c3:
        kpi_card("Promedio del aspecto", f"{bottom['Promedio']:.2f} / 5", "Promedio Likert del ítem con menor favorable", "#B54708")

    section_title("Ranking de P1–P16", "Rojo/ámbar = prioridad descriptiva, no nivel institucional")
    st.markdown(
        '<div class="priority-legend"><b>Importante:</b> el color de este ranking solo ayuda a priorizar los 5 ítems con menor valoración. La escala institucional de 60%/75%/90% se aplica a D1–D4 y P17, no a cada pregunta.</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        go.Bar(
            x=rank["Favorable"],
            y=rank["Etiqueta"],
            orientation="h",
            marker=dict(color=rank["BarColor"]),
            text=rank["Favorable"].map(lambda x: f"{x*100:.1f}%"),
            textposition="outside",
            customdata=rank[["Ítem", "Dimensión", "Texto", "Neutral", "Desfavorable", "Promedio"]],
            hovertemplate=(
                "<b>%{customdata[0]} · %{customdata[1]}</b><br>%{customdata[2]}<br>"
                "Favorable: %{x:.2%}<br>Neutral: %{customdata[3]:.2%}<br>"
                "Desfavorable: %{customdata[4]:.2%}<br>Promedio: %{customdata[5]:.2f}<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(tickformat=".0%", range=[0, 1.03], title="% favorable (respuestas 4–5)")
    fig.update_yaxes(title=None, tickfont=dict(size=10))
    st.plotly_chart(plot_layout(fig, 730), use_container_width=True)

    section_title("5 aspectos con menor valoración favorable")
    top5 = rank.head(5).copy()
    display = top5[["Ítem", "Dimensión", "Texto", "Favorable", "Desfavorable", "Promedio"]].copy()
    display["Favorable"] = display["Favorable"].map(lambda x: pct(x, 2))
    display["Desfavorable"] = display["Desfavorable"].map(lambda x: pct(x, 2))
    display["Promedio"] = display["Promedio"].map(lambda x: f"{x:.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    first3 = rank.head(3)
    msg = ", ".join(f"{r['Ítem']} ({r['Dimensión']})" for _, r in first3.iterrows())
    st.markdown(
        f'<div class="finding alert"><b>Mensaje para la sustentación</b><br>Los tres aspectos con menor valoración favorable son <b>{escape(msg)}</b>. Sirven para orientar las prioridades de mejora sin confundir la valoración favorable del ítem con la satisfacción oficial de su dimensión.</div>',
        unsafe_allow_html=True,
    )


# ==============================================================
# 4) METODOLOGÍA
# ==============================================================
else:
    hero(
        "Metodología e interpretación",
        "Reglas de cálculo, escala institucional e interpretación de los resultados. El semáforo representa los mismos intervalos definidos en el instrumento.",
    )

    section_title("Cómo se calcula")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="method-card">
              <h3>Satisfacción por dimensión</h3>
              <p><b>D1, D2, D3 y D4</b> contienen 4 preguntas cada una.</p>
              <p>Para cada estudiante se calcula el promedio de sus cuatro respuestas.</p>
              <p>Si el promedio es <b>≥ 4</b>, el estudiante se clasifica como satisfecho en esa dimensión.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="method-card">
              <h3>Satisfacción general</h3>
              <p>Se obtiene directamente del ítem <b>P17</b>.</p>
              <p>P17 = 4 o 5 → <b>satisfecho</b>.</p>
              <p>P17 = 1, 2 o 3 → <b>no satisfecho</b>.</p>
              <p>No se calcula promediando D1–D4.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_title("Semáforo e intervalos institucionales", "Se aplica a D1–D4 y P17")
    level_cols = st.columns(4)
    for col, level in zip(level_cols, ["Insatisfactorio", "Regular", "Satisfactorio", "Muy satisfactorio"]):
        m = LEVEL_META[level]
        with col:
            st.markdown(
                f"""
                <div class="level-card" style="--level-color:{m['color']};--level-bg:{m['bg']};--level-border:{m['border']};">
                  <div class="level-name"><span class="status-dot" style="--status-color:{m['color']};margin-right:8px"></span>{escape(level)}</div>
                  <div class="level-range">{m['interval']}</div>
                  <div class="level-help">{m['short']}. El color siempre aparece acompañado por nombre e intervalo.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(f'<div class="panel" style="margin-top:12px">{semaforo_scale()}</div>', unsafe_allow_html=True)

    section_title("Cómo leer los ítems")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            """
            <div class="method-card">
              <h3>Distribución de respuestas</h3>
              <p><b>Desfavorable:</b> respuestas 1 y 2.</p>
              <p><b>Neutral:</b> respuesta 3.</p>
              <p><b>Favorable:</b> respuestas 4 y 5.</p>
              <p>Esto permite localizar qué preguntas explican fortalezas o debilidades.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            """
            <div class="method-card">
              <h3>Separación metodológica</h3>
              <p>Los porcentajes favorables de P1–P16 son <b>descriptivos</b>.</p>
              <p>El semáforo institucional de 60% / 75% / 90% se utiliza para <b>D1–D4 y P17</b>.</p>
              <p>Por eso el ranking de preguntas no asigna un nivel institucional a cada ítem.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
