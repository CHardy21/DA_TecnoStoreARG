import streamlit as st

def render_reset_button(label: str = "🔄 Resetear filtros") -> bool:
    """
    Renderiza un botón de reset en la sidebar.
    Devuelve True si el usuario lo presiona.
    """
    if st.sidebar.button(label):
        # Marcamos un flag en session_state
        st.session_state.reset = True
        st.rerun()
        return True
    return False
