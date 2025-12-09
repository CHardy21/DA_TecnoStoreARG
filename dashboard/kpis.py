import streamlit as st

def formato_millones(valor):
    millones = valor / 1_000_000
    return f"{millones:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def render_kpis(df_filtrado):
    ventas_nominal = df_filtrado['monto_venta_ars_nominal'].sum()
    ventas_constantes = df_filtrado['monto_venta_ars_real_2018'].sum()
    clientes_activos = df_filtrado["nombre_cliente"].nunique()

    # CSS responsive
    st.markdown("""
        <style>
        .metric-box {
            border: 1px solid #1e1e1e;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            background-color: #000;
        }
        .metric-label {
            font-size: 1em;
            color: #fff;
        }
        .metric-value {
            font-size: 3em;
            color: #1c48cb;
        }
        .metric-suffix {
            font-size: 0.5em;
            vertical-align: super;
            color: gray;
            margin-left: 4px;
        }

        /* --- Responsive --- */
        @media (max-width: 768px) {
            .metric-value {
                font-size: 2em;   /* más chico en tablets/móviles */
            }
            .metric-label {
                font-size: 0.9em;
            }
            .metric-suffix {
                font-size: 0.6em;
            }
        }

        @media (max-width: 480px) {
            .metric-value {
                font-size: 1.5em; /* aún más chico en móviles */
            }
            .metric-label {
                font-size: 0.8em;
            }
            .metric-suffix {
                font-size: 0.5em;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

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
        f"<div class='metric-label'>Clientes Activos</div>"
        f"<div class='metric-value'>{clientes_activos:,}".replace(",", ".") + "</div>"
        f"</div>", unsafe_allow_html=True
    )
