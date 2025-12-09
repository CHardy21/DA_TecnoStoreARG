import streamlit as st
import pandas as pd
import plotly.express as px
import json

# --- Configuración de página ---
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# --- Barra superior con segmentadores ---
periodo = st.radio(
    "Selecciona el período:",
    ["Pre-pandemia", "Pandemia", "Post-pandemia"],
    horizontal=True
)

canal = st.selectbox(
    "Selecciona el canal:",
    ["Todos", "Online", "Offline"]
)

# Selector de métrica (default = Ambos)
metrica = st.selectbox(
    "Selecciona la métrica:",
    ["Valores Corrientes (Nominal)", "Valores Constantes (2018)", "Ambos"],
    index=2
)

# --- Cargar modelo estrella ---
@st.cache_data
def load_data():
    df = pd.read_parquet("data/analytical_layer/tecnoStore_modelo_estrella.parquet", engine="fastparquet")
    return df
df = load_data()

print(df.info())

# Crear columna Periodo a partir de la fecha
df["Periodo"] = pd.to_datetime(df["fecha"]).apply(
    lambda x: "Pre-pandemia" if x < pd.Timestamp("2020-03-01")
    else "Pandemia" if x <= pd.Timestamp("2021-12-31")
    else "Post-pandemia"
)

# Filtrar según selección
df_filtrado = df[df["Periodo"] == periodo]
if canal != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Canal_Venta"] == canal]

# --- KPIs arriba ---
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales (Nominal)", f"${df_filtrado['monto_venta_ars_nominal'].sum():,.0f}")
col2.metric("Ventas Totales (Constantes 2018)", f"${df_filtrado['monto_venta_ars_real_2018'].sum():,.0f}")
col3.metric("Clientes Activos", df_filtrado["nombre_cliente"].nunique())

# --- Gráfico de línea ocupa todo el ancho ---
y_col = "monto_venta_ars_nominal" if metrica != "Valores Constantes (2018)" else "monto_venta_ars_real_2018"
fig_linea = px.line(
    df_filtrado,
    x="fecha",
    y=y_col,
    color="Canal_Venta",
    title=f"Evolución de Ventas ({metrica})"
)
st.plotly_chart(fig_linea, use_container_width=True)

# --- Layout inferior: izquierda (dos filas) + derecha (mapa) ---
col_izq, col_der = st.columns([2,1])

# Gráfico de barras por canal (fila 1 izquierda)
fig_barras_canal = px.bar(
    df_filtrado.groupby("Canal_Venta")[y_col].sum().reset_index(),
    x="Canal_Venta",
    y=y_col,
    title=f"Ventas por Canal ({metrica})"
)
col_izq.plotly_chart(fig_barras_canal, use_container_width=True)

# Gráfico de distribución por categoría (fila 2 izquierda)
fig_barras_cat = px.bar(
    df_filtrado.groupby("categoria")[y_col].sum().reset_index(),
    x="categoria",
    y=y_col,
    title=f"Distribución por Categoría ({metrica})"
)
col_izq.plotly_chart(fig_barras_cat, use_container_width=True)

# --- Mapa con puntos centrales usando geojson ---
# Cargar geojson de provincias (ajusta la ruta a tu archivo)
# with open("data/geo/argentina_provincias.geojson", "r", encoding="utf-8") as f:
#     geojson = json.load(f)

# import requests
# url = "https://apis.datos.gob.ar/georef/api/provincias?formato=geojson"
# geojson = requests.get(url).json()

# print(geojson["features"][0]["properties"])

# # Extraer coordenadas de cada provincia
# provincias = []
# for f in geojson["features"]:
#     nombre = f["properties"]["nombre"]
#     lon, lat = f["geometry"]["coordinates"]
#     provincias.append({"Provincia": nombre, "lat": lat, "lon": lon})

# df_geo = pd.DataFrame(provincias)

# # Merge con ventas filtradas
# ventas_prov = df_filtrado.groupby("Provincia").agg({y_col:"sum"}).reset_index()
# df_geo = df_geo.merge(ventas_prov, on="Provincia", how="left").fillna(0)

# # Scatter mapbox
# fig_mapbox = px.scatter_mapbox(
#     df_geo,
#     lat="lat",
#     lon="lon",
#     size=y_col,
#     color=y_col,
#     hover_name="Provincia",
#     mapbox_style="carto-positron",
#     zoom=3,
#     center={"lat": -38.4161, "lon": -63.6167},
#     title=f"Ventas por Provincia ({metrica})"
# )
# col_der.plotly_chart(fig_mapbox, use_container_width=True, height=800)

# --- Conclusión ---
st.markdown("---")
st.subheader("Conclusión y Recomendación")
st.info(
    "El canal online mostró un crecimiento sostenido antes, durante y después de la pandemia, "
    "con provincias líderes como Buenos Aires y Córdoba. "
    "Se recomienda consolidar la inversión digital para expandir la adopción en regiones con menor participación."
)
