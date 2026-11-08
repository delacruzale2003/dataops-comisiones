"""CI test: valida el CSV de comisiones antes de desplegar.
Uso: python tests/validate_csv.py data/ComisionEmpleados_V1_202610.csv
"""
import sys
import pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else "data/ComisionEmpleados_V1_202610.csv"
df = pd.read_csv(path, sep=";", encoding="utf-8")

errors = []
expected = ["empleado_id", "Nombre y Apellido", "Comisión"]
if list(df.columns) != expected:
    errors.append(f"Columnas inesperadas: {list(df.columns)} (esperadas {expected})")
if df.empty:
    errors.append("El archivo esta vacio")
if df["empleado_id"].isna().any():
    errors.append("Hay empleado_id nulos")
if df["empleado_id"].duplicated().any():
    errors.append("Hay empleado_id duplicados")
if not pd.api.types.is_numeric_dtype(df["Comisión"]) or (df["Comisión"] < 0).any():
    errors.append("Comision no numerica o negativa")

if errors:
    print("FALLO:\n- " + "\n- ".join(errors))
    sys.exit(1)
print(f"OK: {len(df)} filas, columnas {list(df.columns)}")
