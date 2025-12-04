import streamlit as st
import pandas as pd

# Importar las funciones de los módulos
from .filter_modules.year_filter import render_year_filter
from .filter_modules.category_filter import render_category_filter


def aplicar_filtro(df: pd.DataFrame, columna: str, seleccion, todas_opciones=None) -> pd.DataFrame:
    """
    Aplica filtro universal para cualquier columna y selección.
    - seleccion puede ser un valor único, lista o 'Todas'
    - todas_opciones: lista con todas las categorías posibles (para detectar selección completa)
    """
    if seleccion is None:
        return df
    
    # Caso multiselect vacío → mostrar todo
    if isinstance(seleccion, list) and len(seleccion) == 0:
        return df
    
    # Caso multiselect con todas las opciones → mostrar todo
    if todas_opciones is not None and isinstance(seleccion, list):
        if set(seleccion) == set(todas_opciones):
            return df
    
    # Caso 'Todas' explícito
    if seleccion == "Todas":
        return df
    
    # Caso lista parcial
    if isinstance(seleccion, list):
        return df[df[columna].isin(seleccion)]
    
    # Caso valor único
    return df[df[columna] == seleccion]


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza todos los filtros en la sidebar, obtiene sus valores
    y aplica la lógica de filtrado al DataFrame.
    """
    st.sidebar.title("🔎 Filtros")

    years = sorted(df["OrderDate"].dt.year.dropna().unique().tolist())
    categorias = sorted(df["Category"].dropna().unique().tolist())

    # --- Renderizado de filtros ---
    year = render_year_filter(df, tipo="segmentedControl", default=None)   # selección única
    categoria = render_category_filter(df, tipo="selectbox")               # incluye "Todas"

    # --- Debug ---
    st.sidebar.caption(f"DEBUG YEAR: '{year}' (Type: {type(year).__name__})")
    st.sidebar.caption(f"DEBUG CAT: '{categoria}' (Type: {type(categoria).__name__})")

    # --- Aplicación de Filtros ---
    df_filtrado = df.copy()

    # Filtro de Año
    if year is not None:
        try:
            year_int = int(year)
            df_filtrado = df_filtrado[df_filtrado["OrderDate"].dt.year == year_int]
        except ValueError:
            st.warning("Advertencia de filtro: El valor del año no es un número entero.")

    # Filtro de Categoría
    df_filtrado = aplicar_filtro(df_filtrado, "Category", categoria, todas_opciones=categorias)

    return df_filtrado
