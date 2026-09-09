"""Consultas detalladas para el módulo de Oferta Académica."""

import pandas as pd
from etl.oferta.transform import normalize_text


# ============================================================
# COLUMNAS TABLA 3
# ============================================================

OFERTA_COLUMNS = [
    "SECTOR",
    "NOMBRE_INSTITUCIÓN",
    "CÓDIGO_SNIES_DEL_PROGRAMA",
    "NOMBRE_DEL_PROGRAMA",
    "MODALIDAD",
    "MUNICIPIO_OFERTA_PROGRAMA",
    "RECONOCIMIENTO_DEL_MINISTERIO",
    "FECHA_DE_RESOLUCIÓN",
    "NÚMERO_PERIODOS_DE_DURACIÓN",
    "PERIODICIDAD",
    "NÚMERO_CRÉDITOS",
]


# ============================================================
# TABLA 3 - PROGRAMAS POR DEPARTAMENTO
# ============================================================

def get_programs_by_department(
    df: pd.DataFrame,
    department: str
) -> pd.DataFrame:
    """
    Filtra los programas por departamento y selecciona las columnas
    exactas requeridas para la Tabla 3, manteniendo la modalidad original.
    """

    filtered = df[
        df["DEPARTAMENTO_OFERTA_PROGRAMA"] == department
    ].copy()

    missing = set(OFERTA_COLUMNS) - set(filtered.columns)

    if missing:
        raise ValueError(
            f"Faltan columnas requeridas en el DataFrame: {missing}"
        )

    return filtered[OFERTA_COLUMNS]


# ============================================================
# BÚSQUEDA POR NOMBRE DEL PROGRAMA
# ============================================================

def search_by_program_name(
    df: pd.DataFrame,
    search_term: str
) -> pd.DataFrame:
    """
    Busca programas por nombre utilizando la columna normalizada.

    La búsqueda:
    - ignora mayúsculas/minúsculas;
    - ignora tildes gracias a la columna normalizada;
    - permite coincidencias parciales;
    - conserva las columnas y valores originales.
    """

    if not isinstance(search_term, str):
        raise ValueError("El término de búsqueda debe ser un texto.")

    search_term = normalize_text(search_term.strip())

    if not search_term:
        return df.copy()

    column = "NOMBRE_DEL_PROGRAMA_NORMALIZADO"

    if column not in df.columns:
        raise ValueError(
            f"No existe la columna requerida: {column}"
        )

    mask = df[column].fillna("").str.contains(
        search_term,
        regex=False,
        na=False,
    )

    return df.loc[mask].copy()


# ============================================================
# BÚSQUEDA POR PALABRAS CLAVE
# ============================================================

def search_by_keywords(
    df: pd.DataFrame,
    keywords: str,
    operator: str = "AND"
) -> pd.DataFrame:
    """
    Busca programas utilizando palabras clave.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de Oferta.

    keywords : str
        Palabras clave separadas por espacios.

    operator : str
        Operador lógico:
        - AND: todas las palabras deben aparecer.
        - OR: al menos una palabra debe aparecer.

    Retorna
    -------
    pd.DataFrame
        DataFrame filtrado conservando las columnas originales.
    """

    if not isinstance(keywords, str):
        raise ValueError("Las palabras clave deben ser un texto.")

    operator = operator.upper().strip()

    if operator not in {"AND", "OR"}:
        raise ValueError(
            "El operador debe ser 'AND' o 'OR'."
        )

    column = "NOMBRE_DEL_PROGRAMA_NORMALIZADO"

    if column not in df.columns:
        raise ValueError(
            f"No existe la columna requerida: {column}"
        )

    # Separar las palabras y eliminar espacios innecesarios
    terms = [
        normalize_text(term.strip())
        for term in keywords.split()
        if term.strip()
    ]

    # Si no hay palabras, devolver copia del DataFrame
    if not terms:
        return df.copy()

    text = df[column].fillna("").astype(str)

    masks = [
        text.str.contains(
            term,
            regex=False,
            na=False,
        )
        for term in terms
    ]

    if operator == "AND":
        final_mask = masks[0]

        for mask in masks[1:]:
            final_mask = final_mask & mask

    else:  # OR
        final_mask = masks[0]

        for mask in masks[1:]:
            final_mask = final_mask | mask

    return df.loc[final_mask].copy()
