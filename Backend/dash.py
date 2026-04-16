import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from db_config import init_db_pool
from db_config import get_dados_sensor
from DataClass import run_pipeline

init_db_pool()
banco_log = get_dados_sensor()
dado_classificado = run_pipeline(banco_log)

# --- VARIÁVEIS DE CONFIGURAÇÃO ---
COR_FUNDO_CARD = "#161B22"
COR_FUNDO_APP  = "#0d1117"
COR_UTIL       = "#1A8FE3"
COR_INUTIL     = "#E74C3C"

PALETA = {
    'Satisfeito':   COR_UTIL,
    'Insatisfeito': COR_INUTIL
}

# --- Configuração da Página ---
st.set_page_config(
    page_title="FlexMedia - Análise de Satisfação",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos Dark Mode ---
st.markdown(f"""
<style>
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
    .insight-box {{
        background-color: {COR_FUNDO_CARD};
        border-left: 4px solid {COR_UTIL};
        padding: 20px 25px;
        border-radius: 8px;
        margin-bottom: 10px;
    }}
    .insight-box h2 {{ color: #58A6FF; margin: 0 0 8px 0; }}
    .insight-box p  {{ color: #C9D1D9; margin: 0; font-size: 1rem; }}
</style>
""", unsafe_allow_html=True)

# --- Cabeçalho ---
st.title("🔬 Dashboard de Análise de Satisfação do Usuário")
st.caption("O modelo analisa o tempo de duração das sessões e prevê se o usuário ficou satisfeito.")
st.markdown("---")

# --- Processamento ---
df = dado_classificado.copy()
df["Satisfação Real"]     = df["satisfacao"].map({1: "Satisfeito", 0: "Insatisfeito"})
df["Satisfação Prevista"] = df["satisfacao_prevista"].map({1: "Satisfeito", 0: "Insatisfeito"})

total_sessoes    = len(df)
total_satisf     = int(df["satisfacao"].sum())
percent_satisf   = (total_satisf / total_sessoes) * 100 if total_sessoes > 0 else 0
total_previsto   = int(df["satisfacao_prevista"].sum())
percent_previsto = (total_previsto / total_sessoes) * 100 if total_sessoes > 0 else 0
tempo_medio      = df["tempo_duracao"].mean()

# Threshold: tempo médio por grupo de satisfação real
tempo_satisfeito   = df[df["satisfacao"] == 1]["tempo_duracao"].mean()
tempo_insatisfeito = df[df["satisfacao"] == 0]["tempo_duracao"].mean()

# ====================================================================
# A. KPIs
# ====================================================================
st.subheader("📊 Métricas Chave")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Sessões", total_sessoes)
with col2:
    st.metric("Satisfação Real", f"{percent_satisf:.1f}%", delta=f"{total_satisf} satisfeitos")
with col3:
    diff = percent_previsto - percent_satisf
    st.metric("Satisfação Prevista (ML)", f"{percent_previsto:.1f}%", delta=f"{diff:+.1f}% vs real")
with col4:
    st.metric("Tempo Médio de Sessão", f"{tempo_medio:.0f}s")

st.markdown("---")

# ====================================================================
# B. Insight principal do modelo em linguagem clara
# ====================================================================
st.subheader("🧠 O que o modelo descobriu")

col_ins1, col_ins2 = st.columns(2)

with col_ins1:
    st.markdown(f"""
    <div class="insight-box">
        <h2>✅ Usuários Satisfeitos</h2>
        <p>Ficam em média <strong>{tempo_satisfeito:.0f} segundos</strong> na sessão.</p>
        <p>Sessões acima de <strong>{tempo_satisfeito:.0f}s</strong> tendem a indicar satisfação.</p>
    </div>
    """, unsafe_allow_html=True)

with col_ins2:
    st.markdown(f"""
    <div class="insight-box" style="border-left-color: {COR_INUTIL};">
        <h2>❌ Usuários Insatisfeitos</h2>
        <p>Ficam em média <strong>{tempo_insatisfeito:.0f} segundos</strong> na sessão.</p>
        <p>Sessões abaixo de <strong>{tempo_insatisfeito:.0f}s</strong> tendem a indicar insatisfação.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ====================================================================
# D. Real vs Previsto
# ====================================================================
st.subheader("📊 Satisfação Real vs Prevista pelo Modelo")

df_comparativo = pd.DataFrame({
    "Tipo":     ["Satisfeito", "Insatisfeito"],
    "Real":     [int(df["satisfacao"].sum()),          int((df["satisfacao"] == 0).sum())],
    "Previsto": [int(df["satisfacao_prevista"].sum()), int((df["satisfacao_prevista"] == 0).sum())]
})

fig_barras = go.Figure()
fig_barras.add_trace(go.Bar(name="Real",     x=df_comparativo["Tipo"], y=df_comparativo["Real"],     marker_color=COR_UTIL,  text=df_comparativo["Real"],     textposition="outside"))
fig_barras.add_trace(go.Bar(name="Previsto", x=df_comparativo["Tipo"], y=df_comparativo["Previsto"], marker_color="#28B463", text=df_comparativo["Previsto"], textposition="outside"))

fig_barras.update_layout(
    barmode="group",
    height=350,
    paper_bgcolor=COR_FUNDO_CARD,
    plot_bgcolor=COR_FUNDO_CARD,
    font=dict(color="#C9D1D9"),
    xaxis_title="",
    yaxis_title="Contagem de Sessões",
    legend=dict(orientation="h", y=-0.2)
)
st.plotly_chart(fig_barras, use_container_width=True, config={'displayModeBar': False})

st.markdown("---")

# ====================================================================
# E. Gráficos temporais
# ====================================================================
st.subheader("📈 Análise Temporal")

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hora"] = df["timestamp"].dt.hour
    df["dia_semana"] = df["timestamp"].dt.dayofweek

    st.markdown("#### 🕐 Sessões por Hora do Dia")
    df_por_hora = df.groupby("hora").size().reset_index(name="sessoes")
    fig_linha = px.line(df_por_hora, x="hora", y="sessoes", markers=True,
                        labels={"hora": "Hora do Dia", "sessoes": "Número de Sessões"})
    fig_linha.update_traces(line_color=COR_UTIL, marker=dict(color=COR_UTIL, size=8))
    fig_linha.update_layout(height=350, paper_bgcolor=COR_FUNDO_CARD,
                             plot_bgcolor=COR_FUNDO_CARD, font=dict(color="#C9D1D9"),
                             xaxis=dict(dtick=1, gridcolor="#30363D"),
                             yaxis=dict(gridcolor="#30363D"))
    st.plotly_chart(fig_linha, use_container_width=True, config={'displayModeBar': False})

    st.markdown("#### 🔥 Horários de Pico (Heatmap)")
    dias_nomes = {0:"Seg",1:"Ter",2:"Qua",3:"Qui",4:"Sex",5:"Sáb",6:"Dom"}
    df["dia_nome"] = df["dia_semana"].map(dias_nomes)
    df_heatmap = df.groupby(["dia_nome","hora"]).size().reset_index(name="total")
    fig_heat = px.density_heatmap(df_heatmap, x="hora", y="dia_nome", z="total",
                                   color_continuous_scale="Blues",
                                   labels={"hora":"Hora","dia_nome":"Dia","total":"Sessões"})
    fig_heat.update_layout(height=350, paper_bgcolor=COR_FUNDO_CARD,
                            plot_bgcolor=COR_FUNDO_CARD, font=dict(color="#C9D1D9"))
    st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})

    st.markdown("#### 😊 Evolução da Satisfação ao Longo do Tempo")
    df["data"] = df["timestamp"].dt.date
    df_satisf_tempo = df.groupby("data")["satisfacao"].mean().reset_index()
    df_satisf_tempo["satisfacao_pct"] = df_satisf_tempo["satisfacao"] * 100
    fig_satisf = px.line(df_satisf_tempo, x="data", y="satisfacao_pct", markers=True,
                          labels={"data":"Data","satisfacao_pct":"% Satisfeitos"})
    fig_satisf.update_traces(line_color="#28B463", marker=dict(color="#28B463", size=8))
    fig_satisf.update_layout(height=350, paper_bgcolor=COR_FUNDO_CARD,
                              plot_bgcolor=COR_FUNDO_CARD, font=dict(color="#C9D1D9"),
                              xaxis=dict(gridcolor="#30363D"),
                              yaxis=dict(gridcolor="#30363D", range=[0,100]))
    st.plotly_chart(fig_satisf, use_container_width=True, config={'displayModeBar': False})

else:
    st.warning("⚠️ Coluna 'timestamp' não encontrada. Aguardando a Pessoa 1.")

st.markdown("---")

# ====================================================================
# F. Métricas de engajamento
# ====================================================================
st.subheader("🎯 Métricas de Engajamento")

try:
    from db_config import get_connection
    conn = get_connection()
    df_interacoes = pd.read_sql(
        "SELECT tipo_interacao, conteudo, resposta_sistema, timestamp FROM logs_interacoes", conn)
    conn.close()

    if df_interacoes.empty:
        st.info("ℹ️ Tabela logs_interacoes ainda sem dados. Aguardando a Pessoa 2.")
    else:
        col_eng1, col_eng2 = st.columns(2)

        with col_eng1:
            st.markdown("#### 💬 Tipo de Interação")
            df_tipos = df_interacoes["tipo_interacao"].value_counts().reset_index()
            df_tipos.columns = ["tipo", "total"]
            fig_pizza = px.pie(df_tipos, names="tipo", values="total",
                               color_discrete_sequence=[COR_UTIL, "#28B463", COR_INUTIL])
            fig_pizza.update_layout(height=350, paper_bgcolor=COR_FUNDO_CARD,
                                     font=dict(color="#C9D1D9"))
            st.plotly_chart(fig_pizza, use_container_width=True, config={'displayModeBar': False})

        with col_eng2:
            st.markdown("#### ⏱️ Quantidade por Tipo de Interação")
            df_tempo_tipo = df_interacoes.groupby("tipo_interacao").size().reset_index(name="quantidade")
            fig_tempo = px.bar(df_tempo_tipo, x="tipo_interacao", y="quantidade",
                               color="tipo_interacao",
                               color_discrete_sequence=[COR_UTIL, "#28B463", COR_INUTIL],
                               labels={"tipo_interacao":"Tipo","quantidade":"Quantidade"})
            fig_tempo.update_layout(height=350, paper_bgcolor=COR_FUNDO_CARD,
                                     plot_bgcolor=COR_FUNDO_CARD, font=dict(color="#C9D1D9"),
                                     showlegend=False)
            st.plotly_chart(fig_tempo, use_container_width=True, config={'displayModeBar': False})

        st.markdown("#### 🏆 Top 10 Perguntas Mais Frequentes")
        df_perguntas = df_interacoes["conteudo"].value_counts().head(10).reset_index()
        df_perguntas.columns = ["Pergunta", "Frequência"]
        st.dataframe(df_perguntas, use_container_width=True, hide_index=True)

except Exception as e:
    st.warning(f"⚠️ Seção de engajamento indisponível: aguardando tabela logs_interacoes (Pessoa 2). Detalhe: {e}")