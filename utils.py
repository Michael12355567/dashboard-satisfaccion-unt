from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def _find_file(filename):
    candidates = [DATA_DIR / filename, BASE_DIR / filename]
    for path in candidates:
        if path.exists():
            return path
    # Fallback: busca sin distinguir mayúsculas/minúsculas en raíz y data
    target = filename.lower()
    for folder in [DATA_DIR, BASE_DIR]:
        if folder.exists():
            for path in folder.iterdir():
                if path.is_file() and path.name.lower() == target:
                    return path
    st.error(f"No se encontró el archivo: {filename}. Súbelo al repositorio en la raíz o dentro de /data.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_data():
    nac = pd.read_excel(_find_file("CONVENIOS_NACIONALES_.xlsx"), sheet_name="Base_PowerBI")
    inte = pd.read_excel(_find_file("CONVENIOS_INTERNACIONALES.xlsx"), sheet_name="Convenios")
    mov = pd.read_excel(_find_file("MOVILIDAD_ACADEMICA.xlsx"), sheet_name="Movilidad")

    # Normalización de fechas
    nac["Fecha_Inicio"] = pd.to_datetime(nac["Fecha_Inicio"], errors="coerce")
    nac["Fecha_Término"] = pd.to_datetime(nac["Fecha_Término"], errors="coerce")
    inte["INICIO"] = pd.to_datetime(inte["INICIO"], errors="coerce")
    inte["VENCE"] = pd.to_datetime(inte["VENCE"], errors="coerce")

    # Normalización de texto de movilidad
    for c in ["MOVILIDAD", "PERÍODO", "MODALIDAD", "QUIÉN", "REGIÓN / PAÍS", "CARRERA PROFESIONAL", "GÉNERO"]:
        if c in mov.columns:
            mov[c] = mov[c].astype(str).str.strip()
    mov["TOTAL"] = pd.to_numeric(mov["TOTAL"], errors="coerce").fillna(0)
    mov["AÑO"] = pd.to_numeric(mov["AÑO"], errors="coerce").astype("Int64")

    # Unificación de convenios
    nac_u = pd.DataFrame({
        "Ámbito": "Nacional",
        "Institución": nac["Institución"],
        "País": "Perú",
        "Tipo": nac["Tipo_Convenio"],
        "Inicio": nac["Fecha_Inicio"],
        "Fin": nac["Fecha_Término"],
        "Año": pd.to_numeric(nac["Año_Registro"], errors="coerce").astype("Int64"),
        "Resolución": nac["N_Resolución"],
        "Responsable": nac["Coordinador_Responsable"],
    })
    int_u = pd.DataFrame({
        "Ámbito": "Internacional",
        "Institución": inte["INSTITUCIÓN"],
        "País": inte["PAÍS"].replace({"Méxcio": "México"}),
        "Tipo": inte["TIPO"],
        "Inicio": inte["INICIO"],
        "Fin": inte["VENCE"],
        "Año": pd.to_numeric(inte["AÑO"], errors="coerce").astype("Int64"),
        "Resolución": inte["RESOLUCIÓN"],
        "Responsable": np.nan,
    })
    conv = pd.concat([nac_u, int_u], ignore_index=True)

    hoy = pd.Timestamp.today().normalize()
    dias = (conv["Fin"] - hoy).dt.days
    conv["Estado"] = np.select(
        [conv["Fin"].isna(), dias < 0, (dias >= 0) & (dias <= 180), dias > 180],
        ["Sin fecha", "Vencido", "Próximo a vencer", "Vigente"],
        default="Sin fecha",
    )
    return nac, inte, mov, conv


def page_config(title):
    st.set_page_config(page_title=title, page_icon="📊", layout="wide", initial_sidebar_state="expanded")
    inject_css()


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {background: #F5F7FA;}
        [data-testid="stSidebar"] {background: linear-gradient(180deg,#5B1027,#7A1733);}
        [data-testid="stSidebar"] * {color: #FFFFFF !important;}
        .block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px;}
        .hero {background: linear-gradient(120deg,#64142D,#8A1C3E); color:white; padding:22px 26px; border-radius:18px; margin-bottom:18px; box-shadow:0 8px 24px rgba(31,41,55,.10)}
        .hero h1 {font-size:2rem; margin:0 0 5px 0;}
        .hero p {margin:0; opacity:.92; font-size:1rem;}
        div[data-testid="stMetric"] {background:white; border:1px solid #E5E7EB; padding:16px 18px; border-radius:16px; box-shadow:0 4px 16px rgba(31,41,55,.06)}
        div[data-testid="stMetricLabel"] {font-weight:700;}
        .insight {background:#FFFFFF; border-left:5px solid #7A1733; padding:14px 16px; border-radius:10px; margin:8px 0; box-shadow:0 3px 12px rgba(31,41,55,.05)}
        .section-title {font-size:1.2rem; font-weight:800; margin-top:8px; margin-bottom:6px; color:#374151;}
        .small-note {color:#6B7280; font-size:.88rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def fmt_int(x):
    try:
        return f"{int(round(float(x))):,}".replace(",", " ")
    except Exception:
        return "—"


def fmt_pct(x, digits=1):
    try:
        return f"{float(x):.{digits}f}%"
    except Exception:
        return "—"


def apply_plot_style(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", size=13),
        legend_title_text="",
        hoverlabel=dict(namelength=-1),
    )
    return fig


def sidebar_brand():
    st.sidebar.markdown("## 📊 Estadística UNT")
    st.sidebar.caption("Cooperación, convenios y movilidad académica")
    st.sidebar.markdown("---")


def download_csv(df, filename, label="Descargar CSV"):
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(label, csv, file_name=filename, mime="text/csv")
