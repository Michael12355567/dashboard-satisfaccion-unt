from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

# ==============================================================
# CONFIGURACIÓN
# ==============================================================
st.set_page_config(
    page_title="UNT | Satisfacción con la formación académica integral",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "basededatos.xlsx"
SHEET_NAME = "Base_Encuesta"

ITEMS = [f"P{i}" for i in range(1, 18)]
VALID_VALUES = {1, 2, 3, 4, 5}

DIMENSIONS = {
    "D1": {
        "name": "Calidad del proceso académico",
        "items": ["P1", "P2", "P3", "P4"],
        "accent": "#2F6FA3",
        "soft": "#EEF6FC",
    },
    "D2": {
        "name": "Desempeño docente y estrategias pedagógicas",
        "items": ["P5", "P6", "P7", "P8"],
        "accent": "#6B62A6",
        "soft": "#F4F1FB",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "items": ["P9", "P10", "P11", "P12"],
        "accent": "#B0734B",
        "soft": "#FFF5EC",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "items": ["P13", "P14", "P15", "P16"],
        "accent": "#2F8271",
        "soft": "#EEF9F6",
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
    "P17": "En general, me siento satisfecho(a) con la formación académica que recibo en la Universidad Nacional de Trujillo.",
}

LIKERT_LABELS = {
    1: "Totalmente en desacuerdo",
    2: "En desacuerdo",
    3: "Ni de acuerdo ni en desacuerdo",
    4: "De acuerdo",
    5: "Totalmente de acuerdo",
}

# ==============================================================
# ESTILOS
# ==============================================================
st.markdown(
    r"""
<style>
:root{
  --ink:#17324D;--muted:#6C7F93;--line:rgba(214,225,237,.90);--blue:#245DB7;
  --green:#19866E;--red:#B85A67;--amber:#B77A12;--cyan:#207C98;
  --glass:rgba(255,255,255,.70);--shadow:0 18px 45px rgba(32,72,122,.10),0 4px 12px rgba(32,72,122,.05);
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"Segoe UI Variable","Aptos","Segoe UI",Arial,sans-serif}
.stApp{
  color:var(--ink);
  background:
    radial-gradient(circle at 8% 3%,rgba(52,104,205,.14),transparent 30%),
    radial-gradient(circle at 94% 7%,rgba(33,166,183,.11),transparent 29%),
    linear-gradient(180deg,#F9FBFF 0%,#FFFFFF 48%,#F7FAFE 100%);
}
header[data-testid="stHeader"]{background:rgba(250,252,255,.68);backdrop-filter:blur(20px)}
#MainMenu,footer{visibility:hidden}
section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}
.block-container{max-width:1580px;padding:.65rem 1.25rem 3rem}

.topbar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:13px 17px;border-radius:0 0 18px 18px;background:linear-gradient(110deg,rgba(17,57,115,.94),rgba(32,90,179,.88));color:#fff;border:1px solid rgba(255,255,255,.20);box-shadow:0 18px 40px rgba(24,67,143,.20);backdrop-filter:blur(22px)}
.brand{display:flex;gap:11px;align-items:center}.brand-mark{width:49px;height:49px;border-radius:13px;background:rgba(255,255,255,.92);color:#17427F;display:grid;place-items:center;font-weight:1000;letter-spacing:.05em;box-shadow:0 8px 18px rgba(5,30,70,.20)}
.brand-title{font-weight:950;font-size:1rem;line-height:1.1}.brand-sub{font-size:.72rem;opacity:.84;margin-top:3px}.top-meta{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.meta{padding:8px 10px;border-radius:10px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);font-size:.66rem}.meta b{display:block;font-size:.78rem;margin-top:2px}

.pagehead{padding:23px 4px 14px}.kicker,.section-kicker{font-size:.72rem;font-weight:950;letter-spacing:.14em;text-transform:uppercase;color:#3369CB}.title{font-size:clamp(2rem,3.4vw,2.8rem);font-weight:950;letter-spacing:-.045em;color:#122E4C;line-height:1.02;margin-top:4px}.sub{font-size:.95rem;line-height:1.62;color:#61768C;max-width:1190px;margin-top:8px}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}.chip{font-size:.72rem;font-weight:850;padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.62);border:1px solid rgba(255,255,255,.92);box-shadow:0 8px 20px rgba(31,72,132,.06)}

.stTabs [data-baseweb="tab-list"]{gap:7px;border-bottom:1px solid #DDE6F0;background:transparent;overflow-x:auto}.stTabs [data-baseweb="tab"]{height:50px;padding:0 15px;font-size:.90rem;font-weight:900;color:#64778D;border-radius:11px 11px 0 0}.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#2456B2,#3472D4)!important;color:#fff!important;box-shadow:0 8px 18px rgba(35,86,178,.16)!important}.stTabs [data-baseweb="tab-highlight"]{display:none}

.section-head{display:flex;justify-content:space-between;align-items:end;gap:18px;margin:1.35rem 0 .70rem}.section-title{font-size:clamp(1.3rem,2.2vw,1.65rem);font-weight:950;letter-spacing:-.025em;color:#17324F;margin-top:3px}.section-note{font-size:.79rem;color:#78899B;line-height:1.48;text-align:right;max-width:720px}
.panel{background:var(--glass);border:1px solid rgba(255,255,255,.92);box-shadow:var(--shadow);backdrop-filter:blur(24px) saturate(145%);border-radius:19px}

.hero-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(330px,.5fr);gap:14px}.hero{padding:25px 27px;position:relative;overflow:hidden;border-left:7px solid #245DB7}.hero:after{content:"";position:absolute;width:330px;height:330px;border-radius:50%;right:-150px;top:-210px;background:radial-gradient(circle,rgba(47,102,200,.12),transparent 68%)}.hero>*{position:relative;z-index:1}.hero-eyebrow{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;font-weight:950;color:#3266C4}.hero-title{font-size:clamp(1.55rem,2.6vw,2.15rem);font-weight:950;line-height:1.13;margin-top:5px}.hero-desc{font-size:.88rem;line-height:1.6;color:#60758B;margin-top:8px;max-width:1040px}.hero-core{display:grid;grid-template-columns:230px minmax(0,1fr);gap:20px;align-items:center;margin-top:18px}.hero-score{font-size:clamp(4rem,7vw,6rem);font-weight:1000;color:#194F94;letter-spacing:-.07em;line-height:.9}.hero-level{font-size:.95rem;font-weight:950;margin-top:9px}.hero-level small{display:block;font-size:.69rem;font-weight:750;color:#73869A;margin-top:4px}.formula{padding:15px 16px;border-radius:15px;background:rgba(242,247,253,.85);border:1px solid #DCE7F2}.formula-k{font-size:.70rem;color:#6C8094;font-weight:900}.formula-eq{font-size:1rem;font-weight:950;margin-top:8px;color:#173B5D}.formula-result{display:inline-block;margin-left:5px;padding:5px 9px;border-radius:9px;background:#fff;border:1px solid #D7E3F0;color:#215DAF}.hero-foot{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:16px}.hero-foot>div{padding:11px 12px;border-radius:12px;background:rgba(247,250,253,.88);border:1px solid #E2EAF2}.hero-foot b{display:block;font-size:.68rem;color:#728297}.hero-foot span{display:block;font-size:.92rem;font-weight:950;color:#183752;margin-top:3px}
.side-stack{display:grid;grid-template-rows:1fr 1fr;gap:12px}.side{padding:18px 19px}.side-k{font-size:.67rem;text-transform:uppercase;letter-spacing:.10em;font-weight:950;color:#7B8B9E}.side-t{font-size:1.04rem;font-weight:950;margin-top:5px}.side-x{font-size:.78rem;line-height:1.56;color:#65798F;margin-top:9px}.side-big{font-size:2.6rem;font-weight:1000;letter-spacing:-.05em;margin-top:12px;color:#B45A66}

.explain{margin-top:12px;padding:14px 16px;border-radius:15px;background:rgba(244,248,253,.84);border:1px solid #DDE7F2;color:#526B84;font-size:.81rem;line-height:1.58}.explain b{color:#153B61}.explain .headline{font-size:.91rem;font-weight:950;color:#153B61;margin-bottom:4px}

.scale{padding:14px 15px}.scale-title{font-size:.83rem;font-weight:950;color:#1B3B59}.scale-sub{font-size:.72rem;color:#718397;line-height:1.48;margin-top:4px}.scale-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:11px}.scale-step{padding:10px 8px;text-align:center;border-radius:12px;border:1px solid #E1E9F1;background:rgba(255,255,255,.64);opacity:.66}.scale-step.active{opacity:1;border:2px solid var(--lvl);box-shadow:0 8px 18px color-mix(in srgb,var(--lvl) 16%,transparent);transform:translateY(-1px)}.scale-dot{width:11px;height:11px;border-radius:50%;margin:0 auto 5px;background:var(--lvl)}.scale-name{font-size:.72rem;font-weight:950}.scale-range{font-size:.65rem;color:#8190A2;margin-top:2px}

.dim-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px}.dim{padding:17px 17px 15px;position:relative;overflow:hidden;border-top:4px solid var(--accent)}.dim-code{font-size:.72rem;font-weight:1000;color:var(--accent)}.dim-name{font-size:.83rem;font-weight:900;line-height:1.32;margin-top:4px;min-height:2.6em}.dim-score{font-size:2.15rem;font-weight:1000;letter-spacing:-.05em;margin-top:13px;color:#173651}.level-badge{display:inline-flex;margin-top:5px;padding:5px 8px;border-radius:9px;background:var(--soft);color:var(--accent);font-size:.68rem;font-weight:950}.dim-meta{font-size:.70rem;line-height:1.53;color:#667A90;margin-top:11px}.dim-meta b{color:#24435F}.dim-rule{margin-top:10px;padding-top:9px;border-top:1px dashed #DDE5EE;font-size:.66rem;color:#718397;line-height:1.45}

.insight-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.insight{padding:15px 16px;border-left:4px solid var(--accent)}.insight-k{font-size:.65rem;letter-spacing:.09em;text-transform:uppercase;color:#8190A2;font-weight:950}.insight-t{font-size:1rem;font-weight:950;margin-top:5px}.insight-x{font-size:.76rem;line-height:1.55;color:#677B91;margin-top:6px}

.item-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}.item{padding:15px;border-left:4px solid var(--accent);position:relative;overflow:hidden}.item-top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}.item-code{font-size:.68rem;font-weight:1000;color:var(--accent);padding:5px 7px;border-radius:8px;background:var(--soft)}.item-score{font-size:1.35rem;font-weight:1000;color:#173650}.item-q{font-size:.78rem;line-height:1.52;color:#5F7489;margin-top:9px;min-height:4.6em}.binary-pill{height:12px;border-radius:999px;background:#EDF2F6;overflow:hidden;display:flex;margin-top:11px}.no-seg{height:100%;background:#CB6470}.sat-seg{height:100%;background:#328A74}.item-meta{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:9px}.item-meta>div{padding:8px;border-radius:10px;background:rgba(248,250,253,.88);border:1px solid #E5EBF1}.item-meta .k{font-size:.58rem;text-transform:uppercase;color:#8593A3;font-weight:900;line-height:1.25}.item-meta .v{font-size:.82rem;font-weight:1000;color:#2A455E;margin-top:3px}.item-note{font-size:.62rem;color:#8190A1;margin-top:8px}

.binary-panel{padding:14px 16px}.legend{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:9px;font-size:.69rem;color:#6F8194;font-weight:850}.legend span{display:flex;align-items:center;gap:6px}.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}.legend .n{background:#CB6470}.legend .s{background:#328A74}.bar-row{display:grid;grid-template-columns:48px minmax(0,1fr);gap:10px;align-items:center;padding:7px 0;border-top:1px solid rgba(228,235,242,.75)}.bar-row:first-of-type{border-top:0}.bar-code{font-size:.70rem;font-weight:1000;color:#4A627A}.bar{height:27px;border-radius:999px;overflow:hidden;display:flex;background:#EFF3F7;box-shadow:inset 0 2px 4px rgba(31,55,82,.07)}.bar>div{display:flex;align-items:center;justify-content:center;color:#fff;font-size:.58rem;font-weight:950;white-space:nowrap}.bar .n{background:linear-gradient(180deg,#D06E79,#BF5663)}.bar .s{background:linear-gradient(180deg,#459D87,#2F826F)}

.method-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.method{padding:16px}.method-t{font-size:.94rem;font-weight:950}.method-x{font-size:.76rem;line-height:1.58;color:#687C91;margin-top:6px}.audit-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.audit{padding:14px}.audit-k{font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#8594A5;font-weight:950}.audit-v{font-size:1.35rem;font-weight:1000;margin-top:5px}.audit-x{font-size:.69rem;line-height:1.48;color:#6E8195;margin-top:4px}.note{padding:13px 15px;border-radius:14px;background:#FFF8E9;border:1px solid #EFDFB7;color:#715A24;font-size:.74rem;line-height:1.55;margin-top:10px}

div[data-baseweb="select"]>div{background:rgba(255,255,255,.78)!important;border:1px solid #D8E3ED!important;border-radius:12px!important;min-height:44px!important}
div[data-testid="stDataFrame"]{border:1px solid #E0E8F0;border-radius:14px;overflow:hidden}

@media(max-width:1100px){.hero-grid{grid-template-columns:1fr}.side-stack{grid-template-columns:1fr 1fr;grid-template-rows:auto}.dim-grid{grid-template-columns:1fr 1fr}.item-grid{grid-template-columns:1fr 1fr}.audit-grid{grid-template-columns:1fr 1fr}}
@media(max-width:700px){.block-container{padding:.45rem .68rem 2rem}.top-meta{display:none}.title{font-size:1.72rem}.sub{font-size:.84rem}.hero{padding:19px 17px}.hero-core{grid-template-columns:1fr}.hero-score{font-size:3.7rem}.hero-foot{grid-template-columns:1fr 1fr}.hero-foot>div:last-child{grid-column:1/-1}.side-stack,.dim-grid,.item-grid,.insight-grid,.method-grid,.audit-grid{grid-template-columns:1fr}.scale-grid{grid-template-columns:1fr 1fr}.section-note{display:none}.item-q{min-height:0}.bar-row{grid-template-columns:38px minmax(0,1fr)}}
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


def level_for_percentage(value: float) -> tuple[str, str, str]:
    """Criterios de interpretación de la propuesta del instrumento.

    Los cortes se implementan como intervalos continuos para porcentajes con decimales:
    <60, 60–<75, 75–<90 y >=90.
    """
    if pd.isna(value):
        return "Sin dato", "—", "#8492A2"
    if value < 0.60:
        return "Insatisfactorio", "0% a <60%", "#B85A67"
    if value < 0.75:
        return "Regular", "60% a <75%", "#B77A12"
    if value < 0.90:
        return "Satisfactorio", "75% a <90%", "#19866E"
    return "Muy satisfactorio", "90% a 100%", "#207C98"


def section_header(kicker: str, title: str, note: str = "") -> None:
    st.markdown(
        f'<div class="section-head"><div><div class="section-kicker">{escape(kicker)}</div>'
        f'<div class="section-title">{escape(title)}</div></div>'
        f'<div class="section-note">{escape(note)}</div></div>',
        unsafe_allow_html=True,
    )


# ==============================================================
# CARGA Y CÁLCULO — RECONSTRUIDOS DESDE P1–P17
# ==============================================================
def require_columns(df: pd.DataFrame) -> None:
    missing = [c for c in ITEMS if c not in df.columns]
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(missing))


@st.cache_data(show_spinner=False)
def load_data(path: str, mtime: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(path, sheet_name=SHEET_NAME)
    require_columns(raw)
    data = raw.copy()
    for c in ITEMS:
        data[c] = pd.to_numeric(data[c], errors="coerce")
    return raw, data


if not DATA_FILE.exists():
    st.error("No se encontró basededatos.xlsx en la misma carpeta que app.py.")
    st.stop()

try:
    raw_df, df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"No pude leer la base: {exc}")
    st.stop()

N_ROWS = len(df)

# Calidad de la matriz P1–P17.
missing_responses = int(df[ITEMS].isna().sum().sum())
invalid_mask = pd.DataFrame(False, index=df.index, columns=ITEMS)
for c in ITEMS:
    invalid_mask[c] = df[c].notna() & ~df[c].isin(VALID_VALUES)
invalid_responses = int(invalid_mask.sum().sum())

# Se excluyen valores inválidos de cualquier cálculo, sin convertirlos a "no satisfecho".
clean = df.copy()
for c in ITEMS:
    clean.loc[~clean[c].isin(VALID_VALUES), c] = pd.NA

# P17 = satisfacción general: 4 o 5 satisfecho; 1,2,3 no satisfecho.
p17_valid = clean["P17"].notna()
p17_sat = clean.loc[p17_valid, "P17"].isin([4, 5])
GLOBAL_D = int(p17_valid.sum())
GLOBAL_N = int(p17_sat.sum())
GLOBAL = GLOBAL_N / GLOBAL_D if GLOBAL_D else float("nan")
GLOBAL_NO_N = GLOBAL_D - GLOBAL_N
GLOBAL_NO = GLOBAL_NO_N / GLOBAL_D if GLOBAL_D else float("nan")
GLOBAL_MEAN = float(clean.loc[p17_valid, "P17"].mean()) if GLOBAL_D else float("nan")
GLOBAL_LEVEL, GLOBAL_RANGE, GLOBAL_COLOR = level_for_percentage(GLOBAL)

# D1–D4: promedio de sus 4 ítems, solo si los 4 son válidos; promedio >=4 = satisfecho.
dim_rows = []
for code, meta in DIMENSIONS.items():
    valid = clean[meta["items"]].notna().all(axis=1)
    score = clean.loc[valid, meta["items"]].mean(axis=1)
    sat = score >= 4
    d = int(valid.sum())
    n = int(sat.sum())
    p = n / d if d else float("nan")
    level, rng, color = level_for_percentage(p)
    dim_rows.append({
        "Código": code,
        "Dimensión": meta["name"],
        "N": n,
        "D": d,
        "Satisfacción": p,
        "No satisfecho": 1 - p if d else float("nan"),
        "Promedio": float(score.mean()) if d else float("nan"),
        "Nivel": level,
        "Rango": rng,
        "Color": color,
    })
DIMS = pd.DataFrame(dim_rows)

# P1–P17: diagnóstico por pregunta. No se crean categorías intermedias.
item_rows = []
for i in range(1, 18):
    item = f"P{i}"
    s = clean[item].dropna()
    d = int(len(s))
    n = int(s.isin([4, 5]).sum())
    no_n = d - n
    code = f"D{((i - 1) // 4) + 1}" if i <= 16 else "GLOBAL"
    rec = {
        "Número": i,
        "Ítem": item,
        "Dimensión": code,
        "Pregunta": ITEM_TEXT[item],
        "N satisfechos": n,
        "N no satisfechos": no_n,
        "D": d,
        "Satisfecho": n / d if d else float("nan"),
        "No satisfecho": no_n / d if d else float("nan"),
        "Promedio": float(s.mean()) if d else float("nan"),
    }
    for v in range(1, 6):
        rec[f"Resp {v}"] = float((s == v).mean()) if d else float("nan")
        rec[f"N Resp {v}"] = int((s == v).sum())
    item_rows.append(rec)
ITEMS_SUM = pd.DataFrame(item_rows)

# Auditoría de columnas calculadas ya presentes en el Excel.
derived_checks = []
for code, meta in DIMENSIONS.items():
    stored_prom = f"{code}_Promedio"
    stored_sat = f"{code}_Satisfecho"
    valid = clean[meta["items"]].notna().all(axis=1)
    calc_prom = clean[meta["items"]].mean(axis=1)
    calc_sat = (calc_prom >= 4).astype(int)
    if stored_prom in raw_df.columns:
        cmp = pd.to_numeric(raw_df[stored_prom], errors="coerce")
        mismatch = int(((cmp - calc_prom).abs() > 1e-9).fillna(valid).sum())
        derived_checks.append((stored_prom, mismatch))
    if stored_sat in raw_df.columns:
        cmp = pd.to_numeric(raw_df[stored_sat], errors="coerce")
        mismatch = int((cmp.loc[valid].astype("Int64") != calc_sat.loc[valid].astype("Int64")).sum())
        derived_checks.append((stored_sat, mismatch))

if "Global_Satisfecho" in raw_df.columns:
    calc_global = clean["P17"].isin([4, 5]).astype(int)
    cmp = pd.to_numeric(raw_df["Global_Satisfecho"], errors="coerce")
    mismatch = int((cmp.loc[p17_valid].astype("Int64") != calc_global.loc[p17_valid].astype("Int64")).sum())
    derived_checks.append(("Global_Satisfecho", mismatch))
if "Categoria_Global" in raw_df.columns:
    calc_cat = pd.Series(pd.NA, index=clean.index, dtype="object")
    calc_cat.loc[p17_valid] = clean.loc[p17_valid, "P17"].isin([4, 5]).map({True: "Satisfecho", False: "No satisfecho"})
    cmp = raw_df["Categoria_Global"].astype(str).str.strip()
    mismatch = int((cmp.loc[p17_valid] != calc_cat.loc[p17_valid]).sum())
    derived_checks.append(("Categoria_Global", mismatch))

DERIVED_MISMATCHES = sum(x[1] for x in derived_checks)
DERIVED_CHECKED = len(derived_checks)

# Fechas descriptivas.
if "Fecha" in raw_df.columns:
    dt = pd.to_datetime(raw_df["Fecha"], errors="coerce")
    date_start = dt.min()
    date_end = dt.max()
else:
    date_start = pd.NaT
    date_end = pd.NaT
period = (
    f"{date_start.strftime('%d/%m/%Y')} – {date_end.strftime('%d/%m/%Y')}"
    if pd.notna(date_start) and pd.notna(date_end)
    else "2026"
)

# ==============================================================
# COMPONENTES
# ==============================================================
def top_header() -> None:
    st.markdown(
        f'''<div class="topbar">
          <div class="brand"><div class="brand-mark">UNT</div><div><div class="brand-title">Tablero de satisfacción académica</div><div class="brand-sub">Universidad Nacional de Trujillo · Formación académica integral</div></div></div>
          <div class="top-meta"><div class="meta">Periodo<b>{escape(period)}</b></div><div class="meta">Base analizada<b>{N_ROWS:,} registros</b></div><div class="meta">Versión<b>Auditada Word + Excel</b></div></div>
        </div>
        <div class="pagehead"><div class="kicker">Encuesta 2026 · indicador institucional</div><div class="title">Satisfacción con la formación académica integral</div>
        <div class="sub">Se reconstruyeron los cálculos directamente desde P1–P17 respetando el instrumento: <b>P17 es la satisfacción general</b>; en cada pregunta, <b>4 o 5 = satisfecho</b> y <b>1, 2 o 3 = no satisfecho</b>; y en D1–D4 el estudiante se considera satisfecho cuando el <b>promedio de los cuatro ítems de la dimensión es ≥4</b>.</div>
        <div class="chips"><span class="chip">Clasificación del indicador: 4–5 vs 1–3</span><span class="chip">Global = P17</span><span class="chip">Dimensiones = promedio individual ≥4</span><span class="chip">Preguntas P1–P17 por separado</span></div></div>''',
        unsafe_allow_html=True,
    )


def scale_html(value: float) -> str:
    level, rng, color = level_for_percentage(value)
    levels = [
        ("Insatisfactorio", "0% a <60%", "#B85A67"),
        ("Regular", "60% a <75%", "#B77A12"),
        ("Satisfactorio", "75% a <90%", "#19866E"),
        ("Muy satisfactorio", "90% a 100%", "#207C98"),
    ]
    blocks = []
    for name, interval, c in levels:
        active = " active" if name == level else ""
        blocks.append(
            f'<div class="scale-step{active}" style="--lvl:{c}"><div class="scale-dot"></div>'
            f'<div class="scale-name">{escape(name)}</div><div class="scale-range">{escape(interval)}</div></div>'
        )
    return (
        f'<div class="panel scale"><div class="scale-title">Cómo se interpreta el porcentaje de satisfacción · '
        f'<span style="color:{color}">resultado actual: {escape(level)}</span></div>'
        f'<div class="scale-sub">Esta escala clasifica el <b>porcentaje final de estudiantes satisfechos</b>; no clasifica respuestas individuales. '
        f'Por ejemplo, P17 = {pct(GLOBAL)} significa {pct(GLOBAL)} de estudiantes satisfechos y, según estos rangos del instrumento, el nivel del porcentaje es “{escape(GLOBAL_LEVEL)}”.</div>'
        f'<div class="scale-grid">{"".join(blocks)}</div></div>'
    )


def hero_html() -> str:
    return f'''<div class="hero-grid">
      <div class="panel hero">
        <div class="hero-eyebrow">Resultado principal · satisfacción general · P17</div>
        <div class="hero-title">Porcentaje de estudiantes de pregrado satisfechos con su formación académica integral</div>
        <div class="hero-desc">P17 es la pregunta global del instrumento. Un estudiante entra al numerador únicamente si respondió <b>4 = De acuerdo</b> o <b>5 = Totalmente de acuerdo</b>.</div>
        <div class="hero-core"><div><div class="hero-score">{pct(GLOBAL)}</div><div class="hero-level" style="color:{GLOBAL_COLOR}">{escape(GLOBAL_LEVEL)}<small>Nivel aplicado al porcentaje de satisfacción · {escape(GLOBAL_RANGE)}</small></div></div>
        <div class="formula"><div class="formula-k">Fórmula del indicador</div><div class="formula-eq">({GLOBAL_N:,} estudiantes satisfechos / {GLOBAL_D:,} estudiantes con P17 válido) × 100 <span class="formula-result">= {pct(GLOBAL)}</span></div></div></div>
        <div class="explain"><div class="headline">Lectura correcta</div><b>{GLOBAL_N:,}</b> de <b>{GLOBAL_D:,}</b> estudiantes respondieron 4 o 5 en P17. Por eso la satisfacción general es <b>{pct(GLOBAL)}</b>. Los <b>{GLOBAL_NO_N:,}</b> restantes ({pct(GLOBAL_NO)}) respondieron 1, 2 o 3 y se clasifican como <b>no satisfechos</b>. “Regular” no es una respuesta de la escala Likert: es únicamente el nivel asignado al <b>porcentaje {pct(GLOBAL)}</b> por los criterios de interpretación del instrumento.</div>
        <div class="hero-foot"><div><b>Satisfechos</b><span>{GLOBAL_N:,} · {pct(GLOBAL)}</span></div><div><b>No satisfechos</b><span>{GLOBAL_NO_N:,} · {pct(GLOBAL_NO)}</span></div><div><b>Promedio P17 (descriptivo)</b><span>{GLOBAL_MEAN:.2f}/5</span></div></div>
      </div>
      <div class="side-stack">
        <div class="panel side"><div class="side-k">Clasificación de P17</div><div class="side-t">Dos grupos para el indicador</div><div class="side-x"><b>Satisfecho:</b> 4 o 5.<br><b>No satisfecho:</b> 1, 2 o 3.<br><br>La opción 3 conserva su nombre original en la tabla Likert, pero para el <b>cálculo del indicador</b> se incluye dentro de “No satisfecho”.</div></div>
        <div class="panel side"><div class="side-k">Resultado complementario</div><div class="side-t">No satisfechos en P17</div><div class="side-big">{pct(GLOBAL_NO)}</div><div class="side-x">{GLOBAL_NO_N:,} de {GLOBAL_D:,} estudiantes. Este valor es exactamente el complemento de la satisfacción general: 100% − {pct(GLOBAL)}.</div></div>
      </div>
    </div>'''


def dimension_cards_html() -> str:
    cards = []
    for _, r in DIMS.sort_values("Código").iterrows():
        code = str(r["Código"])
        meta = DIMENSIONS[code]
        sat = float(r["Satisfacción"])
        no = float(r["No satisfecho"])
        cards.append(
            f'''<div class="panel dim" style="--accent:{meta['accent']};--soft:{meta['soft']}">
              <div class="dim-code">{escape(code)}</div><div class="dim-name">{escape(meta['name'])}</div>
              <div class="dim-score">{pct(sat)}</div><div class="level-badge">Nivel del porcentaje: {escape(str(r['Nivel']))}</div>
              <div class="dim-meta"><b>Satisfechos:</b> {int(r['N']):,} de {int(r['D']):,}<br><b>No satisfechos:</b> {pct(no)}<br><b>Promedio dimensional:</b> {float(r['Promedio']):.2f}/5</div>
              <div class="dim-rule"><b>Regla:</b> para cada estudiante se promedian {', '.join(meta['items'])}; si el promedio es ≥4, se clasifica como satisfecho en {escape(code)}.</div>
            </div>'''
        )
    return '<div class="dim-grid">' + ''.join(cards) + '</div>'


def executive_insights_html() -> str:
    weak_dim = DIMS.sort_values("Satisfacción").iloc[0]
    strong_dim = DIMS.sort_values("Satisfacción", ascending=False).iloc[0]
    p116 = ITEMS_SUM[ITEMS_SUM["Número"] <= 16]
    weak_item = p116.sort_values("Satisfecho").iloc[0]
    strong_item = p116.sort_values("Satisfecho", ascending=False).iloc[0]
    return f'''<div class="insight-grid">
      <div class="panel insight" style="--accent:#B85A67"><div class="insight-k">Mayor brecha dimensional</div><div class="insight-t">{escape(str(weak_dim['Código']))} · {pct(float(weak_dim['Satisfacción']))}</div><div class="insight-x"><b>{escape(str(weak_dim['Dimensión']))}</b> es la dimensión con menor porcentaje de estudiantes que alcanzan el criterio de promedio ≥4.</div></div>
      <div class="panel insight" style="--accent:#19866E"><div class="insight-k">Mejor resultado dimensional</div><div class="insight-t">{escape(str(strong_dim['Código']))} · {pct(float(strong_dim['Satisfacción']))}</div><div class="insight-x"><b>{escape(str(strong_dim['Dimensión']))}</b> presenta el mayor porcentaje de satisfacción dimensional.</div></div>
      <div class="panel insight" style="--accent:#B0734B"><div class="insight-k">Preguntas extremas P1–P16</div><div class="insight-t">{escape(str(weak_item['Ítem']))} {pct(float(weak_item['Satisfecho']))} · {escape(str(strong_item['Ítem']))} {pct(float(strong_item['Satisfecho']))}</div><div class="insight-x">Menor satisfacción: <b>{escape(str(weak_item['Ítem']))}</b>. Mayor satisfacción: <b>{escape(str(strong_item['Ítem']))}</b>. Estos porcentajes por pregunta se calculan con 4–5 frente a 1–3.</div></div>
    </div>'''


def item_cards_html(selected: str) -> str:
    if selected == "Todas":
        d = ITEMS_SUM.copy()
    elif selected == "P17":
        d = ITEMS_SUM[ITEMS_SUM["Ítem"] == "P17"].copy()
    else:
        d = ITEMS_SUM[ITEMS_SUM["Dimensión"] == selected].copy()
    cards = []
    for _, r in d.sort_values("Número").iterrows():
        code = str(r["Dimensión"])
        if code in DIMENSIONS:
            accent = DIMENSIONS[code]["accent"]
            soft = DIMENSIONS[code]["soft"]
            label = f"{code} · {DIMENSIONS[code]['name']}"
        else:
            accent = "#245DB7"
            soft = "#EEF4FF"
            label = "Satisfacción general"
        sat = float(r["Satisfecho"])
        no = float(r["No satisfecho"])
        cards.append(
            f'''<div class="panel item" style="--accent:{accent};--soft:{soft}">
              <div class="item-top"><div class="item-code">{escape(str(r['Ítem']))} · {escape(label)}</div><div class="item-score">{pct(sat)}</div></div>
              <div class="item-q">{escape(str(r['Pregunta']))}</div>
              <div class="binary-pill"><div class="no-seg" style="width:{no*100:.4f}%"></div><div class="sat-seg" style="width:{sat*100:.4f}%"></div></div>
              <div class="item-meta"><div><div class="k">Satisfechos · 4–5</div><div class="v">{pct(sat)} · {int(r['N satisfechos']):,}</div></div><div><div class="k">No satisfechos · 1–3</div><div class="v">{pct(no)} · {int(r['N no satisfechos']):,}</div></div></div>
              <div class="item-note">Base válida del ítem: {int(r['D']):,}. Promedio {float(r['Promedio']):.2f}/5 solo como dato descriptivo.</div>
            </div>'''
        )
    return '<div class="item-grid">' + ''.join(cards) + '</div>'


def binary_distribution_html(selected: str) -> str:
    if selected == "Todas":
        d = ITEMS_SUM.copy()
    elif selected == "P17":
        d = ITEMS_SUM[ITEMS_SUM["Ítem"] == "P17"].copy()
    else:
        d = ITEMS_SUM[ITEMS_SUM["Dimensión"] == selected].copy()
    rows = []
    for _, r in d.sort_values("Número").iterrows():
        no = float(r["No satisfecho"])
        sat = float(r["Satisfecho"])
        rows.append(
            f'<div class="bar-row"><div class="bar-code">{escape(str(r["Ítem"]))}</div><div class="bar">'
            f'<div class="n" style="width:{no*100:.4f}%">{pct(no,0) if no >= .07 else ""}</div>'
            f'<div class="s" style="width:{sat*100:.4f}%">{pct(sat,0) if sat >= .07 else ""}</div>'
            f'</div></div>'
        )
    return '<div class="panel binary-panel"><div class="legend"><span><i class="n"></i>No satisfechos · respuestas 1–3</span><span><i class="s"></i>Satisfechos · respuestas 4–5</span></div>' + ''.join(rows) + '</div>'


# ==============================================================
# APP
# ==============================================================
top_header()

tab1, tab2, tab3 = st.tabs(["◉ Resumen", "▦ Preguntas P1–P17", "ⓘ Metodología y control"])

with tab1:
    section_header(
        "Indicador principal",
        "Satisfacción general · P17",
        "El porcentaje se obtiene de P17: respuestas 4–5 en el numerador y respuestas válidas 1–5 en el denominador.",
    )
    st.markdown(hero_html(), unsafe_allow_html=True)
    st.markdown("<div style='height:11px'></div>", unsafe_allow_html=True)
    st.markdown(scale_html(GLOBAL), unsafe_allow_html=True)

    section_header(
        "Resultados por dimensión",
        "D1–D4 según el promedio individual de sus cuatro ítems",
        "El porcentaje dimensional no es el promedio de los porcentajes de sus preguntas; primero se clasifica a cada estudiante por su promedio dimensional ≥4 y luego se calcula N/D × 100.",
    )
    st.markdown(dimension_cards_html(), unsafe_allow_html=True)

    section_header("Lectura ejecutiva", "Dónde se concentran las fortalezas y las brechas")
    st.markdown(executive_insights_html(), unsafe_allow_html=True)

with tab2:
    section_header(
        "Análisis por pregunta",
        "Satisfechos y no satisfechos en cada ítem",
        "Para cada pregunta: 4 o 5 = satisfecho; 1, 2 o 3 = no satisfecho. No se crea una categoría adicional para la respuesta 3.",
    )
    selected = st.selectbox(
        "Bloque a mostrar",
        ["Todas", "D1", "D2", "D3", "D4", "P17"],
        format_func=lambda x: (
            "Todas las preguntas P1–P17" if x == "Todas" else
            "P17 · Satisfacción general" if x == "P17" else
            f"{x} · {DIMENSIONS[x]['name']}"
        ),
        label_visibility="collapsed",
    )
    st.markdown(item_cards_html(selected), unsafe_allow_html=True)

    section_header(
        "Comparación visual",
        "No satisfechos | Satisfechos",
        "La barra representa exactamente la clasificación utilizada en el cálculo del indicador.",
    )
    st.markdown(binary_distribution_html(selected), unsafe_allow_html=True)

    with st.expander("Ver distribución original de respuestas 1–5"):
        st.caption("La alternativa 3 se conserva aquí porque forma parte de la escala Likert original. Para el indicador, 1–3 se agrupan como no satisfecho y 4–5 como satisfecho.")
        if selected == "Todas":
            dshow = ITEMS_SUM.copy()
        elif selected == "P17":
            dshow = ITEMS_SUM[ITEMS_SUM["Ítem"] == "P17"].copy()
        else:
            dshow = ITEMS_SUM[ITEMS_SUM["Dimensión"] == selected].copy()
        out = dshow[["Ítem", "Pregunta", "D", "Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5", "Satisfecho", "No satisfecho"]].copy()
        for c in ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5", "Satisfecho", "No satisfecho"]:
            out[c] = out[c].map(lambda x: f"{x*100:.1f}%")
        out = out.rename(columns={
            "D": "N válido",
            "Resp 1": "1 Totalmente en desacuerdo",
            "Resp 2": "2 En desacuerdo",
            "Resp 3": "3 Ni de acuerdo ni en desacuerdo",
            "Resp 4": "4 De acuerdo",
            "Resp 5": "5 Totalmente de acuerdo",
            "Satisfecho": "Satisfechos 4–5",
            "No satisfecho": "No satisfechos 1–3",
        })
        st.dataframe(out, use_container_width=True, hide_index=True, height=min(680, 52 + len(out) * 38))

with tab3:
    section_header("Base metodológica", "Reglas que sí pertenecen al instrumento")
    st.markdown(
        '''<div class="method-grid">
          <div class="panel method"><div class="method-t">1. Satisfacción general</div><div class="method-x"><b>P17</b> es la pregunta global. Se considera satisfecho al estudiante que responde <b>4 o 5</b>; se considera no satisfecho si responde <b>1, 2 o 3</b>.</div></div>
          <div class="panel method"><div class="method-t">2. Dimensiones D1–D4</div><div class="method-x">D1 = P1–P4, D2 = P5–P8, D3 = P9–P12 y D4 = P13–P16. Para cada estudiante se calcula el promedio de los cuatro ítems; si es <b>≥4</b>, entra al numerador de satisfechos de esa dimensión.</div></div>
          <div class="panel method"><div class="method-t">3. Fórmula porcentual</div><div class="method-x"><b>Porcentaje de satisfacción = (N/D) × 100</b>. N = estudiantes que cumplen el criterio de satisfacción. D = estudiantes con información válida para la medida calculada.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )

    section_header("Interpretación", "Qué significan 0–59%, 60–74%, 75–89% y 90–100%")
    st.markdown(scale_html(GLOBAL), unsafe_allow_html=True)
    st.markdown(
        '<div class="note"><b>Importante:</b> estos rangos son criterios de interpretación incluidos en la propuesta del instrumento. Sirven para poner un nivel al <b>porcentaje de satisfacción ya calculado</b>; no convierten las respuestas 1–5 en “insatisfactorio / regular / satisfactorio”. Tampoco son una prueba estadística derivada del Excel.</div>',
        unsafe_allow_html=True,
    )

    section_header("Control de la base", "Verificación del Excel antes de mostrar resultados")
    total_cells = N_ROWS * len(ITEMS)
    valid_cells = total_cells - missing_responses - invalid_responses
    valid_pct = valid_cells / total_cells if total_cells else float("nan")
    checks_ok = DERIVED_MISMATCHES == 0
    st.markdown(
        f'''<div class="audit-grid">
          <div class="panel audit"><div class="audit-k">Registros</div><div class="audit-v">{N_ROWS:,}</div><div class="audit-x">Filas analizadas en Base_Encuesta.</div></div>
          <div class="panel audit"><div class="audit-k">Respuestas P1–P17 válidas</div><div class="audit-v">{pct(valid_pct)}</div><div class="audit-x">{missing_responses:,} faltantes y {invalid_responses:,} valores fuera de 1–5.</div></div>
          <div class="panel audit"><div class="audit-k">Columnas calculadas del Excel</div><div class="audit-v">{'Coinciden' if checks_ok else 'Revisar'}</div><div class="audit-x">{DERIVED_CHECKED} campos derivados contrastados; {DERIVED_MISMATCHES:,} discrepancias frente al cálculo reconstruido.</div></div>
          <div class="panel audit"><div class="audit-k">Indicador global usado</div><div class="audit-v">P17</div><div class="audit-x">No se usa el promedio P1–P16 como sustituto del indicador global.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )

    section_header("Resumen verificable", "Resultados calculados directamente desde las respuestas")
    summary_rows = [[
        "P17 · Satisfacción general",
        f"{GLOBAL_N:,} / {GLOBAL_D:,}",
        pct(GLOBAL),
        pct(GLOBAL_NO),
        GLOBAL_LEVEL,
        "P17 = 4 o 5",
    ]]
    for _, r in DIMS.sort_values("Código").iterrows():
        summary_rows.append([
            f"{r['Código']} · {r['Dimensión']}",
            f"{int(r['N']):,} / {int(r['D']):,}",
            pct(float(r['Satisfacción'])),
            pct(float(r['No satisfecho'])),
            str(r['Nivel']),
            "Promedio individual de 4 ítems ≥4",
        ])
    summary = pd.DataFrame(summary_rows, columns=["Medida", "N / D", "% satisfechos", "% no satisfechos", "Nivel del porcentaje", "Regla"])
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.info("La validación de contenido y la confiabilidad del instrumento son análisis separados; no cambian la fórmula del indicador mostrada en este tablero.")
