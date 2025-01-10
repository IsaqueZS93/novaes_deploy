import streamlit as st
from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

# Função para criar o PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Dados", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def add_section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)

    def add_paragraph(self, text):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln(5)

    def add_table(self, df, col_widths=None):
        self.set_font("Arial", "B", 10)
        for col in df.columns:
            self.cell(col_widths, 10, col, 1, 0, "C")
        self.ln()
        self.set_font("Arial", "", 10)
        for index, row in df.iterrows():
            for item in row:
                self.cell(col_widths, 10, str(item), 1, 0, "C")
            self.ln()

# Função principal para exportar os dados
def export_to_pdf():
    # Verificar se os dados estão disponíveis no estado da sessão
    if "merged_result" not in st.session_state or "form_data" not in st.session_state:
        st.error("Nenhum dado disponível para exportação.")
        return

    # Solicitar ao usuário quais informações deseja incluir
    st.title("Exportar Dados para PDF")
    st.subheader("Escolha as informações que deseja incluir no relatório:")
    include_macro_pitometria = st.checkbox("Processamento de arquivos Macro e Pitometria")
    include_fluxo_perfil = st.checkbox("Perfil de Velocidade do Fluxo da Tubulação")
    include_all = st.checkbox("TUDO")

    # Preparar o conteúdo para o PDF
    if st.button("Gerar PDF"):
        if not any([include_macro_pitometria, include_fluxo_perfil, include_all]):
            st.warning("Selecione pelo menos uma seção para incluir no relatório.")
            return

        pdf = PDF()
        pdf.add_page()

        # Adicionar informações de Processamento de Arquivos Macro e Pitometria
        if include_macro_pitometria or include_all:
            pdf.add_section_title("Processamento de Arquivos Macro e Pitometria")
            if "fv" in st.session_state and "kc" in st.session_state:
                pdf.add_paragraph(f"Fator de Correção (FV): {st.session_state['fv']}")
                pdf.add_paragraph(f"Constante de Correção (KC): {st.session_state['kc']}")
            if "merged_result" in st.session_state:
                pdf.add_paragraph("Tabela de Resultados:")
                df = st.session_state["merged_result"]
                pdf.add_table(df, col_widths=40)

        # Adicionar informações do Perfil de Velocidade do Fluxo
        if include_fluxo_perfil or include_all:
            pdf.add_section_title("Perfil de Velocidade do Fluxo da Tubulação")
            if "form_data" in st.session_state:
                pdf.add_paragraph("Tabela de Pontos e Velocidades:")
                df = st.session_state["form_data"]
                pdf.add_table(df, col_widths=50)

        # Salvar PDF
        output_dir = "exported_reports"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        pdf.output(output_file)

        # Informar ao usuário
        st.success(f"Relatório gerado com sucesso: {output_file}")
        st.download_button(
            label="Baixar Relatório",
            data=open(output_file, "rb").read(),
            file_name=os.path.basename(output_file),
            mime="application/pdf",
        )
