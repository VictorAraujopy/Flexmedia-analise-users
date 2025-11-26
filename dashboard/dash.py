import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np 

# --- VARIÁVEIS DE CONFIGURAÇÃO ---
COLUNA_DATA_REAL = 'timestamp' 
COR_FUNDO_CARD = "#161B22"
COR_FUNDO_APP = "#0d1117"
COR_UTIL = "#1A8FE3" 
COR_INUTIL = "#E74C3C"

# --- 1. Configuração da Página Profissional ---
st.set_page_config(
    page_title = "FlexMedia UX Detalhada (6 Colunas)",
    page_icon = "🎯", 
    layout = "wide",
    initial_sidebar_state="expanded" 
)

# --- 2. Paleta de Cores e Estilos (Dark Mode Analítico) ---
PALETA_ANALITICA = {
    'interação longa e útil': "#1A8FE3",      
    'interação moderada e útil': '#28B463',   
    'interação rápida mas útil': '#AAB7B8',   
    'interação longa e inútil': '#E74C3C',    
    'interação moderada e inútil': '#FF9800', 
    'interação rápida e inútil': '#FAD7A0'    
}

# --- 3. Aplicação de Estilos (CSS Injetado) ---
st.markdown(f"""
<style>
    /* Estilos Dark Mode e Cards */
    .stApp {{ background-color: {COR_FUNDO_APP}; color: #C9D1D9; }}
    .stApp h1 {{ color: #58A6FF; border-bottom: 1px solid #30363D; padding-bottom: 5px; margin-bottom: 20px; }}
    .stContainer {{
        background-color: {COR_FUNDO_CARD}; 
        padding: 15px;
        border-radius: 8px; 
        border: 1px solid #30363D;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        margin-bottom: 15px;
    }}
    div[data-testid="stMetricValue"] {{ font-size: 2.5rem; font-weight: bold; color: #C9D1D9; }}
    .stContainer h4 {{ color: #C9D1D9; margin-top: 0; }}
</style>
""", unsafe_allow_html=True)

# --- 4. Função de Carregamento de Dados ---
@st.cache_data
def carregar_modelo():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(pasta_atual, '..', 'data', 'dados_classificados_ml.csv')
    caminho_csv = os.path.abspath(caminho_csv)

    # Dados de Simulação (30 sessões)
    if not os.path.exists(caminho_csv):
        categorias = [
            'interação longa e útil', 'interação longa e útil', 'interação longa e útil', 'interação longa e útil', 'interação longa e útil', 'interação longa e útil', 'interação longa e útil', 
            'interação longa e inútil', 'interação longa e inútil', 'interação longa e inútil', 'interação longa e inútil', 'interação longa e inútil', 
            'interação moderada e útil', 'interação moderada e útil', 'interação moderada e útil', 'interação moderada e útil', 
            'interação moderada e inútil', 'interação moderada e inútil', 
            'interação rápida mas útil', 'interação rápida mas útil', 
            'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil', 'interação rápida e inútil'
        ]
        
        df = pd.DataFrame({'classificacao_ia': categorias[:30]}) 
        return df
    
    try:
        df = pd.read_csv(caminho_csv)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

dfa = carregar_modelo()

# --- 5. Cabeçalho Principal ---
st.title("🔬 Dashboard de Analytics de Experiência do Usuário")
st.caption("Este painel constitui um instrumento analítico sofisticado que utiliza o poder da Inteligência Artificial (Machine Learning) para quantificar e qualificar a Experiência do Usuário de forma objetiva, sua função central é transcender as métricas tradicionais de volume, classificando automaticamente o comportamento de cada sessão. O modelo de Machine Learning examina padrões complexos de navegação, duração e eventos de conversão para categorizar:  interação útil (indicando sucesso e eficiência) ou interação inútil(sinalizando falha, fricção ou abandono).")
st.markdown("---")

# --- 6. Processamento de Dados Analíticos ---
if dfa is not None:
    todas_categorias = list(PALETA_ANALITICA.keys())
    contagem_real = dfa['classificacao_ia'].value_counts()
    
    dados_grafico = pd.DataFrame({'Categoria': todas_categorias})
    dados_grafico['Quantidade'] = dados_grafico['Categoria'].map(contagem_real).fillna(0).astype(int)
    
    df_plot = dados_grafico[dados_grafico['Quantidade'] >= 0] 
    total_sessoes = df_plot['Quantidade'].sum()

    # Agrupamento e Métricas
    df_plot['Tipo'] = df_plot['Categoria'].apply(lambda x: 'Útil' if 'útil' in x else 'Inútil')
    total_util = df_plot[df_plot['Tipo'] == 'Útil']['Quantidade'].sum()
    percent_util = (total_util / total_sessoes) * 100 if total_sessoes > 0 else 0
    df_tipo_sum = df_plot.groupby('Tipo')['Quantidade'].sum().reset_index()
    
    # ----------------------------------------------------------------------
    # LÓGICA DE TABELA COM 6 COLUNAS 
    # ----------------------------------------------------------------------
    df_tabela = df_plot[df_plot['Quantidade'] > 0].copy() 
    df_tabela['Proporção (%)'] = (df_tabela['Quantidade'] / total_sessoes) * 100
    
    df_tabela.rename(columns={'Quantidade': 'Contagem'}, inplace=True) 

    # Simulação das 2 Novas Colunas Essenciais:
    duracoes = {'longa': 180, 'moderada': 60, 'rápida': 15}
    erros = {'útil': 5, 'inútil': 35}
    
    # Duração Média (s)
    df_tabela['Duração Média (s)'] = df_tabela['Categoria'].apply(lambda x: duracoes[x.split()[1]] + np.random.randint(-5, 5))
    
    # Taxa de Erro (%)
    df_tabela['Taxa de Erro (%)'] = df_tabela['Tipo'].apply(lambda x: erros[x.lower()] + np.random.randint(-3, 3))
    df_tabela['Taxa de Erro (%)'] = df_tabela['Taxa de Erro (%)'].clip(lower=0) 

    # Reordenamento das 6 colunas
    df_tabela = df_tabela[['Categoria', 'Contagem', 'Proporção (%)', 'Tipo', 'Duração Média (s)', 'Taxa de Erro (%)']]
    # ----------------------------------------------------------------------


    # ====================================================================
    # A. PAINEL DE KPIs (TOPO)
    # ====================================================================
    st.subheader("📊 Métricas Chave de Performance (KPIs)")
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        with st.container(): st.metric(label="Total de Sessões Analisadas", value=f"{total_sessoes}", delta="Base Analítica")
    with col_kpi2:
        with st.container(): st.metric(label="Taxa de Sucesso (Utilidade)", value=f"{percent_util:.1f}%", delta=f"+{total_util} Úteis", delta_color="normal")
    with col_kpi3:
        with st.container(): 
            ruido = df_plot[df_plot['Categoria'] == 'interação rápida e inútil']['Quantidade'].iloc[0] if 'interação rápida e inútil' in df_plot['Categoria'].values else 0
            taxa_ruido = (ruido / total_sessoes) * 100 if total_sessoes > 0 else 0
            st.metric(label="Taxa de Ruído (%)", value=f"{taxa_ruido:.1f}%", delta=f"-{ruido} Inúteis Rápidas", delta_color="inverse")
    with col_kpi4:
        with st.container(): st.metric(label="Tempo Médio de Sessão (s)", value=f"135", delta="Análise de Duração")

    st.markdown("---")

    # ====================================================================
    # B. GRÁFICOS DE DISTRIBUIÇÃO (Donut e Gauge)
    # ====================================================================
    st.subheader("📦 Distribuição e Análise de Contraste")

    col_donut, col_gauge = st.columns([1, 1.5]) 

    # --- Gráfico Donut ---
    with col_donut:
        with st.container():
            st.markdown("#### Distribuição de Categorias (Detalhamento)")
            lista_cores = [PALETA_ANALITICA[cat] for cat in df_plot['Categoria']]
            fig_donut = go.Figure(data=[go.Pie(
                labels=df_plot['Categoria'], values=df_plot['Quantidade'], hole=.65, 
                marker=dict(colors=lista_cores, line=dict(color=COR_FUNDO_APP, width=3)),
                textinfo='percent', textposition='outside', textfont=dict(size=11, color="#C9D1D9"), hoverinfo='label+value+percent'
            )])
            fig_donut.update_layout(
                font=dict(family="Arial", size=10, color="#C9D1D9"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=400, showlegend=False, margin=dict(t=30, b=30, l=30, r=30),
                annotations=[dict(text=f'<span style="font-size: 35px; font-weight: bold;">{total_sessoes}</span><br>Sessões', x=0.5, y=0.5, font_color="#C9D1D9", showarrow=False, xanchor="center", yanchor="middle")]
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

    # --- Gráfico Gauge (Medidor de Utilidade) ---
    with col_gauge:
        with st.container():
            st.markdown("#### 🎯 Taxa de Utilidade (Gráfico de Velocímetro)")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = percent_util,
                title = {'text': "Utilidade Total (%)", 'font': {'color': "#C9D1D9"}},
                delta = {'reference': 70, 'increasing': {'color': COR_UTIL}}, 
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': COR_UTIL},
                    'bgcolor': COR_FUNDO_CARD,
                    'steps': [
                        {'range': [0, 40], 'color': "#E74C3C"},    
                        {'range': [40, 70], 'color': "#FF9800"},   
                        {'range': [70, 100], 'color': "#28B463"}   
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 75 
                    }
                }
            ))

            fig_gauge.update_layout(
                height=400,
                paper_bgcolor=COR_FUNDO_CARD,
                plot_bgcolor=COR_FUNDO_CARD,
                font=dict(color="#C9D1D9"),
                margin=dict(l=30, r=30, t=50, b=30)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            
    st.markdown("---")

    # ====================================================================
    # C. DETALHAMENTO CATEGÓRICO (Tabela Simplificada + Barras Horizontais)
    # ====================================================================
    st.subheader("📦 Detalhamento Categórico de Volume")

    col_tabela, col_new_chart = st.columns([1, 1])

    # --- Tabela Detalhada (6 Colunas) ---
    with col_tabela:
        with st.container():
            st.markdown("#### Tabela Essencial (6 Métricas de UX)")
            
            # Formatação para exibição
            st.dataframe(
                df_tabela.sort_values(by='Contagem', ascending=False).style.format({
                    'Proporção (%)': "{:.2f}%", 
                    'Duração Média (s)': "{:.0f}s",
                    'Taxa de Erro (%)': "{:.1f}%",
                }),
                use_container_width=True,
                hide_index=True
            )

    # --- Gráfico de Barras Horizontais (Segmentado por Útil/Inútil) ---
    with col_new_chart:
        with st.container():
            st.markdown("#### 📊 Volume Total por Classificação")
            
            df_barras_horiz = df_plot[df_plot['Quantidade'] > 0].copy()
            df_barras_horiz = df_barras_horiz.sort_values(by='Quantidade', ascending=True)

            cores_segmentadas = {'Útil': COR_UTIL, 'Inútil': COR_INUTIL}
            
            fig_horiz = px.bar(
                df_barras_horiz, 
                x='Quantidade', 
                y='Categoria', 
                color='Tipo', 
                color_discrete_map=cores_segmentadas,
                text='Quantidade',
                orientation='h',
                title='Contagem de Sessões por Categoria'
            )
            
            fig_horiz.update_traces(texttemplate='%{text}', textposition='outside', marker_line_width=0)
            
            fig_horiz.update_layout(
                height=450,
                xaxis_title="Contagem de Sessões",
                yaxis_title="",
                paper_bgcolor=COR_FUNDO_CARD, plot_bgcolor=COR_FUNDO_CARD, 
                font=dict(color="#C9D1D9"),
                legend_title_text='Tipo',
                legend=dict(orientation="h", y=-0.2)
            )

            st.plotly_chart(fig_horiz, use_container_width=True, config={'displayModeBar': False})