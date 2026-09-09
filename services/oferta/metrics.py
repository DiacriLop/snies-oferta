"""Métricas y tablas agregadas para el módulo de Oferta Académica."""

import pandas as pd


PROGRAM_ID = "CÓDIGO_SNIES_DEL_PROGRAMA"
INSTITUTION_ID = "CÓDIGO_INSTITUCIÓN"
MUNICIPALITY = "MUNICIPIO_OFERTA_PROGRAMA"
DEPARTMENT = "DEPARTAMENTO_OFERTA_PROGRAMA"

FORMATION_LEVEL = "NIVEL_DE_FORMACIÓN"
SECTOR = "SECTOR"
MODALITY = "MODALIDAD"
MODALITY_GROUPED = "MODALIDAD_AGRUPADA"
MASTER_TYPE = "TIPO_MAESTRIA"


def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula las métricas básicas de oferta para un conjunto de registros.

    Retorna:
        PROG: cantidad de programas distintos.
        INST: cantidad de instituciones distintas.
        MPIO: cantidad de municipios distintos.
        DEPTO: cantidad de departamentos distintos.
    """

    return {
        "PROG": df[PROGRAM_ID].nunique(),
        "INST": df[INSTITUTION_ID].nunique(),
        "MPIO": df[MUNICIPALITY].nunique(),
        "DEPTO": df[DEPARTMENT].nunique(),
    }


def group_modality(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la columna MODALIDAD_AGRUPADA basada en la correspondencia oficial.
    No modifica la columna original MODALIDAD.
    """
    mapping = {
        "Presencial": "Presencial",
        "Presencial-Virtual": "Presencial Virtual",
        "Híbrida (Presencial-Virtual)": "Presencial Virtual",
        "Virtual": "Virtual",
        "Virtual-A distancia": "A Distancia Virtual",
        "Híbrida (A distancia-Virtual)": "A Distancia Virtual",
        "A distancia": "A Distancia",
        "Dual": "Dual",
        "Virtual-Dual": "Dual Virtual",
        "Híbrida (Dual-Virtual)": "Dual Virtual",
        "Presencial-Dual": "Presencial Dual",
        "Presencial-A distancia": "Presencial A Distancia",
        "Presencial-Virtual-A distancia": "Presencial Virtual A Distancia"
    }
    
    df_out = df.copy()
    
    unknown_modalities = (
        set(df_out[MODALITY].dropna().unique())
        - set(mapping.keys())
    )

    if unknown_modalities:
        raise ValueError(
            f"Se encontraron modalidades sin agrupación definida: "
            f"{sorted(unknown_modalities)}"
        )
        
    df_out[MODALITY_GROUPED] = df_out[MODALITY].map(mapping)
    return df_out


def _build_aggregated_table(df: pd.DataFrame, include_distance_virtual: bool = True) -> pd.DataFrame:
    """
    Construye una tabla agregada en formato horizontal.

    Estructura:

        NIVEL DE FORMACIÓN | SECTOR |
        Presencial(PROG, INST, MPIO, DEPTO) |
        Presencial Virtual(PROG, INST, MPIO, DEPTO) |
        Virtual(PROG, INST, MPIO, DEPTO) |
        A Distancia Virtual(PROG, INST, MPIO, DEPTO) |
        Total(PROG, INST, MPIO, DEPTO)

    Incluye:
        - filas por nivel y sector;
        - fila Total por cada nivel;
        - fila Total general.
    """

    df_grouped = group_modality(df)

    # --------------------------------------------------------
    # MODALIDADES QUE DEBEN APARECER EN LA TABLA
    # --------------------------------------------------------

    modalities = [
        "Presencial",
        "Presencial Virtual",
        "Virtual",
    ]
    if include_distance_virtual:
        modalities.append("A Distancia Virtual")

    metrics = [
        "PROG",
        "INST",
        "MPIO",
        "DEPTO",
    ]

    # --------------------------------------------------------
    # GENERAR COLUMNAS DEL REPORTE
    # --------------------------------------------------------

    columns = []

    for modality in modalities:
        for metric in metrics:
            columns.append((modality, metric))

    for metric in metrics:
        columns.append(("Total", metric))

    # --------------------------------------------------------
    # FUNCIÓN AUXILIAR PARA CALCULAR UNA FILA
    # --------------------------------------------------------

    def calculate_row(group: pd.DataFrame) -> dict:
        row = {}

        for modality in modalities:

            modality_data = group[
                group[MODALITY_GROUPED] == modality
            ]

            calculated = calculate_metrics(modality_data)

            for metric in metrics:
                row[(modality, metric)] = calculated[metric]

        # Total independiente del número de modalidades
        total_metrics = calculate_metrics(group)

        for metric in metrics:
            row[("Total", metric)] = total_metrics[metric]

        return row

    # --------------------------------------------------------
    # FILAS POR NIVEL + SECTOR
    # --------------------------------------------------------

    rows = []

    for (formation_level, sector), group in df_grouped.groupby(
        [FORMATION_LEVEL, SECTOR],
        dropna=False,
    ):
        row = calculate_row(group)

        rows.append(
            {
                "NIVEL_DE_FORMACIÓN": formation_level,
                "SECTOR": sector,
                **row,
            }
        )

    # --------------------------------------------------------
    # DATAFRAME DE RESULTADO
    # --------------------------------------------------------

    result = pd.DataFrame(rows)

    # --------------------------------------------------------
    # FILAS TOTAL POR NIVEL DE FORMACIÓN
    # --------------------------------------------------------

    total_level_rows = []

    for formation_level, group in df_grouped.groupby(
        FORMATION_LEVEL,
        dropna=False,
    ):
        row = calculate_row(group)

        total_level_rows.append(
            {
                "NIVEL_DE_FORMACIÓN": formation_level,
                "SECTOR": "Total",
                **row,
            }
        )

    total_levels = pd.DataFrame(total_level_rows)

    # --------------------------------------------------------
    # TOTAL GENERAL
    # --------------------------------------------------------

    general_row = calculate_row(df_grouped)

    total_general = pd.DataFrame(
        [
            {
                "NIVEL_DE_FORMACIÓN": "Total",
                "SECTOR": "",
                **general_row,
            }
        ]
    )

    # --------------------------------------------------------
    # UNIR RESULTADOS
    # --------------------------------------------------------

    result = pd.concat(
        [
            result,
            total_levels,
            total_general,
        ],
        ignore_index=True,
    )

    # --------------------------------------------------------
    # ORDENAR NIVELES
    # --------------------------------------------------------

    level_order = [
        "Maestría",
        "Doctorado",
    ]

    existing_levels = [
        level
        for level in level_order
        if level in result["NIVEL_DE_FORMACIÓN"].values
    ]

    other_levels = [
        level
        for level in result["NIVEL_DE_FORMACIÓN"].unique()
        if level not in existing_levels
        and level != "Total"
    ]

    final_level_order = existing_levels + other_levels + ["Total"]

    result["NIVEL_DE_FORMACIÓN"] = pd.Categorical(
        result["NIVEL_DE_FORMACIÓN"],
        categories=final_level_order,
        ordered=True,
    )

    # --------------------------------------------------------
    # ORDENAR SECTORES
    # --------------------------------------------------------

    result["_sector_order"] = result["SECTOR"].map(
        {
            "Privado": 0,
            "Oficial": 1,
            "Total": 2,
            "": 3,
        }
    ).fillna(4)

    result = result.sort_values(
        by=[
            "NIVEL_DE_FORMACIÓN",
            "_sector_order",
        ]
    )

    result = result.drop(
        columns="_sector_order"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # CONVERTIR A MULTIINDEX DE COLUMNAS
    # --------------------------------------------------------

    result = result[
        [
            "NIVEL_DE_FORMACIÓN",
            "SECTOR",
        ]
        + columns
    ]

    result.columns = pd.MultiIndex.from_tuples(
        [
            ("", "NIVEL DE FORMACIÓN"),
            ("", "SECTOR"),
            *columns,
        ]
    )

    return result


def build_table_1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye la Tabla 1: Oferta general.
    """
    return _build_aggregated_table(df)


def build_table_2_profundizacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye la Tabla 2A:
    Maestrías de profundización.
    """
    filtered = df[
        (df[FORMATION_LEVEL] == "Maestría")
        & (
            df[MASTER_TYPE]
            == "Maestría de profundización"
        )
    ].copy()

    return _build_aggregated_table(filtered, include_distance_virtual=False)


def build_table_2_investigacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye la Tabla 2B:
    Maestrías de investigación.
    """
    filtered = df[
        (df[FORMATION_LEVEL] == "Maestría")
        & (
            df[MASTER_TYPE]
            == "Maestría de investigación"
        )
    ].copy()

    return _build_aggregated_table(filtered, include_distance_virtual=False)


def build_table_3_valle(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye la Tabla 3:
    Oferta específica del Valle del Cauca.
    """
    valle = df[df[DEPARTMENT] == "Valle del Cauca"].copy()
    
    columns = [
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
        "NÚMERO_CRÉDITOS"
    ]
    
    return valle[columns]
