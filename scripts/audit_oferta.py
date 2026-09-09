import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
import re

def auditoria_profunda(file_path=r"C:\Users\DianaC\Desktop\Monitorias\SNIES_YOP\SNIES\data\raw\oferta\oferta_simplificada.xlsx"):
    print("=== AUDITORÍA PROFUNDA DE DATOS ===")
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return

    # 0. Información general
    print("\n➤ 0. INFORMACIÓN GENERAL")
    print(f"  - Cantidad de filas: {df.shape[0]:,}")
    print(f"  - Cantidad de columnas: {df.shape[1]}")
    
    columnas_esperadas = [
        'CÓDIGO_INSTITUCIÓN', 'NOMBRE_INSTITUCIÓN', 'CARÁCTER_ACADÉMICO', 'SECTOR', 
        'CÓDIGO_SNIES_DEL_PROGRAMA', 'NOMBRE_DEL_PROGRAMA', 'TITULO_OTORGADO', 
        'ESTADO_PROGRAMA', 'JUSTIFICACION', 'RECONOCIMIENTO_DEL_MINISTERIO', 
        'FECHA_DE_RESOLUCIÓN', 'CINE_F_2013_AC_CAMPO_AMPLIO', 
        'CINE_F_2013_AC_CAMPO_ESPECÍFIC', 'CINE_F_2013_AC_CAMPO_DETALLADO', 
        'ÁREA_DE_CONOCIMIENTO', 'NÚCLEO_BÁSICO_DEL_CONOCIMIENTO', 'NIVEL_ACADÉMICO', 
        'NIVEL_DE_FORMACIÓN', 'MODALIDAD', 'NÚMERO_CRÉDITOS', 
        'NÚMERO_PERIODOS_DE_DURACIÓN', 'PERIODICIDAD', 'DEPARTAMENTO_OFERTA_PROGRAMA', 
        'MUNICIPIO_OFERTA_PROGRAMA', 'COSTO_MATRÍCULA_ESTUD_NUEVOS'
    ]
    
    columnas_actuales = list(df.columns)
    
    if df.shape[1] == len(columnas_esperadas):
        print(f"  [✓] Validación exitosa: El archivo tiene exactamente {len(columnas_esperadas)} columnas.")
    else:
        print(f"  [!] ADVERTENCIA: Se esperaban {len(columnas_esperadas)} columnas, pero se encontraron {df.shape[1]}.")

    if columnas_actuales == columnas_esperadas:
        print("  [✓] ORDEN DE COLUMNAS: SÍ, el orden y los nombres coinciden exactamente.")
    else:
        print("  [!] ORDEN DE COLUMNAS: NO, el orden o los nombres no coinciden.")
        
        columnas_faltantes = set(columnas_esperadas) - set(columnas_actuales)
        columnas_sobrantes = set(columnas_actuales) - set(columnas_esperadas)
        
        if columnas_faltantes:
            print(f"    * Columnas faltantes: {', '.join(columnas_faltantes)}")
        if columnas_sobrantes:
            print(f"    * Columnas no esperadas: {', '.join(columnas_sobrantes)}")
            
        if not columnas_faltantes and not columnas_sobrantes:
            diferencias = []
            for i, (esperada, actual) in enumerate(zip(columnas_esperadas, columnas_actuales)):
                if esperada != actual:
                    diferencias.append(f"Posición {i}: esperada '{esperada}', actual '{actual}'")
            if diferencias:
                print(f"    * {len(diferencias)} columnas están en posiciones incorrectas:")
                for diff in diferencias[:5]:
                    print(f"      - {diff}")
                if len(diferencias) > 5:
                    print(f"      - ... y {len(diferencias) - 5} más.")

    # 1. Tipos de Datos y Consistencia
    print("\n➤ 1. TIPOS DE DATOS")
    print(df.dtypes.value_counts().to_string())

    # 2. Análisis de Calidad de Texto (Texto Específico)
    print("\n➤ 2. AUDITORÍA ESPECÍFICA DE TEXTO")
    cols_obj = df.select_dtypes(include=['object', 'string']).columns  # type: ignore
    
    # Patrones sospechosos
    patron_espacios_ext = r'^\s+|\s+$'
    patron_multiespacio = r'\s{2,}'
    patron_saltos = r'[\n\r]'
    patron_corrupto = r'[¿\ufffd]'
    nulos_texto = ['N/A', 'NA', '-', 'NULL', 'SIN INFORMACIÓN', '', 'NO APLICA', 'NO DISPONIBLE', 'NONE']
    
    for col in cols_obj:
        serie_str = df[col].astype(str)
        
        espacios_ext = serie_str.str.contains(patron_espacios_ext, regex=True).sum()
        multi_espacios = serie_str.str.contains(patron_multiespacio, regex=True).sum()
        saltos = serie_str.str.contains(patron_saltos, regex=True).sum()
        corruptos = serie_str.str.contains(patron_corrupto, flags=re.IGNORECASE, regex=True).sum()
        falsos_nulos = serie_str.str.strip().str.upper().isin(nulos_texto).sum()
        
        if any([espacios_ext, multi_espacios, saltos, corruptos, falsos_nulos]):
            print(f"  - Columna '{col}':")
            if espacios_ext: print(f"    * {espacios_ext} con espacios inicio/fin.")
            if multi_espacios: print(f"    * {multi_espacios} con múltiples espacios internos.")
            if saltos: print(f"    * {saltos} con saltos de línea.")
            if corruptos: print(f"    * {corruptos} con caracteres corruptos (¿, , etc.).")
            if falsos_nulos: print(f"    * {falsos_nulos} con valores tipo N/A, vacíos o similares.")

    print("\n➤ 2.1 ANÁLISIS PROFUNDO DE TEXTOS CORRUPTOS (Símbolos '¿' o similares)")
    
    # Creamos un DataFrame booleano donde True significa que la celda es corrupta
    mask_corrupt = pd.DataFrame()
    for col in cols_obj:
        mask_corrupt[col] = df[col].astype(str).str.contains(patron_corrupto, flags=re.IGNORECASE, regex=True)
        
    total_celdas_corruptas = mask_corrupt.sum().sum()
    
    if total_celdas_corruptas > 0:
        # 1. Total y Columnas afectadas
        print(f"  - Total de campos (celdas) con texto corrupto: {total_celdas_corruptas:,}")
        print("  - Desglose por columnas afectadas:")
        col_sums = mask_corrupt.sum()
        for col, val in col_sums[col_sums > 0].items():
            print(f"    * '{col}': {val:,} registros")
            
        # 2. Análisis por filas
        filas_corruptas = mask_corrupt.sum(axis=1)
        total_filas_afectadas = (filas_corruptas > 0).sum()
        filas_multi_corruptas = (filas_corruptas > 1).sum()
        max_corrupcion = filas_corruptas.max()
        
        print(f"\n  - Impacto por registros (filas):")
        print(f"    * Filas totales con al menos 1 campo corrupto: {total_filas_afectadas:,}")
        print(f"    * Filas con MÚLTIPLES campos corruptos: {filas_multi_corruptas:,}")
        if max_corrupcion > 0:
            print(f"    * Peor caso: un solo registro tiene {max_corrupcion} columnas corruptas al mismo tiempo.")
        
        # 3. Vocabulario corrupto único
        palabras_corruptas = set()
        for col in cols_obj:
            words = df[col].astype(str).str.extractall(r'([A-Z]*[¿\ufffd][A-Z]*)', flags=re.IGNORECASE)
            if not words.empty:
                for w in words[0].dropna().str.upper().unique():
                    palabras_corruptas.add(w)
                    
        print("\n  - Diccionario de palabras corruptas únicas detectadas:")
        for w in sorted(palabras_corruptas):
            print(f"    * {w}")
    else:
        print("  - [✓] No se detectaron celdas con caracteres corruptos (¿, etc.).")
        palabras_corruptas = set()

    print("\n➤ 2.2 AUDITORÍA DE TILDES (Para futura normalización)")
    
    patron_tilde = r'[ÁÉÍÓÚáéíóú]'
    mask_tilde = pd.DataFrame()
    for col in cols_obj:
        mask_tilde[col] = df[col].astype(str).str.contains(patron_tilde, regex=True)
        
    total_celdas_tilde = mask_tilde.sum().sum()
    
    if total_celdas_tilde > 0:
        print(f"  - Total de campos (celdas) que contienen palabras con tilde: {total_celdas_tilde:,}")
        print("  - Desglose por columnas afectadas:")
        col_sums_tilde = mask_tilde.sum()
        for col, val in col_sums_tilde[col_sums_tilde > 0].items():
            print(f"    * '{col}': {val:,} registros con tildes")
            
        palabras_con_tilde = set()
        for col in cols_obj:
            todas_las_palabras = df[col].astype(str).str.extractall(r'([A-ZÁÉÍÓÚÑa-záéíóúñ]+)', flags=re.IGNORECASE)
            if not todas_las_palabras.empty:
                vocabulario = todas_las_palabras[0].str.upper().unique()
                for w in vocabulario:
                    if re.search(r'[ÁÉÍÓÚ]', w):
                        palabras_con_tilde.add(w)
                        
        print(f"\n  - Total de palabras ÚNICAS con tilde detectadas en todo el archivo: {len(palabras_con_tilde):,}")
        
        # Mostrar unos ejemplos
        if palabras_con_tilde:
            ejemplos = sorted(palabras_con_tilde)[:15]
            print(f"    * Ejemplos de palabras a normalizar: {', '.join(ejemplos)} ...")
    else:
        print("  - [✓] No se detectaron palabras con tilde en ninguna columna de texto.")

    print("\n➤ 3. VALORES ÚNICOS DE VARIABLES CATEGÓRICAS")
    cat_cols_interes = ['ESTADO_INSTITUCIÓN', 'SECTOR', 'MODALIDAD', 'NIVEL_DE_FORMACIÓN', 'ESTADO_PROGRAMA']
    for col in cat_cols_interes:
        if col in df.columns:
            print(f"\n  - Valores únicos en '{col}':")
            vc = df[col].value_counts(dropna=False)
            for val, count in vc.items():
                print(f"    * {repr(val)}: {count}")

    print("\n➤ 4. DUPLICADOS COMPLETOS Y PARCIALES")
    duplicados_completos = df.duplicated().sum()
    print(f"  - Filas completamente duplicadas: {duplicados_completos}")
    
    if 'CÓDIGO_SNIES_DEL_PROGRAMA' in df.columns:
        dup_snies = df['CÓDIGO_SNIES_DEL_PROGRAMA'].duplicated().sum()
        print(f"  - Códigos SNIES duplicados: {dup_snies}")
        
    cols_logicas = ['CÓDIGO_INSTITUCIÓN', 'NOMBRE_DEL_PROGRAMA', 'MUNICIPIO_OFERTA_PROGRAMA']
    cols_presentes = [c for c in cols_logicas if c in df.columns]
    if len(cols_presentes) == len(cols_logicas):
        dup_logicos = df.duplicated(subset=cols_logicas).sum()
        print(f"  - Duplicados lógicos ({' + '.join(cols_logicas)}): {dup_logicos}")

    print("\n➤ 5. CONSISTENCIA ENTRE VARIABLES")
    if 'ESTADO_PROGRAMA' in df.columns and 'ESTADO_INSTITUCIÓN' in df.columns:
        prog_activos_inst_inactiva = df[
            (df['ESTADO_PROGRAMA'].astype(str).str.strip().str.upper() == 'ACTIVO') &
            (df['ESTADO_INSTITUCIÓN'].astype(str).str.strip().str.upper() != 'ACTIVO')
        ].shape[0]
        print(f"  - Programas ACTIVOS en Instituciones NO ACTIVAS: {prog_activos_inst_inactiva}")
        
    if 'CÓDIGO_INSTITUCIÓN' in df.columns:
        sin_inst = df['CÓDIGO_INSTITUCIÓN'].isnull().sum()
        print(f"  - Programas sin CÓDIGO_INSTITUCIÓN: {sin_inst}")
        
    if 'MUNICIPIO_OFERTA_PROGRAMA' in df.columns:
        sin_mun = df['MUNICIPIO_OFERTA_PROGRAMA'].isnull().sum()
        print(f"  - Programas sin MUNICIPIO_OFERTA_PROGRAMA: {sin_mun}")
        
    if 'DEPARTAMENTO_OFERTA_PROGRAMA' in df.columns:
        sin_dep = df['DEPARTAMENTO_OFERTA_PROGRAMA'].isnull().sum()
        print(f"  - Programas sin DEPARTAMENTO_OFERTA_PROGRAMA: {sin_dep}")

    print("\n➤ 6. RELACIONES GEOGRÁFICAS")
    if 'DEPARTAMENTO_OFERTA_PROGRAMA' in df.columns and 'MUNICIPIO_OFERTA_PROGRAMA' in df.columns:
        dep_nulo_mun_no = df[df['DEPARTAMENTO_OFERTA_PROGRAMA'].isnull() & df['MUNICIPIO_OFERTA_PROGRAMA'].notnull()].shape[0]
        mun_nulo_dep_no = df[df['MUNICIPIO_OFERTA_PROGRAMA'].isnull() & df['DEPARTAMENTO_OFERTA_PROGRAMA'].notnull()].shape[0]
        print(f"  - Departamento Nulo pero Municipio NO Nulo: {dep_nulo_mun_no}")
        print(f"  - Municipio Nulo pero Departamento NO Nulo: {mun_nulo_dep_no}")

    print("\n➤ 7. VALIDACIONES ESPECÍFICAS DE FECHAS")
    fechas_cols = ['FECHA_DE_RESOLUCIÓN', 'FECHA_EJECUTORIA', 'FECHA_DE_REGISTRO_EN_SNIES']
    for fc in fechas_cols:
        if fc in df.columns:
            s_fechas = pd.to_datetime(df[fc], errors='coerce')
            fechas_antiguas = s_fechas[s_fechas.dt.year < 1950]
            absurdas = fechas_antiguas.shape[0]
            futuras = s_fechas[s_fechas > pd.Timestamp.now()].shape[0]
            if absurdas > 0 or futuras > 0:
                print(f"  - {fc}: {absurdas} fechas sospechosas antiguas (<1950), {futuras} fechas futuras.")
                if absurdas > 0:
                    fechas_unicas = fechas_antiguas.dt.strftime('%Y-%m-%d').unique()
                    print(f"    * Fechas antiguas encontradas: {', '.join(fechas_unicas)}")
                
    if 'FECHA_DE_RESOLUCIÓN' in df.columns and 'FECHA_EJECUTORIA' in df.columns:
        f_res = pd.to_datetime(df['FECHA_DE_RESOLUCIÓN'], errors='coerce')
        f_eje = pd.to_datetime(df['FECHA_EJECUTORIA'], errors='coerce')
        inconsistentes = (f_res > f_eje).sum()
        if inconsistentes > 0:
            print(f"  - [!] {inconsistentes} casos donde FECHA_DE_RESOLUCIÓN > FECHA_EJECUTORIA")

    print("\n➤ 8. VALIDACIONES DE REGLAS DE NEGOCIO (Errores)")
    s_cred = None
    s_dur = None
    s_costo = None

    if 'NÚMERO_CRÉDITOS' in df.columns:
        s_cred = pd.to_numeric(df['NÚMERO_CRÉDITOS'], errors='coerce')
        cero_o_neg = (s_cred <= 0).sum()
        print(f"  - NÚMERO_CRÉDITOS con valor <= 0: {cero_o_neg} errores.")
        
    if 'NÚMERO_PERIODOS_DE_DURACIÓN' in df.columns:
        s_dur = pd.to_numeric(df['NÚMERO_PERIODOS_DE_DURACIÓN'], errors='coerce')
        cero_o_neg = (s_dur <= 0).sum()
        print(f"  - NÚMERO_PERIODOS_DE_DURACIÓN con valor <= 0: {cero_o_neg} errores.")
        
    if 'COSTO_MATRÍCULA_ESTUD_NUEVOS' in df.columns:
        s_costo = pd.to_numeric(df['COSTO_MATRÍCULA_ESTUD_NUEVOS'], errors='coerce')
        negativos = (s_costo < 0).sum()
        print(f"  - COSTO_MATRÍCULA_ESTUD_NUEVOS negativos: {negativos} errores.")

    print("\n➤ 8.1 VALORES FUERA DE RANGO DE ALERTA (Revisión manual sugerida)")
    if s_cred is not None:
        altos = (s_cred > 300).sum()
        print(f"  - NÚMERO_CRÉDITOS anormalmente altos (> 300): {altos} alertas.")
        
    if s_dur is not None:
        altos = (s_dur > 20).sum()
        print(f"  - NÚMERO_PERIODOS_DE_DURACIÓN anormalmente altos (> 20 periodos): {altos} alertas.")
        
    if s_costo is not None:
        ceros = (s_costo == 0).sum()
        altos = (s_costo > 100_000_000).sum()
        print(f"  - COSTO_MATRÍCULA_ESTUD_NUEVOS en $0: {ceros} alertas.")
        print(f"  - COSTO_MATRÍCULA_ESTUD_NUEVOS excesivamente altos (> $100M): {altos} alertas.")

    print("\n➤ 9. CALIDAD DE IDENTIFICADORES")
    ids = ['CÓDIGO_INSTITUCIÓN', 'CÓDIGO_SNIES_DEL_PROGRAMA', 'CÓDIGO_INSTITUCIÓN_PADRE', 'REGISTRO_UNICO', 'CÓDIGO_ANTERIOR_ICFES']
    for col in ids:
        if col in df.columns:
            s_id = df[col]
            nulos = s_id.isnull().sum()
            no_numericos = pd.to_numeric(s_id, errors='coerce').isnull().sum() - nulos
            decimales = 0
            if pd.api.types.is_numeric_dtype(s_id):
                decimales = (s_id % 1 != 0).sum()
                negativos = (s_id < 0).sum()
            else:
                negativos = s_id.astype(str).str.startswith('-').sum()
            
            print(f"  - Identificador '{col}':")
            print(f"    * Nulos: {nulos}")
            if no_numericos > 0: print(f"    * No numéricos detectados: {no_numericos}")
            if decimales > 0: print(f"    * Valores con decimales (.0 o similares): {decimales}")
            if negativos > 0: print(f"    * Valores negativos: {negativos}")

    print("\n=== FIN DE LA AUDITORÍA ===")

if __name__ == "__main__":
    auditoria_profunda()