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
        "accent": "#7064A5",
        "soft": "#F4F1FB",
    },
    "D3": {
        "name": "Servicios y gestión educativa",
        "items": ["P9", "P10", "P11", "P12"],
        "accent": "#AF744C",
        "soft": "#FFF4EA",
    },
    "D4": {
        "name": "Formación integral y desarrollo personal",
        "items": ["P13", "P14", "P15", "P16"],
        "accent": "#338373",
        "soft": "#EDF8F5",
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
  --ink:#17324D;--muted:#6B7F94;--blue:#245DB7;--blue2:#3674D3;
  --green:#27836F;--red:#BD5C68;--amber:#B57912;--cyan:#237E98;
  --line:rgba(214,225,237,.92);--glass:rgba(255,255,255,.74);
  --shadow:0 18px 45px rgba(32,72,122,.10),0 4px 12px rgba(32,72,122,.05);
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"Segoe UI Variable","Aptos","Segoe UI",Arial,sans-serif}
.stApp{color:var(--ink);background:radial-gradient(circle at 7% 2%,rgba(52,104,205,.13),transparent 31%),radial-gradient(circle at 94% 7%,rgba(33,166,183,.10),transparent 29%),linear-gradient(180deg,#F9FBFF 0%,#FFFFFF 48%,#F7FAFE 100%)}
header[data-testid="stHeader"]{background:rgba(250,252,255,.68);backdrop-filter:blur(20px)}
#MainMenu,footer{visibility:hidden}section[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}.block-container{max-width:1580px;padding:.65rem 1.25rem 3rem}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:13px 17px;border-radius:0 0 18px 18px;background:linear-gradient(110deg,rgba(17,57,115,.94),rgba(32,90,179,.88));color:#fff;border:1px solid rgba(255,255,255,.20);box-shadow:0 18px 40px rgba(24,67,143,.20);backdrop-filter:blur(22px)}
.brand{display:flex;gap:11px;align-items:center}.brand-mark{width:49px;height:49px;border-radius:13px;background:rgba(255,255,255,.92);color:#17427F;display:grid;place-items:center;font-weight:1000;letter-spacing:.05em}.brand-title{font-weight:950;font-size:1rem;line-height:1.1}.brand-sub{font-size:.72rem;opacity:.84;margin-top:3px}.top-meta{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.meta{padding:8px 10px;border-radius:10px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);font-size:.66rem}.meta b{display:block;font-size:.78rem;margin-top:2px}
.pagehead{padding:23px 4px 14px}.kicker,.section-kicker{font-size:.72rem;font-weight:950;letter-spacing:.14em;text-transform:uppercase;color:#3369CB}.title{font-size:clamp(2rem,3.4vw,2.8rem);font-weight:950;letter-spacing:-.045em;color:#122E4C;line-height:1.02;margin-top:4px}.sub{font-size:.94rem;line-height:1.62;color:#61768C;max-width:1210px;margin-top:8px}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}.chip{font-size:.71rem;font-weight:850;padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.66);border:1px solid rgba(255,255,255,.92);box-shadow:0 8px 20px rgba(31,72,132,.06)}
.stTabs [data-baseweb="tab-list"]{gap:7px;border-bottom:1px solid #DDE6F0;background:transparent;overflow-x:auto}.stTabs [data-baseweb="tab"]{height:50px;padding:0 15px;font-size:.90rem;font-weight:900;color:#64778D;border-radius:11px 11px 0 0}.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#2456B2,#3472D4)!important;color:#fff!important;box-shadow:0 8px 18px rgba(35,86,178,.16)!important}.stTabs [data-baseweb="tab-highlight"]{display:none}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:18px;margin:1.35rem 0 .70rem}.section-title{font-size:clamp(1.3rem,2.2vw,1.65rem);font-weight:950;letter-spacing:-.025em;color:#17324F;margin-top:3px}.section-note{font-size:.79rem;color:#78899B;line-height:1.48;text-align:right;max-width:720px}.panel{background:var(--glass);border:1px solid rgba(255,255,255,.92);box-shadow:var(--shadow);backdrop-filter:blur(24px) saturate(145%);border-radius:19px}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(325px,.5fr);gap:14px}.hero{padding:25px 27px;position:relative;overflow:hidden;border-left:7px solid #245DB7}.hero:after{content:"";position:absolute;width:330px;height:330px;border-radius:50%;right:-150px;top:-210px;background:radial-gradient(circle,rgba(47,102,200,.12),transparent 68%)}.hero>*{position:relative;z-index:1}.hero-eyebrow{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;font-weight:950;color:#3266C4}.hero-title{font-size:clamp(1.55rem,2.6vw,2.15rem);font-weight:950;line-height:1.13;margin-top:5px}.hero-desc{font-size:.88rem;line-height:1.6;color:#60758B;margin-top:8px;max-width:1040px}.hero-core{display:grid;grid-template-columns:230px minmax(0,1fr);gap:20px;align-items:center;margin-top:18px}.hero-score{font-size:clamp(4rem,7vw,6rem);font-weight:1000;color:#194F94;letter-spacing:-.07em;line-height:.9}.hero-level{font-size:.95rem;font-weight:950;margin-top:9px}.hero-level small{display:block;font-size:.69rem;font-weight:750;color:#73869A;margin-top:4px}.formula{padding:15px 16px;border-radius:15px;background:rgba(242,247,253,.85);border:1px solid #DCE7F2}.formula-k{font-size:.70rem;color:#6C8094;font-weight:900}.formula-eq{font-size:1rem;font-weight:950;margin-top:8px;color:#173B5D}.formula-result{display:inline-block;margin-left:5px;padding:5px 9px;border-radius:9px;background:#fff;border:1px solid #D7E3F0;color:#215DAF}.hero-foot{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:16px}.hero-foot>div{padding:11px 12px;border-radius:12px;background:rgba(247,250,253,.88);border:1px solid #E2EAF2}.hero-foot b{display:block;font-size:.68rem;color:#728297}.hero-foot span{display:block;font-size:.92rem;font-weight:950;color:#183752;margin-top:3px}
.side-stack{display:grid;grid-template-rows:1fr 1fr;gap:12px}.side{padding:18px 19px}.side-k{font-size:.67rem;text-transform:uppercase;letter-spacing:.10em;font-weight:950;color:#7B8B9E}.side-t{font-size:1.04rem;font-weight:950;margin-top:5px}.side-x{font-size:.78rem;line-height:1.56;color:#65798F;margin-top:9px}.side-big{font-size:2.5rem;font-weight:1000;letter-spacing:-.05em;margin-top:12px;color:#B45A66}
.explain{margin-top:12px;padding:14px 16px;border-radius:15px;background:rgba(244,248,253,.84);border:1px solid #DDE7F2;color:#526B84;font-size:.81rem;line-height:1.58}.explain b{color:#153B61}.explain .headline{font-size:.91rem;font-weight:950;color:#153B61;margin-bottom:4px}
.dim-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px}.dim{padding:17px 17px 15px;position:relative;overflow:hidden;border-top:4px solid var(--accent)}.dim-code{font-size:.72rem;font-weight:1000;color:var(--accent)}.dim-name{font-size:.84rem;font-weight:900;line-height:1.32;margin-top:4px;min-height:2.6em}.dim-score{font-size:2.18rem;font-weight:1000;letter-spacing:-.05em;margin-top:13px;color:#173651}.level-badge{display:inline-flex;margin-top:5px;padding:5px 8px;border-radius:9px;background:var(--soft);color:var(--accent);font-size:.68rem;font-weight:950}.dim-meta{font-size:.70rem;line-height:1.53;color:#667A90;margin-top:11px}.dim-meta b{color:#24435F}.dim-rule{margin-top:10px;padding-top:9px;border-top:1px dashed #DDE5EE;font-size:.66rem;color:#718397;line-height:1.45}
.insight-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.insight{padding:15px 16px;border-left:4px solid var(--accent)}.insight-k{font-size:.65rem;letter-spacing:.09em;text-transform:uppercase;color:#8190A2;font-weight:950}.insight-t{font-size:1rem;font-weight:950;margin-top:5px}.insight-x{font-size:.76rem;line-height:1.55;color:#677B91;margin-top:6px}
.item-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}.item{padding:15px;border-left:4px solid var(--accent);position:relative;overflow:hidden}.item-top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}.item-code{font-size:.68rem;font-weight:1000;color:var(--accent);padding:5px 7px;border-radius:8px;background:var(--soft)}.item-score{font-size:1.35rem;font-weight:1000;color:#173650}.item-q{font-size:.78rem;line-height:1.52;color:#5F7489;margin-top:9px;min-height:4.6em}.binary-pill{height:12px;border-radius:999px;background:#EDF2F6;overflow:hidden;display:flex;margin-top:11px}.seg13{height:100%;background:#A9B5C2}.seg45{height:100%;background:#328A74}.item-meta{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:9px}.item-meta>div{padding:8px;border-radius:10px;background:rgba(248,250,253,.88);border:1px solid #E5EBF1}.item-meta .k{font-size:.57rem;text-transform:uppercase;color:#8593A3;font-weight:900;line-height:1.25}.item-meta .v{font-size:.82rem;font-weight:1000;color:#2A455E;margin-top:3px}.item-note{font-size:.63rem;color:#8190A1;margin-top:8px;line-height:1.45}
.binary-panel{padding:14px 16px}.legend{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:9px;font-size:.69rem;color:#6F8194;font-weight:850}.legend span{display:flex;align-items:center;gap:6px}.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}.legend .a{background:#A9B5C2}.legend .b{background:#328A74}.bar-row{display:grid;grid-template-columns:48px minmax(0,1fr);gap:10px;align-items:center;padding:7px 0;border-top:1px solid rgba(228,235,242,.75)}.bar-row:first-of-type{border-top:0}.bar-code{font-size:.70rem;font-weight:1000;color:#4A627A}.bar{height:27px;border-radius:999px;overflow:hidden;display:flex;background:#EFF3F7;box-shadow:inset 0 2px 4px rgba(31,55,82,.07)}.bar>div{display:flex;align-items:center;justify-content:center;color:#fff;font-size:.58rem;font-weight:950;white-space:nowrap}.bar .a{background:linear-gradient(180deg,#B7C2CD,#98A6B4)}.bar .b{background:linear-gradient(180deg,#459D87,#2F826F)}
.scale{padding:15px 16px}.scale-title{font-size:.88rem;font-weight:950;color:#1B3B59}.scale-sub{font-size:.73rem;color:#718397;line-height:1.5;margin-top:4px}.scale-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:11px}.scale-step{padding:10px 8px;text-align:center;border-radius:12px;border:1px solid #E1E9F1;background:rgba(255,255,255,.64)}.scale-dot{width:11px;height:11px;border-radius:50%;margin:0 auto 5px;background:var(--lvl)}.scale-name{font-size:.72rem;font-weight:950}.scale-range{font-size:.65rem;color:#8190A2;margin-top:2px}
.method-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.method{padding:16px}.method-t{font-size:.94rem;font-weight:950}.method-x{font-size:.76rem;line-height:1.58;color:#687C91;margin-top:6px}.audit-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.audit{padding:14px}.audit-k{font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#8594A5;font-weight:950}.audit-v{font-size:1.35rem;font-weight:1000;margin-top:5px}.audit-x{font-size:.69rem;line-height:1.48;color:#6E8195;margin-top:4px}.note{padding:13px 15px;border-radius:14px;background:#FFF8E9;border:1px solid #EFDFB7;color:#715A24;font-size:.74rem;line-height:1.55;margin-top:10px}.info{padding:13px 15px;border-radius:14px;background:#F1F6FD;border:1px solid #DCE7F3;color:#4F6983;font-size:.74rem;line-height:1.55;margin-top:10px}
div[data-baseweb="select"]>div{background:rgba(255,255,255,.78)!important;border:1px solid #D8E3ED!important;border-radius:12px!important;min-height:44px!important}div[data-testid="stDataFrame"]{border:1px solid #E0E8F0;border-radius:14px;overflow:hidden}
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
    """Operacionaliza los rangos de interpretación escritos en el instrumento."""
    if pd.isna(value):
        return "Sin dato", "—", "#8492A2"
    if value < 0.60:
        return "Insatisfactorio", "0–59%", "#B85A67"
    if value < 0.75:
        return "Regular", "60–74%", "#B77A12"
    if value < 0.90:
        return "Satisfactorio", "75–89%", "#19866E"
    return "Muy satisfactorio", "90–100%", "#207C98"


def section_header(kicker: str, title: str, note: str = "") -> None:
    st.markdown(
        f'<div class="section-head"><div><div class="section-kicker">{escape(kicker)}</div>'
        f'<div class="section-title">{escape(title)}</div></div>'
        f'<div class="section-note">{escape(note)}</div></div>',
        unsafe_allow_html=True,
    )


# ==============================================================
# CARGA Y CÁLCULO DESDE EL EXCEL
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
missing_responses = int(df[ITEMS].isna().sum().sum())
invalid_mask = pd.DataFrame(False, index=df.index, columns=ITEMS)
for c in ITEMS:
    invalid_mask[c] = df[c].notna() & ~df[c].isin(VALID_VALUES)
invalid_responses = int(invalid_mask.sum().sum())

clean = df.copy()
for c in ITEMS:
    clean.loc[~clean[c].isin(VALID_VALUES), c] = pd.NA

# --- Satisfacción general: P17. Aquí el Word sí dice expresamente 4–5 = satisfecho y 1–3 = no satisfecho.
p17_valid = clean["P17"].notna()
p17_sat = clean.loc[p17_valid, "P17"].isin([4, 5])
GLOBAL_D = int(p17_valid.sum())
GLOBAL_N = int(p17_sat.sum())
GLOBAL = GLOBAL_N / GLOBAL_D if GLOBAL_D else float("nan")
GLOBAL_NO_N = GLOBAL_D - GLOBAL_N
GLOBAL_NO = GLOBAL_NO_N / GLOBAL_D if GLOBAL_D else float("nan")
GLOBAL_MEAN = float(clean.loc[p17_valid, "P17"].mean()) if GLOBAL_D else float("nan")
GLOBAL_LEVEL, GLOBAL_RANGE, GLOBAL_COLOR = level_for_percentage(GLOBAL)

# --- Dimensiones: promedio individual de los 4 ítems >= 4.
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
        "No alcanza": 1 - p if d else float("nan"),
        "Promedio": float(score.mean()) if d else float("nan"),
        "Nivel": level,
        "Rango": rng,
        "Color": color,
    })
DIMS = pd.DataFrame(dim_rows)

# --- Preguntas P1–P17: lectura descriptiva por respuesta.
# Para P1–P16 no inventamos una categoría "neutral" ni afirmamos que el Word defina 1–3 como "no satisfecho" por ítem.
# Mostramos simplemente qué porcentaje respondió 4–5 (cumple el criterio de satisfacción) y qué porcentaje respondió 1–3.
item_rows = []
for i in range(1, 18):
    item = f"P{i}"
    s = clean[item].dropna()
    d = int(len(s))
    n45 = int(s.isin([4, 5]).sum())
    n13 = d - n45
    code = f"D{((i - 1) // 4) + 1}" if i <= 16 else "GLOBAL"
    rec = {
        "Número": i,
        "Ítem": item,
        "Dimensión": code,
        "Pregunta": ITEM_TEXT[item],
        "N 4-5": n45,
        "N 1-3": n13,
        "D": d,
        "Resp 4-5": n45 / d if d else float("nan"),
        "Resp 1-3": n13 / d if d else float("nan"),
        "Promedio": float(s.mean()) if d else float("nan"),
    }
    for v in range(1, 6):
        rec[f"Resp {v}"] = float((s == v).mean()) if d else float("nan")
        rec[f"N Resp {v}"] = int((s == v).sum())
    item_rows.append(rec)
ITEMS_SUM = pd.DataFrame(item_rows)

# --- Auditoría de las columnas derivadas ya existentes en el Excel.
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

if "Fecha" in raw_df.columns:
    dt = pd.to_datetime(raw_df["Fecha"], errors="coerce")
    date_start, date_end = dt.min(), dt.max()
else:
    date_start = date_end = pd.NaT
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
          <div class="top-meta"><div class="meta">Periodo<b>{escape(period)}</b></div><div class="meta">Base analizada<b>{N_ROWS:,} registros</b></div><div class="meta">Fuente<b>Word + Excel</b></div></div>
        </div>
        <div class="pagehead"><div class="kicker">Encuesta de satisfacción · 2026</div><div class="title">Satisfacción con la formación académica integral</div>
        <div class="sub">El tablero sigue la lógica operativa del instrumento: <b>P17</b> representa la satisfacción general; allí el documento indica expresamente <b>4–5 = satisfecho</b> y <b>1–3 = no satisfecho</b>. En <b>D1–D4</b>, cada estudiante se clasifica según el <b>promedio de los cuatro ítems de la dimensión: promedio ≥4 = satisfecho</b>. En P1–P16 se muestran las respuestas 4–5 y 1–3 como lectura descriptiva, sin crear una categoría “neutral”.</div>
        <div class="chips"><span class="chip">Global = P17</span><span class="chip">D1–D4 = promedio individual ≥4</span><span class="chip">P1–P16 = análisis descriptivo por pregunta</span><span class="chip">Escala Likert original 1–5 conservada</span></div></div>''',
        unsafe_allow_html=True,
    )


def interpretation_scale_html() -> str:
    levels = [
        ("Insatisfactorio", "0–59%", "#B85A67"),
        ("Regular", "60–74%", "#B77A12"),
        ("Satisfactorio", "75–89%", "#19866E"),
        ("Muy satisfactorio", "90–100%", "#207C98"),
    ]
    blocks = ''.join(
        f'<div class="scale-step" style="--lvl:{c}"><div class="scale-dot"></div><div class="scale-name">{escape(name)}</div><div class="scale-range">{escape(interval)}</div></div>'
        for name, interval, c in levels
    )
    return (
        '<div class="panel scale"><div class="scale-title">Criterios de interpretación institucional del porcentaje</div>'
        '<div class="scale-sub">Estos rangos se aplican <b>después de calcular el porcentaje de satisfacción</b>. No son categorías de respuesta de la escala Likert y no equivalen a “favorable / neutral / desfavorable”.</div>'
        f'<div class="scale-grid">{blocks}</div></div>'
    )


def hero_html() -> str:
    return f'''<div class="hero-grid">
      <div class="panel hero">
        <div class="hero-eyebrow">Indicador principal · Satisfacción general · P17</div>
        <div class="hero-title">Porcentaje de estudiantes de pregrado satisfechos con su formación académica integral</div>
        <div class="hero-desc">Para P17, el documento define de forma explícita: <b>Satisfecho = respuesta 4 o 5</b>; <b>No satisfecho = respuesta 1, 2 o 3</b>.</div>
        <div class="hero-core"><div><div class="hero-score">{pct(GLOBAL)}</div><div class="hero-level" style="color:{GLOBAL_COLOR}">{escape(GLOBAL_LEVEL)}<small>Nivel del porcentaje según la escala del instrumento · {escape(GLOBAL_RANGE)}</small></div></div>
        <div class="formula"><div class="formula-k">Cálculo</div><div class="formula-eq">({GLOBAL_N:,} / {GLOBAL_D:,}) × 100 <span class="formula-result">= {pct(GLOBAL)}</span></div></div></div>
        <div class="explain"><div class="headline">Cómo se lee</div><b>{GLOBAL_N:,}</b> estudiantes respondieron 4 o 5 en P17 y son los que entran al numerador del indicador. Los <b>{GLOBAL_NO_N:,}</b> restantes respondieron 1, 2 o 3. El término <b>{escape(GLOBAL_LEVEL)}</b> clasifica el porcentaje obtenido ({pct(GLOBAL)}); no es una respuesta del cuestionario.</div>
        <div class="hero-foot"><div><b>Satisfechos · P17 = 4–5</b><span>{GLOBAL_N:,} · {pct(GLOBAL)}</span></div><div><b>No satisfechos · P17 = 1–3</b><span>{GLOBAL_NO_N:,} · {pct(GLOBAL_NO)}</span></div><div><b>Promedio P17 · descriptivo</b><span>{GLOBAL_MEAN:.2f}/5</span></div></div>
      </div>
      <div class="side-stack">
        <div class="panel side"><div class="side-k">Regla literal de P17</div><div class="side-t">Satisfecho / No satisfecho</div><div class="side-x"><b>4 o 5:</b> satisfecho.<br><b>1, 2 o 3:</b> no satisfecho.<br><br>Esta clasificación está escrita de forma explícita para la satisfacción general.</div></div>
        <div class="panel side"><div class="side-k">Evitar confusiones</div><div class="side-t">La respuesta 3 no se elimina</div><div class="side-x">La opción <b>3 = Ni de acuerdo ni en desacuerdo</b> se conserva en la distribución Likert 1–5. Para el cálculo de P17, el propio instrumento la incluye dentro de <b>No satisfecho</b>.</div></div>
      </div>
    </div>'''


def dimension_cards_html() -> str:
    cards = []
    for _, r in DIMS.sort_values("Código").iterrows():
        code = str(r["Código"])
        meta = DIMENSIONS[code]
        p = float(r["Satisfacción"])
        no = float(r["No alcanza"])
        cards.append(
            f'''<div class="panel dim" style="--accent:{meta['accent']};--soft:{meta['soft']}">
              <div class="dim-code">{escape(code)}</div><div class="dim-name">{escape(meta['name'])}</div>
              <div class="dim-score">{pct(p)}</div><div class="level-badge">{escape(str(r['Nivel']))}</div>
              <div class="dim-meta"><b>Satisfechos en la dimensión:</b> {int(r['N']):,} de {int(r['D']):,}<br><b>No alcanzan el criterio:</b> {pct(no)}<br><b>Promedio dimensional descriptivo:</b> {float(r['Promedio']):.2f}/5</div>
              <div class="dim-rule"><b>Regla del instrumento:</b> promedio individual de {', '.join(meta['items'])} ≥ 4. El porcentaje se calcula después de clasificar a cada estudiante.</div>
            </div>'''
        )
    return '<div class="dim-grid">' + ''.join(cards) + '</div>'


def executive_insights_html() -> str:
    high = DIMS.sort_values("Satisfacción", ascending=False).iloc[0]
    low = DIMS.sort_values("Satisfacción").iloc[0]
    p116 = ITEMS_SUM[ITEMS_SUM["Número"] <= 16]
    high_item = p116.sort_values("Resp 4-5", ascending=False).iloc[0]
    low_item = p116.sort_values("Resp 4-5").iloc[0]
    return f'''<div class="insight-grid">
      <div class="panel insight" style="--accent:#338373"><div class="insight-k">Mayor resultado dimensional</div><div class="insight-t">{escape(str(high['Código']))} · {pct(float(high['Satisfacción']))}</div><div class="insight-x">{escape(str(high['Dimensión']))}. El valor representa estudiantes cuyo promedio individual de la dimensión es ≥4.</div></div>
      <div class="panel insight" style="--accent:#AF744C"><div class="insight-k">Menor resultado dimensional</div><div class="insight-t">{escape(str(low['Código']))} · {pct(float(low['Satisfacción']))}</div><div class="insight-x">{escape(str(low['Dimensión']))}. Se interpreta con la misma regla de promedio individual ≥4.</div></div>
      <div class="panel insight" style="--accent:#2F6FA3"><div class="insight-k">Lectura por pregunta P1–P16</div><div class="insight-t">{escape(str(low_item['Ítem']))} {pct(float(low_item['Resp 4-5']))} ↔ {escape(str(high_item['Ítem']))} {pct(float(high_item['Resp 4-5']))}</div><div class="insight-x">Aquí se compara únicamente el porcentaje de <b>respuestas 4–5</b> por ítem. No se aplica la clasificación institucional de niveles a cada pregunta.</div></div>
    </div>'''


def filter_items(selected: str) -> pd.DataFrame:
    if selected == "Todas":
        return ITEMS_SUM.copy()
    if selected == "P17":
        return ITEMS_SUM[ITEMS_SUM["Ítem"] == "P17"].copy()
    return ITEMS_SUM[ITEMS_SUM["Dimensión"] == selected].copy()


def item_cards_html(selected: str) -> str:
    d = filter_items(selected)
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
        p45 = float(r["Resp 4-5"])
        p13 = float(r["Resp 1-3"])
        is_p17 = str(r["Ítem"]) == "P17"
        k45 = "Satisfechos · 4–5" if is_p17 else "Respuestas 4–5 · cumplen criterio"
        k13 = "No satisfechos · 1–3" if is_p17 else "Respuestas 1–3 · fuera del criterio"
        note = (
            "P17 sí tiene clasificación explícita Satisfecho / No satisfecho en el instrumento."
            if is_p17
            else "Lectura descriptiva del ítem. El resultado oficial de la dimensión se calcula con el promedio individual de sus cuatro preguntas."
        )
        cards.append(
            f'''<div class="panel item" style="--accent:{accent};--soft:{soft}">
              <div class="item-top"><div class="item-code">{escape(str(r['Ítem']))} · {escape(label)}</div><div class="item-score">{pct(p45)}</div></div>
              <div class="item-q">{escape(str(r['Pregunta']))}</div>
              <div class="binary-pill"><div class="seg13" style="width:{p13*100:.4f}%"></div><div class="seg45" style="width:{p45*100:.4f}%"></div></div>
              <div class="item-meta"><div><div class="k">{escape(k45)}</div><div class="v">{pct(p45)} · {int(r['N 4-5']):,}</div></div><div><div class="k">{escape(k13)}</div><div class="v">{pct(p13)} · {int(r['N 1-3']):,}</div></div></div>
              <div class="item-note">{escape(note)} Base válida: {int(r['D']):,}. Promedio descriptivo: {float(r['Promedio']):.2f}/5.</div>
            </div>'''
        )
    return '<div class="item-grid">' + ''.join(cards) + '</div>'


def grouped_distribution_html(selected: str) -> str:
    d = filter_items(selected)
    rows = []
    for _, r in d.sort_values("Número").iterrows():
        p13 = float(r["Resp 1-3"])
        p45 = float(r["Resp 4-5"])
        rows.append(
            f'<div class="bar-row"><div class="bar-code">{escape(str(r["Ítem"]))}</div><div class="bar">'
            f'<div class="a" style="width:{p13*100:.4f}%">{pct(p13,0) if p13 >= .07 else ""}</div>'
            f'<div class="b" style="width:{p45*100:.4f}%">{pct(p45,0) if p45 >= .07 else ""}</div>'
            f'</div></div>'
        )
    return '<div class="panel binary-panel"><div class="legend"><span><i class="a"></i>Respuestas 1–3</span><span><i class="b"></i>Respuestas 4–5 · criterio de satisfacción</span></div>' + ''.join(rows) + '</div>'


def methodology_cards_html() -> str:
    return '''<div class="method-grid">
      <div class="panel method"><div class="method-t">1. Escala de respuesta</div><div class="method-x">Likert de 5 puntos: <b>1 Totalmente en desacuerdo</b>, <b>2 En desacuerdo</b>, <b>3 Ni de acuerdo ni en desacuerdo</b>, <b>4 De acuerdo</b> y <b>5 Totalmente de acuerdo</b>.</div></div>
      <div class="panel method"><div class="method-t">2. Criterio de satisfacción</div><div class="method-x">El instrumento señala que se considera satisfecho al estudiante que marque <b>4 o 5</b>. Para la satisfacción general P17, además especifica: <b>1, 2 o 3 = No satisfecho</b>.</div></div>
      <div class="panel method"><div class="method-t">3. Dimensiones</div><div class="method-x"><b>D1 = P1–P4</b>, <b>D2 = P5–P8</b>, <b>D3 = P9–P12</b> y <b>D4 = P13–P16</b>. Un estudiante es satisfecho en la dimensión si su <b>promedio individual ≥4</b>.</div></div>
      <div class="panel method"><div class="method-t">4. Satisfacción general</div><div class="method-x"><b>P17</b> es la pregunta de satisfacción general. El porcentaje global se obtiene con estudiantes que responden 4 o 5 sobre el total de respuestas válidas.</div></div>
      <div class="panel method"><div class="method-t">5. Fórmula del porcentaje</div><div class="method-x"><b>Porcentaje de satisfacción = (N de estudiantes satisfechos / total de estudiantes evaluados válidos) × 100.</b></div></div>
      <div class="panel method"><div class="method-t">6. Ficha técnica</div><div class="method-x">Instrumento: <b>Encuesta de satisfacción sobre la formación académica integral</b>. Tipo: cuestionario estructurado. Población objetivo: estudiantes de pregrado de la UNT. Unidad de análisis: estudiante. Aplicación: autoadministrada y anónima.</div></div>
    </div>'''


# ==============================================================
# APP
# ==============================================================
top_header()

tab1, tab2, tab3, tab4 = st.tabs(["◉ Resumen", "▦ Dimensiones", "☷ Preguntas P1–P17", "ⓘ Metodología y control"])

with tab1:
    section_header(
        "Indicador principal",
        "Satisfacción general · P17",
        "El indicador global se calcula con P17; no se sustituye por el promedio P1–P16.",
    )
    st.markdown(hero_html(), unsafe_allow_html=True)

    section_header(
        "Resultados por dimensión",
        "Resumen D1–D4",
        "Cada porcentaje dimensional se obtiene clasificando primero a cada estudiante según su promedio de cuatro ítems ≥4.",
    )
    st.markdown(dimension_cards_html(), unsafe_allow_html=True)

    section_header("Lectura ejecutiva", "Resultados que conviene observar")
    st.markdown(executive_insights_html(), unsafe_allow_html=True)

with tab2:
    section_header(
        "Cálculo dimensional",
        "D1–D4: promedio individual ≥4",
        "No se promedian porcentajes de preguntas. Se promedian respuestas por estudiante dentro de cada dimensión.",
    )
    st.markdown(dimension_cards_html(), unsafe_allow_html=True)
    st.markdown('<div class="info"><b>Importante:</b> la clasificación “Insatisfactorio / Regular / Satisfactorio / Muy satisfactorio” corresponde al <b>porcentaje final de satisfacción</b> de cada dimensión; no corresponde a las opciones 1–5 del cuestionario.</div>', unsafe_allow_html=True)

with tab3:
    section_header(
        "Análisis por pregunta",
        "P1–P17 sin inventar categorías",
        "P1–P16 se presentan descriptivamente como respuestas 4–5 y respuestas 1–3. Solo P17 usa de forma explícita la etiqueta Satisfecho / No satisfecho del documento.",
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
        "Comparación agrupada",
        "Respuestas 1–3 | Respuestas 4–5",
        "Esta agrupación sirve para visualizar el criterio 4–5. No crea una categoría 'neutral'.",
    )
    st.markdown(grouped_distribution_html(selected), unsafe_allow_html=True)

    with st.expander("Ver distribución original Likert 1–5"):
        st.caption("Aquí se conserva exactamente la escala original del instrumento. La respuesta 3 mantiene su nombre: 'Ni de acuerdo ni en desacuerdo'.")
        dshow = filter_items(selected)
        out = dshow[["Ítem", "Pregunta", "D", "Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5", "Resp 4-5", "Resp 1-3"]].copy()
        for c in ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5", "Resp 4-5", "Resp 1-3"]:
            out[c] = out[c].map(lambda x: f"{x*100:.1f}%")
        out = out.rename(columns={
            "D": "N válido",
            "Resp 1": "1 Totalmente en desacuerdo",
            "Resp 2": "2 En desacuerdo",
            "Resp 3": "3 Ni de acuerdo ni en desacuerdo",
            "Resp 4": "4 De acuerdo",
            "Resp 5": "5 Totalmente de acuerdo",
            "Resp 4-5": "Respuestas 4–5",
            "Resp 1-3": "Respuestas 1–3",
        })
        st.dataframe(out, use_container_width=True, hide_index=True, height=min(680, 52 + len(out) * 38))

with tab4:
    section_header("Base metodológica", "Reglas tomadas del instrumento")
    st.markdown(methodology_cards_html(), unsafe_allow_html=True)

    section_header(
        "Interpretación institucional",
        "Niveles aplicados al porcentaje ya calculado",
        "Estos rangos pertenecen al documento. No se usan para recodificar las respuestas 1–5.",
    )
    st.markdown(interpretation_scale_html(), unsafe_allow_html=True)
    st.markdown(
        f'<div class="note"><b>Ejemplo con P17:</b> el porcentaje calculado es <b>{pct(GLOBAL)}</b>. Como está dentro del intervalo 60–74%, el nivel del porcentaje es <b>{escape(GLOBAL_LEVEL)}</b>. Esto no significa que exista una respuesta “Regular” en la encuesta.</div>',
        unsafe_allow_html=True,
    )

    section_header("Estructura de datos", "Cómo se relaciona el Word con tu Excel")
    st.markdown(
        '''<div class="method-grid">
          <div class="panel method"><div class="method-t">Ítems originales</div><div class="method-x"><b>P1 a P17</b> son las respuestas de la escala 1–5 y constituyen la base para todos los cálculos.</div></div>
          <div class="panel method"><div class="method-t">Variables calculadas</div><div class="method-x"><b>D1_Promedio, D2_Promedio, D3_Promedio y D4_Promedio</b> representan el promedio de los cuatro ítems de cada dimensión.</div></div>
          <div class="panel method"><div class="method-t">Variables dicotómicas</div><div class="method-x"><b>D1_Satisfecho a D4_Satisfecho</b> codifican 1 si el promedio de la dimensión es ≥4 y 0 en caso contrario. <b>Global_Satisfecho</b> se obtiene de P17.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )

    section_header("Control del Excel", "Comprobación automática antes de mostrar resultados")
    total_cells = N_ROWS * len(ITEMS)
    valid_cells = total_cells - missing_responses - invalid_responses
    valid_pct = valid_cells / total_cells if total_cells else float("nan")
    checks_ok = DERIVED_MISMATCHES == 0
    st.markdown(
        f'''<div class="audit-grid">
          <div class="panel audit"><div class="audit-k">Registros</div><div class="audit-v">{N_ROWS:,}</div><div class="audit-x">Filas analizadas en la hoja {escape(SHEET_NAME)}.</div></div>
          <div class="panel audit"><div class="audit-k">Respuestas válidas P1–P17</div><div class="audit-v">{pct(valid_pct)}</div><div class="audit-x">{missing_responses:,} faltantes y {invalid_responses:,} valores fuera de 1–5.</div></div>
          <div class="panel audit"><div class="audit-k">Columnas derivadas</div><div class="audit-v">{'Coinciden' if checks_ok else 'Revisar'}</div><div class="audit-x">{DERIVED_CHECKED} columnas del Excel contrastadas; {DERIVED_MISMATCHES:,} discrepancias.</div></div>
          <div class="panel audit"><div class="audit-k">Indicador global</div><div class="audit-v">P17</div><div class="audit-x">El promedio P1–P16 no se utiliza como sustituto del indicador global.</div></div>
        </div>''',
        unsafe_allow_html=True,
    )

    section_header("Resumen verificable", "Resultados obtenidos con las reglas del instrumento")
    summary_rows = [[
        "P17 · Satisfacción general",
        f"{GLOBAL_N:,} / {GLOBAL_D:,}",
        pct(GLOBAL),
        GLOBAL_LEVEL,
        "P17 = 4 o 5",
    ]]
    for _, r in DIMS.sort_values("Código").iterrows():
        summary_rows.append([
            f"{r['Código']} · {r['Dimensión']}",
            f"{int(r['N']):,} / {int(r['D']):,}",
            pct(float(r['Satisfacción'])),
            str(r['Nivel']),
            "Promedio individual de 4 ítems ≥4",
        ])
    summary = pd.DataFrame(summary_rows, columns=["Medida", "N / D", "% satisfacción", "Nivel del porcentaje", "Regla"])
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.markdown('<div class="info"><b>Validación y confiabilidad:</b> el Word plantea como pasos posteriores la V de Aiken y el Alfa de Cronbach. Esos análisis evalúan el instrumento y no cambian la regla de cálculo del porcentaje de satisfacción mostrada en este tablero.</div>', unsafe_allow_html=True)
