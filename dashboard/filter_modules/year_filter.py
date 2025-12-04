import streamlit as st
import pandas as pd

def render_year_filter(df, tipo="selectbox", default=None):
    """
    Renderiza el filtro de Año con distintos estilos según 'tipo'.
    - default: valor o lista de valores seleccionados por defecto (None = vacío).
    """
    years = sorted(df["OrderDate"].dt.year.dropna().unique().tolist())

    if tipo == "selectbox":
        # Si default es None → no selección inicial
        index = years.index(default) if default in years else 0
        year = st.sidebar.selectbox("Año", years, index=index)

    elif tipo == "radio":
        index = years.index(default) if default in years else 0
        year = st.sidebar.radio("Año", years, index=index, horizontal=True)

    elif tipo == "segmentedControl":
        year = st.sidebar.segmented_control("Año", years, default=default)

    elif tipo == "multiselect":
        year = st.sidebar.multiselect("Año", years, default=default if default else [])

    elif tipo == "checkboxes":
        st.sidebar.subheader("Año")
        selected_years = []
        for y in years:
            if st.sidebar.checkbox(str(y), value=(default and y in default)):
                selected_years.append(y)
        year = selected_years

    else:
        st.sidebar.warning("Tipo de filtro no soportado")
        year = None

    return year




# def render_year_filter(df: pd.DataFrame):
    
#     # 1. Obtener opciones (como ENTEROS)
#     years_series = df["OrderDate"].dt.year.dropna()
#     available_years = sorted(years_series.unique().tolist())
    
#     if not available_years:
#         return None 
    
#     # 2. Valor por defecto (siempre el último año, como ENTERO)
#     default_year_int = available_years[-1]
    
#     # 3. Preparar para st.pills (convirtiendo a STRING)
#     options_as_strings = [str(year) for year in available_years]
#     default_year_str = str(default_year_int)
    
#     # Renderizar el filtro (devuelve una lista de strings)
#     # CORRECCIÓN: AÑADIMOS key="year_filter_key" para forzar la actualización
#     selected_years = st.sidebar.pills(
#         "Año",
#         options=options_as_strings,
#         default=default_year_str,
#         key="year_filter_key" # <-- SOLUCIÓN AL PROBLEMA DE ACTUALIZACIÓN
#     )
    
#     # 4. Devolver el valor seleccionado como ENTERO
#     if selected_years and selected_years[0].isdigit():
#         # Devolver el valor seleccionado como entero
#         return int(selected_years[0])
#     else:
#         # Devolver el valor por defecto como entero (en caso de fallas)
#         return default_year_int