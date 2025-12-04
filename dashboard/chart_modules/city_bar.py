import streamlit as st
import plotly.express as px
import pandas as pd

def render_city_bar(df: pd.DataFrame, column):
    # Lógica de cálculo: Barras por ciudad
    if "City" in df.columns:
        df_ciudad = df.groupby("City")["Profit"].sum().reset_index()
        
        fig_ciudad = px.bar(
            df_ciudad, 
            x="City", 
            y="Profit", 
            title="Profit por Ciudad"
        )
        
        # Renderizar en la columna pasada
        with column:
            st.plotly_chart(fig_ciudad, use_container_width=True)
    else:
        with column:
            st.warning("Columna 'City' no disponible en los datos.")