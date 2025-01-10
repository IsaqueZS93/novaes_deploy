import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import streamlit_folium as st_folium
from folium import Map, Marker

# Funções auxiliares
def criar_dataframe(pontos, velocidades):
    """
    Cria um DataFrame com os dados de Pontos, Velocidades e Distâncias.

    Args:
        pontos (list): Lista com as distâncias dos pontos.
        velocidades (list): Lista com as velocidades.

    Returns:
        pd.DataFrame: DataFrame estruturado.
    """
    return pd.DataFrame({
        "Ponto": range(1, len(pontos) + 1),
        "Velocidade (m/s)": velocidades,
        "Distância (mm)": pontos,
    })

def criar_grafico(df):
    """
    Cria um gráfico usando os dados do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados.

    Returns:
        plotly.graph_objs.Figure: Objeto de gráfico.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Velocidade (m/s)"],
        y=df["Distância (mm)"],
        mode="lines+markers+text",
        name="Velocidade x Distância",
        line=dict(color='blue', width=2),
        marker=dict(size=6),
        text=df["Velocidade (m/s)"],
        textposition="top center"
    ))
    fig.update_layout(
        title={"text": "Perfil de Velocidade do Fluxo", "font": {"size": 18}, "x": 0.5, "xanchor": "center"},
        xaxis_title="Velocidade (m/s)",
        yaxis_title="Distância (mm)",
        template="plotly_white",
        width=600,
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    return fig

# Layout principal do formulário
def layout():
    # Título e introdução
    st.title("Perfil de Velocidade do Fluxo da Tubulação")
    st.markdown("### Preencha as informações abaixo para gerar o perfil de velocidade do fluxo.")

    # Seção de informações básicas
    st.subheader("Informações Básicas")
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data", key="data_coleta_form")
        horario_inicial = st.time_input("Horário Inicial", key="horario_inicial")
    with col2:
        horario_final = st.time_input("Horário Final", key="horario_final")
        equipe = st.text_input("Equipe", placeholder="Nome da equipe", key="equip_form")

    col3, col4 = st.columns(2)
    with col3:
        diametro_tubo = st.number_input("Diâmetro do Tubo (mm)", step=1.0, format="%.2f", min_value=0.0, key="diametro_tubo")
    with col4:
        diametro_medido = st.number_input("Diâmetro Medido (mm)", step=1.0, format="%.2f", min_value=0.0, key="diametro_medido")

    # Captura de coordenadas
    st.subheader("Localização da Coleta")
    coordenadas = st.text_input("Coordenadas do Local (latitude, longitude)", placeholder="Exemplo: -10.4025, -36.4501", key="coordenadas")

    if coordenadas:
        try:
            lat, lon = map(float, coordenadas.split(","))
            mapa = Map(location=[lat, lon], zoom_start=15)
            marker = Marker(location=[lat, lon], draggable=False)
            mapa.add_child(marker)
            st_folium.folium_static(mapa, width=700, height=500)
        except ValueError:
            st.warning("Formato de coordenadas inválido. Use o formato: latitude, longitude")

    # Validação inicial
    if not equipe or diametro_tubo <= 0 or diametro_medido <= 0 or not coordenadas:
        st.warning("Preencha todas as informações corretamente antes de prosseguir.")
        return

    # Seção de coleta de pontos e velocidades
    st.subheader("Pontos e Velocidades")
    pontos = []
    velocidades = []
    for i in range(1, 12):
        col_ponto, col_velocidade = st.columns(2)
        with col_ponto:
            ponto = st.number_input(f"Ponto {i} (mm)", step=1.0, key=f"ponto-{i}", min_value=0.0)
        with col_velocidade:
            velocidade = st.number_input(f"Velocidade {i} (m/s)", step=0.01, format="%.2f", key=f"velocidade-{i}", min_value=0.0)
        pontos.append(ponto)
        velocidades.append(velocidade)

    # Botão para processar os dados
    if st.button("Concluir", key="concluir_coleta"):
        # Validação final
        if any(p <= 0 for p in pontos) or any(v <= 0 for v in velocidades):
            st.error("Todos os valores de Pontos e Velocidades devem ser preenchidos corretamente.")
            return

        # Criar DataFrame
        df = criar_dataframe(pontos, velocidades)

        # Exibir resultados
        st.subheader("Resultados da Coleta")
        col_result_tabela, col_result_grafico = st.columns([1, 1])
        with col_result_tabela:
            st.dataframe(df)
        with col_result_grafico:
            st.plotly_chart(criar_grafico(df))
        st.success("Dados processados com sucesso!")

        # Salvando dados no session_state para exportação
        st.session_state["coleta_dados"] = {
            "data": str(data),
            "horario_inicial": str(horario_inicial),
            "horario_final": str(horario_final),
            "equipe": equipe,
            "diametro_tubo": diametro_tubo,
            "diametro_medido": diametro_medido,
            "coordenadas": coordenadas,
            "pontos_velocidades": df
        }
