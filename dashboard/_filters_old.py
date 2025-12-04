import streamlit as st
import pandas as pd

# Importar las funciones de los módulos
from .filter_modules.year_filter import render_year_filter
from .filter_modules.category_filter import render_category_filter


def aplicar_filtro(df: pd.DataFrame, columna: str, seleccion) -> pd.DataFrame:
    """
    Aplica filtro universal para cualquier columna y selección.
    - seleccion puede ser un valor único, lista o 'Todas'
    """
    if seleccion == "Todas" or seleccion is None:
        return df
    if isinstance(seleccion, list):
        return df[df[columna].isin(seleccion)]
    else:
        return df[df[columna] == seleccion]


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza todos los filtros en la sidebar, obtiene sus valores
    y aplica la lógica de filtrado al DataFrame.
    """
    st.sidebar.title("🔎 Filtros")

    # 1. Obtener valores de los filtros llamando a los módulos:
    year = render_year_filter(df)       # Debe devolver INT
    categoria = render_category_filter(df)  # Puede devolver STR, lista o "Todas"

    # --- LÍNEAS DE DEBUG (PARA VER EL VALOR Y EL TIPO) ---
    st.sidebar.caption(f"DEBUG YEAR: '{year}' (Type: {type(year).__name__})")
    st.sidebar.caption(f"DEBUG CAT: '{categoria}' (Type: {type(categoria).__name__})")
    # -----------------------------------------------------

    # --- Aplicación de Filtros (Lógica Secuencial Confirmada) ---
    df_filtrado = df.copy()

    # 2. Aplicar filtro de Año
    if year is not None:
        try:
            year_int = int(year)
            df_filtrado = df_filtrado[df_filtrado["OrderDate"].dt.year == year_int]
        except ValueError:
            st.warning("Advertencia de filtro: El valor del año no es un número entero.")

    # 3. Aplicar filtro de Categoría (usando función universal)
    df_filtrado = aplicar_filtro(df_filtrado, "Category", categoria)

    # 4. Retorna el DataFrame filtrado
    return df_filtrado

