import streamlit as st

def apply_custom_css():
    """
    Inyecta CSS global para aplicar bordes y fondos a KPIs y contenedores de gráficos.
    """
    st.markdown(
        """
        <style>
        
        /* ================================================= */
        /* === 0. AJUSTE DE ESPACIO SUPERIOR GLOBAL === */
        /* ================================================= */

        /* 1. Apunta al contenedor principal de la aplicación (.stApp) */
        .stApp {
            padding-top: 10px !important; /* Reducido a 10px para subir todo. */
        }
        
        /* 2. Apunta al título h1 para eliminar su margen superior inherente */
        h1 {
            margin-top: 0px !important; 
            margin-bottom: 10px; 
        }

        /* 3. Apunta al contenedor principal del 'bloque' de contenido (el div que contiene todo después del título) */
        /* Esto elimina el padding superior que Streamlit pone en el 'block-container' */
        .block-container {
            padding-top: 2rem; /* Valor por defecto de Streamlit */
            padding-top: 1rem !important; /* Reducido para acercar el contenido superior */
        }

        /* Opcional: Si el bloque principal sigue teniendo margen (depende de la versión) */
        /* div[data-testid="stSidebarContent"] + div {
            padding-top: 1rem !important;
        } */
        
        /* Toolbar superior de Streamlit (modo dev) */
        .st-emotion-cache-gquqoo {
            background: transparent !important;
        }


        /* ================================================= */
        /* === 1. ESTILOS PARA KPIs (st.metric) === */
        /* ================================================= */
        div[data-testid="stMetric"] {
            /* Estilos de Borde y Fondo */
            border: 1px solid grey;
            border-radius: 5px;
            padding: 10px;
            /*background-color: #F0F2F6; */
            text-align: center;
            /* Margen: importante para separar las cajas cuando están en columnas */
            margin-bottom: 10px; 
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Sombra suave opcional */
        }
        
        /* Estilo para el valor (sin cambiar el tamaño, solo el color) */
        div[data-testid="stMetricValue"] {
            color: #1E88E5; 
        }

        /* Estilo para la etiqueta */
        div[data-testid="stMetricLabel"] p {
            font-weight: bold;
        }

        /* ================================================= */
        /* === 2. ESTILOS PARA GRÁFICOS (Plotly/ECharts/Altair) === */
        /* ================================================= */
        
        /* Contenedor principal para Plotly (st.plotly_chart) y otros gráficos */
        /* stPlotlyChart es el selector más robusto para Plotly Express */
        div[data-testid="stPlotlyChart"],
        div[data-testid="stVegaLiteChart"],
        div.stECharts { 
            /* Mismo estilo de Borde y Fondo que los KPIs */
            border: 1px solid #D3D3D3;
            border-radius: 5px;
            padding: 1px; 
            /*background-color: #F0F2F6;*/
            margin-bottom: 25px; /* Separación entre filas de gráficos */
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Sombra suave opcional */
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )
