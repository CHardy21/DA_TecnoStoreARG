import streamlit as st
from dashboard.kpis import render_kpis
from dashboard.charts import render_charts

def render_layout(df_filtrado):
    st.title("MegaStore Dashboard ")

    # KPIs en fila superior
    render_kpis(df_filtrado)

    st.markdown("---")

    # Gráficos en grid 2x2
    render_charts(df_filtrado)
