import streamlit as st
import pandas as pd

def render_category_filter(df: pd.DataFrame, tipo="selectbox"):
    """Renderiza el filtro de Categoría con distintos estilos según 'tipo'."""

    # Opciones de categorías
    options = ["Todas"] + sorted(df["Category"].dropna().unique())

    if tipo == "selectbox":
        categoria = st.sidebar.selectbox("Categoría", options)

    elif tipo == "radio":
        categoria = st.sidebar.radio("Categoría", options, horizontal=True)

    elif tipo == "segmentedControl":
        categoria = st.sidebar.segmented_control("Categoría", options)

    elif tipo == "buttons":
        if "selected_category" not in st.session_state:
            st.session_state.selected_category = options[0]  # "Todas" por defecto

        n_cols = 3
        for i in range(0, len(options), n_cols):
            cols = st.sidebar.columns(n_cols)
            for j, cat in enumerate(options[i:i+n_cols]):
                if cols[j].button(str(cat), key=f"btn_cat_{cat}"):
                    st.session_state.selected_category = cat

        categoria = st.session_state.selected_category

    elif tipo == "multiselect":
        categoria = st.sidebar.multiselect("Categoría", options, default=[options[0]])

    elif tipo == "checkboxes":
        st.sidebar.subheader("Categoría") 
        selected_cats = []
        for cat in options:
            if st.sidebar.checkbox(str(cat), value=(cat == options[0])):
                selected_cats.append(cat)
        categoria = selected_cats

    else:
        st.sidebar.warning("Tipo de filtro no soportado")
        categoria = None

    return categoria
