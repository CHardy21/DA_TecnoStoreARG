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

        div[data-testid="stToolbar"] {
            background: transparent !important;
        }
        /* Todos los hijos dentro del header */
        .stAppHeader{
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

        /* === 1.2. ESTILOS PARA KPIs (markdown <div>) === */
        .metric-box {
            border: 1px solid #1e1e1e;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
            background-color: #000;
            margin-bottom: 10px;
        }
        .metric-label {
            font-size: 0.8em;
            color: #fff;
        }
        .metric-value {
            font-size: 2.5em;
            color: #1c48cb;
        }
        .metric-suffix {
            font-size: 0.35em;
            vertical-align: super;
            color: gray;
            margin-left: 4px;
        }

        /* --- Responsive --- */
        @media (max-width: 768px) {
            .metric-value {
                font-size: 1.6em;   /* más chico en tablets/móviles */
            }
            .metric-label {
                font-size: 0.7em;
            }
            .metric-suffix {
                font-size: 0.4em;
            }
        }

        @media (max-width: 480px) {
            .metric-value {
                font-size: 1.5em; /* aún más chico en móviles */
            }
            .metric-label {
                font-size: 0.8em;
            }
            .metric-suffix {
                font-size: 0.5em;
            }
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
            border: 0px solid #D3D3D3;
            border-radius: 5px;
            margin: 0px;
            padding: 0px 10px 0px 10px; 
            /*background-color: #F0F2F6;*/
            /*margin-bottom: 25px; /* Separación entre filas de gráficos */*/
            /*box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Sombra suave opcional */*/
        }

        /* Aplica estilo al padre del padre que contiene un stPlotlyChart */
        div[data-testid="stElementContainer"]:has(div[data-testid="stFullScreenFrame"] > div[data-testid="stPlotlyChart"]) {
            border: 1px solid #D3D3D3;
            border-radius: 10px;
           }



        </style>
        """,
        unsafe_allow_html=True,
    )
