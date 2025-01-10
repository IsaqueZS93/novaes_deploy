import os
from time import sleep
import streamlit as st
from langchain_community.document_loaders import (WebBaseLoader,
                                                  YoutubeLoader, 
                                                  CSVLoader, 
                                                  PyPDFLoader, 
                                                  TextLoader)
from fake_useragent import UserAgent

def carrega_site(url):
    """
    Carrega o conte do de um site. Se no der certo, tenta novamente 5 vezes.
    """
    documento = ''
    for i in range(5):
        try:
            # Coloca um User Agent aleat rio para evitar bloqueios
            os.environ['USER_AGENT'] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            lista_documentos = loader.load()
            documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
            break
        except:
            # Se no der certo, imprime um erro e espera 3 segundos
            print(f'Erro ao carregar o site {i+1}')
            sleep(3)
    if documento == '':
        # Se no der certo at 5 tentativas, imprime um erro e para a execu o
        st.error('N o foi poss vel carregar o site')
        st.stop()
    return documento

def carrega_youtube(video_id):
    """
    Carrega o conteúdo de um vídeo do YouTube.

    Args:
        video_id (str): O ID do vídeo do YouTube.

    Returns:
        str: O conteúdo concatenado das páginas do vídeo.
    """
    # Cria um carregador para o vídeo do YouTube com informações de vídeo desativadas
    loader = YoutubeLoader(video_id, add_video_info=False, language=['pt'])
    
    # Carrega os documentos associados ao vídeo
    lista_documentos = loader.load()
    
    # Concatena o conteúdo das páginas dos documentos em uma única string
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    
    return documento

def carrega_csv(caminho):
    loader = CSVLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carrega_pdf(caminho):
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carrega_txt(caminho):
    loader = TextLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento
