# Informe Final - Proyecto DataOps: Comisiones de Empleados

**Alumno:** ______  **Curso:** DataOps  **Fecha:** 2026-11-08

## 1. Resumen del proyecto
Se implemento un pipeline en Azure Data Factory que extrae `rrhh.empleado` de PostgreSQL,
lee `ComisionEmpleados_V1_202610.csv` desde Blob Storage, realiza un Join por `empleado_id`,
calcula `salario_total = mnt_salario + comision` y escribe un Parquet en el Data Lake.
El codigo se versiona en Azure Repos y se despliega con Azure Pipelines (CI -> Dev -> Test -> Prod).

## 2. Arquitectura
(insertar diagrama / captura del pipeline)

## 3. Repositorio Git
(captura de repo, ramas, commits, PR) 

## 4. CI/CD
(captura de ejecucion CI, stages Dev/Test/Prod, aprobacion en Prod)

## 5. Registro de pruebas

| # | Prueba | Esperado | Resultado | Evidencia |
|---|--------|----------|-----------|-----------|
| 1 | Conexion Linked Service PostgreSQL | Test connection OK | | Fig. |
| 2 | Conexion Linked Service Blob/Lake | Test connection OK | | Fig. |
| 3 | `validate_csv.py` en CI | 34 filas, sin duplicados | OK (34 filas) | Log CI |
| 4 | Validacion ADF (`npm run build validate`) | Sin errores | | Log CI |
| 5 | Debug del Data Flow | Join y columna salario_total | | Fig. |
| 6 | Ejecucion del pipeline en Dev | Succeeded, Parquet creado | | Fig. |
| 7 | `validate_output.py` | salario_total = salario + comision | | Salida |
| 8 | Deploy a Test | Succeeded | | Fig. |
| 9 | Deploy a Prod con aprobacion | Succeeded tras aprobar | | Fig. |
| 10 | Ejecucion en Prod | Succeeded | | Fig. |

## 6. Conclusiones y lecciones aprendidas
