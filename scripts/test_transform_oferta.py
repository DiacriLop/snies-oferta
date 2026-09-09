import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from etl.oferta.ingest import load_oferta
from etl.oferta.clean import clean_oferta
from etl.oferta.transform import transform_oferta


def main():

    ruta = Path("data/raw/oferta/oferta_simplificada.xlsx")

    print("[INFO] Cargando datos...")
    df_raw = load_oferta(ruta)

    print("[INFO] Aplicando limpieza...")
    df_clean = clean_oferta(df_raw)

    print("[INFO] Aplicando transformación...")
    df_transformado = transform_oferta(df_clean)

    print("\n" + "=" * 70)
    print(" PRUEBAS DE TRANSFORMACIÓN - OFERTA")
    print("=" * 70)

    # 1. Verificar cantidad de registros
    assert len(df_transformado) == len(df_raw)

    print("[OK] No se perdieron registros.")

    # 2. Verificar cantidad de columnas
    assert len(df_transformado.columns) > len(df_raw.columns)

    print("[OK] Se agregaron columnas auxiliares.")

    # 3. Verificar existencia de columnas normalizadas
    assert "NOMBRE_DEL_PROGRAMA_NORMALIZADO" in df_transformado.columns
    assert "NOMBRE_INSTITUCIÓN_NORMALIZADO" in df_transformado.columns

    print("[OK] Las columnas normalizadas existen.")

    # 4. Verificar que las columnas originales siguen existiendo
    assert "NOMBRE_DEL_PROGRAMA" in df_transformado.columns
    assert "NOMBRE_INSTITUCIÓN" in df_transformado.columns

    print("[OK] Las columnas originales se conservaron.")

    # 5. Verificar que el original no fue modificado
    pd.testing.assert_frame_equal(
        df_raw,
        load_oferta(ruta)
    )

    print("[OK] El DataFrame original permanece intacto.")

    # 6. Mostrar ejemplos
    print("\n" + "=" * 70)
    print(" EJEMPLOS DE NORMALIZACIÓN")
    print("=" * 70)

    columnas = [
        "NOMBRE_DEL_PROGRAMA",
        "NOMBRE_DEL_PROGRAMA_NORMALIZADO",
        "NOMBRE_INSTITUCIÓN",
        "NOMBRE_INSTITUCIÓN_NORMALIZADO",
    ]

    print(
        df_transformado[columnas]
        .head(10)
        .to_string(index=False)
    )

    # 7. Verificar clasificación de maestrías

    assert "TIPO_MAESTRIA" in df_transformado.columns

    print("[OK] La columna TIPO_MAESTRIA existe.")

    maestrias = df_transformado[
        df_transformado["NIVEL_DE_FORMACIÓN"] == "Maestría"
    ]

    valores_maestria = set(maestrias["TIPO_MAESTRIA"].dropna().unique())

    valores_esperados = {
        "Maestría de profundización",
        "Maestría de investigación",
        "NO APLICA"
    }

    assert valores_maestria.issubset(valores_esperados)

    print("[OK] Las maestrías fueron clasificadas correctamente.")

    # 8. Verificar que otros niveles no sean clasificados como maestría

    no_maestrias = df_transformado[
        df_transformado["NIVEL_DE_FORMACIÓN"] != "Maestría"
    ]

    assert (
        no_maestrias["TIPO_MAESTRIA"] == "NO APLICA"
    ).all()

    print("[OK] Los programas que no son maestría quedaron como NO APLICA.")

    print("\n" + "=" * 70)
    print(" DISTRIBUCIÓN DE TIPO_MAESTRIA")
    print("=" * 70)

    print(
        df_transformado["TIPO_MAESTRIA"]
        .value_counts()
        .to_string()
    )

    print("\n[OK] TODAS LAS PRUEBAS DE TRANSFORMACIÓN PASARON.")


if __name__ == "__main__":
    main()
