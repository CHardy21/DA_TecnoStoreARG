import streamlit as st
import pandas as pd
from dashboard.styles import apply_custom_css
from dashboard.filters import render_filters
from dashboard.layout import render_layout

# --- Configuración inicial ---
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="TecnoStore - Dashboard Analítico"
)

# --- Aplicar CSS ---
apply_custom_css()

# --- Función de carga optimizada ---
@st.cache_data(show_spinner="Cargando modelo estrella...")
def cargar_modelo_datos():
    cols = [
        "fecha","año","mes","cantidad",
        "monto_venta_ars_nominal","monto_venta_ars_real_2018",
        "Canal_Venta","categoria","Provincia","nombre_cliente"
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
    return df

# --- Ejecución principal ---
df = cargar_modelo_datos()
df_filtrado, metrica = render_filters(df)
render_layout(df_filtrado, metrica)
