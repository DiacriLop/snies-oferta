import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from etl.oferta.ingest import load_oferta
from etl.oferta.clean import clean_oferta
from etl.oferta.transform import transform_oferta


def main():

    ruta_raw = Path("data/raw/oferta/oferta_simplificada.xlsx")
    ruta_processed = Path(
        "data/processed/oferta/oferta_procesada.parquet"
    )

    print("[INFO] Cargando archivo original...")
    df_raw = load_oferta(ruta_raw)

    print("[INFO] Aplicando limpieza...")
    df_clean = clean_oferta(df_raw)

    print("[INFO] Aplicando transformación...")
    df_processed = transform_oferta(df_clean)

    print("[INFO] Validando resultado...")

    if len(df_processed) != len(df_raw):
        raise ValueError(
            "La transformación modificó la cantidad de registros."
        )

    if len(df_processed) < len(df_raw):
        raise ValueError(
            "Se perdieron registros durante el procesamiento."
        )

    ruta_processed.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("[INFO] Guardando archivo procesado...")

    df_processed.to_parquet(
        ruta_processed,
        index=False
    )

    print("\n" + "=" * 70)
    print(" PROCESAMIENTO DE OFERTA COMPLETADO")
    print("=" * 70)

    print(f"Filas: {len(df_processed)}")
    print(f"Columnas: {len(df_processed.columns)}")
    print(f"Archivo: {ruta_processed}")

    print("\n[OK] Archivo procesado generado correctamente.")


if __name__ == "__main__":
    main()
