import streamlit as st
import pandas as pd

def render_year_filter(df):
    
    # 1. Obtener opciones (como ENTEROS)
    years_series = df["OrderDate"].dt.year.dropna()
    available_years = sorted(years_series.unique().tolist())
    
    if not available_years:
        return None 
    
    # 2. Valor por defecto (siempre el último año, como ENTERO)
    default_year_int = available_years[-1]
    
    # 3. Preparar para st.pills (convirtiendo a STRING)
    options_as_strings = [str(year) for year in available_years]
    default_year_str = str(default_year_int)
    
    # Renderizar el filtro (devuelve una lista de strings)
    # CORRECCIÓN: AÑADIMOS key="year_filter_key" para forzar la actualización
    selected_years = st.sidebar.pills(
        "Año",
        options=options_as_strings,
        default=default_year_str,
        key="year_filter_key" # <-- SOLUCIÓN AL PROBLEMA DE ACTUALIZACIÓN
    )
    
    # 4. Devolver el valor seleccionado como ENTERO
    if selected_years and selected_years[0].isdigit():
        # Devolver el valor seleccionado como entero
        return int(selected_years[0])
    else:
        # Devolver el valor por defecto como entero (en caso de fallas)
        return default_year_int