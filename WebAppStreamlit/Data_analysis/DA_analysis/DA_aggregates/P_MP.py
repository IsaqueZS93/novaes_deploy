import pandas as pd

def merge_macro_pitometria(macro_result, pitometria_result):
    """
    Função para unir os resultados dos códigos Macro e Pitometria.

    Parameters:
        macro_result (dict): Contém os resultados do processamento do Macro.
            - "all_values": lista de dicionários com os valores completos de Flow Speed e Volume Flow.
            - "averaged_values": lista de dicionários com as médias calculadas de Flow Speed e Volume Flow.
        pitometria_result (dict): Contém os resultados do processamento do Pitometria.
            - "fv": Valor de FV extraído.
            - "kc": Valor de KC extraído.
            - "data": lista de dicionários com os dados processados da tabela Pitometria.

    Returns:
        pd.DataFrame: Tabela consolidada com os dados do Macro e Pitometria.
    """
    # Extraindo informações de Macro
    all_values_macro = pd.DataFrame(macro_result['all_values'])
    averaged_values_macro = pd.DataFrame(macro_result['averaged_values'])

    # Extraindo informações de Pitometria
    pitometria_data = pd.DataFrame(pitometria_result['data'])

    # Padronizar o número de linhas entre Macro e Pitometria
    max_rows = max(len(all_values_macro), len(pitometria_data))

    # Repetir ou truncar dados do Macro para ajustar o número de linhas
    all_values_macro = pd.concat([all_values_macro] * (max_rows // len(all_values_macro) + 1), ignore_index=True).iloc[:max_rows]

    # Repetir ou truncar dados do Pitometria para ajustar o número de linhas
    pitometria_data = pd.concat([pitometria_data] * (max_rows // len(pitometria_data) + 1), ignore_index=True).iloc[:max_rows]

    # Concatenar os dados do Macro e Pitometria lado a lado
    merged_data = pd.concat([all_values_macro.reset_index(drop=True), pitometria_data.reset_index(drop=True)], axis=1)

    return merged_data

# O código não realiza teste diretamente. Deve ser chamado com os resultados de Macro e Pitometria
# Exemplo de como integrar isso no dashboard ou em um sistema externo:
# merged_data = merge_macro_pitometria(macro_result, pitometria_result)
