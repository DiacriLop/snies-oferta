"""Módulo de limpieza para los datos de Oferta Académica.

Se encarga de realizar limpiezas superficiales sobre los datos,
principalmente relacionadas con espacios en columnas de texto.

No realiza normalización semántica, corrección de datos corruptos,
eliminación de duplicados ni aplicación de reglas de negocio.
"""

import re
import pandas as pd

from etl.oferta.schema import TEXT_COLUMNS


def clean_text(value):
    """
    Limpia espacios innecesarios de un valor de texto.

    - Elimina espacios al inicio y al final.
    - Reemplaza múltiples espacios consecutivos por uno.
    - Conserva tildes, mayúsculas y contenido original.

    Args:
        value: Valor que se desea limpiar.

    Returns:
        El valor limpio.
    """

    if not isinstance(value, str):
        return value

    value = value.strip()
    value = re.sub(r"\s+", " ", value)

    return value


def clean_oferta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia las columnas de texto del DataFrame de Oferta.

    Args:
        df: DataFrame con los datos de Oferta.

    Returns:
        DataFrame limpio.
    """

    df_clean = df.copy()

    for column in TEXT_COLUMNS:
        if column in df_clean.columns:
            df_clean[column] = df_clean[column].apply(clean_text)

    return df_clean

if __name__ == "__main__":
    from pathlib import Path
    from etl.oferta.ingest import load_oferta
    
    print("[INFO] Cargando archivo de Excel para prueba de limpieza...")
    ruta = Path("data/raw/oferta/oferta_simplificada.xlsx")
    
    try:
        df_raw = load_oferta(ruta)
        print("\n[TEST] Ejecutando limpieza sobre el DataFrame crudo...")
        df_clean = clean_oferta(df_raw)
        
        print("\n[OK] Limpieza exitosa. Muestra de las primeras 3 filas (Columnas de texto limpias):")
        print(df_clean[TEXT_COLUMNS].head(3))
    except Exception as e:
        print(f"\n[!] Error durante la prueba: {e}")
