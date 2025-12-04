import streamlit as st
import plotly.express as px
import pandas as pd

# Mapeo de estados fuera de la función para mayor limpieza
STATE_MAP = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT",
    "Delaware":"DE","Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA",
    "Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
    "Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH",
    "New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK",
    "Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN",
    "Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
}

def render_state_map(df: pd.DataFrame, column):
    # Lógica de cálculo: Mapa por estado (USA)
    df_estado = df.groupby("State")["TotalSales"].sum().reset_index()
    df_estado["StateCode"] = df_estado["State"].map(STATE_MAP)
    
    fig_mapa = px.choropleth(
        df_estado,
        locations="StateCode",
        locationmode="USA-states",
        color="TotalSales",
        scope="usa",
        title="Ventas por Estado"
    )
    
    # Renderizar en la columna pasada
    with column:
        st.plotly_chart(fig_mapa, use_container_width=True)