import pandas as pd
from pathlib import Path
import sys

# Agregar la raíz del proyecto al sys.path para poder importar 'etl'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from etl.oferta.clean import clean_text, clean_oferta


def test_clean_text():
    print("Iniciando pruebas de clean.py...\n")

    # Prueba 1: espacios al inicio y final
    print("Prueba 1: Espacios al inicio y final")

    resultado = clean_text("   Ingeniería de Sistemas   ")

    esperado = "Ingeniería de Sistemas"

    if resultado == esperado:
        print("[OK] PASÓ")
    else:
        print(f"[FALLO] Esperado: {esperado} | Obtenido: {resultado}")

    print("-" * 60)

    # Prueba 2: múltiples espacios
    print("Prueba 2: Múltiples espacios internos")

    resultado = clean_text("Ingeniería     de     Sistemas")

    esperado = "Ingeniería de Sistemas"

    if resultado == esperado:
        print("[OK] PASÓ")
    else:
        print(f"[FALLO] Esperado: {esperado} | Obtenido: {resultado}")

    print("-" * 60)

    # Prueba 3: conservación de tildes
    print("Prueba 3: Conservación de tildes")

    resultado = clean_text("  Ingeniería de Sistemas  ")

    esperado = "Ingeniería de Sistemas"

    if resultado == esperado and "í" in resultado:
        print("[OK] PASÓ")
    else:
        print(f"[FALLO] Se alteraron las tildes: {resultado}")

    print("-" * 60)

    # Prueba 4: no corregir datos corruptos
    print("Prueba 4: Conservación de datos corruptos")

    resultado = clean_text("  INGENIER¿A DE SISTEMAS  ")

    esperado = "INGENIER¿A DE SISTEMAS"

    if resultado == esperado:
        print("[OK] PASÓ")
    else:
        print(f"[FALLO] El valor fue alterado: {resultado}")

    print("-" * 60)

    # Prueba 5: valores que no son texto
    print("Prueba 5: Valores no textuales")

    valor = 12345

    resultado = clean_text(valor)

    if resultado == valor:
        print("[OK] PASÓ")
    else:
        print(f"[FALLO] El valor fue alterado: {resultado}")

    print("-" * 60)


def test_clean_oferta():
    print("\nPrueba de limpieza del DataFrame...\n")

    df = pd.DataFrame({
        "NOMBRE_INSTITUCIÓN": [
            "  Universidad del Valle  ",
            "Universidad     Nacional"
        ],
        "NOMBRE_DEL_PROGRAMA": [
            "  Ingeniería     de Sistemas  ",
            "  Administración de Empresas "
        ],
        "NÚMERO_CRÉDITOS": [
            160,
            120
        ]
    })

    df_clean = clean_oferta(df)

    if df_clean["NOMBRE_INSTITUCIÓN"].iloc[0] == "Universidad del Valle":
        print("[OK] Nombre de institución limpiado")
    else:
        print("[FALLO] Nombre de institución")

    if df_clean["NOMBRE_INSTITUCIÓN"].iloc[1] == "Universidad Nacional":
        print("[OK] Múltiples espacios corregidos")
    else:
        print("[FALLO] Múltiples espacios")

    if df_clean["NOMBRE_DEL_PROGRAMA"].iloc[0] == "Ingeniería de Sistemas":
        print("[OK] Nombre de programa limpiado")
    else:
        print("[FALLO] Nombre de programa")

    if df_clean["NÚMERO_CRÉDITOS"].iloc[0] == 160:
        print("[OK] Columna numérica conservada")
    else:
        print("[FALLO] Columna numérica alterada")

    print("-" * 60)


if __name__ == "__main__":
    test_clean_text()
    test_clean_oferta()
