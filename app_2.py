import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
from dashboard.styles import apply_custom_css
from dashboard.filters import render_filters
from dashboard.layout import render_layout

# --- Configuración de página ---
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# --- Aplicar CSS ---
# IMPORTANTE: Esto queda fuera de la caché para que veas los cambios 
# visuales inmediatamente cada vez que edites los archivos CSS.
apply_custom_css()

# --- Barra superior con segmentadores ---
# --- Barra superior con segmentadores en una fila ---
col1, col2, col3 = st.columns([1,1,1])

with col1:
    periodo = st.segmented_control(
        "Período",
        ["Pre-pandemia", "Pandemia", "Post-pandemia"]
    )

with col2:
    canal = st.selectbox(
        "Canal",
        ["Todos los Canales", "Online", "Offline"]
    )

with col3:
    metrica = st.selectbox(
        "Métrica",
        ["Valores Corrientes (Nominal)", "Valores Constantes (2018)", "Ambos"],
        index=2
    )

# --- Cargar modelo estrella optimizado ---
@st.cache_data
def load_data():
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
    # Optimizar tipos
    df["monto_venta_ars_nominal"] = df["monto_venta_ars_nominal"].astype("float32")
    df["monto_venta_ars_real_2018"] = df["monto_venta_ars_real_2018"].astype("float32")
    df["cantidad"] = df["cantidad"].astype("int32")
    return df

df = load_data()

# Crear columna Periodo a partir de la fecha
df["Periodo"] = pd.to_datetime(df["fecha"]).apply(
    lambda x: "Pre-pandemia" if x < pd.Timestamp("2020-03-01")
    else "Pandemia" if x <= pd.Timestamp("2021-12-31")
    else "Post-pandemia"
)

# Filtrar según selección
df_filtrado = df[df["Periodo"] == periodo]
if canal != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Canal_Venta"] == canal]

# --- KPIs arriba ---
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales (Nominal)", f"${df_filtrado['monto_venta_ars_nominal'].sum():,.0f}")
col2.metric("Ventas Totales (Constantes 2018)", f"${df_filtrado['monto_venta_ars_real_2018'].sum():,.0f}")
col3.metric("Clientes Activos", df_filtrado["nombre_cliente"].nunique())

# --- Selección de métrica para gráficos ---
if metrica == "Valores Corrientes (Nominal)":
    y_col = "monto_venta_ars_nominal"
elif metrica == "Valores Constantes (2018)":
    y_col = "monto_venta_ars_real_2018"
else:
    y_col = "monto_venta_ars_nominal"  # default

# --- Gráfico de línea mensual (todo el ancho) ---
df_mensual = (
    df_filtrado.groupby(["año","mes","Canal_Venta"])[y_col]
    .sum()
    .reset_index()
)
df_mensual["Periodo_Mes"] = pd.to_datetime(
    df_mensual["año"].astype(str) + "-" + df_mensual["mes"].astype(str) + "-01"
)

fig_linea = px.line(
    df_mensual,
    x="Periodo_Mes",
    y=y_col,
    color="Canal_Venta",
    title=f"Evolución Mensual de Ventas ({metrica})"
)
st.plotly_chart(fig_linea, width="stretch")

# --- Layout inferior: izquierda (dos filas) + derecha (mapa) ---
col_izq, col_der = st.columns([2,1])

# Gráfico de barras por canal
fig_barras_canal = px.bar(
    df_filtrado.groupby("Canal_Venta")[y_col].sum().reset_index(),
    x="Canal_Venta",
    y=y_col,
    title=f"Ventas por Canal ({metrica})"
)
col_izq.plotly_chart(fig_barras_canal, width="stretch")

# Gráfico de distribución por categoría
fig_barras_cat = px.bar(
    df_filtrado.groupby("categoria")[y_col].sum().reset_index(),
    x="categoria",
    y=y_col,
    title=f"Distribución por Categoría ({metrica})"
)
col_izq.plotly_chart(fig_barras_cat, width="stretch")

# --- Mapa con puntos centrales usando geojson ---
# with open("data/geo/argentina_provincias.geojson", "r", encoding="utf-8") as f:
#     geojson = json.load(f)

# import requests
url = "https://apis.datos.gob.ar/georef/api/provincias?formato=geojson"
geojson = requests.get(url).json()

print(geojson["features"][0]["properties"])

provincias = []
for f in geojson["features"]:
    # Detectar automáticamente la clave de nombre
    props = f["properties"]
    nombre = props.get("nombre") or props.get("provincia") or props.get("NAME")
    lon, lat = f["geometry"]["coordinates"]
    provincias.append({"Provincia": nombre, "lat": lat, "lon": lon})

df_geo = pd.DataFrame(provincias)

ventas_prov = df_filtrado.groupby("Provincia")[y_col].sum().reset_index()
df_geo = df_geo.merge(ventas_prov, on="Provincia", how="left").fillna(0)

fig_mapbox = px.scatter_mapbox(
    df_geo,
    lat="lat",
    lon="lon",
    size=y_col,
    color=y_col,
    hover_name="Provincia",
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": -38.4161, "lon": -63.6167},
    title=f"Ventas por Provincia ({metrica})"
)
col_der.plotly_chart(fig_mapbox, width="stretch", height=800)

# --- Conclusión ---
st.markdown("---")
st.subheader("Conclusión:")
st.info(
    "El canal online mostró un crecimiento sostenido desde la etapa pre‑pandemia, acelerándose durante la pandemia"
    "y consolidándose en el período post. Este comportamiento se refleja de manera heterogénea entre provincias, "
    "con Buenos Aires y Córdoba liderando la adopción digital, mientras que otras regiones mantienen valores más "
    "constantes."
    "Recomendación de negocio: Consolidar la inversión en canales online, reforzando la infraestructura y estrategias"
    "de marketing digital en las provincias con mayor potencial de expansión, para capitalizar la tendencia "
    "y equilibrar la participación territorial."
)
st.subheader("Recomendación de negocio:")
st.info(
    "Consolidar la inversión en canales online, reforzando la infraestructura y estrategias"
    "de marketing digital en las provincias con mayor potencial de expansión, para capitalizar la tendencia "
    "y equilibrar la participación territorial."
)
    # "El canal online mostró un crecimiento sostenido antes, durante y después de la pandemia, "
    # "con provincias líderes como Buenos Aires y Córdoba. "
    # "Se recomienda consolidar la inversión digital para expandir la adopción en regiones con menor participación."