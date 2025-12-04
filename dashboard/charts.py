# dashboard/charts.py

import streamlit as st
import pandas as pd

# Importar las funciones específicas de los módulos de gráficos
from .chart_modules.line_chart import render_line_chart
from .chart_modules.product_bar import render_product_bar
from .chart_modules.city_bar import render_city_bar
from .chart_modules.state_map import render_state_map


def render_charts(df_filtrado: pd.DataFrame):
    """
    Define el layout de las columnas y llama a las funciones
    modulares para renderizar cada gráfico.
    """
    # 1. Definición de la estructura de la interfaz
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # 2. Renderizado modular: pasar el DataFrame y la columna de destino
    
    # Fila 1
    render_line_chart(df_filtrado, row1_col1)
    render_product_bar(df_filtrado, row1_col2)

    # Fila 2
    render_city_bar(df_filtrado, row2_col1)
    render_state_map(df_filtrado, row2_col2)