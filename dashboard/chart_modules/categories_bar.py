import streamlit as st
import plotly.express as px


def render_categories_bar(df_filtrado, y_col, metrica, ALTO):

    fig_barras_cat = px.bar(
                df_filtrado.groupby("categoria")[y_col].sum().reset_index(),
                x="categoria",
                y=y_col,
                title=f"Distribución por Categoría ({metrica})",
                labels={
                    "categoria": "Categoría de Productos",
                    y_col: "Monto   de  Ventas"  # acá renombrás el eje Y
                    }
            )
    fig_barras_cat.update_layout(height=ALTO)
            
    st.plotly_chart(fig_barras_cat, width='stretch')
