import streamlit as st

# Importar o layout
try:
    from DA_Screen_graphics import layout
except ImportError as e:
    st.error("Erro ao importar o módulo DA_Screen_graphics.")
    st.write("Detalhes do erro:", e)
    raise e

# Tentar executar o layout
try:
    layout()
except Exception as e:
    st.error("Erro ao executar o layout do DA_Screen_graphics.")
    st.write("Detalhes do erro:", e)
    raise e
