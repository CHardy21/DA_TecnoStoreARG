import streamlit as st
import plotly.express as px
import pandas as pd

def render_product_bar(df: pd.DataFrame, column):
    # Lógica de cálculo: Barras por producto
    df_prod = df.groupby("ProductName")[["TotalSales", "TotalDiscount", "Profit"]].sum().reset_index()
    
    fig_prod = px.bar(
        df_prod, 
        x="ProductName", 
        y=["TotalSales", "TotalDiscount", "Profit"], 
        title="Métricas por Producto"
    )
    
    # Renderizar en la columna pasada
    with column:
        st.plotly_chart(fig_prod, use_container_width=True)