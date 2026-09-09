"""Contrato de datos (Schema) para el módulo de Oferta Académica.
Este módulo se encarga EXCLUSIVAMENTE de validar la estructura del archivo entrante 
(columnas, orden, tipos de datos e identificadores). 
No aplica limpieza, ni transformación, ni reglas de negocio.
"""
import pandas as pd

EXPECTED_COLUMNS = [
    "CÓDIGO_INSTITUCIÓN",
    "NOMBRE_INSTITUCIÓN",
    "CARÁCTER_ACADÉMICO",
    "SECTOR",
    "CÓDIGO_SNIES_DEL_PROGRAMA",
    "NOMBRE_DEL_PROGRAMA",
    "TITULO_OTORGADO",
    "ESTADO_PROGRAMA",
    "JUSTIFICACION",
    "RECONOCIMIENTO_DEL_MINISTERIO",
    "FECHA_DE_RESOLUCIÓN",
    "CINE_F_2013_AC_CAMPO_AMPLIO",
    "CINE_F_2013_AC_CAMPO_ESPECÍFIC",
    "CINE_F_2013_AC_CAMPO_DETALLADO",
    "ÁREA_DE_CONOCIMIENTO",
    "NÚCLEO_BÁSICO_DEL_CONOCIMIENTO",
    "NIVEL_ACADÉMICO",
    "NIVEL_DE_FORMACIÓN",
    "MODALIDAD",
    "NÚMERO_CRÉDITOS",
    "NÚMERO_PERIODOS_DE_DURACIÓN",
    "PERIODICIDAD",
    "DEPARTAMENTO_OFERTA_PROGRAMA",
    "MUNICIPIO_OFERTA_PROGRAMA",
    "COSTO_MATRÍCULA_ESTUD_NUEVOS",
]

IDENTIFIER_COLUMNS = [
    "CÓDIGO_INSTITUCIÓN",
    "CÓDIGO_SNIES_DEL_PROGRAMA",
]

TEXT_COLUMNS = [
    "NOMBRE_INSTITUCIÓN",
    "CARÁCTER_ACADÉMICO",
    "SECTOR",
    "NOMBRE_DEL_PROGRAMA",
    "TITULO_OTORGADO",
    "ESTADO_PROGRAMA",
    "JUSTIFICACION",
    "RECONOCIMIENTO_DEL_MINISTERIO",
    "CINE_F_2013_AC_CAMPO_AMPLIO",
    "CINE_F_2013_AC_CAMPO_ESPECÍFIC",
    "CINE_F_2013_AC_CAMPO_DETALLADO",
    "ÁREA_DE_CONOCIMIENTO",
    "NÚCLEO_BÁSICO_DEL_CONOCIMIENTO",
    "NIVEL_ACADÉMICO",
    "NIVEL_DE_FORMACIÓN",
    "MODALIDAD",
    "PERIODICIDAD",
    "DEPARTAMENTO_OFERTA_PROGRAMA",
    "MUNICIPIO_OFERTA_PROGRAMA",
]

NUMERIC_COLUMNS = [
    "NÚMERO_CRÉDITOS",
    "NÚMERO_PERIODOS_DE_DURACIÓN",
    "COSTO_MATRÍCULA_ESTUD_NUEVOS",
]

DATE_COLUMNS = [
    "FECHA_DE_RESOLUCIÓN",
]

def validate_columns(df: pd.DataFrame) -> dict:
    """
    Valida que el DataFrame contenga exactamente las 25 columnas esperadas
    y en el orden correcto.
    """
    actual_columns = list(df.columns)

    missing_columns = [
        column for column in EXPECTED_COLUMNS if column not in actual_columns
    ]
    unexpected_columns = [
        column for column in actual_columns if column not in EXPECTED_COLUMNS
    ]
    correct_order = actual_columns == EXPECTED_COLUMNS

    return {
        "valid": not missing_columns and not unexpected_columns and correct_order,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "correct_order": correct_order,
    }

def validate_types(df: pd.DataFrame) -> dict:
    """
    Verifica que las columnas numéricas sean interpretables como números 
    y las de fechas como datetimes. (Las de texto se ignoran estructuralmente).
    """
    errors = {}
    
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors[col] = f"Se esperaba numérico, pero es {df[col].dtype}"
                
    for col in DATE_COLUMNS:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                errors[col] = f"Se esperaba fecha, pero es {df[col].dtype}"
                
    return {
        "valid": len(errors) == 0,
        "type_errors": errors
    }

def validate_identifiers(df: pd.DataFrame) -> dict:
    """
    Comprueba que las columnas que sirven como llaves primarias (identificadores)
    existan y no estén completamente vacías.
    """
    errors = {}
    
    for col in IDENTIFIER_COLUMNS:
        if col in df.columns:
            nulos = df[col].isnull().sum()
            if nulos == len(df):
                errors[col] = "Columna identificadora está completamente vacía"
            elif nulos > 0:
                errors[col] = f"Contiene {nulos} valores nulos"
                
    return {
        "valid": len(errors) == 0,
        "identifier_errors": errors
    }

def validate_schema(df: pd.DataFrame) -> dict:
    """
    Función maestra que ejecuta todas las validaciones de esquema de Oferta.
    Devuelve un diccionario detallado con el estado de cada prueba.
    """
    column_result = validate_columns(df)
    type_result = validate_types(df)
    identifier_result = validate_identifiers(df)

    return {
        "valid": column_result["valid"] and type_result["valid"] and identifier_result["valid"],
        "rows": len(df),
        "columns": column_result,
        "types": type_result,
        "identifiers": identifier_result
    }

if __name__ == "__main__":
    print("[INFO] Cargando archivo de Excel para validar el esquema...")
    df_test = pd.read_excel(r'data/raw/oferta/oferta_simplificada.xlsx')
    
    print("\n[TEST] Ejecutando validación de esquema...")
    resultado = validate_schema(df_test)
    
    print("\n" + "="*40)
    print(" REPORTE DE VALIDACIÓN DE ESQUEMA")
    print("="*40)
    
    if resultado["valid"]:
        print("\n[OK] ESTADO FINAL: El archivo cumple con toda la estructura requerida.")
    else:
        print("\n[!] ESTADO FINAL: El archivo presenta problemas de estructura.")
        
    print(f"       -> Total de registros (filas) leídos: {resultado['rows']}")
        
    print("\n1. Análisis de Columnas:")
    cols = resultado["columns"]
    if cols["valid"]:
        print("   - [OK] Las 25 columnas están presentes y en el orden correcto.")
    else:
        if cols["missing_columns"]:
            print(f"   - [ERROR] Faltan columnas: {', '.join(cols['missing_columns'])}")
        if cols["unexpected_columns"]:
            print(f"   - [ERROR] Sobran columnas: {', '.join(cols['unexpected_columns'])}")
        if not cols["correct_order"] and not cols["missing_columns"] and not cols["unexpected_columns"]:
            print("   - [ERROR] Las columnas están desordenadas respecto a la plantilla.")
            
    print("\n2. Análisis de Tipos (Numéricos y Fechas):")
    types = resultado["types"]
    if types["valid"]:
        print("   - [OK] Todos los tipos de datos requeridos son compatibles.")
    else:
        for col, err in types["type_errors"].items():
            print(f"   - [ERROR] {col}: {err}")
            
    print("\n3. Análisis de Identificadores Principales:")
    ids = resultado["identifiers"]
    if ids["valid"]:
        print("   - [OK] Los identificadores principales están completos.")
    else:
        for col, err in ids["identifier_errors"].items():
            print(f"   - [ERROR] {col}: {err}")
            
    print("\n" + "="*40)