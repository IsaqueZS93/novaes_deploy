import pandas as pd

def process_macro_file(uploaded_file):
    # Carrega o arquivo enviado com o delimitador correto
    macro_data = pd.read_csv(uploaded_file, skiprows=10, delimiter=';')

    # Renomeia as colunas para facilitar o processamento e remove linhas de cabeçalho no meio dos dados
    macro_data.columns = macro_data.iloc[0]  # Define a primeira linha como cabeçalho
    macro_data = macro_data[1:].reset_index(drop=True)  # Remove a linha do cabeçalho extra e redefine os índices

    # Converte as colunas relevantes para valores numéricos, substituindo vírgulas por pontos
    macro_data['Flow Speed'] = pd.to_numeric(macro_data['Flow Speed'].str.replace(',', '.'), errors='coerce')
    macro_data['Volume Flow'] = pd.to_numeric(macro_data['Volume Flow'].str.replace(',', '.'), errors='coerce')

    # Combina os valores de Flow Speed e Volume Flow na mesma linha
    macro_data['Flow Speed'] = macro_data['Flow Speed'].fillna(method='ffill')  # Preenche valores ausentes de Flow Speed
    filtered_data = macro_data[~macro_data['Volume Flow'].isna()]  # Remove linhas onde Volume Flow é nulo

    # Calcula a média de Flow Speed e Volume Flow a cada 8 linhas
    grouped_data = (
        filtered_data[['Flow Speed', 'Volume Flow']]  # Seleciona apenas as colunas relevantes
        .reset_index(drop=True)  # Redefine os índices
        .groupby(filtered_data.index // 8)  # Agrupa a cada 8 linhas
        .mean()  # Calcula a média dos grupos
        .reset_index(drop=True)  # Redefine os índices novamente
    )

    # Renomeia as colunas para maior clareza
    grouped_data.columns = ['Avg Flow Speed', 'Avg Volume Flow']

    # Prepara os dados de saída para integração com o sistema de Pitometria
    result = {
        "all_values": filtered_data[['Flow Speed', 'Volume Flow']].to_dict(orient='records'),  # Todos os valores
        "averaged_values": grouped_data.to_dict(orient='records')  # Médias calculadas
    }

    return result

# Uso real do código
if __name__ == "__main__":
    import argparse

    # Configura o parser de argumentos para aceitar o caminho do arquivo de upload
    parser = argparse.ArgumentParser(description="Processa o arquivo Macro para integração com Pitometria.")
    parser.add_argument("uploaded_file", type=str, help="Caminho do arquivo enviado para processamento.")
    args = parser.parse_args()

    try:
        # Processa o arquivo
        result = process_macro_file(args.uploaded_file)

        # Salva os resultados em arquivos CSV para integração
        all_values_df = pd.DataFrame(result["all_values"])
        averaged_values_df = pd.DataFrame(result["averaged_values"])

        all_values_df.to_csv("All_Macro_Values.csv", index=False, sep=';')  # Salva todos os valores
        averaged_values_df.to_csv("Averaged_Macro_Values.csv", index=False, sep=';')  # Salva as médias

        print("Processamento concluído com sucesso. Arquivos gerados:")
        print("All_Macro_Values.csv e Averaged_Macro_Values.csv")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
