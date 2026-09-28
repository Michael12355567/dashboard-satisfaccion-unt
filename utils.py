
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import unicodedata
from datetime import date

BASE_DIR = Path(__file__).resolve().parent

def _norm(s):
    s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip().lower().replace(" ", "").replace("_", "").replace("-", "")

def find_file(names):
    wanted = {_norm(x) for x in names}
    candidates = list((BASE_DIR / "data").glob("*.xlsx")) + list(BASE_DIR.glob("*.xlsx"))
    if not candidates:
        candidates = list(BASE_DIR.rglob("*.xlsx"))
    for p in candidates:
        if _norm(p.name) in wanted:
            return p
    # Fallback flexible
    for p in candidates:
        n = _norm(p.name)
        if any(w in n or n in w for w in wanted):
            return p
    raise FileNotFoundError(
        f"No se encontró el archivo requerido. Archivos Excel visibles: "
        f"{[str(x.relative_to(BASE_DIR)) for x in candidates]}"
    )

@st.cache_data(show_spinner=False)
def load_data():
    p_nac = find_file(["CONVENIOS_NACIONALES_.xlsx", "CONVENIOS NACIONALES.xlsx"])
    p_int = find_file(["CONVENIOS_INTERNACIONALES.xlsx", "CONVENIOS INTERNACIONALES VF.xlsx"])
    p_mov = find_file(["MOVILIDAD_ACADEMICA.xlsx", "MOVILIDAD ACADEMICA.xlsx"])

    nac = pd.read_excel(p_nac, sheet_name="Base_PowerBI")
    inte = pd.read_excel(p_int, sheet_name="Convenios")
    mov = pd.read_excel(p_mov, sheet_name="Movilidad")

    # National agreements: standard model
    nac2 = pd.DataFrame({
        "ID": nac.get("ID_Convenio"),
        "AÑO": pd.to_numeric(nac.get("Año_Registro"), errors="coerce"),
        "INSTITUCIÓN": nac.get("Institución").astype(str).str.strip(),
        "ÁMBITO": "Nacional",
        "PAÍS": "Perú",
        "TIPO": nac.get("Tipo_Convenio").astype(str).str.strip(),
        "INICIO": pd.to_datetime(nac.get("Fecha_Inicio"), errors="coerce"),
        "VENCE": pd.to_datetime(nac.get("Fecha_Término"), errors="coerce"),
        "RESOLUCIÓN": nac.get("N_Resolución").astype(str).str.strip(),
        "RESPONSABLE": nac.get("Coordinador_Responsable").astype(str).str.strip(),
    })

    # International agreements: standard model
    inte2 = pd.DataFrame({
        "ID": inte.get("N°"),
        "AÑO": pd.to_numeric(inte.get("AÑO"), errors="coerce"),
        "INSTITUCIÓN": inte.get("INSTITUCIÓN").astype(str).str.strip(),
        "ÁMBITO": "Internacional",
        "PAÍS": inte.get("PAÍS").astype(str).str.strip(),
        "TIPO": inte.get("TIPO").astype(str).str.strip(),
        "INICIO": pd.to_datetime(inte.get("INICIO"), errors="coerce"),
        "VENCE": pd.to_datetime(inte.get("VENCE"), errors="coerce"),
        "RESOLUCIÓN": inte.get("RESOLUCIÓN").astype(str).str.strip(),
        "RESPONSABLE": "",
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

    # Mobility cleanup
    mov = mov.copy()
    mov.columns = [str(c).strip() for c in mov.columns]
    mov["AÑO"] = pd.to_numeric(mov["AÑO"], errors="coerce").astype("Int64")
    mov["TOTAL"] = pd.to_numeric(mov["TOTAL"], errors="coerce").fillna(1)
    for c in ["MOVILIDAD","PERÍODO","MODALIDAD","QUIÉN","REGIÓN / PAÍS",
              "CARRERA PROFESIONAL","UNIVERSIDAD DE ORIGEN","SIGLAS ORIGEN",
              "UNIVERSIDAD DE DESTINO","SIGLAS DESTINO","GÉNERO"]:
        if c in mov.columns:
            mov[c] = mov[c].astype(str).str.strip()

    return conv, mov

def fmt_int(x):
    try:
        return f"{int(round(float(x))):,}".replace(",", " ")
    except Exception:
        return "0"

def fmt_pct(x, d=1):
    try:
        return f"{float(x):.{d}f}%"
    except Exception:
        return "0.0%"

def pct(n, d):
    return (100*n/d) if d else 0

def safe_unique(series):
    vals = pd.Series(series).dropna().astype(str)
    vals = vals[~vals.str.lower().isin(["nan","none",""])]
    return sorted(vals.unique().tolist())

def filter_mobility(df, years=None, modalidad=None, who=None, movement=None):
    out = df.copy()
    if years:
        out = out[out["AÑO"].isin(years)]
    if modalidad:
        out = out[out["MODALIDAD"].isin(modalidad)]
    if who:
        out = out[out["QUIÉN"].isin(who)]
    if movement:
        out = out[out["MOVILIDAD"].isin(movement)]
    return out

def filter_agreements(df, years=None, scope=None, status=None):
    out = df.copy()
    if years:
        out = out[out["AÑO"].isin(years)]
    if scope:
        out = out[out["ÁMBITO"].isin(scope)]
    if status:
        out = out[out["ESTADO"].isin(status)]
    return out
