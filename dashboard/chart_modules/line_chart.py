import streamlit as st
import plotly.express as px
import pandas as pd

def render_line_chart(df, y_col, metrica, ALTO):
    fig_linea = px.line(
        df,
        x="Periodo_Mes",
        y=y_col,
        color="Canal_Venta",
        title=f"Evolución Mensual de Ventas ({metrica})",
        labels={
            "Periodo_Mes": "Periodo",
            y_col: "Monto   de  Ventas"  # acá renombrás el eje Y
            }
    )
    fig_linea.update_layout(height=ALTO)
    st.plotly_chart(fig_linea, width='stretch')