# DataOps - Comisiones de Empleados (Azure Data Factory + Azure DevOps)

Pipeline que calcula `salario_total = mnt_salario + comision` combinando la tabla
`rrhh.empleado` (PostgreSQL) con el CSV `ComisionEmpleados_V1_202610.csv` (Blob Storage)
y publica el resultado en Parquet en el Data Lake. Se versiona en Git y se despliega con CI/CD.

## Arquitectura

```
PostgreSQL rrhh.empleado --(Copy activity)--> Data Lake /staging/empleado.parquet --+
                                                                                    +--(Data Flow: Join empleado_id + Derived Column)--> Data Lake /output/empleado_comision.parquet
Blob /input/ComisionEmpleados_V1_202610.csv ----------------------------------------+
```

## Contenido del repositorio

| Ruta | Descripcion |
|------|-------------|
| `adf/` | Recursos de ADF (pipeline, dataflow, datasets, linked services) generados por la integracion Git de ADF |
| `azure-pipelines.yml` | CI (validar + generar plantilla ARM + pruebas) y CD (Dev -> Test -> Prod) |
| `parameters/` | Parametros ARM por entorno (`dev`, `test`, `prod`) |
| `tests/validate_csv.py` | Prueba de calidad del CSV (ejecutada en CI) |
| `tests/validate_output.py` | Prueba del Parquet de salida |
| `data/` | Copia del CSV de ejemplo |
| `package.json` | Dependencia `@microsoft/azure-data-factory-utilities` para validar/exportar ARM |

## Pasos para desplegar

1. Crear 3 Data Factory (`adf-dataops-dev`, `-test`, `-prod`) en sus Resource Groups. Solo **dev** se conecta a Git (root folder `/adf`, colaboracion `main`).
2. Crear en Azure DevOps una Service Connection (`sc-azure-dataops`) hacia la suscripcion.
3. Crear Environments `dev`, `test`, `prod`; agregar aprobacion manual en `prod` (y opcional en `test`).
4. Editar `azure-pipelines.yml` (`subscriptionId`, nombre de service connection).
5. Hacer push a `main`: se ejecuta CI y luego CD por los tres entornos.
6. Ejecutar el pipeline `PL_Comisiones` en cada ADF y validar el Parquet con `tests/validate_output.py`.

## Seguridad
Las credenciales de PostgreSQL **no** estan en el repositorio. Se configuran en el Linked Service
(o Azure Key Vault) y se sobreescriben por entorno en el despliegue.
