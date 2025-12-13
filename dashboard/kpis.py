import streamlit as st

# --- Funciones de formato ---
def formato_latino(num):
    """Formatea un número con punto como separador de miles y coma como decimal (formato latino)."""
    return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formato_millones(valor):
    millones = valor / 1_000_000
    return f"{millones:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_kpis(df_filtrado, metrica):
    ventas_nominal = df_filtrado['monto_venta_ars_nominal'].sum()
    ventas_constantes = df_filtrado['monto_venta_ars_real_2018'].sum()
    clientes_activos = df_filtrado["nombre_cliente"].nunique()
    # --- Cálculo participación online ---
    ventas_online = df_filtrado.loc[df_filtrado["Canal_Venta"] == "Online", "monto_venta_ars_nominal"].sum()
    participacion_online = (ventas_online / ventas_nominal) * 100
    if metrica=="Valores Constantes (2018)":
        ticket_promedio = df_filtrado['monto_venta_ars_real_2018'].mean()
    else:
        ticket_promedio = df_filtrado['monto_venta_ars_nominal'].mean()

   
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-label'>Ventas Totales (Nominal)</div>"
        f"<div class='metric-value'>${formato_millones(ventas_nominal)}"
        f"<span class='metric-suffix'>Mill.</span></div>"
        f"</div>", unsafe_allow_html=True
    )

    col2.markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-label'>Ventas Totales (Constantes 2018)</div>"
        f"<div class='metric-value'>${formato_millones(ventas_constantes)}"
        f"<span class='metric-suffix'>Mill.</span></div>"
        f"</div>", unsafe_allow_html=True
    )
    col3.markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-label'>Participación Canal Online</div>"
        f"<div class='metric-value'>{formato_latino(participacion_online)}"
        f"<span class='metric-suffix'>%</span></div>"
        f"</div>", unsafe_allow_html=True
    )

    col4.markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-label'>Ticket Promedio</div>"
        f"<div class='metric-value'>${formato_latino(ticket_promedio)}</div>"
        f"</div>", unsafe_allow_html=True
    )
