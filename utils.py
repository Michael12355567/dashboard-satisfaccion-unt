
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import unicodedata, re
from datetime import date

BASE_DIR = Path(__file__).resolve().parent

def norm(s):
    s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.upper().strip()
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return " ".join(s.split())

def _file(name):
    p = BASE_DIR / "data" / name
    if not p.exists():
        raise FileNotFoundError(f"No se encontró {name} dentro de data/")
    return p

@st.cache_data(show_spinner=False)
def load_data():
    nac = pd.read_excel(_file("CONVENIOS_NACIONALES_.xlsx"), sheet_name="Base_PowerBI")
    inte = pd.read_excel(_file("CONVENIOS_INTERNACIONALES.xlsx"), sheet_name="Convenios")
    mov = pd.read_excel(_file("MOVILIDAD_ACADEMICA.xlsx"), sheet_name="Movilidad")
    mat = pd.read_csv(_file("MATRICULADOS_PERIODO1_AGREGADO.csv"))

    nac2 = pd.DataFrame({
        "ID": nac.get("ID_Convenio"),
        "AÑO": pd.to_numeric(nac.get("Año_Registro"), errors="coerce"),
        "INSTITUCIÓN": nac.get("Institución").astype(str).str.strip(),
        "ÁMBITO": "Nacional",
        "PAÍS": "Perú",
        "TIPO": nac.get("Tipo_Convenio").astype(str).str.strip(),
        "INICIO": pd.to_datetime(nac.get("Fecha_Inicio"), errors="coerce"),
        "VENCE": pd.to_datetime(nac.get("Fecha_Término"), errors="coerce"),
        "RESOLUCIÓN": nac.get("N_Resolución").astype(str).str.strip()
    })

    inte2 = pd.DataFrame({
        "ID": inte.get("N°"),
        "AÑO": pd.to_numeric(inte.get("AÑO"), errors="coerce"),
        "INSTITUCIÓN": inte.get("INSTITUCIÓN").astype(str).str.strip(),
        "ÁMBITO": "Internacional",
        "PAÍS": inte.get("PAÍS").astype(str).str.strip(),
        "TIPO": inte.get("TIPO").astype(str).str.strip(),
        "INICIO": pd.to_datetime(inte.get("INICIO"), errors="coerce"),
        "VENCE": pd.to_datetime(inte.get("VENCE"), errors="coerce"),
        "RESOLUCIÓN": inte.get("RESOLUCIÓN").astype(str).str.strip()
    })

    conv = pd.concat([nac2, inte2], ignore_index=True)
    conv["AÑO"] = conv["AÑO"].astype("Int64")
    today = pd.Timestamp(date.today())
    conv["ESTADO"] = np.select(
        [
            conv["VENCE"].isna(),
            conv["VENCE"] < today,
            (conv["VENCE"] >= today) & (conv["VENCE"] <= today + pd.Timedelta(days=365))
        ],
        ["Sin fecha", "Vencido", "Vence ≤ 12 meses"],
        default="Vigente"
    )

    mov.columns = [str(c).strip() for c in mov.columns]
    mov["AÑO"] = pd.to_numeric(mov["AÑO"], errors="coerce").astype("Int64")
    mov["TOTAL"] = pd.to_numeric(mov["TOTAL"], errors="coerce").fillna(1)
    for c in ["MOVILIDAD","PERÍODO","MODALIDAD","QUIÉN","REGIÓN / PAÍS",
              "CARRERA PROFESIONAL","UNIVERSIDAD DE ORIGEN","UNIVERSIDAD DE DESTINO","GÉNERO"]:
        if c in mov.columns:
            mov[c] = mov[c].astype(str).str.strip()

    mat["AÑO"] = pd.to_numeric(mat["AÑO"], errors="coerce").astype("Int64")
    mat["MATRICULADOS"] = pd.to_numeric(mat["MATRICULADOS"], errors="coerce").fillna(0)
    for c in ["SEDE","FACULTAD","CARRERA","SEXO"]:
        mat[c] = mat[c].astype(str).str.strip()

    # Mapping career -> faculty using matriculation data
    map_fac = (mat.groupby("CARRERA")["FACULTAD"]
               .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else "")
               .to_dict())

    # Canonical aliases for mobility career labels
    aliases = {
        "ARQUITECTURA":"ARQUITECTURA Y URBANISMO",
        "C BIOLOGICAS":"CIENCIAS BIOLÓGICAS",
        "CIENCIAS POLITICAS":"CIENCIA POLÍTICA Y GOBERNABILIDAD",
        "CONTABILIDAD":"CONTABILIDAD Y FINANZAS",
        "INFORMATICA":"INGENIERÍA INFORMÁTICA",
        "ING AMBIENTAL":"INGENIERÍA AMBIENTAL",
        "ING INDUSTRIAL":"INGENIERÍA INDUSTRIAL",
        "ING QUIMICA":"INGENIERÍA QUÍMICA",
        "DERECHO":"DERECHO Y CIENCIAS POLÍTICAS",
        "ING AGROINDUSTRIAL":"INGENIERÍA AGROINDUSTRIAL",
        "ING CIVIL":"INGENIERÍA CIVIL",
        "MICROBIOLOGIA":"MICROBIOLOGÍA Y PARASITOLOGÍA",
        "ING MECATRONICA":"INGENIERÍA MECATRÓNICA",
        "C COMUNICACION":"CIENCIAS DE LA COMUNICACIÓN",
        "ING AGRICOLA":"INGENIERÍA AGRÍCOLA",
        "ING MINAS":"INGENIERÍA DE MINAS",
        "C MATEMATICAS":"MATEMÁTICA",
        "C PSICOLOGICAS":"EDUCACIÓN SECUNDARIA CON MENCIÓN EN FILOSOFÍA - PSICOLOGÍA Y CIENCIAS SOCIALES",
        "IDIOMAS":"EDUCACIÓN SECUNDARIA - MENCIÓN EN IDIOMAS - INGLÉS FRANCÉS O INGLÉS ALEMÁN",
        "ING MECANICA":"INGENIERÍA MECÁNICA",
        "ING SISTEMAS":"INGENIERÍA DE SISTEMAS",
        "PESQUERA":"PESQUERÍA",
        "ING INFORMATICA":"INGENIERÍA INFORMÁTICA",
        "ESTADISTICA":"INGENIERÍA ESTADÍSTICA",
        "LENGUA Y LITERATURA":"EDUCACIÓN SECUNDARIA - MENCIÓN LENGUA Y LITERATURA",
        "C SOCIALES":"EDUCACIÓN SECUNDARIA CON MENCIÓN EN FILOSOFÍA - PSICOLOGÍA Y CIENCIAS SOCIALES",
        "ING CIVIL":"INGENIERÍA CIVIL"
    }

    canonical_by_norm = {norm(c): c for c in mat["CARRERA"].dropna().unique()}
    aliases = {norm(k): v for k,v in aliases.items()}

    def canon(c):
        n = norm(c)
        if n in canonical_by_norm:
            return canonical_by_norm[n]
        if n in aliases:
            return aliases[n]
        if n in {"EDUCACION SECUNDARIA","EDU SECUNDARIA"}:
            return "EDUCACIÓN SECUNDARIA (TODAS)"
        return c

    mov["CARRERA_CANON"] = mov["CARRERA PROFESIONAL"].apply(canon)

    sec_fac = "EDUCACION Y CIENCIAS DE LA COMUNICACION"
    def fac_from_canon(c):
        if c == "EDUCACIÓN SECUNDARIA (TODAS)":
            return sec_fac
        return map_fac.get(c, "")
    mov["FACULTAD"] = mov["CARRERA_CANON"].apply(fac_from_canon)

    return conv, mov, mat

def fmt_int(x):
    try: return f"{int(round(float(x))):,}".replace(",", " ")
    except: return "0"

def fmt_pct(x, d=1):
    try: return f"{float(x):.{d}f}%"
    except: return "0.0%"

def pct(n,d):
    return 100*n/d if d else 0

def safe_values(s):
    vals = pd.Series(s).dropna().astype(str)
    vals = vals[~vals.str.lower().isin(["nan","none",""])]
    return sorted(vals.unique().tolist())

def mat_for_filter(mat, years=None, sede=None, facultad=None, carrera=None):
    d = mat.copy()
    if years: d = d[d["AÑO"].isin(years)]
    if sede and sede != "Todas": d = d[d["SEDE"] == sede]
    if facultad and facultad != "Todas": d = d[d["FACULTAD"] == facultad]
    if carrera and carrera != "Todas":
        if carrera == "EDUCACIÓN SECUNDARIA (TODAS)":
            d = d[d["CARRERA"].str.upper().str.startswith("EDUCACIÓN SECUNDARIA")]
        else:
            d = d[d["CARRERA"] == carrera]
    return d
