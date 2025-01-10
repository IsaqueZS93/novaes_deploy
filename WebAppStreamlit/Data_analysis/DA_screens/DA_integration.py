import streamlit as st

# Adiciona o caminho base ao sys.path
import sys
sys.path.append(r"C:\\Users\\Novaes Engenharia\\WebAppStreamlit")
import imports

from DA_manipulation_cards_table import layout as cards_table_layout
from DA_Screen_coleta_form import layout as coleta_form_layout
from DA_exp_ia import layout as export_layout

def DA_integration_layout():
    """
    Layout principal para integração de coleta e exportação de dados.
    Pode ser consumido por uma tela principal.
    """
    # Título estilizado
    st.markdown("<h1 style='text-align:center; color:#00509e;'>Coleta e Exportação de Dados</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2em;'>Gerencie os dados utilizando as seções abaixo.</p>", unsafe_allow_html=True)

    # Estados para controle da visibilidade das telas
    if "show_table" not in st.session_state:
        st.session_state.show_table = False
    if "show_coleta" not in st.session_state:
        st.session_state.show_coleta = False
    if "show_export" not in st.session_state:
        st.session_state.show_export = False

    # Botões estilizados de controle
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Análise de Dados", use_container_width=True):
            st.session_state.show_table = not st.session_state.show_table
    with col2:
        if st.button("📝 Coleta de Dados - Pitometria", use_container_width=True):
            st.session_state.show_coleta = not st.session_state.show_coleta
    with col3:
        if st.button("📊 Exportar Relatório", use_container_width=True):
            st.session_state.show_export = not st.session_state.show_export

    # Renderização condicional com cartões estilizados
    if st.session_state.show_table:
        st.markdown("<div class='card'><h4>Análise de Dados</h4></div>", unsafe_allow_html=True)
        cards_table_layout()

    if st.session_state.show_coleta:
        st.markdown("<div class='card'><h4>Coleta de Dados - Pitometria</h4></div>", unsafe_allow_html=True)
        coleta_form_layout()

    if st.session_state.show_export:
        st.markdown("<div class='card'><h4>Exportação de Relatórios</h4></div>", unsafe_allow_html=True)
        export_layout()
