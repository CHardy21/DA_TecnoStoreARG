# Guarda este código en un archivo: app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Datos de ejemplo ---
data = {
    "Ciudad": ["Resistencia", "Corrientes", "Formosa", "Posadas", "Resistencia", "Corrientes"],
    "Producto": ["A", "A", "B", "B", "C", "C"],
    "Ventas": [120, 90, 75, 60, 150, 110],
    "Profit": [30, 20, 15, 10, 40, 25],
    "Fecha": pd.date_range("2025-01-01", periods=6, freq="M")
}
df = pd.DataFrame(data)

# --- Layout del dashboard ---
st.title("📊 Mini Dashboard de Ventas")

# KPI cards
st.metric("Total Ventas", df["Ventas"].sum())
st.metric("Total Profit", df["Profit"].sum())

# Filtro interactivo
ciudad = st.selectbox("Selecciona una ciudad:", df["Ciudad"].unique())
df_filtrado = df[df["Ciudad"] == ciudad]

# Gráfico de tendencia temporal
fig = px.line(df_filtrado, x="Fecha", y="Ventas", title=f"Tendencia de Ventas en {ciudad}")
st.plotly_chart(fig)

# Gráfico de barras por producto
fig2 = px.bar(df_filtrado, x="Producto", y="Profit", title=f"Profit por Producto en {ciudad}")
st.plotly_chart(fig2)
