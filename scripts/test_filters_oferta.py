import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

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


DATA_PATH = "data/processed/oferta/oferta_procesada.parquet"


def load_data():
    return pd.read_parquet(DATA_PATH)


def test_filter_by_sector(df):
    result = filter_by_sector(df, "Privado")

    assert len(result) > 0
    assert result["SECTOR"].eq("Privado").all()

    print("[OK] Filtro por sector")


def test_filter_by_formation_level(df):
    result = filter_by_formation_level(df, "Maestría")

    assert len(result) > 0
    assert result["NIVEL_DE_FORMACIÓN"].eq("Maestría").all()

    print("[OK] Filtro por nivel de formación")


def test_filter_by_modality(df):
    result = filter_by_modality(df, "Presencial")

    assert len(result) > 0
    assert result["MODALIDAD"].eq("Presencial").all()

    print("[OK] Filtro por modalidad")


def test_filter_by_department(df):
    result = filter_by_department(df, "Valle del Cauca")

    assert len(result) > 0
    assert result["DEPARTAMENTO_OFERTA_PROGRAMA"].eq(
        "Valle del Cauca"
    ).all()

    print("[OK] Filtro por departamento")


def test_filter_by_municipality(df):
    municipality = (
        df["MUNICIPIO_OFERTA_PROGRAMA"]
        .dropna()
        .iloc[0]
    )

    result = filter_by_municipality(df, municipality)

    assert len(result) > 0
    assert result["MUNICIPIO_OFERTA_PROGRAMA"].eq(
        municipality
    ).all()

    print("[OK] Filtro por municipio")


def test_filter_by_institution(df):
    institution = (
        df["NOMBRE_INSTITUCIÓN"]
        .dropna()
        .iloc[0]
    )

    result = filter_by_institution(df, institution)

    assert len(result) > 0
    assert result["NOMBRE_INSTITUCIÓN"].eq(
        institution
    ).all()

    print("[OK] Filtro por institución")


def test_filter_by_program_state(df):
    result = filter_by_program_state(df, "Activo")

    assert len(result) > 0
    assert result["ESTADO_PROGRAMA"].eq("Activo").all()

    print("[OK] Filtro por estado del programa")


def test_filter_by_recognition(df):
    result = filter_by_recognition(
        df,
        "Registro calificado"
    )

    assert len(result) > 0
    assert result["RECONOCIMIENTO_DEL_MINISTERIO"].eq(
        "Registro calificado"
    ).all()

    print("[OK] Filtro por reconocimiento")


def test_filter_by_academic_character(df):
    result = filter_by_academic_character(
        df,
        "Universidad"
    )

    assert len(result) > 0
    assert result["CARÁCTER_ACADÉMICO"].eq(
        "Universidad"
    ).all()

    print("[OK] Filtro por carácter académico")


def test_filter_by_master_type(df):
    result = filter_by_master_type(
        df,
        "Maestría de profundización"
    )

    assert len(result) > 0
    assert result["TIPO_MAESTRIA"].eq(
        "Maestría de profundización"
    ).all()

    print("[OK] Filtro por tipo de maestría")


def test_original_dataframe_not_modified(df):
    original_shape = df.shape
    original_columns = df.columns.tolist()

    filter_by_sector(df, "Privado")
    filter_by_formation_level(df, "Maestría")
    filter_by_department(df, "Valle del Cauca")

    assert df.shape == original_shape
    assert df.columns.tolist() == original_columns

    print("[OK] DataFrame original permanece intacto")


def main():
    df = load_data()

    print("=" * 60)
    print("PRUEBAS DE FILTROS - OFERTA")
    print("=" * 60)

    test_filter_by_sector(df)
    test_filter_by_formation_level(df)
    test_filter_by_modality(df)
    test_filter_by_department(df)
    test_filter_by_municipality(df)
    test_filter_by_institution(df)
    test_filter_by_program_state(df)
    test_filter_by_recognition(df)
    test_filter_by_academic_character(df)
    test_filter_by_master_type(df)
    test_original_dataframe_not_modified(df)

    print("=" * 60)
    print("[OK] TODAS LAS PRUEBAS DE FILTROS PASARON")
    print("=" * 60)


if __name__ == "__main__":
    main()
