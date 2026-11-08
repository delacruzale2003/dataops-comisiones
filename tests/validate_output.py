"""Prueba post-ejecucion: valida el Parquet generado por el pipeline.
Descargue el parquet del Data Lake y ejecute:
  python tests/validate_output.py salida.parquet
"""
import sys
import pandas as pd

df = pd.read_parquet(sys.argv[1])
required = {"empleado_id", "mnt_salario", "comision", "salario_total"}
missing = required - set(df.columns)
assert not missing, f"Faltan columnas: {missing}"
assert len(df) > 0, "Parquet vacio"
assert not df["empleado_id"].duplicated().any(), "empleado_id duplicado"
bad = df[(df["mnt_salario"] + df["comision"] - df["salario_total"]).abs() > 0.01]
assert bad.empty, f"salario_total incorrecto en {len(bad)} filas"
print(f"OK: {len(df)} filas, salario_total = mnt_salario + comision en todas")
print(df.head(10).to_string())
