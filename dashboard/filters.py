import streamlit as st

def render_filters(df):
        # --- Logo + Título en la misma fila ---
    col1, col2 = st.columns([0.1, 0.9])  # ajustá proporciones según tamaño del logo
    with col1:
        st.image("assets/favicon.png", width=90)  # tu logo en carpeta assets
    with col2:
        st.title("TecnoStore Dashboard")

    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        periodo = st.segmented_control(
            "Período",
            ["Pre-pandemia", "Pandemia", "Post-pandemia"]
        )
    with col2:
        canal = st.selectbox("Canal", ["Todos", "Online", "Offline"])
    with col3:
        metrica = st.selectbox(
            "Métrica",
            ["Valores Corrientes (Nominal)", "Valores Constantes (2018)", "Ambos"],
            index=2
        )

    df_filtrado = df[df["Periodo"] == periodo]
    if canal != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Canal_Venta"] == canal]

    return df_filtrado, metrica
