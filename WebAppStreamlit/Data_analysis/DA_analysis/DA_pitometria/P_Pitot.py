import pandas as pd

def process_pitometria_file(uploaded_file):
    # Abrir o arquivo enviado e capturar as linhas relevantes para FV e KC
    with open(uploaded_file, 'r', encoding='latin1') as file:
        lines = file.readlines()
        fv_line = lines[7]  # Linha 8 (índice 7)
        kc_line = lines[12]  # Linha 13 (índice 12)

    # Processar os valores de FV e KC
    fv_value = float(fv_line.split(':')[-1].split(';')[0].strip().replace(',', '.'))  # Extrair e converter FV
    kc_value = float(kc_line.split(':')[-1].split(';')[0].strip().replace(',', '.'))  # Extrair e converter KC

    # Carregar os dados da tabela começando da linha correta
    pitometria_data = pd.read_csv(uploaded_file, skiprows=13, delimiter=';', encoding='latin1')

    # Selecionar apenas as colunas necessárias
    selected_columns = pitometria_data[['Ponto', 'Data', 'Hora', 'Veloc.(m/s)', 'Vazão(Q m³/h)']].copy()

    # Converter os valores numéricos para o formato correto
    selected_columns['Veloc.(m/s)'] = selected_columns['Veloc.(m/s)'].str.replace(',', '.').astype(float)  # Velocidade
    selected_columns['Vazão(Q m³/h)'] = selected_columns['Vazão(Q m³/h)'].str.replace(',', '.').astype(float)  # Vazão

    return fv_value, kc_value, selected_columns

# Teste do código
if __name__ == "__main__":
    # Caminho do arquivo para o teste
    file_path = r"C:\Users\Novaes Engenharia\DAsh\Pitometria.csv"

    try:
        # Processar o arquivo
        fv, kc, processed_data = process_pitometria_file(file_path)

        # Exibir os resultados no console
        print(f"FV: {fv}")
        print(f"KC: {kc}")
        print("\nTabela Processada:")
        print(processed_data)

        # Opcional: Salvar a tabela processada em um arquivo CSV
        processed_data.to_csv("Processed_Pitometria_Data.csv", index=False, sep=';')
        print("\nTabela processada salva como 'Processed_Pitometria_Data.csv'.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
