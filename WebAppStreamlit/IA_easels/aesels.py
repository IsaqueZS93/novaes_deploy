import streamlit as st
import sys
import os
import traceback
from PIL import Image
from langchain_groq.chat_models import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

def aesels_layout():
    # Adiciona o caminho base ao sys.path
    sys.path.append(r"C:\\Users\\Novaes Engenharia\\WebAppStreamlit")

    # Função para registrar logs de erros
    def log_error(context, exception):
        st.error(f"Erro em {context}: {str(exception)}")
        st.write("Detalhes do erro:")
        st.text(traceback.format_exc())

    # Importar dependências específicas
    try:
        from image_analysis_yolo import analyze_image
        from IAE_manual_train import run_validation
    except ImportError as e:
        log_error("Importação de módulos específicos", e)
        analyze_image = None
        run_validation = None

    # Diretório para salvar as imagens analisadas
    ANALYSIS_DIR = r"C:\\Users\\Novaes Engenharia\\WebAppStreamlit\\IA_easels\\IAE_data\\IAE_analysis"
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    # Configurar modelo LangChain com Groq
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key="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"
    )

    # Função para salvar imagens analisadas
    def save_analyzed_image(image, filename):
        sanitized_filename = filename.replace(" ", "_").replace(":", "_").replace("\\", "_").replace("/", "_")
        save_path = os.path.join(ANALYSIS_DIR, sanitized_filename)
        image.save(save_path)
        return save_path

    # Função para processar a análise com YOLO
    def process_image_analysis(image_path):
        if analyze_image is None:
            raise Exception("Módulo de análise de imagem não carregado corretamente.")
        try:
            results = analyze_image(image_path)
            return results
        except Exception as e:
            raise Exception(f"Erro ao realizar a análise da imagem: {e}")

    # Função para gerar comentários usando LangChain Groq
    def generate_comments(detections):
        try:
            if not detections:
                return "Nenhuma detecção foi encontrada na imagem."

            detection_descriptions = [
                f"Rótulo: {detection['label']}, Caixa: {detection['bbox']}"
                for detection in detections if detection['confidence'] > 0.7
            ]

            prompt_text = (
                "Baseado nas seguintes detecções, forneça um comentário detalhado sobre a imagem. \n"
                + "\n".join(detection_descriptions) + "\n"
                + "Quando houver detecções de um mesmo rótulo, apresente apenas uma vez.\n"
                + "Quando for detectado Hidrometro novo e Lacre Azul mencione que o cavalete está padronizado em negrito no início da frase.\n"
                + "Quando houver presença de hidrometro velho, comente que o hidrometro deve ser substituído e coloque em negrito no início da frase 'Necessidade de substituição de hidrometro'.\n"
                + "Não tem necessidade de falar sobre a confiança da detecção, quando for superior a 70%.\n"
                + "Todos os comentários devem ser escritos em português e não ultrapassar 200 palavras. \n"
                + "Quando for detectado calçada ou muro danificado comente a necessidade de recomposição e informe a necessidade de abertura de Ordem de serviço.\n"
                + "Quando entulhos forem detectados, informe a necessidade de limpar o ambiente antes de concluir o serviço.\n"
                + "Em caso das detecções não localizadas, não comente sobre elas.\n"
            )

            prompt = ChatPromptTemplate.from_messages([HumanMessage(content=prompt_text)])
            response = llm(prompt.format_prompt().to_messages())
            return response.content.strip()
        except Exception as e:
            return f"Erro ao gerar comentários: {e}"

    # Tela principal de Upload e Análise
    def upload_and_analyze():
        st.title("Analisador de Cavaletes - Upload e Análise")
        st.markdown("<div class='dcc-upload'>Envie suas imagens para análise detalhada.</div>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Selecione as imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Imagem carregada: {uploaded_file.name}", use_column_width=True)

                if st.button(f"Analisar {uploaded_file.name}"):
                    try:
                        analyzed_image_path = save_analyzed_image(image, uploaded_file.name)
                        results = process_image_analysis(analyzed_image_path)

                        st.subheader("Resultados da Análise")
                        st.image(results["annotated_image"], caption="Imagem Anotada", use_column_width=True)

                        if results["detections"]:
                            st.write("### Detecções:")
                            for detection in results["detections"]:
                                st.write(f"- **Rótulo:** {detection['label']}")

                            comments = generate_comments(results["detections"])
                            st.subheader("Comentários da IA")
                            st.write(f"<div class='card'>{comments}</div>", unsafe_allow_html=True)
                        else:
                            st.write("Nenhuma detecção foi encontrada.")
                    except Exception as e:
                        st.error(f"Erro ao realizar a análise: {e}")

    # Tela principal para Validação Manual
    def manual_validation():
        st.title("Validação Manual e Rotulagem")
        st.markdown("<div class='dcc-upload'>Envie suas imagens para rotulagem manual.</div>", unsafe_allow_html=True)
        if run_validation:
            run_validation()
        else:
            st.error("❌ Módulo de validação manual não disponível.")

    # Menu de Navegação
    try:
        st.sidebar.title("Menu de Navegação")
        st.sidebar.markdown("---")
        selected_page = st.sidebar.radio(
            "Escolha a funcionalidade:",
            ["Upload e Análise", "Validação Manual"]
        )

        if selected_page == "Upload e Análise":
            upload_and_analyze()
        elif selected_page == "Validação Manual":
            manual_validation()
    except Exception as e:
        log_error("Configuração do menu de navegação", e)
