import streamlit as st
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from services.oferta.filters import (
    filter_by_sector,
    filter_by_formation_level,
    filter_by_modality,
    filter_by_department,
    filter_by_municipality,
    filter_by_institution,
    filter_by_program_state,
    filter_by_recognition,
    filter_by_academic_character,
    filter_by_master_type,
)

from services.oferta.queries import (
    search_by_program_name,
    search_by_keywords,
)

from services.oferta.metrics import (
    build_table_1,
    build_table_2_profundizacion,
    build_table_2_investigacion,
    build_table_3_valle,
)



# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Módulo Oferta - SNIES",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================



PROCESSED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "oferta"
    / "oferta_procesada.parquet"
)


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data
def load_data():
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo procesado: {PROCESSED_FILE}"
        )

    return pd.read_parquet(PROCESSED_FILE)


# ============================================================
# INTERFAZ
# ============================================================

st.title("🎓 Módulo de Oferta Académica")

st.write(
    "Consulta y análisis de la oferta de programas académicos "
    "registrada en SNIES."
)

try:
    df = load_data()

    st.success("Dataset de Oferta cargado correctamente.")

    # ========================================================
    # BÚSQUEDA
    # ========================================================

    st.subheader("🔎 Búsqueda")

    # --------------------------------------------------------
    # BÚSQUEDA POR NOMBRE DEL PROGRAMA
    # --------------------------------------------------------

    nombre_programa = st.text_input(
        "Nombre del programa",
        placeholder="Ejemplo: Ingeniería de Sistemas",
    )

    # --------------------------------------------------------
    # BÚSQUEDA POR PALABRAS CLAVE
    # --------------------------------------------------------

    palabras_clave = st.text_input(
        "Palabras clave",
        placeholder="Ejemplo: ingeniería sistemas software",
    )

    operador = st.selectbox(
        "Operador para palabras clave",
        options=["AND", "OR"],
    )

    # --------------------------------------------------------
    # APLICAR BÚSQUEDAS
    # --------------------------------------------------------

    df_filtrado = df.copy()

    if nombre_programa.strip():
        df_filtrado = search_by_program_name(
            df_filtrado,
            nombre_programa,
        )

    if palabras_clave.strip():
        df_filtrado = search_by_keywords(
            df_filtrado,
            palabras_clave,
            operator=operador,
        )

    # ========================================================
    # FILTROS
    # ========================================================

    st.subheader("🎛️ Filtros")

    # ========================================================
    # FILTRO: SECTOR
    # ========================================================

    sectores = sorted(
        df["SECTOR"].dropna().unique().tolist()
    )

    sector_seleccionado = st.selectbox(
        "Sector",
        options=["Todos"] + sectores,
    )

    if sector_seleccionado != "Todos":
        df_filtrado = filter_by_sector(
            df_filtrado,
            sector_seleccionado,
        )

    # ========================================================
    # FILTRO: NIVEL DE FORMACIÓN
    # ========================================================

    niveles_formacion = sorted(
        df["NIVEL_DE_FORMACIÓN"].dropna().unique().tolist()
    )

    nivel_seleccionado = st.selectbox(
        "Nivel de formación",
        options=["Todos"] + niveles_formacion,
    )

    if nivel_seleccionado != "Todos":
        df_filtrado = filter_by_formation_level(
            df_filtrado,
            nivel_seleccionado,
        )

    # ========================================================
    # FILTRO: MODALIDAD
    # ========================================================

    modalidades = sorted(
        df["MODALIDAD"].dropna().unique().tolist()
    )

    modalidad_seleccionada = st.selectbox(
        "Modalidad",
        options=["Todas"] + modalidades,
    )

    if modalidad_seleccionada != "Todas":
        df_filtrado = filter_by_modality(
            df_filtrado,
            modalidad_seleccionada,
        )

    # ========================================================
    # FILTRO: DEPARTAMENTO
    # ========================================================

    departamentos = sorted(
        df["DEPARTAMENTO_OFERTA_PROGRAMA"]
        .dropna()
        .unique()
        .tolist()
    )

    departamento_seleccionado = st.selectbox(
        "Departamento",
        options=["Todos"] + departamentos,
    )

    if departamento_seleccionado != "Todos":
        df_filtrado = filter_by_department(
            df_filtrado,
            departamento_seleccionado,
        )

    # ========================================================
    # FILTRO: MUNICIPIO
    # ========================================================

    municipios = sorted(
        df_filtrado["MUNICIPIO_OFERTA_PROGRAMA"]
        .dropna()
        .unique()
        .tolist()
    )

    municipio_seleccionado = st.selectbox(
        "Municipio",
        options=["Todos"] + municipios,
    )

    if municipio_seleccionado != "Todos":
        df_filtrado = filter_by_municipality(
            df_filtrado,
            municipio_seleccionado,
        )

    # ========================================================
    # FILTRO: INSTITUCIÓN
    # ========================================================

    instituciones = sorted(
        df_filtrado["NOMBRE_INSTITUCIÓN"]
        .dropna()
        .unique()
        .tolist()
    )

    institucion_seleccionada = st.selectbox(
        "Institución",
        options=["Todas"] + instituciones,
    )

    if institucion_seleccionada != "Todas":
        df_filtrado = filter_by_institution(
            df_filtrado,
            institucion_seleccionada,
        )

    # ========================================================
    # FILTRO: ESTADO DEL PROGRAMA
    # ========================================================

    estados_programa = sorted(
        df_filtrado["ESTADO_PROGRAMA"]
        .dropna()
        .unique()
        .tolist()
    )

    estado_programa_seleccionado = st.selectbox(
        "Estado del programa",
        options=["Todos"] + estados_programa,
    )

    if estado_programa_seleccionado != "Todos":
        df_filtrado = filter_by_program_state(
            df_filtrado,
            estado_programa_seleccionado,
        )

    # ========================================================
    # FILTRO: RECONOCIMIENTO DEL MINISTERIO
    # ========================================================

    reconocimientos = sorted(
        df_filtrado["RECONOCIMIENTO_DEL_MINISTERIO"]
        .dropna()
        .unique()
        .tolist()
    )

    reconocimiento_seleccionado = st.selectbox(
        "Reconocimiento del Ministerio",
        options=["Todos"] + reconocimientos,
    )

    if reconocimiento_seleccionado != "Todos":
        df_filtrado = filter_by_recognition(
            df_filtrado,
            reconocimiento_seleccionado,
        )

    # ========================================================
    # FILTRO: CARÁCTER ACADÉMICO
    # ========================================================

    caracteres_academicos = sorted(
        df_filtrado["CARÁCTER_ACADÉMICO"]
        .dropna()
        .unique()
        .tolist()
    )

    caracter_academico_seleccionado = st.selectbox(
        "Carácter académico",
        options=["Todos"] + caracteres_academicos,
    )

    if caracter_academico_seleccionado != "Todos":
        df_filtrado = filter_by_academic_character(
            df_filtrado,
            caracter_academico_seleccionado,
        )

    # ========================================================
    # FILTRO: TIPO DE MAESTRÍA
    # ========================================================

    tipos_maestria = sorted(
        df_filtrado["TIPO_MAESTRIA"]
        .dropna()
        .unique()
        .tolist()
    )

    tipo_maestria_seleccionado = st.selectbox(
        "Tipo de maestría",
        options=["Todos"] + tipos_maestria,
    )

    if tipo_maestria_seleccionado != "Todos":
        df_filtrado = filter_by_master_type(
            df_filtrado,
            tipo_maestria_seleccionado,
        )

    # ========================================================
    # RESULTADOS DE LA CONSULTA
    # ========================================================

    st.subheader("📊 Resultados de la consulta")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Registros encontradas", f"{len(df_filtrado):,}")

    with col2:
        st.metric("Columnas", len(df_filtrado.columns))

    st.write("**Vista preliminar:**")

    st.dataframe(
        df_filtrado.head(10),
        width="stretch",
    )

    # ========================================================
    # TABLAS OFICIALES
    # ========================================================

    st.divider()
    st.subheader("📋 Tablas oficiales")
    
    st.info(
        "Las siguientes tablas muestran el consolidado oficial de la oferta "
        "académica. Estos valores se recalculan dinámicamente según los "
        "filtros que hayas aplicado en la sección superior."
    )

    # --------------------------------------------------------
    # TABLA 1: OFERTA GENERAL
    # --------------------------------------------------------

    st.markdown("#### Tabla 1 — Oferta general por nivel académico y sector")
    
    tabla_1 = build_table_1(df_filtrado)
    
    st.dataframe(
        tabla_1,
        width="stretch",
    )

    # --------------------------------------------------------
    # TABLA 2A: MAESTRÍA DE PROFUNDIZACIÓN
    # --------------------------------------------------------

    st.markdown("#### Tabla 2A — Maestrías de profundización")

    tabla_2a = build_table_2_profundizacion(df_filtrado)

    st.dataframe(
        tabla_2a,
        width="stretch",
    )

    # --------------------------------------------------------
    # TABLA 2B: MAESTRÍA DE INVESTIGACIÓN
    # --------------------------------------------------------

    st.markdown("#### Tabla 2B — Maestrías de investigación")

    tabla_2b = build_table_2_investigacion(df_filtrado)

    st.dataframe(
        tabla_2b,
        width="stretch",
    )

    # --------------------------------------------------------
    # TABLA 3: OFERTA ESPECÍFICA DEL VALLE DEL CAUCA
    # --------------------------------------------------------

    st.markdown("#### Tabla 3 — Oferta específica del Valle del Cauca")

    tabla_3 = build_table_3_valle(df_filtrado)

    st.dataframe(
        tabla_3,
        width="stretch",
    )

except FileNotFoundError as error:
    st.error(str(error))

except Exception as error:
    st.error(
        f"Ocurrió un error al cargar el dataset: {error}"
    )
