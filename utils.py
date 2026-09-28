
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import unicodedata, re
from datetime import date

BASE_DIR = Path(__file__).resolve().parent

def _norm(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+","",s.lower())

def _find_file(names):
    wanted = {_norm(n) for n in names}
    candidates = [p for p in BASE_DIR.rglob("*") if p.is_file()]
    for p in candidates:
        if _norm(p.name) in wanted:
            return p
    for p in candidates:
        pn = _norm(p.name)
        if any(w in pn or pn in w for w in wanted):
            return p
    available = [str(p.relative_to(BASE_DIR)) for p in candidates if p.suffix.lower() in [".xlsx",".xls",".csv"]]
    raise FileNotFoundError(f"No se encontró el archivo requerido. Archivos visibles: {available}")

def _read_excel(path, preferred):
    xls = pd.ExcelFile(path)
    for sh in preferred:
        if sh in xls.sheet_names:
            return pd.read_excel(path, sheet_name=sh)
    norm_map = {_norm(s):s for s in xls.sheet_names}
    for sh in preferred:
        if _norm(sh) in norm_map:
            return pd.read_excel(path, sheet_name=norm_map[_norm(sh)])
    return pd.read_excel(path, sheet_name=xls.sheet_names[0])

@st.cache_data(show_spinner=False)
def load_data():
    p_nac = _find_file(["CONVENIOS_NACIONALES_.xlsx","CONVENIOS NACIONALES.xlsx"])
    p_int = _find_file(["CONVENIOS_INTERNACIONALES.xlsx","CONVENIOS INTERNACIONALES VF.xlsx"])
    p_mov = _find_file(["MOVILIDAD_ACADEMICA.xlsx","MOVILIDAD ACADEMICA.xlsx"])
    p_mat = _find_file(["MATRICULADOS_PERIODO1_AGREGADO.csv","matriculados_periodo1_agg.csv"])

    nac = _read_excel(p_nac, ["Base_PowerBI"])
    inte = _read_excel(p_int, ["Convenios","Base_PowerBI"])
    mov = _read_excel(p_mov, ["Movilidad","Base_PowerBI"])
    mat = pd.read_csv(p_mat)

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
        [conv["VENCE"].isna(), conv["VENCE"] < today,
         (conv["VENCE"] >= today) & (conv["VENCE"] <= today + pd.Timedelta(days=365))],
        ["Sin fecha","Vencido","Vence ≤ 12 meses"], default="Vigente"
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
        if c in mat.columns:
            mat[c] = mat[c].astype(str).str.strip()

    map_fac = (mat.groupby("CARRERA")["FACULTAD"]
               .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else "")
               .to_dict())

    def nt(s):
        s = unicodedata.normalize("NFKD", str(s))
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = re.sub(r"[^A-Z0-9]+"," ",s.upper()).strip()
        return " ".join(s.split())

    aliases = {
        "ARQUITECTURA":"ARQUITECTURA Y URBANISMO",
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
        "ING AGRICOLA":"INGENIERÍA AGRÍCOLA",
        "ING MINAS":"INGENIERÍA DE MINAS",
        "ING MECANICA":"INGENIERÍA MECÁNICA",
        "ING SISTEMAS":"INGENIERÍA DE SISTEMAS",
        "PESQUERA":"PESQUERÍA",
        "ESTADISTICA":"INGENIERÍA ESTADÍSTICA",
    }
    canonical = {nt(c):c for c in mat["CARRERA"].dropna().unique()}
    alias_norm = {nt(k):v for k,v in aliases.items()}

    def canon(c):
        n = nt(c)
        if n in canonical: return canonical[n]
        if n in alias_norm: return alias_norm[n]
        if n in {"EDUCACION SECUNDARIA","EDU SECUNDARIA"}:
            return "EDUCACIÓN SECUNDARIA (TODAS)"
        return str(c).strip()

    mov["CARRERA_CANON"] = mov["CARRERA PROFESIONAL"].apply(canon)
    mov["FACULTAD"] = mov["CARRERA_CANON"].apply(
        lambda c: "EDUCACION Y CIENCIAS DE LA COMUNICACION"
        if c=="EDUCACIÓN SECUNDARIA (TODAS)" else map_fac.get(c,"")
    )

    return conv, mov, mat

def fmt_int(x):
    try: return f"{int(round(float(x))):,}".replace(","," ")
    except: return "0"

def fmt_pct(x,d=1):
    try: return f"{float(x):.{d}f}%"
    except: return "0.0%"

def pct(n,d):
    return 100*n/d if d else 0

def safe_values(s):
    vals = pd.Series(s).dropna().astype(str)
    vals = vals[~vals.str.lower().isin(["nan","none",""])]
    return sorted(vals.unique().tolist())
