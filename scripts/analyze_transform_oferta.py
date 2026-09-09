import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from etl.oferta.ingest import load_oferta
from etl.oferta.clean import clean_oferta
from etl.oferta.schema import TEXT_COLUMNS


def main():
    ruta = Path("data/raw/oferta/oferta_simplificada.xlsx")

    print("[INFO] Cargando datos...")
    df_raw = load_oferta(ruta)

    print("[INFO] Aplicando limpieza...")
    df_clean = clean_oferta(df_raw)

    print("\n" + "=" * 70)
    print(" ANÁLISIS PARA TRANSFORMACIÓN - OFERTA")
    print("=" * 70)

    print(f"\nFilas: {len(df_clean)}")
    print(f"Columnas: {len(df_clean.columns)}")

    # ---------------------------------------------------------
    # 1. VALORES ÚNICOS DE COLUMNAS CATEGÓRICAS
    # ---------------------------------------------------------

    columnas_categoricas = [
        "CARÁCTER_ACADÉMICO",
        "SECTOR",
        "ESTADO_PROGRAMA",
        "RECONOCIMIENTO_DEL_MINISTERIO",
        "NIVEL_ACADÉMICO",
        "NIVEL_DE_FORMACIÓN",
        "MODALIDAD",
        "PERIODICIDAD",
        "DEPARTAMENTO_OFERTA_PROGRAMA",
    ]

    print("\n" + "=" * 70)
    print(" VALORES ÚNICOS")
    print("=" * 70)

    for columna in columnas_categoricas:

        if columna not in df_clean.columns:
            continue

        print(f"\n--- {columna} ---")

        valores = (
            df_clean[columna]
            .dropna()
            .astype(str)
            .value_counts()
        )

        print(f"Valores diferentes: {len(valores)}")
        print(valores.to_string())

    # ---------------------------------------------------------
    # 2. JUSTIFICACION
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print(" ANÁLISIS DE JUSTIFICACION")
    print("=" * 70)

    justificaciones = (
        df_clean["JUSTIFICACION"]
        .dropna()
        .astype(str)
        .value_counts()
    )

    print(f"\nValores diferentes: {len(justificaciones)}")
    print("\nPrimeros 30 valores:\n")

    print(justificaciones.head(30).to_string())

    # ---------------------------------------------------------
    # 3. EJEMPLOS PARA NORMALIZACIÓN
    # ---------------------------------------------------------

    columnas_normalizacion = [
        "NOMBRE_INSTITUCIÓN",
        "NOMBRE_DEL_PROGRAMA",
        "TITULO_OTORGADO",
        "DEPARTAMENTO_OFERTA_PROGRAMA",
        "MUNICIPIO_OFERTA_PROGRAMA",
    ]

    print("\n" + "=" * 70)
    print(" EJEMPLOS DE TEXTOS")
    print("=" * 70)

    for columna in columnas_normalizacion:

        print(f"\n--- {columna} ---")

        valores = (
            df_clean[columna]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .head(20)
        )

        for valor in valores:
            print(repr(valor))

    # ---------------------------------------------------------
    # 4. TIPOS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print(" TIPOS DE DATOS")
    print("=" * 70)

    print(df_clean.dtypes.to_string())


if __name__ == "__main__":
    main()
