import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import sys
sys.path.append(r"C:\Users\Novaes Engenharia\WebAppStreamlit")
import imports

from IA_loaders import *

# Tipos de arquivos válidos para upload
TIPOS_ARQUIVOS_VALIDOS = [
    'Site', 'Youtube', 'Pdf', 'Csv', 'Txt'
]

# Configuração dos modelos disponíveis
CONFIG_MODELOS = {'Groq': 
                        {'modelos': ['llama-3.1-70b-versatile', 'gemma2-9b-it', 'mixtral-8x7b-32768', 'llava-v1.5-7b-4096-prévia'],
                         'chat': ChatGroq},
                  'OpenAI': 
                        {'modelos': ['gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini'],
                         'chat': ChatOpenAI}}

# Memória persistente da conversa
MEMORIA = ConversationBufferMemory()

# Função para carregar arquivos
def carrega_arquivos(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Site':
        documento = carrega_site(arquivo)
    elif tipo_arquivo == 'Youtube':
        documento = carrega_youtube(arquivo)
    elif tipo_arquivo == 'Pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_pdf(nome_temp)
    elif tipo_arquivo == 'Csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_csv(nome_temp)
    elif tipo_arquivo == 'Txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_txt(nome_temp)
    return documento

# Função para carregar o modelo selecionado
def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
    documento = carrega_arquivos(tipo_arquivo, arquivo)

    system_message = f"""
    Você é um assistente amigável chamado Águia.
    Você possui acesso às seguintes informações vindas de um documento {tipo_arquivo}: 

    ####
    {documento}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substitua por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Águia!
    """

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])
    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat

    st.session_state['chain'] = chain

# Página de chat do Águia
def pagina_chat():
    st.markdown('<h1 class="custom-header">🦅 IA CHATBOT - Águia</h1>', unsafe_allow_html=True)

    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carregue o Águia para iniciar a conversa.')
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Fale com Águia')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input': input_usuario, 
            'chat_history': memoria.buffer_as_messages
            }))
        
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

# Barra lateral com configuração do chatbot
def sidebar():
    st.sidebar.markdown('<h2 class="sidebar-header">Configurações do Águia</h2>', unsafe_allow_html=True)
    tabs = st.sidebar.tabs(['Upload de Arquivos', 'Seleção de Modelos'])

    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a URL do site')
        elif tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a URL do vídeo')
        elif tipo_arquivo in ['Pdf', 'Csv', 'Txt']:
            arquivo = st.file_uploader(f'Faça o upload do arquivo {tipo_arquivo.lower()}', type=[f'.{tipo_arquivo.lower()}'])

    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor do modelo', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        api_key = st.text_input(
            f'Adicione a API key para o provedor {provedor}',
            value=st.session_state.get(f'api_key_{provedor}', ''))
        st.session_state[f'api_key_{provedor}'] = api_key

    if st.sidebar.button('Inicializar Águia', use_container_width=True):
        carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)
    if st.sidebar.button('Apagar Histórico de Conversa', use_container_width=True):
        st.session_state['memoria'] = MEMORIA

# Tela integrada ao projeto
def layout():
    with st.sidebar:
        sidebar()
    pagina_chat()
