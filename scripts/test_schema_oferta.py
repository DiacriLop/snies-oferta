import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from etl.oferta.schema import validate_schema, EXPECTED_COLUMNS

def print_result(name, result):
    print(f"\n{'='*60}")
    print(f" CASO: {name}")
    print(f"{'='*60}")
    print(f"Estado de Validación Global: {'[APROBADO]' if result['valid'] else '[RECHAZADO]'}")
    
    if not result['valid']:
        if not result['columns']['valid']: 
            print("   -> Falló estructura de columnas:")
            if result['columns']['missing_columns']:
                print(f"      Faltan: {result['columns']['missing_columns']}")
            if result['columns']['unexpected_columns']:
                print(f"      Sobran: {result['columns']['unexpected_columns']}")
            if not result['columns']['correct_order']:
                print("      El orden está mal.")
                
        if not result['types']['valid']: 
            print("   -> Falló tipos de datos:")
            for c, err in result['types']['type_errors'].items():
                print(f"      {c}: {err}")
                
        if not result['identifiers']['valid']: 
            print("   -> Falló identificadores principales:")
            for c, err in result['identifiers']['identifier_errors'].items():
                print(f"      {c}: {err}")

def run_tests():
    print("Iniciando pruebas controladas sobre schema.py...")
    
    # 1. Caso base (Correcto)
    df_base = pd.DataFrame(columns=EXPECTED_COLUMNS)
    # Agregar fila válida
    df_base.loc[0] = ["123", "INST", "UNIV", "PRIV", "456", "PROG", "TIT", "ACT", "JUS", "REC", 
                      pd.Timestamp("2020-01-01"), "C1", "C2", "C3", "A1", "N1", "NIV", "FOR", "MOD", 
                      120, 8, "SEM", "DEP", "MUN", 5000000.0]
    
    # Casting a los tipos correctos para evitar object general de pandas
    df_base["NÚMERO_CRÉDITOS"] = df_base["NÚMERO_CRÉDITOS"].astype(int)
    df_base["NÚMERO_PERIODOS_DE_DURACIÓN"] = df_base["NÚMERO_PERIODOS_DE_DURACIÓN"].astype(int)
    df_base["COSTO_MATRÍCULA_ESTUD_NUEVOS"] = df_base["COSTO_MATRÍCULA_ESTUD_NUEVOS"].astype(float)
    df_base["FECHA_DE_RESOLUCIÓN"] = pd.to_datetime(df_base["FECHA_DE_RESOLUCIÓN"])

    res = validate_schema(df_base)
    print_result("1. Archivo Perfecto", res)

    # 2. Columna faltante
    df_missing = df_base.drop(columns=["SECTOR"])
    res = validate_schema(df_missing)
    print_result("2. Columna Faltante (Se eliminó 'SECTOR')", res)

    # 3. Columna extra
    df_extra = df_base.copy()
    df_extra["COLUMNA_FANTASMA"] = "Hola"
    res = validate_schema(df_extra)
    print_result("3. Columna Extra (Se agregó 'COLUMNA_FANTASMA')", res)

    # 4. Columna desordenada
    df_reordered = df_base.copy()
    cols = list(df_reordered.columns)
    cols[0], cols[1] = cols[1], cols[0] # Intercambiar las primeras dos
    df_reordered = df_reordered[cols]
    res = validate_schema(df_reordered)
    print_result("4. Columnas Desordenadas", res)

    # 5. Tipo incorrecto
    df_bad_type = df_base.copy()
    df_bad_type["NÚMERO_CRÉDITOS"] = df_bad_type["NÚMERO_CRÉDITOS"].astype(str)
    df_bad_type.loc[0, "NÚMERO_CRÉDITOS"] = "Ciento Veinte" # Forzar texto en numérica
    res = validate_schema(df_bad_type)
    print_result("5. Tipo Incorrecto (NÚMERO_CRÉDITOS viene como texto)", res)

    # 6. Identificador completamente vacío
    df_bad_id = df_base.copy()
    df_bad_id["CÓDIGO_INSTITUCIÓN"] = np.nan
    res = validate_schema(df_bad_id)
    print_result("6. Identificador Vacío (CÓDIGO_INSTITUCIÓN 100% nulo)", res)

if __name__ == "__main__":
    run_tests()
