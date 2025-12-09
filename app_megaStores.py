import streamlit as st
import pandas as pd
from etl.megaStore.ms_transformar_clientes import transformar_clientes
from etl.megaStore.ms_transformar_localizacion import transformar_localizacion
from etl.megaStore.ms_transformar_productos import transformar_productos
from etl.megaStore.ms_transformar_ordenes import transformar_ordenes
from etl.megaStore.ms_build_modelo_estrella import construir_modelo
from etl.megaStore.ms_generar_calendar import generar_calendar
from dashboard.styles import apply_custom_css
from dashboard.filters import render_filters
from dashboard.layout import render_layout

# --- Configuración inicial ---
st.set_page_config(
    layout="wide",  
    initial_sidebar_state="expanded",
    page_title="MegaStore - Dashboard Analítico" # Opcional: ponerle título a la pestaña
)

# --- Aplicar CSS ---
# IMPORTANTE: Esto queda fuera de la caché para que veas los cambios 
# visuales inmediatamente cada vez que edites los archivos CSS.
apply_custom_css()

# --- Función ETL con Caché ---
# Streamlit ejecutará esto la primera vez. Las siguientes veces, si el código
# de esta función no cambió, leerá el resultado de la memoria RAM instantáneamente.
@st.cache_data(show_spinner="Cargando y procesando datos...")
def cargar_modelo_datos():
    # 1. Carga de datos crudos
    clientes = pd.read_csv("data/raw/megaStore/clientes.csv")
    localizacion = pd.read_csv("data/raw/megaStore/localizacion.csv")
    productos = pd.read_csv("data/raw/megaStore/productos.csv")
    ordenes = pd.read_csv("data/raw/megaStore/ordenes.csv")

    # 2. ETL modular
    clientes = transformar_clientes(clientes)
    localizacion = transformar_localizacion(localizacion)
    productos = transformar_productos(productos)
    ordenes = transformar_ordenes(ordenes)

    # 3. Generar calendario
    calendar = generar_calendar(ordenes)

    # 4. Construcción del modelo estrella
    df_final = construir_modelo(clientes, localizacion, productos, ordenes, calendar)
    
    return df_final

# --- Ejecución Principal ---

# Llamamos a la función cacheada
df = cargar_modelo_datos()

# --- Sidebar de filtros ---
# ESTO ES CRÍTICO: Asegúrate de que OrderDate sea de tipo datetime
if not pd.api.types.is_datetime64_any_dtype(df["OrderDate"]):
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors='coerce')
df_filtrado = render_filters(df)

# --- Renderizar Layout ---
render_layout(df_filtrado)