# dashboard/charts.py

# import streamlit as st
# import pandas as pd

# # Importar las funciones específicas de los módulos de gráficos
# from .chart_modules.line_chart import render_line_chart
# from .chart_modules.product_bar import render_product_bar
# from .chart_modules.city_bar import render_city_bar
# from .chart_modules.state_map import render_state_map


# def render_charts(df_filtrado: pd.DataFrame):
#     """
#     Define el layout de las columnas y llama a las funciones
#     modulares para renderizar cada gráfico.
#     """
#     # 1. Definición de la estructura de la interfaz
#     row1_col1, row1_col2 = st.columns(2)
#     row2_col1, row2_col2 = st.columns(2)

#     # 2. Renderizado modular: pasar el DataFrame y la columna de destino
    
#     # Fila 1
#     render_line_chart(df_filtrado, row1_col1)
#     render_product_bar(df_filtrado, row1_col2)

#     # Fila 2
#     render_city_bar(df_filtrado, row2_col1)
#     render_state_map(df_filtrado, row2_col2)

import streamlit as st
import plotly.express as px

def render_charts(df_filtrado, metrica):
    # Selección de métrica
    if metrica == "Valores Corrientes (Nominal)":
        y_col = "monto_venta_ars_nominal"
    elif metrica == "Valores Constantes (2018)":
        y_col = "monto_venta_ars_real_2018"
    else:
        y_col = "monto_venta_ars_nominal"

    # Gráfico de línea mensual
    df_mensual = (
        df_filtrado.groupby(["año","mes","Canal_Venta"])[y_col]
        .sum()
        .reset_index()
    )
    df_mensual["Periodo_Mes"] = pd.to_datetime(
        df_mensual["año"].astype(str) + "-" + df_mensual["mes"].astype(str) + "-01"
    )

    fig_linea = px.line(
        df_mensual,
        x="Periodo_Mes",
        y=y_col,
        color="Canal_Venta",
        title=f"Evolución Mensual de Ventas ({metrica})"
    )

    # Gráfico de barras por canal
    fig_barras_canal = px.bar(
        df_filtrado.groupby("Canal_Venta")[y_col].sum().reset_index(),
        x="Canal_Venta",
        y=y_col,
        title=f"Ventas por Canal ({metrica})"
    )

    # Gráfico de distribución por categoría
    fig_barras_cat = px.bar(
        df_filtrado.groupby("categoria")[y_col].sum().reset_index(),
        x="categoria",
        y=y_col,
        title=f"Distribución por Categoría ({metrica})"
    )

    # Layout en grid 2x2
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_linea, width="stretch")
    col2.plotly_chart(fig_barras_canal, width="stretch")

    col3, col4 = st.columns(2)
    col3.plotly_chart(fig_barras_cat, width="stretch")
    # col4 → aquí podrías poner el mapa o dejarlo como placeholder
    col4.markdown("Mapa de burbujas (placeholder)")
