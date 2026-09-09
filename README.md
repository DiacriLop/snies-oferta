# SNIES_YOP

Aplicativo web para consulta y análisis
de información de educación superior del SNIES.

## Tecnologías:
- Python
- Streamlit
- Pandas
- PyArrow

No contiene lógica del sistema en su raíz. Es documentación para entender el proyecto.
La estructura principal es:
1. **ETL**: Extrae, transforma y carga los datos desde la fuente.
2. **Data**: Almacena datos procesados (ej. en formato Parquet).
3. **Services**: Lógica del negocio (filtros, métricas, queries).
4. **App**: Interfaz de usuario (Streamlit), sólo presenta información delegando el procesamiento.
