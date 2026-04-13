import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:5000")

def enviar_mensagem(texto: str, tipo: str = "texto"):
    try:
        response = requests.post(
            f"{API_URL}/api/interacao",
            json={"texto": texto, "tipo": tipo},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("resposta", "Sem resposta.")
        return "Erro ao processar sua mensagem."
    except requests.exceptions.RequestException:
        return "API indisponível no momento."

st.set_page_config(page_title="Smart-Guide", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 200px);
    overflow-y: auto;
}
section[data-testid="stSidebar"] {
    background-color: transparent;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🤖 Smart-Guide")
    st.caption("Totem Inteligente")
    st.divider()
    st.markdown("#### Perguntas rápidas")

    opcoes = {
        "🚻 Banheiro": "onde fica o banheiro",
        "📶 Wi-Fi": "qual a senha do wifi",
        "🚪 Saída": "onde fica a saída",
        "🕐 Horário": "qual o horário de funcionamento",
        "🅿️ Estacionamento": "onde fica o estacionamento",
    }

    for label, texto in opcoes.items():
        if st.button(label, use_container_width=True):
            resposta = enviar_mensagem(texto, tipo="botao")
            st.session_state.historico.append({"autor": "Visitante", "texto": texto})
            st.session_state.historico.append({"autor": "Smart-Guide", "texto": resposta})
            st.rerun()

if "historico" not in st.session_state:
    st.session_state.historico = []

st.markdown("### Histórico de conversa")

for mensagem in st.session_state.historico:
    if mensagem["autor"] == "Visitante":
        with st.chat_message("user"):
            st.write(mensagem["texto"])
    else:
        with st.chat_message("assistant"):
            st.write(mensagem["texto"])

entrada = st.chat_input("Digite sua dúvida...")

if entrada and entrada.strip():
    resposta = enviar_mensagem(entrada.strip(), tipo="texto")
    st.session_state.historico.append({"autor": "Visitante", "texto": entrada.strip()})
    st.session_state.historico.append({"autor": "Smart-Guide", "texto": resposta})
    st.rerun()