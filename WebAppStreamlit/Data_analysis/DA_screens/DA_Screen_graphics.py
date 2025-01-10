import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from fpdf import FPDF
import os
from datetime import datetime

# Adiciona o caminho base ao sys.path
import sys
sys.path.append(r"C:\Users\Novaes Engenharia\WebAppStreamlit")
import imports

from P_Macro import process_macro_file
from P_Pitot import process_pitometria_file
from P_MP import merge_macro_pitometria
from DA_Screen_coleta_form import layout as coleta_form_layout

# Caminho para a logo
LOGO_PATH = r"C:\Users\Novaes Engenharia\WebAppStreamlit\utils_styles\US_Imagens\logo_grupo_novaes.png"

# Função para inicializar o estado
def initialize_session_state():
    st.session_state.setdefault("show_results", False)
    st.session_state.setdefault("form_data", None)
    st.session_state.setdefault("graph", None)
    st.session_state.setdefault("merged_result", None)

# Classe para criação de PDFs
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

    def add_table(self, df, col_widths=40):
        self.set_font("Arial", "B", 10)
        for col in df.columns:
            self.cell(col_widths, 10, str(col), 1, 0, "C")
        self.ln()
        self.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            for item in row:
                self.cell(col_widths, 10, str(item), 1, 0, "C")
            self.ln()

    def add_graph(self, graph_image_path):
        self.add_section_title("Gráficos")
        self.image(graph_image_path, x=10, y=None, w=190)

# Função para exportar os dados para PDF
def export_to_pdf(include_table, include_graphs, include_profile):
    pdf = PDF()
    pdf.add_page()

    if include_table and st.session_state["merged_result"] is not None:
        pdf.add_section_title("Tabela de Resultados - Exportação Parcial")
        pdf.add_paragraph("Esta tabela contém as 30 primeiras linhas dos resultados processados.")
        data = st.session_state["merged_result"].head(30)
        pdf.add_table(data)

    if include_graphs and st.session_state["graph"] is not None:
        try:
            import kaleido
            graph_image_path = "temp_graph.png"
            st.session_state["graph"].write_image(graph_image_path, format="png")
            pdf.add_graph(graph_image_path)
            os.remove(graph_image_path)
        except ImportError:
            st.error("A biblioteca 'kaleido' é necessária para exportar gráficos. Instale-a usando 'pip install -U kaleido'.")

    if include_profile and st.session_state["form_data"] is not None:
        pdf.add_section_title("Perfil de Velocidade do Fluxo da Tubulação")
        profile_data = st.session_state["form_data"]
        pdf.add_table(profile_data)

    output_file = f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(output_file, 'F')

    with open(output_file, "rb") as f:
        st.download_button(
            label="Baixar Relatório em PDF",
            data=f.read(),
            file_name=output_file,
            mime="application/pdf",
        )

    os.remove(output_file)

# Função principal para o layout
def layout():
    initialize_session_state()

    st.title("Upload de Arquivos e Informações")
    st.markdown("### Processamento de arquivos Macro e Pitometria")

    macro_file = st.file_uploader("Arquivo do Macromedidor", type=["csv", "xlsx"])
    pitometria_file = st.file_uploader("Arquivo de Pitometria", type=["csv", "xlsx"])

    unidade = st.text_input("Unidade", placeholder="Digite a unidade")
    empresa = st.text_input("Empresa responsável", placeholder="Digite a empresa responsável")

    if st.button("Processar Dados"):
        if macro_file and pitometria_file:
            try:
                with open("temp_macro.csv", "wb") as macro_temp:
                    macro_temp.write(macro_file.getbuffer())
                with open("temp_pitometria.csv", "wb") as pitometria_temp:
                    pitometria_temp.write(pitometria_file.getbuffer())

                macro_result = process_macro_file("temp_macro.csv")
                fv, kc, pitometria_data = process_pitometria_file("temp_pitometria.csv")

                pitometria_result = {"fv": fv, "kc": kc, "data": pitometria_data.to_dict("records")}
                merged_result = merge_macro_pitometria(macro_result, pitometria_result)
                merged_result = merged_result.drop_duplicates(subset=["Hora"])

                desvio_relativo = "N/A"
                if "Flow Speed" in merged_result.columns and "Veloc.(m/s)" in merged_result.columns:
                    desvio_relativo = (abs(merged_result["Flow Speed"] - merged_result["Veloc.(m/s)"]) / merged_result["Flow Speed"]).mean() * 100
                    desvio_relativo = f"{desvio_relativo:.2f}%"

                st.session_state.update({
                    "fv": fv,
                    "kc": kc,
                    "desvio_relativo": desvio_relativo,
                    "merged_result": merged_result,
                    "show_results": True
                })

                st.success("Dados processados com sucesso!")

            except Exception as e:
                st.error(f"Erro ao processar os dados: {e}")
        else:
            st.warning("Ambos os arquivos devem ser enviados para processamento.")

    if st.session_state["show_results"]:
        st.subheader("Resultados")
        col1, col2, col3 = st.columns(3)
        col1.metric("FV", st.session_state["fv"])
        col2.metric("KC", st.session_state["kc"])
        col3.metric("Desvio Relativo (%)", st.session_state["desvio_relativo"])

        st.subheader("Tabela de Resultados")
        st.data_editor(st.session_state["merged_result"], height=400)

        st.subheader("Gráficos")
        fig = go.Figure()
        merged_result = st.session_state["merged_result"]

        if "Vazão(Q m³/h)" in merged_result:
            fig.add_trace(go.Scatter(x=merged_result["Hora"], y=merged_result["Vazão(Q m³/h)"], mode='lines', name='Vazão (Q m³/h)', line=dict(color='black')))
        if "Veloc.(m/s)" in merged_result:
            fig.add_trace(go.Scatter(x=merged_result["Hora"], y=merged_result["Veloc.(m/s)"], mode='lines', name='Velocidade (m/s)', line=dict(color='red')))
        if "Flow Speed" in merged_result:
            fig.add_trace(go.Scatter(x=merged_result["Hora"], y=merged_result["Flow Speed"], mode='lines', name='Velocidade do Fluxo', line=dict(color='blue')))
        if "Volume Flow" in merged_result:
            fig.add_trace(go.Scatter(x=merged_result["Hora"], y=merged_result["Volume Flow"], mode='lines', name='Fluxo de Volume', line=dict(color='green')))

        st.plotly_chart(fig)
        st.session_state["graph"] = fig

        st.subheader("Exportação de Dados")
        st.markdown("Escolha o que deseja exportar:")
        include_table = st.checkbox("Tabela de Resultados", value=True)
        include_graphs = st.checkbox("Gráficos", value=False)
        include_profile = st.checkbox("Perfil de Velocidade", value=False)

        if st.button("Exportar"):
            export_to_pdf(include_table, include_graphs, include_profile)

    if st.button("Coletar Dados do Perfil de Velocidade"):
        st.session_state["form_open"] = True

    if st.session_state.get("form_open"):
        coleta_form_layout()
