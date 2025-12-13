import streamlit as st
import plotly.express as px
import pandas as pd

def render_line_chart(df: pd.DataFrame, column):
    # Lógica de cálculo: Línea temporal: ventas y profit por mes
    df["Month"] = df["OrderDate"].dt.month
    df_mes = df.groupby("Month")[["TotalSales", "Profit"]].sum().reset_index()
    
    fig_linea = px.line(
        df_mes, 
        x="Month", 
        y=["TotalSales", "Profit"], 
        title="Ventas y Profit por Mes"
    )
    
    # Renderizar en la columna pasada
    with column:
        st.plotly_chart(fig_linea, use_container_width=True)