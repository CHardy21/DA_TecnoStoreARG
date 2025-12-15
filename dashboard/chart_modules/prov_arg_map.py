import streamlit as st
import plotly.express as px

def render_map(df_filtrado, y_col, metrica, ALTO, size, zoomm):
        # --- Diccionario de coordenadas de provincias argentinas ---
        coords_provincias = {
            "Buenos Aires": (-34.61, -58.38),
            "Catamarca": (-28.47, -65.78),
            "Chaco": (-27.45, -58.99),
            "Chubut": (-43.30, -65.10),
            "Córdoba": (-31.42, -64.18),
            "Corrientes": (-27.48, -58.83),
            "Entre Ríos": (-31.73, -60.53),
            "Formosa": (-26.18, -58.17),
            "Jujuy": (-24.19, -65.30),
            "La Pampa": (-36.62, -64.29),
            "La Rioja": (-29.41, -66.85),
            "Mendoza": (-32.89, -68.84),
            "Misiones": (-27.36, -55.89),
            "Neuquén": (-38.95, -68.06),
            "Río Negro": (-39.03, -67.58),
            "Salta": (-24.79, -65.41),
            "San Juan": (-31.53, -68.52),
            "San Luis": (-33.30, -66.34),
            "Santa Cruz": (-51.62, -69.22),
            "Santa Fe": (-31.63, -60.70),
            "Santiago del Estero": (-27.79, -64.26),
            "Tierra del Fuego": (-54.80, -68.30),
            "Tucumán": (-26.83, -65.22)
        }

        # Agregar coordenadas al df de ventas por provincia
        ventas_prov = df_filtrado.groupby("Provincia")[y_col].sum().reset_index()
        ventas_prov["lat"] = ventas_prov["Provincia"].map(lambda x: coords_provincias.get(x, (None, None))[0])
        ventas_prov["lon"] = ventas_prov["Provincia"].map(lambda x: coords_provincias.get(x, (None, None))[1])

        fig_mapbox = px.scatter_mapbox(
        ventas_prov,
        lat="lat",
        lon="lon",
        size=y_col,
        color=y_col,
        color_continuous_scale="plasma",
        hover_name="Provincia",
        mapbox_style="carto-positron",
        zoom=zoomm,
        center={"lat": -38.4161, "lon": -63.6167},
        title=f"Ventas por Provincia ({metrica})",
        size_max=size
    )

        # Layout: alto y márgenes, más colorbar compacta
        fig_mapbox.update_layout(
            autosize=True,
            height=ALTO+15,  # controla el viewport vertical
            margin=dict(l=10,),
            #paper_bgcolor="white",
            #plot_bgcolor="white",
            coloraxis_colorbar=dict(
                title="", thickness=12, len=0.6, x=0.99  # barra de color más angosta y centrada
            ),
            legend=dict(yanchor="top", y=1, xanchor="left", x=10)
        )

        # Ajuste de zoom al contenido (si cambia el set de provincias)
        fig_mapbox.update_layout(
            mapbox=dict(center={"lat": -38.4161, "lon": -63.6167}, zoom=zoomm)
        )

        # Render en Streamlit
        st.plotly_chart(fig_mapbox, width='stretch')