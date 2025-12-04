# ⚙️ Buenas prácticas para optimizar dashboards en Python
## 1. Carga de datos
- Usa formatos eficientes: **Parquet** o **Feather** en vez de CSV.
- Filtra y agrupa antes de graficar (ej. ventas por mes en vez de cada transacción).
- Si el dataset es muy grande, conecta una base de datos (SQLite, PostgreSQL) en lugar de cargar todo en memoria.

## 2. Caché y reutilización
- En Streamlit:

    ````python
    @st.cache_data
    def cargar_datos():
        return pd.read_csv("ventas.csv")
    ````

    Esto evita recalcular o recargar datos cada vez que cambias un filtro.


- En Dash: usa dcc.Store para guardar resultados intermedios.

## 3. Modularidad
- Divide tu código en funciones pequeñas y reutilizables (ej. graficar_tendencia(df) en vez de repetir código).

- Mantén separado:
  - ETL / limpieza
  -  Visualización
  - Layout del dashboard

## 4. Optimización de gráficos
- Usa librerías interactivas eficientes: **Plotly** o **Altair**.
- Evita graficar demasiados puntos → mejor agrupar o muestrear.
- Precalcula métricas (ej. KPIs) en Pandas antes de pasarlas al gráfico.

## 5. Uso de memoria
- Convierte columnas a tipos más ligeros (``category`` para texto repetido, ``int32`` en vez de ``int64``).

- Borra dataframes intermedios que no uses (``del df_temp``).

- Si trabajás con millones de filas, considera Dask o Polars para procesamiento paralelo.

## 6. Layout y experiencia
- Usa sidebar para filtros → mantiene el espacio central limpio.
- Limita el número de gráficos por página → mejor 3 visualizaciones clave que 10 lentas.
- Documenta cada visualización con títulos narrativos (“Ventas crecieron 20% en 2025”) en vez de etiquetas genéricas.
  
---

# 📌 Checklist rápido para tu laboratorio

- [ ] Dataset en formato eficiente (Parquet/Feather)
- [ ] Funciones modulares para ETL y gráficos
- [ ] Caché activado para cargas y cálculos
- [ ] KPIs precalculados en Pandas
- [ ] Sidebar para filtros y layout limpio
- [ ] Documentación clara en README sobre cada paso
---
*Con esto, tu dashboard en Python puede ser tan profesional como en Power BI, pero con la ventaja de ser exportable, versionable y escalable.*