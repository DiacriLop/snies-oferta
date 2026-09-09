"""Módulo de transformación para los datos de Oferta Académica.

Se encarga de preparar los datos para búsquedas y consultas posteriores,
manteniendo intactos los valores originales.

Responsabilidades:
- Normalizar textos para búsqueda.
- Crear columnas auxiliares normalizadas.
- Clasificar el tipo de maestría.

No realiza:
- Lectura del Excel.
- Limpieza de espacios.
- Corrección de datos corruptos.
- Eliminación de duplicados.
- Filtrado de programas.
- Reglas de negocio de consulta.
"""

import unicodedata

import pandas as pd


NORMALIZABLE_COLUMNS = [
    "NOMBRE_INSTITUCIÓN",
    "NOMBRE_DEL_PROGRAMA",
    "TITULO_OTORGADO",
    "CARÁCTER_ACADÉMICO",
    "SECTOR",
    "ESTADO_PROGRAMA",
    "RECONOCIMIENTO_DEL_MINISTERIO",
    "NIVEL_ACADÉMICO",
    "NIVEL_DE_FORMACIÓN",
    "MODALIDAD",
    "PERIODICIDAD",
    "DEPARTAMENTO_OFERTA_PROGRAMA",
    "MUNICIPIO_OFERTA_PROGRAMA",
]


def normalize_text(value):
    """Normaliza un texto para facilitar búsquedas y comparaciones.

    La normalización:
    - Convierte el texto a minúsculas.
    - Elimina tildes únicamente en la versión normalizada.
    - Conserva el contenido textual.
    - Reduce espacios innecesarios.

    El valor original nunca es modificado.
    """

    if not isinstance(value, str):
        return value

    value = value.strip()
    value = " ".join(value.split())
    value = value.lower()

    value = unicodedata.normalize("NFD", value)

    value = "".join(
        character
        for character in value
        if unicodedata.category(character) != "Mn"
    )

    return value


def classify_master_type(row):
    """Clasifica el tipo de maestría a partir de NIVEL_DE_FORMACIÓN
    y JUSTIFICACION.
    """

    nivel = row["NIVEL_DE_FORMACIÓN"]
    justificacion = row["JUSTIFICACION"]

    if nivel != "Maestría":
        return "NO APLICA"

    if justificacion == "PROFUNDIZACION":
        return "Maestría de profundización"

    if justificacion == "INVESTIGACION":
        return "Maestría de investigación"

    return "NO APLICA"


def transform_oferta(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma los datos de Oferta sin modificar los originales."""

    df_transformado = df.copy()

    for column in NORMALIZABLE_COLUMNS:

        if column not in df_transformado.columns:
            continue

        normalized_column = f"{column}_NORMALIZADO"

        df_transformado[normalized_column] = (
            df_transformado[column].apply(normalize_text)
        )

    df_transformado["TIPO_MAESTRIA"] = df_transformado.apply(
        classify_master_type,
        axis=1
    )

    return df_transformado
