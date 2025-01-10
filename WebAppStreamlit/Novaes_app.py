import streamlit as st
import os
import sys
import traceback

# Adiciona o caminho base ao sys.path
sys.path.append(r"C:/Users/Novaes Engenharia/WebAppStreamlit")
import imports

# Função para registrar logs de erros
def log_error(context, exception):
    st.error(f"Erro em {context}: {str(exception)}")
    st.write("Detalhes do erro:")
    st.text(traceback.format_exc())

# Configuração inicial do aplicativo
try:
    st.set_page_config(page_title="Grupo NOVAES Dashboard", layout="wide")
except Exception as e:
    st.error("Configuração inicial já definida. Ignorando esta configuração.")

# Função para carregar o arquivo de estilo
def load_css():
    css_file = os.path.join("C:/Users/Novaes Engenharia/WebAppStreamlit/utils_styles/US_styles", "US_style.css")
    try:
        if os.path.exists(css_file):
            with open(css_file, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            raise FileNotFoundError(f"Arquivo CSS não encontrado: {css_file}")
    except Exception as e:
        log_error("Carregar arquivo CSS", e)

# Carregar o estilo personalizado
load_css()

# Importação das telas com logs de erros
try:
    from WAS_home import layout as home_layout
except ImportError as e:
    log_error("Carregar tela Home", e)
    home_layout = lambda: st.error("Erro ao carregar a tela Home.")

try:
    from DA_integration import DA_integration_layout as integration_layout
except ImportError as e:
    log_error("Carregar tela Integração", e)
    integration_layout = lambda: st.error("Erro ao carregar a tela de Integração.")

try:
    from IA_chatbot import layout as chatbot_layout
except ImportError as e:
    log_error("Carregar tela do IA CHATBOT", e)
    chatbot_layout = lambda: st.error("Erro ao carregar a tela do IA CHATBOT.")

try:
    from aesels import aesels_layout
except ImportError as e:
    log_error("Carregar layout do AESels", e)
    aesels_layout = lambda: st.error("Erro ao carregar o layout do AESels.")

# Carregar logotipo com logs
logo_path = "C:/Users/Novaes Engenharia/WebAppStreamlit/utils_styles/US_Imagens/logo_grupo_novaes.png"
try:
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, caption="Grupo Novaes", width=150)
    else:
        st.sidebar.error("Logotipo não encontrado. Verifique o caminho.")
except Exception as e:
    log_error("Carregar logotipo", e)

# Navegação entre páginas com logs
try:
    st.sidebar.title("Menu de Navegação")
    st.sidebar.markdown("---")
    selected_page = st.sidebar.radio(
        "Ir para",
        options=["Início", "Análise de Dados - Águia", "IA CHATBOT - Águia", "Visão - Águia"]
    )
except Exception as e:
    log_error("Configuração do menu de navegação", e)

# Exibe o layout correspondente com logs
try:
    if selected_page == "Início":
        home_layout()
    elif selected_page == "Análise de Dados - Águia":
        integration_layout()
    elif selected_page == "IA CHATBOT - Águia":
        chatbot_layout()
    elif selected_page == "Visão - Águia":
        aesels_layout()
    else:
        st.error("Página não encontrada.")
except Exception as e:
    log_error(f"Renderizar página selecionada: {selected_page}", e)
