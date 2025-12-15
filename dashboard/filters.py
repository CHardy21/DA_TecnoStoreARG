import streamlit as st


def segmented_pills(label: str, options: list[str], state_key: str, default: str):
    # Inicializar estado
    if state_key not in st.session_state:
        st.session_state[state_key] = default

    st.sidebar.write(label)

    # Render: cada opción en su propia línea
    for opt in options:
        if st.session_state[state_key] == opt:
            st.sidebar.markdown(f'<div class="chip chip-selected">{opt}</div>', unsafe_allow_html=True)
        else:
            if st.sidebar.button(opt, key=f"{state_key}_{opt}"):
                st.session_state[state_key] = opt

    return st.session_state[state_key]



def render_filters(df, sidebar: bool):
    # --- Logo + Título ---
    if sidebar:
        st.sidebar.image("assets/logo.png", width=300)
        
    else:
        col1, col2 = st.columns([0.1, 1.5])  
        with col1:
            st.image("assets/favicon.png", width=70)  
        with col2:
            st.title("CHardy TecnoStore ARG ")

    # --- Filtros ---
    if sidebar:
        periodo = st.sidebar.segmented_control(
            "Períodos",
            options=["Todos", "Pre-pandemia", "Pandemia", "Post-pandemia"],
            default="Todos"
        )
        canal = st.sidebar.segmented_control(
            "Canal de Venta",
            ["Todos", "Sucursal Fisica", "Online"],
            default="Todos"
        )

        metrica = st.sidebar.radio(
            "Métrica",
            ["Valores Corrientes (Nominal)", "Valores Constantes (2018)"],
            index=0,
            horizontal=True
        )
    else:
        col1, col2, col3 = st.columns([1.5, 1, 1.5])

        with col1:
            periodo = st.segmented_control(
                "Períodos",
                ["Todos", "Pre-pandemia", "Pandemia", "Post-pandemia"], 
                default="Todos"
            )
        with col2:
            canal = st.segmented_control(
                "Canal de Venta",
                ["Todos", "Sucursal Fisica", "Online"],
                default="Todos"
            )
        with col3:
            metrica = st.radio(
                "Métrica",
                ["Valores Corrientes (Nominal)", "Valores Constantes (2018)"],
                index=0,
                horizontal=True
            )

    # --- Aplicar filtros al DataFrame ---
    if periodo == "Todos":
        df_filtrado = df.copy()
    else:
        df_filtrado = df[df["Periodo"] == periodo]

    if canal != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Canal_Venta"] == canal]

    return df_filtrado, metrica
