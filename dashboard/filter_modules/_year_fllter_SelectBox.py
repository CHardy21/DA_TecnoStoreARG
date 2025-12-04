import streamlit as st

def render_year_filter(df):
    year = st.sidebar.selectbox("Año", sorted(df["OrderDate"].dt.year.dropna().unique()),
    )