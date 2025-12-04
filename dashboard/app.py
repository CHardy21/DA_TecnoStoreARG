import streamlit as st
import pandas as pd
import plotly.express as px
from etl.ms_transformar_clientes import transformar_clientes
from etl.ms_transformar_localizacion import transformar_localizacion
from etl.ms_transformar_productos import transformar_productos
from etl.ms_transformar_ordenes import transformar_ordenes
from etl.ms_build_modelo_estrella import construir_modelo
from etl.ms_generar_calendar import generar_calendar


# --- Carga de datos crudos ---
clientes = pd.read_csv("data/raw/clientes.csv")
localizacion = pd.read_csv("data/raw/localizacion.csv")
productos = pd.read_csv("data/raw/productos.csv")
ordenes = pd.read_csv("data/raw/ordenes.csv")
calendar = generar_calendar(ordenes)

# --- ETL modular (por ahora vacío) ---
clientes = transformar_clientes(clientes)
localizacion = transformar_localizacion(localizacion)
productos = transformar_productos(productos)
ordenes = transformar_ordenes(ordenes)

# --- Construcción del modelo estrella ---
df = construir_modelo(clientes, localizacion, productos, ordenes, calendar)

# --- Sidebar de filtros ---
st.sidebar.title("🔎 Filtros")
year = st.sidebar.selectbox("Año", sorted(df["OrderDate"].dt.year.unique()))
categoria = st.sidebar.selectbox("Categoría", ["Todas"] + sorted(df["Category"].unique()))

# --- Aplicación de filtros ---
df_filtrado = df[df["OrderDate"].dt.year == year]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Category"] == categoria]

# --- KPIs ---
df_filtrado["TotalSales"] = df_filtrado["Sales"] * df_filtrado["Quantity"]
df_filtrado["TotalDiscount"] = df_filtrado["TotalSales"] * df_filtrado["Discount"]

total_sales = df_filtrado["TotalSales"].sum()
total_profit = df_filtrado["Profit"].sum()
total_discount = df_filtrado["TotalDiscount"].sum()
avg_sales_per_order = df_filtrado["TotalSales"].mean()

st.title("📊 MegaStore Dashboard (Python)")
st.metric("Total Sales Amount", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Total Discount", f"${total_discount:,.2f}")
st.metric("Average Sales per Order", f"${avg_sales_per_order:,.2f}")

# --- Línea temporal: ventas y profit por mes ---
df_filtrado["Month"] = df_filtrado["OrderDate"].dt.month
df_mes = df_filtrado.groupby("Month")[["TotalSales", "Profit"]].sum().reset_index()
fig_linea = px.line(df_mes, x="Month", y=["TotalSales", "Profit"], title="Ventas y Profit por Mes")
st.plotly_chart(fig_linea)

# --- Barras por producto ---
df_prod = df_filtrado.groupby("Product Name")[["TotalSales", "TotalDiscount", "Profit"]].sum().reset_index()
fig_prod = px.bar(df_prod, x="Product Name", y=["TotalSales", "TotalDiscount", "Profit"], title="Métricas por Producto")
st.plotly_chart(fig_prod)

# --- Barras por ciudad ---
df_ciudad = df_filtrado.groupby("City")["Profit"].sum().reset_index()
fig_ciudad = px.bar(df_ciudad, x="City", y="Profit", title="Profit por Ciudad")
st.plotly_chart(fig_ciudad)

# --- Mapa por estado ---
df_estado = df_filtrado.groupby("State")["TotalSales"].sum().reset_index()
fig_mapa = px.choropleth(df_estado, locations="State", locationmode="USA-states", color="TotalSales",
                         scope="usa", title="Ventas por Estado")
st.plotly_chart(fig_mapa)
