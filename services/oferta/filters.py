"""Filtros reutilizables para el módulo de Oferta Académica."""

import pandas as pd


def filter_by_column(
    df: pd.DataFrame,
    column: str,
    value
) -> pd.DataFrame:
    """
    Filtra un DataFrame por una columna y un valor exacto.

    Retorna una copia del DataFrame filtrado.
    """
    if column not in df.columns:
        raise ValueError(f"La columna '{column}' no existe en el DataFrame.")

    return df[df[column] == value].copy()  # type: ignore


def filter_by_sector(
    df: pd.DataFrame,
    sector: str
) -> pd.DataFrame:
    """Filtra por sector: Oficial o Privado."""
    return filter_by_column(df, "SECTOR", sector)


def filter_by_formation_level(
    df: pd.DataFrame,
    level: str
) -> pd.DataFrame:
    """Filtra por nivel de formación."""
    return filter_by_column(df, "NIVEL_DE_FORMACIÓN", level)


def filter_by_modality(
    df: pd.DataFrame,
    modality: str
) -> pd.DataFrame:
    """Filtra por modalidad."""
    return filter_by_column(df, "MODALIDAD", modality)


def filter_by_department(
    df: pd.DataFrame,
    department: str
) -> pd.DataFrame:
    """Filtra por departamento."""
    return filter_by_column(
        df,
        "DEPARTAMENTO_OFERTA_PROGRAMA",
        department
    )


def filter_by_municipality(
    df: pd.DataFrame,
    municipality: str
) -> pd.DataFrame:
    """Filtra por municipio."""
    return filter_by_column(
        df,
        "MUNICIPIO_OFERTA_PROGRAMA",
        municipality
    )


def filter_by_institution(
    df: pd.DataFrame,
    institution: str
) -> pd.DataFrame:
    """Filtra por institución."""
    return filter_by_column(
        df,
        "NOMBRE_INSTITUCIÓN",
        institution
    )


def filter_by_program_state(
    df: pd.DataFrame,
    state: str
) -> pd.DataFrame:
    """Filtra por estado del programa."""
    return filter_by_column(
        df,
        "ESTADO_PROGRAMA",
        state
    )


def filter_by_recognition(
    df: pd.DataFrame,
    recognition: str
) -> pd.DataFrame:
    """Filtra por reconocimiento del Ministerio."""
    return filter_by_column(
        df,
        "RECONOCIMIENTO_DEL_MINISTERIO",
        recognition
    )


def filter_by_academic_character(
    df: pd.DataFrame,
    academic_character: str
) -> pd.DataFrame:
    """Filtra por carácter académico de la institución."""
    return filter_by_column(
        df,
        "CARÁCTER_ACADÉMICO",
        academic_character
    )


def filter_by_master_type(
    df: pd.DataFrame,
    master_type: str
) -> pd.DataFrame:
    """Filtra por tipo de maestría."""
    return filter_by_column(
        df,
        "TIPO_MAESTRIA",
        master_type
    )
