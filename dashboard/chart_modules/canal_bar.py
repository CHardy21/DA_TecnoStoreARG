import streamlit as st
import plotly.express as px


def render_canal_bar(df_filtrado, y_col, metrica, ALTO):

    fig_barras_canal = px.bar(
        df_filtrado.groupby("Canal_Venta")[y_col].sum().reset_index(),
        x="Canal_Venta",
        y=y_col,
        title=f"Ventas por Canal ({metrica})",
        labels={
            "Canal_Venta": "Canal  de  Ventas",
            y_col: "Monto   de  Ventas"  # acá renombrás el eje Y
            }
    )
    fig_barras_canal.update_layout(height=ALTO)
    st.plotly_chart(fig_barras_canal, width='stretch')