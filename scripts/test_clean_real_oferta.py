import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from etl.oferta.ingest import load_oferta
from etl.oferta.clean import clean_oferta
from etl.oferta.schema import TEXT_COLUMNS


def main():
    ruta = Path("data/raw/oferta/oferta_simplificada.xlsx")

    print("[INFO] Cargando datos originales...")
    df_raw = load_oferta(ruta)

    print(f"[INFO] Filas: {len(df_raw)}")
    print(f"[INFO] Columnas: {len(df_raw.columns)}")

    print("\n[INFO] Aplicando limpieza...")
    df_clean = clean_oferta(df_raw)

    print("[OK] Limpieza aplicada.")

    print("\n" + "=" * 60)
    print(" COMPARACIÓN RAW VS CLEAN")
    print("=" * 60)

    cambios = 0

    for column in TEXT_COLUMNS:
        if column not in df_raw.columns:
            continue

        diferencias = (df_raw[column] != df_clean[column]).sum()

        if diferencias > 0:
            print(f"[CAMBIOS] {column}: {diferencias}")

            cambios += diferencias

    print("-" * 60)
    print(f"[INFO] Total de celdas modificadas: {cambios}")

    print("\n[INFO] Comprobando que las tildes siguen presentes...")

    ejemplos = [
        "NOMBRE_INSTITUCIÓN",
        "NOMBRE_DEL_PROGRAMA",
        "TITULO_OTORGADO",
    ]

    for column in ejemplos:
        if column in df_clean.columns:
            valores = df_clean[column].dropna().astype(str)

            contiene_tildes = valores.str.contains(
                r"[áéíóúÁÉÍÓÚñÑ]",
                regex=True
            ).any()

            print(
                f"[OK] {column}: "
                f"{'contiene tildes' if contiene_tildes else 'no se encontraron tildes'}"
            )

    print("\n[INFO] Comprobando que el DataFrame original no fue modificado...")

    if df_raw.equals(load_oferta(ruta)):
        print("[OK] El DataFrame original permanece intacto.")
    else:
        print("[FALLO] El DataFrame original fue modificado.")


if __name__ == "__main__":
    main()
