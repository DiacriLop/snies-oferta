"""Módulo de ingestión para los datos de Oferta Académica.
Se encarga exclusivamente de leer el archivo origen (Excel) de manera segura
y devolver un DataFrame de Pandas, sin aplicar transformaciones ni limpiezas ni validaciones.
"""
import pandas as pd
from pathlib import Path
from typing import Union

def load_oferta(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Carga un archivo Excel de Oferta Académica y lo devuelve como DataFrame crudo.
    
    Args:
        file_path: Ruta al archivo Excel (puede ser un string o un objeto Path).
        
    Returns:
        pd.DataFrame: Los datos leídos directamente del archivo.
        
    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta.
        ValueError: Si el archivo no tiene formato .xlsx.
        RuntimeError: Si el archivo está corrupto o no se puede leer.
    """
    path = Path(file_path)
    
    # 1. Comprobar que el archivo existe
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo en la ruta: {path}")
        
    # 2. Comprobar que es un formato válido
    if path.suffix.lower() not in ['.xlsx']:
        raise ValueError(f"Formato inválido ({path.suffix}). Solo se permiten archivos .xlsx")
        
    # 3. Intentar leer el Excel
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        # 4. Manejo de error de lectura (corrupto, bloqueado, etc.)
        raise RuntimeError(f"No se pudo leer el archivo Excel. Detalle: {str(e)}") from e

if __name__ == "__main__":
    # Pequeña prueba directa
    ruta = Path("data/raw/oferta/oferta_simplificada.xlsx")
    print(f"[INFO] Intentando cargar: {ruta}")
    
    try:
        df_test = load_oferta(ruta)
        print(f"[OK] Carga exitosa. Se obtuvo un DataFrame con {len(df_test)} filas y {len(df_test.columns)} columnas.")
    except Exception as error:
        print(f"[!] Falló la carga: {error}")
