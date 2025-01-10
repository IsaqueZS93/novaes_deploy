import streamlit as st
import plotly.graph_objs as go

def layout(merged_result):
    """
    Layout para geração de gráficos interativos com base na tabela de resultados.

    :param merged_result: DataFrame contendo os resultados processados.
    """
    st.title("Gráfico Interativo de Vazões e Velocidades")

    if merged_result is not None:
        st.subheader("Gráfico de Vazões e Velocidades")
        
        # Criando a figura
        fig = go.Figure()

        # Adicionando as séries de dados ao gráfico
        if "Vazão(Q m³/h)" in merged_result:
            fig.add_trace(go.Scatter(
                x=merged_result["Hora"],
                y=merged_result["Vazão(Q m³/h)"],
                mode='lines',
                name='Vazão (Q m³/h)',
                line=dict(color='black')
            ))

        if "Veloc.(m/s)" in merged_result:
            fig.add_trace(go.Scatter(
                x=merged_result["Hora"],
                y=merged_result["Veloc.(m/s)"],
                mode='lines',
                name='Velocidade (m/s)',
                line=dict(color='red')
            ))

        if "Flow Speed" in merged_result:
            fig.add_trace(go.Scatter(
                x=merged_result["Hora"],
                y=merged_result["Flow Speed"],
                mode='lines',
                name='Velocidade do Fluxo',
                line=dict(color='blue')
            ))

        if "Volume Flow" in merged_result:
            fig.add_trace(go.Scatter(
                x=merged_result["Hora"],
                y=merged_result["Volume Flow"],
                mode='lines',
                name='Fluxo de Volume',
                line=dict(color='green')
            ))

        # Configurações do layout do gráfico
        fig.update_layout(
            title="Gráfico Interativo de Vazões e Velocidades",
            xaxis_title="Hora",
            yaxis_title="Valores",
            legend_title="Legenda",
            hovermode="x unified"
        )

        # Exibindo o gráfico
        st.plotly_chart(fig)

        # Salvando o gráfico no session_state para exportação
        st.session_state["graph"] = fig

    else:
        st.warning("A tabela de resultados precisa ser processada antes de gerar o gráfico.")
