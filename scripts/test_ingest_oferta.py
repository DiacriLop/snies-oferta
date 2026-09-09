import pandas as pd
from pathlib import Path
import sys

# Agregar la raíz del proyecto al sys.path para poder importar 'etl'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from etl.oferta.ingest import load_oferta

def test_ingest():
    print("Iniciando pruebas de error sobre ingest.py...\n")
    
    # Prueba 1: Archivo inexistente
    print("Prueba 1: Archivo inexistente")
    try:
        load_oferta("data/raw/oferta/archivo_fantasma.xlsx")
        print("[FALLO] No lanzó ningún error.")
    except FileNotFoundError as e:
        print(f"[OK] PASÓ: Lanzó FileNotFoundError -> {e}")
    except Exception as e:
        print(f"[FALLO] Lanzó {type(e)} en lugar de FileNotFoundError -> {e}")
        
    print("-" * 60)
    
    # Prueba 2: Extensión incorrecta
    print("Prueba 2: Extensión incorrecta (.csv)")
    temp_csv = None
    try:
        temp_csv = Path("temp_test.csv")
        temp_csv.write_text("dummy,data")
        load_oferta(temp_csv)
        print("[FALLO] No lanzó ningún error.")
    except ValueError as e:
        print(f"[OK] PASÓ: Lanzó ValueError -> {e}")
    except Exception as e:
        print(f"[FALLO] Lanzó {type(e)} en lugar de ValueError -> {e}")
    finally:
        if temp_csv is not None and temp_csv.exists():
            temp_csv.unlink()
            
    print("-" * 60)
    
    # Prueba 3: Excel ilegible (corrupto)
    print("Prueba 3: Excel ilegible")
    temp_bad_xlsx = None
    try:
        temp_bad_xlsx = Path("temp_corrupto.xlsx")
        temp_bad_xlsx.write_text("Esto es texto plano, no soy un excel real.")
        load_oferta(temp_bad_xlsx)
        print("[FALLO] No lanzó ningún error.")
    except RuntimeError as e:
        print(f"[OK] PASÓ: Lanzó RuntimeError -> {e}")
    except Exception as e:
        print(f"[FALLO] Lanzó {type(e)} en lugar de RuntimeError -> {e}")
    finally:
        if temp_bad_xlsx is not None and temp_bad_xlsx.exists():
            temp_bad_xlsx.unlink()

if __name__ == "__main__":
    test_ingest()
