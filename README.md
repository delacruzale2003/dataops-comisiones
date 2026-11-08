# DataOps - Comisiones de Empleados (Azure Data Factory + GitHub Actions)

Pipeline que calcula `salario_total = mnt_salario + comision` combinando la tabla
`rrhh.empleado` (PostgreSQL) con el CSV `ComisionEmpleados_V1_202610.csv` (Blob Storage)
y publica el resultado en Parquet en el Data Lake. El factory se versiona en Git y se despliega
con CI/CD a Dev, Test y Prod.

## Arquitectura

```
PostgreSQL rrhh.empleado --(Copy)--> Data Lake /staging/empleado.parquet --+
                                                                           +--(Data Flow: Join empleado_id + salario_total)--> /output/empleado_comision.parquet
Blob /input/ComisionEmpleados_V1_202610.csv -------------------------------+
```

Recursos de ADF: pipeline `PL_Comisiones`, data flow `df_comisiones`, linked services
`LS_Postgres` y `LS_DataLake`, datasets `ds_pg_empleado`, `ds_csv_comision`,
`ds_parquet_staging` y `ds_parquet_output`.

## Contenido del repositorio

| Ruta | Descripcion |
|------|-------------|
| `adf/` | Recursos de ADF (pipeline, dataflow, datasets, linked services) generados por la integracion Git de ADF |
| `.github/workflows/ci-cd.yml` | CI (pruebas + validacion + plantilla ARM) y CD (Dev -> Test -> Prod con aprobacion) |
| `arm-template/` | Plantilla ARM generada por el CI (`ARMTemplateForFactory.json` y parametros). Los secretos van vacios; se reconfiguran por entorno |
| `parameters/` | Parametros ARM por entorno (`dev`, `test`, `prod`) |
| `tests/validate_csv.py` | Prueba de calidad del CSV (se ejecuta en CI) |
| `tests/validate_output.py` | Prueba del Parquet de salida (`salario_total` correcto) |
| `data/` | CSV de ejemplo y Parquet generado |
| `azure-pipelines.yml` | Equivalente para Azure Pipelines (referencia; no se ejecuto, el CI/CD real usa GitHub Actions) |

## Flujo de trabajo Git

1. El desarrollo se hace en ADF Studio sobre la rama `feature/pipeline-comisiones` (solo la fabrica de **dev** esta conectada a Git).
2. Se abre un Pull Request hacia `main`; el CI valida los recursos antes de permitir el merge.
3. Al hacer merge a `main` se ejecuta el CD.

## CI/CD (GitHub Actions)

- **CI**: prueba de calidad del CSV, `npm run build validate` y `npm run build export` (genera la plantilla ARM como artefacto).
- **CD - Desarrollo** y **CD - Prueba**: despliegue automatico con `azure/arm-deploy`.
- **CD - Produccion**: requiere aprobacion manual (Required reviewers en el Environment `prod`).

## Pasos para desplegar desde cero

1. Crear los grupos de recursos `rg-dataops-dev`, `rg-dataops-test`, `rg-dataops-prod`.
2. Crear en `rg-dataops-dev` una cuenta de almacenamiento ADLS Gen2 con los contenedores `input`, `staging` y `output`, y subir el CSV a `input`.
3. Crear las tres Data Factory (`adf-dataops-dev-aledc`, `adf-dataops-test-aledc`, `adf-dataops-prod-aledc`). Conectar solo la de dev a este repositorio (rama `main`, carpeta raiz `/adf`).
4. Crear un service principal con rol Contributor sobre la suscripcion:
   `az ad sp create-for-rbac --name sp-dataops-gh --role contributor --scopes /subscriptions/<ID> --sdk-auth`
5. En GitHub guardar los secretos `AZURE_CREDENTIALS` (JSON del paso anterior) y `AZURE_SUBSCRIPTION_ID`, y crear los Environments `dev`, `test` y `prod` (con Required reviewers en `prod`).
6. Hacer push/merge a `main`: se ejecutan CI y CD.
7. En las fabricas de **test** y **prod**, editar los linked services `LS_Postgres` y `LS_DataLake` para ingresar la contrasena/clave (los secretos no viajan en la plantilla ARM) y ejecutar `PL_Comisiones`.
8. Validar la salida: `python tests/validate_output.py data/empleado_comision.parquet`.

## Seguridad

Las credenciales de PostgreSQL y del service principal **no** estan en el repositorio (`*.sql` esta en `.gitignore`).
En un entorno productivo las contrasenas de los linked services deberian gestionarse con Azure Key Vault.
