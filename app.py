import streamlit as st
import pandas as pd
from dashboard.styles import apply_custom_css
from dashboard.filters import render_filters
from dashboard.layout import render_layout

# --- Configuración inicial ---
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="CHardy TecnoStore ARG - Dashboard Analítico"
)

# --- Aplicar CSS ---
apply_custom_css()

# Leer parámetros de la URL
params = st.query_params

# Si existe ?sidebar=true en la URL, lo activamos
show_sidebar = params.get("sidebar", "false").lower() == "true"


# --- Función de carga optimizada ---
@st.cache_data(show_spinner="Cargando modelo de CHardy TecnoStore ARG...")
def cargar_modelo_datos():
    cols = [
        "fecha","año","mes","cantidad",
        "monto_venta_ars_nominal","monto_venta_ars_real_2018",
        "Canal_Venta","categoria","Provincia","nombre_cliente","ciudad_cliente"
    ]
    df = pd.read_parquet(
        "data/analytical_layer/tecnoStore_modelo_estrella.parquet",
        columns=cols,
        engine="fastparquet"
    )
    df["monto_venta_ars_nominal"] = df["monto_venta_ars_nominal"].astype("float32")
    df["monto_venta_ars_real_2018"] = df["monto_venta_ars_real_2018"].astype("float32")
    df["cantidad"] = df["cantidad"].astype("int32")

    # Crear columna Periodo
    df["Periodo"] = pd.to_datetime(df["fecha"]).apply(
        lambda x: "Pre-pandemia" if x < pd.Timestamp("2020-03-01")
        else "Pandemia" if x <= pd.Timestamp("2021-12-31")
        else "Post-pandemia"
    )
    # Diccionario ciudad -> provincia
    ciudad_a_provincia = {
        "San Salvador de Jujuy": "Jujuy",
        "San Luis": "San Luis",
        "Merlo": "Buenos Aires",
        "Neuquén": "Neuquén",
        "San Ferando del Valle de Catamarca": "Catamarca",
        "Salta": "Salta",
        "Viedma": "Río Negro",
        "Paraná": "Entre Ríos",
        "La Plata": "Buenos Aires",
        "Ushuaia": "Tierra del Fuego",
        "La Rioja": "La Rioja",
        "San Miguel de Tucumán": "Tucumán",
        "Río Gallegos": "Santa Cruz",
        "Rawson": "Chubut",
        "Santiago del Estero": "Santiago del Estero",
        "Posadas": "Misiones",
        "Santa Rosa": "La Pampa",
        "San Juan": "San Juan",
        "Bahía Blanca": "Buenos Aires",
        "Chilecito": "La Rioja",
        "Mar del Plata": "Buenos Aires",
        "Mendoza": "Mendoza",
        "Resistencia": "Chaco",
        "Constitución": "Buenos Aires",
        "Formosa": "Formosa",
        "Corrientes": "Corrientes",
        "Córdoba": "Córdoba",
        "Santa Fe": "Santa Fe",
        "Comodoro Rivadavia": "Chubut",
        "Rosario": "Santa Fe"
        }

    # Actualizar columna Provincia solo si está vacía y el canal es Online
    mask_online = (df["Canal_Venta"] == "Online") & (df["Provincia"]=="N/A")
    df.loc[mask_online, "Provincia"] = df.loc[mask_online, "ciudad_cliente"].map(ciudad_a_provincia)


    return df

# --- Ejecución principal ---
df = cargar_modelo_datos()

#SIDEBAR_ON = False

df_filtrado, metrica = render_filters(df, show_sidebar)

render_layout(df_filtrado, metrica, show_sidebar)
