import streamlit as st
import plotly.express as px
import pandas as pd
from .chart_modules.line_chart import render_line_chart
from .chart_modules.canal_bar import render_canal_bar
from .chart_modules.categories_bar import render_categories_bar
from .chart_modules.prov_arg_map import render_map

def render_charts(df_filtrado, metrica, sidebar: bool):

    if sidebar:
        ALTO = 250
        ANCHO = 200
        COL_L = 2
        COL_R = 1
    else:
        ALTO = 400
        ANCHO = 200
        COL_L = 1.5
        COL_R = 1.5

    # Selección de métrica
    if metrica == "Valores Corrientes (Nominal)":
        y_col = "monto_venta_ars_nominal"
    elif metrica == "Valores Constantes (2018)":
        y_col = "monto_venta_ars_real_2018"
    else:
        y_col = "monto_venta_ars_nominal"

    # --- Gráfico de línea mensual ---
    df_mensual = (
        df_filtrado.groupby(["año","mes","Canal_Venta"])[y_col]
        .sum()
        .reset_index()
    )
    df_mensual["Periodo_Mes"] = pd.to_datetime(
        df_mensual["año"].astype(str) + "-" + df_mensual["mes"].astype(str) + "-01"
    )


    if sidebar:
        col_izq, col_der = st.columns([COL_L,COL_R])
        with col_izq:
            render_line_chart(df_mensual, y_col, metrica, ALTO)
        # Subdividir la columna izquierda en dos
            subcol1, subcol2 = st.columns([1,1])  

            with subcol1:
                render_canal_bar(df_filtrado,y_col, metrica, ALTO)
            with subcol2:
                # Gráfico de distribución por categoría
                render_categories_bar(df_filtrado,y_col, metrica, ALTO)
        with col_der:
            render_map(df_filtrado,y_col, metrica, ALTO*2, 40, 2.5) 

    else:
        # Gráfico de lineas
        render_line_chart(df_mensual, y_col, metrica, ALTO)

        # --- Layout inferior: izquierda (dos filas) + derecha (mapa) ---
        col_izq, col_der = st.columns([COL_L,COL_R])

        
        with col_izq:
            # Gráfico de barras por canal
            render_canal_bar(df_filtrado,y_col, metrica, ALTO)
            # Gráfico de distribución por categoría
            render_categories_bar(df_filtrado,y_col, metrica, ALTO)
        with col_der:
            render_map(df_filtrado,y_col, metrica, ALTO*2, 60, 3)

