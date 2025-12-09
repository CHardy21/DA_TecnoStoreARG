import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests

# --- Configuración inicial ---
st.set_page_config(page_title="Dashboard Ventas Argentina", layout="wide")
st.title("📊 Historia de Ventas - Modelo Estrella Consolidado")

# --- Cargar modelo estrella ---
@st.cache_data
def load_data():
    df = pd.read_parquet("data/analytical_layer/tecnoStore_modelo_estrella.parquet", engine="fastparquet")
    return df

df = load_data()

# --- Filtros ---
st.sidebar.header("Filtros")
years = st.sidebar.multiselect("Selecciona año(s)", df["anio_origen"].unique(), default=df["anio_origen"].unique())
canales = st.sidebar.multiselect("Selecciona canal(es)", df["Canal_Venta"].unique(), default=df["Canal_Venta"].unique())
categorias = st.sidebar.multiselect("Selecciona categoría(s)", df["categoria"].unique(), default=df["categoria"].unique())

df_filtered = df[(df["anio_origen"].isin(years)) & 
                 (df["Canal_Venta"].isin(canales)) & 
                 (df["categoria"].isin(categorias))]

# --- KPIs principales ---
total_nominal = df_filtered["monto_venta_ars_nominal"].sum()
total_real = df_filtered["monto_venta_ars_real_2018"].sum()
ticket_promedio = df_filtered["monto_venta_ars_nominal"].sum() / df_filtered["transaction_id"].nunique()
participacion_online = df_filtered[df_filtered["Canal_Venta"]=="Online"]["monto_venta_ars_nominal"].sum() / total_nominal * 100 if "Online" in df_filtered["Canal_Venta"].unique() else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas Nominales (ARS)", f"{total_nominal:,.0f}")
col2.metric("Ventas Reales (ARS 2018)", f"{total_real:,.0f}")
col3.metric("Participación Online (%)", f"{participacion_online:.1f}%")
col4.metric("Ticket Promedio (ARS)", f"{ticket_promedio:,.0f}")

st.markdown("---")

# --- Gráfico 1: Evolución temporal ---
ventas_time = df_filtered.groupby("fecha").agg({
    "monto_venta_ars_nominal":"sum",
    "monto_venta_ars_real_2018":"sum"
}).reset_index()

fig1 = px.line(ventas_time, x="fecha", y=["monto_venta_ars_nominal","monto_venta_ars_real_2018"],
               labels={"value":"Monto (ARS)", "fecha":"Fecha"}, 
               title="Evolución de Ventas Nominales vs Reales (Base 2018)")
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: Participación por canal ---
canales_share = df_filtered.groupby(["anio_origen","Canal_Venta"]).agg({"monto_venta_ars_nominal":"sum"}).reset_index()
fig2 = px.bar(canales_share, x="anio_origen", y="monto_venta_ars_nominal", color="Canal_Venta", barmode="stack",
              labels={"monto_venta_ars_nominal":"Ventas (ARS)", "anio_origen":"Año"}, 
              title="Participación de Canales")
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Impacto de eventos ---
eventos = df_filtered.groupby(["anio_origen","es_evento_x"]).agg({"monto_venta_ars_nominal":"sum"}).reset_index()
eventos["tipo"] = eventos["es_evento_x"].map({0:"Normal",1:"Evento"})
fig3 = px.bar(eventos, x="anio_origen", y="monto_venta_ars_nominal", color="tipo", barmode="group",
              labels={"monto_venta_ars_nominal":"Ventas (ARS)", "anio_origen":"Año"}, 
              title="Impacto de Eventos (Hot Sale, Cyber, etc.)")
st.plotly_chart(fig3, use_container_width=True)

# --- Gráfico 4: Mapa de ventas por provincia ---

# Agrupamos ventas por provincia
ventas_prov = df_filtered.groupby("Provincia").agg({"monto_venta_ars_nominal":"sum"}).reset_index()

# Normalizamos nombres para que coincidan con el GeoJSON oficial
mapping = {
    "Buenos Aires": "Buenos Aires",
    "Río Negro": "Rio Negro",
    "Chaco": "Chaco",
    "Córdoba": "Cordoba",
    "Santa Fe": "Santa Fe",
    "Salta": "Salta",
    "Santa Cruz": "Santa Cruz",
    "Mendoza": "Mendoza",
    "Misiones": "Misiones",
    "N/A": None
}
ventas_prov["Provincia_geo"] = ventas_prov["Provincia"].map(mapping)

# Cargamos GeoJSON oficial desde API de datos.gob.ar
url = "https://apis.datos.gob.ar/georef/api/provincias?formato=geojson"
geojson = requests.get(url).json()

fig4 = px.choropleth(
    ventas_prov,
    geojson=geojson,
    locations="Provincia_geo",
    featureidkey="properties.nombre",
    color="monto_venta_ars_nominal",
    title="Mapa de Ventas por Provincia",
    color_continuous_scale="Blues"
)
fig4.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.write("📌 *Dashboard basado en el modelo estrella consolidado: ventas nominales y reales, participación de canales, impacto de eventos y distribución geográfica.*")
