import streamlit as st
import pandas as pd
import plotly.express as px

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

# --- Diccionario de coordenadas de provincias argentinas ---
coords_provincias = {
    "Buenos Aires": (-34.61, -58.38),
    "Catamarca": (-28.47, -65.78),
    "Chaco": (-27.45, -58.99),
    "Chubut": (-43.30, -65.10),
    "Córdoba": (-31.42, -64.18),
    "Corrientes": (-27.48, -58.83),
    "Entre Ríos": (-31.73, -60.53),
    "Formosa": (-26.18, -58.17),
    "Jujuy": (-24.19, -65.30),
    "La Pampa": (-36.62, -64.29),
    "La Rioja": (-29.41, -66.85),
    "Mendoza": (-32.89, -68.84),
    "Misiones": (-27.36, -55.89),
    "Neuquén": (-38.95, -68.06),
    "Río Negro": (-39.03, -67.58),
    "Salta": (-24.79, -65.41),
    "San Juan": (-31.53, -68.52),
    "San Luis": (-33.30, -66.34),
    "Santa Cruz": (-51.62, -69.22),
    "Santa Fe": (-31.63, -60.70),
    "Santiago del Estero": (-27.79, -64.26),
    "Tierra del Fuego": (-54.80, -68.30),
    "Tucumán": (-26.83, -65.22)
}

# Merge coordenadas al dataframe
df_filtrado["lat"] = df_filtrado["Provincia"].map(lambda x: coords_provincias.get(x, (None, None))[0])
df_filtrado["lon"] = df_filtrado["Provincia"].map(lambda x: coords_provincias.get(x, (None, None))[1])

# --- KPIs arriba ---
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales (Nominal)", f"${df_filtrado['monto_venta_ars_nominal'].sum():,.0f}")
col2.metric("Ventas Totales (Constantes 2018)", f"${df_filtrado['monto_venta_ars_real_2018'].sum():,.0f}")
col3.metric("Clientes Activos", df_filtrado["nombre_cliente"].nunique())

# --- Gráfico de línea ocupa todo el ancho ---
fig_linea = px.line(
    df_filtrado,
    x="fecha",
    y="monto_venta_ars_nominal",
    color="Canal_Venta",
    title="Evolución de Ventas (Nominal)"
)
st.plotly_chart(fig_linea, use_container_width=True)

# --- Layout inferior: izquierda (dos filas) + derecha (mapa) ---
col_izq, col_der = st.columns([2,1])

# Gráfico de barras por canal (fila 1 izquierda)
fig_barras_canal = px.bar(
    df_filtrado.groupby("Canal_Venta")["monto_venta_ars_nominal"].sum().reset_index(),
    x="Canal_Venta",
    y="monto_venta_ars_nominal",
    title="Ventas por Canal"
)
col_izq.plotly_chart(fig_barras_canal, use_container_width=True)

# Gráfico de distribución por producto/categoría (fila 2 izquierda)
fig_barras_prod = px.bar(
    df_filtrado.groupby("categoria")["monto_venta_ars_nominal"].sum().reset_index(),
    x="categoria",
    y="monto_venta_ars_nominal",
    title="Distribución por Categoría de Producto"
)
col_izq.plotly_chart(fig_barras_prod, use_container_width=True)

# Mapa de burbujas (derecha, ocupa ambas filas)
df_map = df_filtrado.groupby("Provincia")["monto_venta_ars_nominal"].sum().reset_index()
df_map = df_map.merge(
    pd.DataFrame.from_dict(coords_provincias, orient="index", columns=["lat","lon"]).reset_index().rename(columns={"index":"Provincia"}),
    on="Provincia", how="left"
)

fig_burbujas = px.scatter_geo(
    df_map,
    lat="lat",
    lon="lon",
    size="monto_venta_ars_nominal",
    hover_name="Provincia",
    title="Mapa de Burbujas – Ventas por Provincia",
    projection="mercator"
)
col_der.plotly_chart(fig_burbujas, use_container_width=True, height=800)

# --- Conclusión ---
st.markdown("---")
st.subheader("Conclusión y Recomendación")
st.info(
    "El canal online mostró un crecimiento sostenido antes, durante y después de la pandemia, "
    "con provincias líderes como Buenos Aires y Córdoba. "
    "Se recomienda consolidar la inversión digital para expandir la adopción en regiones con menor participación."
)
