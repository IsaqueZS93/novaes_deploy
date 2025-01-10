import openai

# Configurar a chave da API da OpenAI
openai.api_key = "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"

def generate_report(image_analysis):
    """
    Gera um relatório detalhado usando a OpenAI com base na análise fornecida.

    Parâmetros:
        image_analysis (str): Uma descrição da análise da imagem.

    Retorna:
        str: Um texto detalhado gerado pela IA com base na análise.
    """
    try:
        # Utilizar o modelo GPT-3.5-turbo com a API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que gera relatórios detalhados com base em análises de imagens."},
                {"role": "user", "content": f"Detalhe os resultados da análise da imagem com base na descrição a seguir:\n\n{image_analysis}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        # Extração do conteúdo do relatório gerado
        report = response["choices"][0]["message"]["content"].strip()
        return report
    except openai.error.OpenAIError as e:
        return f"Erro na API OpenAI: {e}"
    except Exception as e:
        return f"Erro inesperado ao gerar o relatório: {e}"

# Exemplo de uso real
if __name__ == "__main__":
    # Simulação de uma análise de imagem gerada anteriormente
    image_analysis = "A imagem apresenta um lacre azul intacto e sem danos visíveis, com o hidrômetro em bom estado."
    report = generate_report(image_analysis)
    print("Relatório Gerado pela IA:")
    print(report)
