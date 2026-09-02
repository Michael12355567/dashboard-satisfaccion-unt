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

# Paleta moderna (puedes cambiarla luego)
COLORS_DIM = {
    "D1": "#4F46E5",  # índigo
    "D2": "#06B6D4",  # cyan
    "D3": "#F59E0B",  # ámbar
    "D4": "#10B981",  # esmeralda
}

COLORS_LEVEL = {
    "Insatisfactorio": "#EF4444",
    "Regular": "#F59E0B",
    "Satisfactorio": "#10B981",
    "Muy satisfactorio": "#0F766E",
    "Sin dato": "#94A3B8",
}

LIKERT_COLORS = {
    "Desfavorable (1–2)": "#F87171",
    "Neutral (3)": "#94A3B8",
    "Favorable (4–5)": "#34D399",
}

st.markdown(
    """
    <style>
    .stApp {
        background:
          radial-gradient(circle at 8% 5%, rgba(79,70,229,.10), transparent 25%),
          radial-gradient(circle at 92% 15%, rgba(6,182,212,.09), transparent 24%),
          linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 55%, #ECFDF5 100%);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    h1, h2, h3 { color: #0F172A; }
    .subtitle {
        color: #64748B;
        margin-top: -8px;
        margin-bottom: 18px;
        font-size: 0.98rem;
    }
    .glass-card {
        background: rgba(255,255,255,.78);
        border: 1px solid rgba(148,163,184,.22);
        border-radius: 18px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 10px 28px rgba(15,23,42,.07);
        min-height: 132px;
    }
    .glass-card .kpi-code {
        font-size: .82rem;
        letter-spacing: .08em;
        font-weight: 800;
        color: #64748B;
        text-transform: uppercase;
    }
    .glass-card .kpi-value {
        font-size: 2rem;
        line-height: 1.05;
        font-weight: 800;
        color: #0F172A;
        margin: 6px 0 5px 0;
    }
    .glass-card .kpi-label {
        font-size: .86rem;
        color: #475569;
        line-height: 1.35;
    }
    .finding {
        background: rgba(255,255,255,.80);
        border: 1px solid rgba(148,163,184,.20);
        border-left: 5px solid #4F46E5;
        border-radius: 14px;
        padding: 14px 15px;
        margin-bottom: 10px;
        box-shadow: 0 7px 20px rgba(15,23,42,.05);
    }
    .finding.alert { border-left-color: #EF4444; }
    .finding.good { border-left-color: #10B981; }
    .method-card {
        background: rgba(255,255,255,.80);
        border: 1px solid rgba(148,163,184,.20);
        border-radius: 16px;
        padding: 18px;
        min-height: 205px;
        box-shadow: 0 8px 22px rgba(15,23,42,.05);
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.78);
        border: 1px solid rgba(148,163,184,.20);
        padding: 14px 16px;
        border-radius: 16px;
        box-shadow: 0 8px 22px rgba(15,23,42,.05);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #172554 100%);
    }
    section[data-testid="stSidebar"] * { color: #F8FAFC; }
    section[data-testid="stSidebar"] .stFileUploaderDropzone * { color: #0F172A; }
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


def pct(p: float) -> str:
    return "—" if pd.isna(p) else f"{p * 100:.2f}%"


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required = [f"P{i}" for i in range(1, 18)]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "Faltan columnas obligatorias en el Excel: " + ", ".join(missing)
        )

    # Convertimos las respuestas a número para evitar problemas si Excel las trae como texto.
    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Recalculamos siempre los indicadores para que la app también funcione
    # con una base que solo tenga P1-P17.
    for code, info in DIMENSIONS.items():
        prom_col = f"{code}_Promedio"
        sat_col = f"{code}_Satisfecho"
        df[prom_col] = df[info["items"]].mean(axis=1)
        df[sat_col] = (df[prom_col] >= 4).astype(int)

    df["Global_Satisfecho"] = (df["P17"] >= 4).astype(int)
    df["Categoria_Global"] = df["Global_Satisfecho"].map(
        {1: "Satisfecho", 0: "No satisfecho"}
    )
    df["Promedio_P1_P16"] = df[[f"P{i}" for i in range(1, 17)]].mean(axis=1)
    return df


def read_excel(source) -> pd.DataFrame:
    try:
        return pd.read_excel(source, sheet_name="Base_Encuesta", engine="openpyxl")
    except ValueError as exc:
        raise ValueError(
            "No encuentro la hoja 'Base_Encuesta'. Revisa que el Excel tenga esa hoja."
        ) from exc


@st.cache_data(show_spinner=False)
def load_uploaded_excel(file_bytes: bytes) -> pd.DataFrame:
    from io import BytesIO

    return prepare_data(read_excel(BytesIO(file_bytes)))


def dimension_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, info in DIMENSIONS.items():
        sat = df[f"{code}_Satisfecho"].mean()
        avg = df[f"{code}_Promedio"].mean()
        rows.append(
            {
                "Código": code,
                "Dimensión": info["name"],
                "Preguntas": f"{info['items'][0]}–{info['items'][-1]}",
                "Satisfacción": sat,
                "Promedio Likert": avg,
                "Nivel": nivel_inst(sat),
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


def plot_layout(fig, height=430):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=25, t=45, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Arial", color="#334155"),
        hoverlabel=dict(bgcolor="white", font_color="#0F172A"),
    )
    return fig


def render_dim_card(code: str, value: float):
    info = DIMENSIONS[code]
    level = nivel_inst(value)
    color = COLORS_DIM[code]
    st.markdown(
        f"""
        <div class="glass-card" style="border-top:5px solid {color};">
            <div class="kpi-code">{code}</div>
            <div class="kpi-value">{pct(value)}</div>
            <div class="kpi-label"><b>{info['name']}</b><br>{level}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================
# SIDEBAR + CARGA DE EXCEL
# ==============================================================
with st.sidebar:
    st.title("🎓 UNT")
    st.caption("Dashboard de satisfacción estudiantil")
    st.markdown("---")

    uploaded = st.file_uploader(
        "Sube tu archivo Excel",
        type=["xlsx"],
        help="Selecciona el archivo que contiene la hoja Base_Encuesta.",
    )

    use_local = False
    local_file = Path("basededatos.xlsx")
    if local_file.exists():
        use_local = st.checkbox(
            "Usar basededatos.xlsx de la carpeta",
            value=False,
            help="Útil cuando ejecutas la app en tu propia computadora.",
        )

    page = st.radio(
        "Navegación",
        [
            "🏛️ Panorama institucional",
            "🔎 Explorar dimensiones",
            "🎯 Prioridades de mejora",
            "ℹ️ Cómo se interpreta",
        ],
    )


if uploaded is None and not use_local:
    st.title("Dashboard de Satisfacción Estudiantil")
    st.markdown(
        '<div class="subtitle">Python + Streamlit · carga tu Excel para generar el dashboard automáticamente.</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "👈 En la barra izquierda pulsa **Browse files / Examinar archivos** y selecciona tu `basededatos.xlsx`. "
        "No tienes que subir el Excel a VS Code. Se selecciona desde esta página de Streamlit."
    )
    st.markdown("### ¿Qué mostrará la app?")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**D1**  \nCalidad del proceso académico")
    with c2:
        st.markdown("**D2**  \nDesempeño docente")
    with c3:
        st.markdown("**D3**  \nServicios y gestión")
    with c4:
        st.markdown("**D4**  \nFormación integral")
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

with st.sidebar:
    st.success(f"Archivo cargado: {source_name}")
    st.caption(f"{len(df):,} registros")


# ==============================================================
# 1) PANORAMA INSTITUCIONAL
# ==============================================================
if page == "🏛️ Panorama institucional":
    st.title("Panorama institucional")
    st.markdown(
        '<div class="subtitle">Resultado general y satisfacción de las cuatro dimensiones D1–D4.</div>',
        unsafe_allow_html=True,
    )

    global_sat = df["Global_Satisfecho"].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Estudiantes encuestados", f"{len(df):,}")
    c2.metric("Satisfacción general · P17", pct(global_sat))
    c3.metric("Nivel general", nivel_inst(global_sat))

    st.markdown("### Satisfacción por dimensión")
    cols = st.columns(4)
    for col, code in zip(cols, ["D1", "D2", "D3", "D4"]):
        with col:
            value = float(summary_dim.loc[summary_dim["Código"] == code, "Satisfacción"].iloc[0])
            render_dim_card(code, value)

    st.markdown("### Comparación D1–D4")
    chart_df = summary_dim.sort_values("Satisfacción", ascending=True).copy()
    fig = px.bar(
        chart_df,
        x="Satisfacción",
        y="Código",
        orientation="h",
        color="Código",
        color_discrete_map=COLORS_DIM,
        text=chart_df["Satisfacción"].map(lambda x: f"{x*100:.2f}%"),
        custom_data=["Dimensión", "Nivel", "Promedio Likert", "Brecha a 75%"],
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>%{y} · %{customdata[0]}</b><br>"
            "Satisfacción: %{x:.2%}<br>"
            "Nivel: %{customdata[1]}<br>"
            "Promedio Likert: %{customdata[2]:.2f}<br>"
            "Brecha a 75%: %{customdata[3]:.2%}<extra></extra>"
        ),
    )
    fig.add_vline(x=0.60, line_dash="dash", line_color="#F59E0B", annotation_text="60%")
    fig.add_vline(x=0.75, line_dash="dash", line_color="#10B981", annotation_text="75%")
    fig.update_xaxes(tickformat=".0%", range=[0, 1], title="% de estudiantes satisfechos")
    fig.update_yaxes(title=None)
    fig.update_layout(showlegend=False)
    st.plotly_chart(plot_layout(fig, 430), use_container_width=True)

    left, right = st.columns([1.7, 1])
    with left:
        st.markdown("### Tablero de situación institucional")
        table = summary_dim.copy()
        table["Satisfacción"] = table["Satisfacción"].map(pct)
        table["Promedio Likert"] = table["Promedio Likert"].map(lambda x: f"{x:.2f}")
        table["Brecha a 75%"] = table["Brecha a 75%"].map(lambda x: f"{x*100:.2f} pp")
        st.dataframe(
            table[["Código", "Dimensión", "Preguntas", "Satisfacción", "Promedio Likert", "Nivel", "Brecha a 75%"]],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.markdown("### Conclusiones clave")
        worst = summary_dim.sort_values("Satisfacción").iloc[0]
        best = summary_dim.sort_values("Satisfacción", ascending=False).iloc[0]
        meets = int((summary_dim["Satisfacción"] >= 0.75).sum())
        st.markdown(
            f'<div class="finding"><b>Resultado general</b><br>P17 alcanza <b>{pct(global_sat)}</b> · {nivel_inst(global_sat)}.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="finding alert"><b>Principal prioridad: {worst["Código"]}</b><br>{worst["Dimensión"]}<br><b>{pct(worst["Satisfacción"])}</b> de estudiantes satisfechos.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="finding good"><b>Fortaleza relativa: {best["Código"]}</b><br>{best["Dimensión"]}<br><b>{pct(best["Satisfacción"])}</b>.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="finding"><b>Meta institucional</b><br><b>{meets} de 4</b> dimensiones alcanzan 75% o más.</div>',
            unsafe_allow_html=True,
        )


# ==============================================================
# 2) EXPLORAR DIMENSIONES
# ==============================================================
elif page == "🔎 Explorar dimensiones":
    st.title("Explorador de dimensiones")
    st.markdown(
        '<div class="subtitle">Selecciona una dimensión o compara los 16 ítems de D1–D4.</div>',
        unsafe_allow_html=True,
    )

    options = {
        "Todas las dimensiones": "TODAS",
        "D1 · Calidad del proceso académico": "D1",
        "D2 · Desempeño docente y estrategias pedagógicas": "D2",
        "D3 · Servicios y gestión educativa": "D3",
        "D4 · Formación integral y desarrollo personal": "D4",
    }
    label = st.selectbox("Dimensión", list(options.keys()), index=3)
    selected = options[label]

    if selected == "TODAS":
        items = all_items
        st.info("Vista comparativa: se muestran P1–P16 de las cuatro dimensiones.")
        best = summary_dim.sort_values("Satisfacción", ascending=False).iloc[0]
        worst = summary_dim.sort_values("Satisfacción").iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Vista", "D1–D4")
        c2.metric(f"Mayor resultado · {best['Código']}", pct(best["Satisfacción"]))
        c3.metric(f"Menor resultado · {worst['Código']}", pct(worst["Satisfacción"]))
    else:
        info = DIMENSIONS[selected]
        items = info["items"]
        sat = df[f"{selected}_Satisfecho"].mean()
        avg = df[f"{selected}_Promedio"].mean()
        gap = max(0, 0.75 - sat)
        st.info(f"**{selected} · {info['name']}** — {info['description']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Satisfacción", pct(sat))
        c2.metric("Promedio Likert", f"{avg:.2f} / 5")
        c3.metric("Distancia a 75%", f"{gap*100:.2f} pp")

    items_df = item_summary(df, items).sort_values("Favorable", ascending=True)
    items_df["Etiqueta"] = items_df.apply(
        lambda r: f"{r['Ítem']} · {r['Texto'][:62]}{'…' if len(r['Texto']) > 62 else ''}", axis=1
    )

    st.markdown("### Valoración favorable de los ítems")
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
    fig.update_xaxes(tickformat=".0%", range=[0, 1], title="% favorable (4–5)")
    fig.update_yaxes(title=None)
    fig.update_layout(showlegend=(selected == "TODAS"), legend_title_text="Dimensión")
    height = 680 if selected == "TODAS" else 470
    st.plotly_chart(plot_layout(fig, height), use_container_width=True)

    # Distribución Likert
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

    st.markdown("### Distribución de respuestas")
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
    fig2.update_traces(
        hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>%{fullData.name}: %{x:.2%}<extra></extra>"
    )
    fig2.update_xaxes(tickformat=".0%", range=[0, 1], title="Distribución")
    fig2.update_yaxes(title=None)
    fig2.update_layout(legend_title_text=None)
    st.plotly_chart(plot_layout(fig2, height), use_container_width=True)

    # Diagnóstico
    worst_item = items_df.sort_values("Favorable").iloc[0]
    best_item = items_df.sort_values("Favorable", ascending=False).iloc[0]
    st.markdown("### Lectura del filtro seleccionado")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="finding alert"><b>Menor valoración · {worst_item["Ítem"]}</b><br>{worst_item["Texto"]}<br><br><b>{pct(worst_item["Favorable"])}</b> favorable.</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="finding good"><b>Mayor valoración · {best_item["Ítem"]}</b><br>{best_item["Texto"]}<br><br><b>{pct(best_item["Favorable"])}</b> favorable.</div>',
            unsafe_allow_html=True,
        )


# ==============================================================
# 3) PRIORIDADES DE MEJORA
# ==============================================================
elif page == "🎯 Prioridades de mejora":
    st.title("Prioridades de mejora")
    st.markdown(
        '<div class="subtitle">Ranking descriptivo de P1–P16 según porcentaje de respuestas favorables (4–5).</div>',
        unsafe_allow_html=True,
    )

    rank = item_summary(df, all_items).sort_values("Favorable", ascending=True).copy()
    rank["Etiqueta"] = rank.apply(
        lambda r: f"{r['Ítem']} · {r['Texto'][:55]}{'…' if len(r['Texto']) > 55 else ''}", axis=1
    )

    fig = px.bar(
        rank,
        x="Favorable",
        y="Etiqueta",
        orientation="h",
        color="Dimensión",
        color_discrete_map=COLORS_DIM,
        text=rank["Favorable"].map(lambda x: f"{x*100:.1f}%"),
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
    fig.update_xaxes(tickformat=".0%", range=[0, 1], title="% favorable (4–5)")
    fig.update_yaxes(title=None)
    fig.update_layout(legend_title_text="Dimensión")
    st.plotly_chart(plot_layout(fig, 720), use_container_width=True)

    st.markdown("### 5 aspectos con menor valoración favorable")
    top5 = rank.head(5).copy()
    display = top5[["Ítem", "Dimensión", "Texto", "Favorable", "Desfavorable", "Promedio"]].copy()
    display["Favorable"] = display["Favorable"].map(pct)
    display["Desfavorable"] = display["Desfavorable"].map(pct)
    display["Promedio"] = display["Promedio"].map(lambda x: f"{x:.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    first3 = rank.head(3)
    msg = ", ".join(f"{r['Ítem']} ({r['Dimensión']})" for _, r in first3.iterrows())
    st.markdown(
        f'<div class="finding alert"><b>Mensaje para la sustentación</b><br>Los tres aspectos con menor valoración favorable son <b>{msg}</b>. Esta lectura sirve para priorizar aspectos concretos sin confundir el porcentaje favorable del ítem con la satisfacción oficial de la dimensión.</div>',
        unsafe_allow_html=True,
    )


# ==============================================================
# 4) METODOLOGÍA
# ==============================================================
else:
    st.title("Cómo se interpreta")
    st.markdown(
        '<div class="subtitle">Reglas de cálculo para satisfacción dimensional, satisfacción general y valoración por ítem.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="method-card">
            <h3>Satisfacción por dimensión</h3>
            <p><b>D1, D2, D3 y D4</b> tienen 4 preguntas cada una.</p>
            <p>Para cada estudiante se calcula el promedio de sus 4 respuestas.</p>
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
            <p>Se obtiene directamente de <b>P17</b>.</p>
            <p>P17 = 4 o 5 → <b>satisfecho</b>.</p>
            <p>P17 = 1, 2 o 3 → <b>no satisfecho</b>.</p>
            <p>No se calcula promediando D1–D4.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Escala institucional")
    thresholds = pd.DataFrame(
        {
            "Porcentaje": ["0% a <60%", "60% a <75%", "75% a <90%", "90% a 100%"],
            "Nivel": ["Insatisfactorio", "Regular", "Satisfactorio", "Muy satisfactorio"],
        }
    )
    st.dataframe(thresholds, use_container_width=True, hide_index=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(
            """
            <div class="method-card">
            <h3>Lectura de los ítems</h3>
            <p><b>Desfavorable:</b> respuestas 1 y 2.</p>
            <p><b>Neutral:</b> respuesta 3.</p>
            <p><b>Favorable:</b> respuestas 4 y 5.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            """
            <div class="method-card">
            <h3>Importante</h3>
            <p>Los porcentajes favorables de P1–P16 son descriptivos.</p>
            <p>La escala institucional se aplica a <b>D1–D4 y P17</b>, no a cada ítem individual.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
