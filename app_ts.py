import streamlit as st
import pandas as pd
# Importar la función de limpieza y unión de datos (la que harás en data_prep.py)
# from data_prep import cargar_y_limpiar_datos 

# Simulación de la carga de datos limpios para el ejemplo
# Asume que esta variable tiene el DataFrame final consolidado
df_final = pd.read_csv('data/generated_IA/ventas_electro_tecnologia_simulado.csv') 
df_final['Fecha'] = pd.to_datetime(df_final['Fecha'])

# --- Configuración y Título ---
st.set_page_config(layout="wide", page_title="Tesis: Evolución de Ventas Tech & Electro")

st.title("📊 La Gran Transformación: Ventas Tech y Electro (2018-2024)")
st.markdown("---")

# --- Barra Lateral para la Narrativa y Filtros ---
st.sidebar.header("📜 Narrativa de Datos")

# Opción de filtrar por Periodo (esto es clave para tu historia)
periodo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Periodo Histórico:",
    ["Visión General", "1. Pre-Pandemia (2018-Mar 2020)", "2. Pandemia (Mar 2020-Dic 2021)", "3. Post-Pandemia (2022-2024)"]
)

# Lógica de Filtrado (Muy simplificada para el ejemplo)
if "Pre-Pandemia" in periodo_seleccionado:
    df_filtered = df_final[df_final['Fecha'] < '2020-03-01']
elif "Pandemia" in periodo_seleccionado:
    df_filtered = df_final[(df_final['Fecha'] >= '2020-03-01') & (df_final['Fecha'] < '2022-01-01')]
elif "Post-Pandemia" in periodo_seleccionado:
    df_filtered = df_final[df_final['Fecha'] >= '2022-01-01']
else:
    df_filtered = df_final.copy() # Visión General

# --- Visualización de la Historia ---

st.header(f"Foco Analítico: {periodo_seleccionado}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ventas Netas Totales vs. Canal")
    st.markdown(f"**Análisis:** Visualización de la **Gran Transformación** de canales. Observa cómo el canal Online (azul) gana terreno sobre Sucursales (rojo) especialmente en el periodo 'Pandemia'.")
    
    # Crear un DataFrame para el gráfico apilado de ventas por canal
    df_canales = df_filtered.set_index('Fecha')[['Ventas_Online_USD_MM', 'Ventas_Sucursales_USD_MM']]
    st.line_chart(df_canales, use_container_width=True)

with col2:
    st.subheader("KPIs del Periodo")
    
    # Cálculo de KPIs
    ventas_totales_periodo = df_filtered['Ventas_Netas_Totales_USD_MM'].sum()
    ventas_online_periodo = df_filtered['Ventas_Online_USD_MM'].sum()
    porcentaje_online = (ventas_online_periodo / ventas_totales_periodo) * 100 if ventas_totales_periodo else 0
    
    st.metric(label="Ventas Totales (USD MM)", value=f"{ventas_totales_periodo:,.2f}")
    st.metric(label="% Ventas Online", value=f"{porcentaje_online:.1f}%")

st.markdown("---")

# --- Mapeo Geográfico (Simulación) ---
# Necesitarías las coordenadas de latitud/longitud en tu DataFrame de sucursales para esto.
st.header("📍 Distribución Geográfica de Sucursales (Argentina)")
st.markdown("Muestra la distribución de las sucursales (ejemplo) para cumplir con el requisito de mapa.")

# Simulación de datos geográficos para el mapa
map_data = pd.DataFrame({
    'lat': [-34.6037, -31.4201, -32.8895], # Buenos Aires, Córdoba, Mendoza
    'lon': [-58.3816, -64.1888, -68.8458],
    'size': [100, 50, 30] # El tamaño podría ser proporcional a las ventas
})

st.map(map_data, size='size')

st.markdown("---")
st.success("¡Streamlit te permitirá presentar tu tesis de forma interactiva y profesional!")