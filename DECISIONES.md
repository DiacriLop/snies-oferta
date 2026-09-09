# Decisiones de Arquitectura

**Decisión:** Utilizar Streamlit en lugar de Angular + Spring Boot.
**Motivo:** El aplicativo será utilizado por un único usuario, principalmente para consultas, filtros, tablas, gráficas y exportaciones.

**Decisión:** Uso de archivos Parquet para el almacenamiento de datos.
**Motivo:** Parquet es altamente eficiente para consultas grandes, evitando la carga pesada de procesar Excel en memoria repetidamente desde Streamlit.

**Decisión:** Arquitectura ETL -> DATA -> SERVICES -> APP
**Motivo:** Separación estricta de responsabilidades. ETL no sabe que existe Streamlit, Services no dependen de la UI, y la interfaz (App) no hace limpieza de datos.
