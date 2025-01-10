import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(r"C:\Users\Novaes Engenharia\WebAppStreamlit")
import imports

from P_Macro import process_macro_file
from P_Pitot import process_pitometria_file
from P_MP import merge_macro_pitometria
from DA_manipulation_graphics import layout as graphics_layout

def layout():
    st.title("Upload de Arquivos e Informações")

    # Upload dos arquivos
    macro_file = st.file_uploader("Arquivo do Macromedidor", type=["csv", "xlsx"], key="macro_file")
    pitometria_file = st.file_uploader("Arquivo de Pitometria", type=["csv", "xlsx"], key="pitometria_file")

    # Informações adicionais
    unidade = st.text_input("Unidade", placeholder="Digite a unidade", key="unidade")
    empresa = st.text_input("Empresa Responsável", placeholder="Digite a empresa responsável", key="empresa")
    data = st.date_input("Data da Coleta", key="data_coleta")
    equipe = st.text_input("Equipe Responsável", placeholder="Digite o nome da equipe", key="equipe")

    if st.button("Processar Dados", key="processar_dados"):
        if macro_file and pitometria_file:
            try:
                # Salvando arquivos temporariamente
                macro_temp_path = "temp_macro.csv"
                pitometria_temp_path = "temp_pitometria.csv"
                
                with open(macro_temp_path, "wb") as macro_temp:
                    macro_temp.write(macro_file.getbuffer())
                with open(pitometria_temp_path, "wb") as pitometria_temp:
                    pitometria_temp.write(pitometria_file.getbuffer())

                # Processando os arquivos
                macro_result = process_macro_file(macro_temp_path)
                fv, kc, pitometria_data = process_pitometria_file(pitometria_temp_path)
                pitometria_result = {"fv": fv, "kc": kc, "data": pitometria_data.to_dict("records")}

                # Unindo os resultados
                merged_result = merge_macro_pitometria(macro_result, pitometria_result)
                merged_result = merged_result.drop_duplicates(subset=["Hora"])

                # Calculando desvio relativo
                desvio_relativo = "N/A"
                if "Flow Speed" in merged_result.columns and "Veloc.(m/s)" in merged_result.columns:
                    desvio_relativo = (abs(merged_result["Flow Speed"] - merged_result["Veloc.(m/s)"]) / merged_result["Flow Speed"]).mean() * 100
                    desvio_relativo = f"{desvio_relativo:.2f}%"

                # Salvando informações no session_state
                st.session_state["processed_data"] = {
                    "unidade": unidade,
                    "empresa": empresa,
                    "data": str(data),
                    "equipe": equipe,
                    "metrics": {"FV": fv, "KC": kc, "Desvio Relativo": desvio_relativo},
                    "table": merged_result
                }

                # Exibindo resultados
                st.success("Dados processados com sucesso!")
                col1, col2, col3 = st.columns(3)
                col1.metric("FV", fv)
                col2.metric("KC", kc)
                col3.metric("Desvio Relativo (%)", desvio_relativo)

                # Exibindo tabela de resultados
                st.subheader("Tabela de Resultados")
                st.dataframe(merged_result, height=400)

                # Chamando o layout de gráficos
                st.subheader("Gráficos Interativos")
                graphics_layout(merged_result)

            except Exception as e:
                st.error(f"Erro ao processar os dados: {e}")
        else:
            st.warning("Ambos os arquivos devem ser enviados para processamento.")
