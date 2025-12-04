import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración inicial ---
st.set_page_config(page_title="Análisis de Ventas Argentina", layout="wide")

st.title("📊 Historia de Ventas - Electrodomésticos y Tecnología en Argentina")

# --- Cargar datos ---
@st.cache_data
def load_data():
    fact = pd.read_csv("data/fact_ventas_deflactado.csv", parse_dates=["fecha"])
    dim_prod = pd.read_csv("data/dim_productos.csv")
    dim_canales = pd.read_csv("data/dim_canales.csv")
    dim_suc = pd.read_csv("data/dim_sucursales.csv")
    return fact, dim_prod, dim_canales, dim_suc

fact, dim_prod, dim_canales, dim_suc = load_data()

# --- Filtros ---
st.sidebar.header("Filtros")
year_filter = st.sidebar.multiselect("Selecciona año(s)", fact["año"].unique(), default=fact["año"].unique())
canal_filter = st.sidebar.multiselect("Selecciona canal(es)", dim_canales["nombre_canal"].unique(), default=dim_canales["nombre_canal"].unique())

df_filtered = fact[fact["año"].isin(year_filter) & fact["canal_id"].isin([dim_canales.loc[dim_canales["nombre_canal"]==c,"canal_id"].values[0] for c in canal_filter])]

# --- KPIs principales ---
total_nominal = df_filtered["monto_venta_ars_nominal"].sum()
total_real = df_filtered["monto_venta_ars_real_2018"].sum()
participacion_online = df_filtered[df_filtered["canal_id"]==1]["monto_venta_ars_nominal"].sum() / total_nominal * 100
ticket_promedio = df_filtered["monto_venta_ars_nominal"].sum() / df_filtered["transaction_id"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas Nominales (ARS)", f"{total_nominal:,.0f}")
col2.metric("Ventas Reales (ARS 2018)", f"{total_real:,.0f}")
col3.metric("Participación Online (%)", f"{participacion_online:.1f}%")
col4.metric("Ticket Promedio (ARS)", f"{ticket_promedio:,.0f}")

st.markdown("---")

# --- Gráfico 1: Ventas nominales vs reales ---
ventas_time = df_filtered.groupby(["fecha"]).agg({
    "monto_venta_ars_nominal":"sum",
    "monto_venta_ars_real_2018":"sum"
}).reset_index()

fig1 = px.line(ventas_time, x="fecha", y=["monto_venta_ars_nominal","monto_venta_ars_real_2018"],
               labels={"value":"Monto (ARS)", "fecha":"Fecha"}, title="Evolución de Ventas Nominales vs Reales (Base 2018)")
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: Participación de canales ---
canales_share = df_filtered.groupby(["año","canal_id"]).agg({"monto_venta_ars_nominal":"sum"}).reset_index()
canales_share = canales_share.merge(dim_canales, on="canal_id")

fig2 = px.bar(canales_share, x="año", y="monto_venta_ars_nominal", color="nombre_canal", barmode="stack",
              labels={"monto_venta_ars_nominal":"Ventas (ARS)", "año":"Año"}, title="Participación de Canales")
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Impacto de eventos ---
eventos = df_filtered.groupby(["año","es_evento"]).agg({"monto_venta_ars_nominal":"sum"}).reset_index()
eventos["tipo"] = eventos["es_evento"].map({0:"Normal",1:"Evento"})
fig3 = px.bar(eventos, x="año", y="monto_venta_ars_nominal", color="tipo", barmode="group",
              labels={"monto_venta_ars_nominal":"Ventas (ARS)", "año":"Año"}, title="Impacto de Eventos (Hot Sale, Cyber)")
st.plotly_chart(fig3, use_container_width=True)

# --- Mapa de Argentina: Ventas por provincia ---
ventas_prov = df_filtered.dropna(subset=["sucursal_id"]).merge(dim_suc, on="sucursal_id")
ventas_prov = ventas_prov.groupby("provincia_sucursal").agg({"monto_venta_ars_nominal":"sum"}).reset_index()

# GeoJSON de provincias argentinas
geojson_url = "https://raw.githubusercontent.com/juan-giraldo/argentina-geojson/master/argentina.json"

fig4 = px.choropleth(
    ventas_prov,
    locations="provincia_sucursal",
    locationmode="geojson-id",
    geojson=geojson_url,
    color="monto_venta_ars_nominal",
    title="Mapa de Ventas por Provincia",
    color_continuous_scale="Blues"
)
fig4.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.write("📌 *Este dashboard muestra la evolución de ventas nominales y reales, la participación de canales y el impacto de eventos promocionales en Argentina.*")
