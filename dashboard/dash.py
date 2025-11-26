import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(
    page_title = "FlexMedia Dashboard",
    page_icon = "📊",
    layout = "wide"
)


st.title("📊 FlexMedia Dashboard de Classificação de Experiência do Usuário")


def carregar_modelo():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(pasta_atual, '..', 'data', 'dados_classificados_ml.csv')
    caminho_csv = os.path.abspath(caminho_csv)

    try:
        df = pd.read_csv(caminho_csv)
        return df
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_csv}")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

dfa = carregar_modelo()




dfa = carregar_modelo()

if dfa is not None:
    # 1. Preparar Dados (Garantindo que todas as categorias existam para a legenda ficar bonita)
    todas_categorias = [
        'interação longa e útil', 'interação moderada e útil', 'interação rápida mas útil',
        'interação longa e inútil', 'interação moderada e inútil', 'interação rápida e inútil'
    ]
    
    # Conta o que tem de verdade
    contagem_real = dfa['classificacao_ia'].value_counts()
    
    # Cria uma tabela final forçando todas as categorias (preenchendo com 0 as que faltam)
    dados_grafico = pd.DataFrame({'Categoria': todas_categorias})
    dados_grafico['Quantidade'] = dados_grafico['Categoria'].map(contagem_real).fillna(0)
    
    # Filtramos apenas o que tem valor > 0 para o gráfico não ficar com fatias invisíveis bugadas
    # Mas mantemos a ordem das cores
    df_plot = dados_grafico[dados_grafico['Quantidade'] > 0]

    # 2. Paleta de Cores "Cyberpunk"
    cores_map = {
        'interação longa e útil': "#00ff62",      # Verde Neon
        'interação moderada e útil': '#00d4ff',   # Azul Neon
        'interação rápida mas útil': '#bc13fe',   # Roxo Neon
        'interação longa e inútil': '#ff005c',    # Vermelho Neon
        'interação moderada e inútil': '#ff8700', # Laranja Neon
        'interação rápida e inútil': '#ffd300'    # Amarelo Neon
    }
    
    lista_cores = [cores_map[cat] for cat in df_plot['Categoria']] # Mantém a ordem correta

    # 3. Construção do Gráfico PRO (Graph Objects)
    col1, col2, col3 = st.columns([1, 2, 1]) # Centralizando
    
 

    with col2:
        # Criando o gráfico
        fig = go.Figure(data=[go.Pie(
            labels=df_plot['Categoria'],
            values=df_plot['Quantidade'],
            hole=.7,
            marker=dict(colors=lista_cores, line=dict(color='#000000', width=2)),# Bordas pretas para destacar
            textinfo='percent',
            textfont=dict(size=14, color="white", family="Arial Black"),
            hoverinfo='label+value+percent'
        )])

        total_usuarios = int(df_plot['Quantidade'].sum())

        fig.update_layout(
            
            # 1. Ajuste Fino de Layout
            font=dict(family="Verdana", size=12, color="white"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            
            # 2. Legenda e Margens
            showlegend=True,
            legend=dict(orientation="h", y=-0.1), # Legenda embaixo
            margin=dict(t=20, b=20, l=20, r=20),  # Margens zeradas/pequenas para centralizar
            
            

            annotations=[
                dict(
                    text=str(total_usuarios), 
                    x=0.5, y=0.5, # Centro absoluto
                    font_size=40, font_color="white", 
                    showarrow=False, xanchor="center", yanchor="middle"
                ),
                dict(
                    text="Sessões", 
                    x=0.5, y=0.4, # Um pouco abaixo do número
                    font_size=12, font_color="gray", 
                    showarrow=False, xanchor="center", yanchor="middle"
                )
            ]
        )

        st.plotly_chart(fig, use_container_width=True)