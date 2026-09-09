import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from services.oferta.queries import (
    get_programs_by_department,
    search_by_program_name,
    search_by_keywords,
    OFERTA_COLUMNS,
)


DATA_PATH = "data/processed/oferta/oferta_procesada.parquet"


def load_data():
    return pd.read_parquet(DATA_PATH)


def test_get_programs_by_department(df):
    result = get_programs_by_department(df, "Valle del Cauca")

    # 1. Verificar que las columnas son exactamente las 11 esperadas
    assert list(result.columns) == OFERTA_COLUMNS
    assert len(result.columns) == 11
    
    # 2. Verificar que hay registros
    assert len(result) > 0

    # 3. Verificar cantidad de registros contra el df original
    expected_len = len(df[df["DEPARTAMENTO_OFERTA_PROGRAMA"] == "Valle del Cauca"])
    assert len(result) == expected_len

    # 4. Revisar fechas
    assert "FECHA_DE_RESOLUCIÓN" in result.columns
    # Debe existir al menos alguna fecha válida
    assert result["FECHA_DE_RESOLUCIÓN"].notna().any()

    # 5. La modalidad debe ser la original de SNIES
    assert "MODALIDAD" in result.columns
    assert "MODALIDAD_AGRUPADA" not in result.columns

    print(f"[OK] Tabla 3 (Valle del Cauca) generada con {len(result)} registros")
    print(f"[OK] 11 columnas exactas conservadas")


def test_search_by_program_name(df):
    # Prueba ignorando tildes y mayúsculas
    result = search_by_program_name(df, "ingenieria")
    assert len(result) > 0
    # Verificamos que contenga 'ingenieria'
    assert result["NOMBRE_DEL_PROGRAMA_NORMALIZADO"].str.contains("ingenieria").all()
    print(f"[OK] Búsqueda por nombre ('ingenieria') encontró {len(result)} registros")

    # Búsqueda vacía
    result_empty = search_by_program_name(df, "   ")
    assert len(result_empty) == len(df)
    print(f"[OK] Búsqueda vacía por nombre devuelve DataFrame original")


def test_search_by_keywords(df):
    # Prueba AND
    result_and = search_by_keywords(df, "ingenieria sistemas", operator="AND")
    assert len(result_and) >= 0
    if len(result_and) > 0:
        assert result_and["NOMBRE_DEL_PROGRAMA_NORMALIZADO"].str.contains("ingenieria").all()
        assert result_and["NOMBRE_DEL_PROGRAMA_NORMALIZADO"].str.contains("sistemas").all()
    print(f"[OK] Búsqueda por keywords (AND) encontró {len(result_and)} registros")

    # Prueba OR
    result_or = search_by_keywords(df, "ingenieria medicina", operator="OR")
    assert len(result_or) > 0
    mask = result_or["NOMBRE_DEL_PROGRAMA_NORMALIZADO"].str.contains("ingenieria") | \
           result_or["NOMBRE_DEL_PROGRAMA_NORMALIZADO"].str.contains("medicina")
    assert mask.all()
    print(f"[OK] Búsqueda por keywords (OR) encontró {len(result_or)} registros")

    # Prueba cadena vacía
    result_empty = search_by_keywords(df, "   ")
    assert len(result_empty) == len(df)
    print(f"[OK] Búsqueda vacía por keywords devuelve DataFrame original")

    # Prueba operador inválido
    try:
        search_by_keywords(df, "ingenieria", operator="INVALID")
        assert False, "Debería haber lanzado ValueError"
    except ValueError:
        pass
    print("[OK] Excepción lanzada correctamente al pasar un operador inválido")


def test_original_dataframe_not_modified(df):
    original_shape = df.shape
    original_columns = df.columns.tolist()

    get_programs_by_department(df, "Valle del Cauca")
    search_by_program_name(df, "ingenieria")
    search_by_keywords(df, "ingenieria sistemas", operator="AND")

    assert df.shape == original_shape
    assert df.columns.tolist() == original_columns

    print("[OK] DataFrame original permanece intacto tras todas las consultas")


def main():
    df = load_data()

    print("=" * 60)
    print("PRUEBAS DE QUERIES - OFERTA")
    print("=" * 60)

    test_get_programs_by_department(df)
    test_search_by_program_name(df)
    test_search_by_keywords(df)
    test_original_dataframe_not_modified(df)

    print("=" * 60)
    print("[OK] TODAS LAS PRUEBAS DE QUERIES PASARON")
    print("=" * 60)


if __name__ == "__main__":
    main()
