import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from db_config import get_dados_sensor
from DataClass import run_pipeline

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
