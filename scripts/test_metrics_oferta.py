import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from services.oferta.metrics import (
    calculate_metrics,
    group_modality,
    build_table_1,
    build_table_2_profundizacion,
    build_table_2_investigacion,
)


DATA_PATH = "data/processed/oferta/oferta_procesada.parquet"


def load_data():
    return pd.read_parquet(DATA_PATH)


def test_calculate_metrics(df):
    metrics = calculate_metrics(df)

    assert set(metrics.keys()) == {
        "PROG",
        "INST",
        "MPIO",
        "DEPTO",
    }
    assert metrics["PROG"] == df["CÓDIGO_SNIES_DEL_PROGRAMA"].nunique()
    print("[OK] Cálculo de métricas")


def test_group_modality(df):
    df_grouped = group_modality(df)
    
    assert "MODALIDAD_AGRUPADA" in df_grouped.columns
    assert "MODALIDAD" in df_grouped.columns
    assert "Presencial Virtual" in df_grouped["MODALIDAD_AGRUPADA"].values
    
    print("[OK] Agrupación de modalidades")


def test_group_modality_coverage(df):
    df_grouped = group_modality(df)
    
    assert df_grouped["MODALIDAD_AGRUPADA"].notna().sum() == df["MODALIDAD"].notna().sum()
    
    df_fake = df.copy()
    df_fake.loc[df_fake.index[0], "MODALIDAD"] = "Modalidad Inventada"
    
    try:
        group_modality(df_fake)
        assert False, "Debería haber lanzado ValueError"
    except ValueError as e:
        assert "Modalidad Inventada" in str(e)
        
    print("[OK] Cobertura de agrupación de modalidades")


def test_table_1(df):
    result = build_table_1(df)

    assert isinstance(result.columns, pd.MultiIndex)
    assert ("", "NIVEL DE FORMACIÓN") in result.columns
    assert ("", "SECTOR") in result.columns
    assert "Total" in result.columns.levels[0]

    assert len(result) > 0
    assert (result[("", "NIVEL DE FORMACIÓN")] == "Total").any()

    print("[OK] Tabla 1 (formato horizontal y Total)")


def test_table_2_profundizacion(df):
    result = build_table_2_profundizacion(df)

    assert len(result) > 0
    niveles = result.loc[result[("", "SECTOR")] != "", ("", "NIVEL DE FORMACIÓN")]
    assert (niveles == "Maestría").all()
    assert (result[("", "NIVEL DE FORMACIÓN")] == "Total").any()

    print("[OK] Tabla 2A - Maestría de profundización (horizontal)")


def test_table_2_investigacion(df):
    result = build_table_2_investigacion(df)

    assert len(result) > 0
    niveles = result.loc[result[("", "SECTOR")] != "", ("", "NIVEL DE FORMACIÓN")]
    assert (niveles == "Maestría").all()
    assert (result[("", "NIVEL DE FORMACIÓN")] == "Total").any()

    print("[OK] Tabla 2B - Maestría de investigación (horizontal)")


def test_master_tables_do_not_overlap(df):
    profundizacion = build_table_2_profundizacion(df)
    investigacion = build_table_2_investigacion(df)

    prog_profundizacion = set(
        df.loc[
            df["TIPO_MAESTRIA"] == "Maestría de profundización",
            "CÓDIGO_SNIES_DEL_PROGRAMA"
        ]
    )

    prog_investigacion = set(
        df.loc[
            df["TIPO_MAESTRIA"] == "Maestría de investigación",
            "CÓDIGO_SNIES_DEL_PROGRAMA"
        ]
    )

    assert prog_profundizacion.isdisjoint(prog_investigacion)

    print("[OK] Tablas de maestría no se superponen")


def test_metrics_are_non_negative(df):
    metrics = calculate_metrics(df)

    assert all(
        value >= 0
        for value in metrics.values()
    )

    print("[OK] Métricas no negativas")


def main():
    df = load_data()

    print("=" * 60)
    print("PRUEBAS DE MÉTRICAS - OFERTA (V2)")
    print("=" * 60)

    test_calculate_metrics(df)
    test_group_modality(df)
    test_group_modality_coverage(df)
    test_table_1(df)
    test_table_2_profundizacion(df)
    test_table_2_investigacion(df)
    test_master_tables_do_not_overlap(df)
    test_metrics_are_non_negative(df)

    print("=" * 60)
    print("[OK] TODAS LAS PRUEBAS DE MÉTRICAS PASARON")
    print("=" * 60)


if __name__ == "__main__":
    main()
