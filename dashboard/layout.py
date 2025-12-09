# import streamlit as st
# from dashboard.kpis import render_kpis
# from dashboard.charts import render_charts

# def render_layout(df_filtrado):
#     st.title("MegaStore Dashboard ")

#     # KPIs en fila superior
#     render_kpis(df_filtrado)

#     st.markdown("---")

#     # Gráficos en grid 2x2
#     render_charts(df_filtrado)

# import streamlit as st
# import plotly.express as px

# def render_layout(df_filtrado, metrica):
#     # --- KPIs ---
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Ventas Totales (Nominal)", f"${df_filtrado['monto_venta_ars_nominal'].sum():,.0f}")
#     col2.metric("Ventas Totales (Constantes 2018)", f"${df_filtrado['monto_venta_ars_real_2018'].sum():,.0f}")
#     col3.metric("Clientes Activos", df_filtrado["nombre_cliente"].nunique())

#     # --- Selección de métrica ---
#     if metrica == "Valores Corrientes (Nominal)":
#         y_col = "monto_venta_ars_nominal"
#     elif metrica == "Valores Constantes (2018)":
#         y_col = "monto_venta_ars_real_2018"
#     else:
#         y_col = "monto_venta_ars_nominal"

#     # --- Gráfico de línea mensual ---
#     df_mensual = (
#         df_filtrado.groupby(["año","mes","Canal_Venta"])[y_col]
#         .sum()
#         .reset_index()
#     )
#     df_mensual["Periodo_Mes"] = pd.to_datetime(
#         df_mensual["año"].astype(str) + "-" + df_mensual["mes"].astype(str) + "-01"
#     )

#     fig_linea = px.line(
#         df_mensual,
#         x="Periodo_Mes",
#         y=y_col,
#         color="Canal_Venta",
#         title=f"Evolución Mensual de Ventas ({metrica})"
#     )
#     st.plotly_chart(fig_linea, width="stretch")

#     # --- Placeholder para más gráficos ---
#     st.markdown("### Próximos gráficos aquí...")
#     # Ejemplo: barras por canal, categorías, mapa

import streamlit as st
from dashboard.kpis import render_kpis
from dashboard.charts import render_charts

def render_layout(df_filtrado, metrica):
    
    # KPIs en fila superior
    render_kpis(df_filtrado)

    st.markdown("---")

    # Gráficos en grid 2x2
    render_charts(df_filtrado, metrica)
