import streamlit as st
from dashboard.kpis import render_kpis
from dashboard.charts import render_charts


def render_layout(df_filtrado, metrica, sidebar: bool):
    
    # KPIs en fila superior
    render_kpis(df_filtrado, metrica)

    #st.markdown("---")

    # Gráficos en grid 2x2
    render_charts(df_filtrado, metrica, sidebar)

    # --- Conclusión ---
    st.markdown("---")
    st.subheader("Conclusión:")
    st.info(
        "El canal online mostró un crecimiento sostenido desde la etapa pre‑pandemia, acelerándose durante la pandemia "
        "y consolidándose en el período post-pandemia.\n\n Este comportamiento se refleja de manera heterogénea entre provincias, "
        "con Buenos Aires y Santa Fe liderando la adopción digital, mientras que otras regiones mantienen valores más "
        "constantes."
    )
    st.subheader("Recomendación de negocio:")
    st.info(
        "Consolidar la inversión en canales online, reforzando la infraestructura y estrategias"
        "de marketing digital en las provincias con mayor potencial de expansión, para capitalizar la tendencia "
        "y equilibrar la participación territorial.\n\n"
        "**El futuro del consumo ya no es híbrido, es digital‑centrado.**"
    )
