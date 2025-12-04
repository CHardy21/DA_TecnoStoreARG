import streamlit as st

# --- Función de formato ---
def formato_latino(num):
    """Formatea un número con punto como separador de miles y coma como decimal (formato latino)."""
    return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Función principal de renderizado de KPIs ---
def render_kpis(df_filtrado):
    df_filtrado["TotalSales"] = df_filtrado["Sales"] * df_filtrado["Quantity"]
    df_filtrado["TotalDiscount"] = df_filtrado["TotalSales"] * df_filtrado["Discount"]

    total_sales = df_filtrado["TotalSales"].sum()
    total_profit = df_filtrado["Profit"].sum()
    total_discount = df_filtrado["TotalDiscount"].sum()
    avg_sales_per_order = df_filtrado["TotalSales"].mean()

    # --- KPIs en horizontal ---
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.metric("Total Sales Amount", f"${formato_latino(total_sales)}")
    with kpi_cols[1]:
        st.metric("Total Profit", f"${formato_latino(total_profit)}")
    with kpi_cols[2]:
        st.metric("Total Discount", f"${formato_latino(total_discount)}")
    with kpi_cols[3]:
        st.metric("Avg Sales per Order", f"${formato_latino(avg_sales_per_order)}")
