import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:5000")

INTENCOES = {
    "banheiro": {
        "palavras": ["banheiro", "wc", "sanitário", "toalete"],
        "resposta": "O banheiro fica no corredor B, ao lado da loja 12. 🚻",
        "categoria": "localizacao"
    },
    "saida": {
        "palavras": ["saída", "sair", "porta", "saida"],
        "resposta": "A saída principal é pela porta norte. A saída de emergência fica no corredor C.",
        "categoria": "localizacao"
    },
    "wifi": {
        "palavras": ["wifi", "wi-fi", "internet", "rede", "senha"],
        "resposta": "A rede Wi-Fi gratuita é 'FlexMedia_Guest'. Não precisa de senha.",
        "categoria": "informacao"
    },
    "estacionamento": {
        "palavras": ["estacionamento", "carro", "vaga", "estacionar"],
        "resposta": "O estacionamento tem capacidade para 500 vagas. Entrada pela Rua das Flores.",
        "categoria": "localizacao"
    },
    "horario": {
        "palavras": ["horário", "horario", "abre", "fecha", "funcionamento"],
        "resposta": "Funcionamos de segunda a sábado, das 10h às 22h. Domingos das 14h às 20h.",
        "categoria": "informacao"
    },
}

RESPOSTA_PADRAO = "Desculpe, não entendi sua pergunta. Posso te ajudar com: banheiro, saída, Wi-Fi, estacionamento ou horário."
CATEGORIA_PADRAO = "desconhecido"

def processar(texto: str) -> tuple[str, str]:
    texto_lower = texto.lower()
    for intencao in INTENCOES.values():
        for palavra in intencao["palavras"]:
            if palavra in texto_lower:
                return intencao["resposta"], intencao["categoria"]
    return RESPOSTA_PADRAO, CATEGORIA_PADRAO

def registrar_interacao(satisfacao: int, tempo_duracao: int):
    payload = {
        "valor_sensor": 1,
        "satisfacao": satisfacao,
        "tempo_duracao": tempo_duracao
    }
    try:
        response = requests.post(f"{API_URL}/api/dados_sensor", json=payload, timeout=5)
        if response.status_code == 200:
            print("[LOG] Interação registrada com sucesso.")
        else:
            print(f"[LOG] Falha ao registrar: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[LOG] API indisponível: {e}")

if __name__ == "__main__":
    import time

    print("=" * 40)
    print("  Bem-vindo ao Smart-Guide! 👋")
    print("  Como posso te ajudar hoje?")
    print("  (Digite 'sair' para encerrar)")
    print("=" * 40)

    inicio = time.time()
    satisfacao_final = 0

    while True:
        usuario = input("\nVocê: ").strip()

        if not usuario:
            continue

        if usuario.lower() in ["ótimo", "bom", "gostei", "obrigado"]:
            satisfacao_final = 1

        if usuario.lower() in ["sair", "tchau"]:
            tempo = int(time.time() - inicio)
            print("\nTotem: Até logo! Foi um prazer ajudar. 😊")
            registrar_interacao(satisfacao=satisfacao_final, tempo_duracao=tempo)
            break

        resposta, categoria = processar(usuario)
        print(f"\nTotem: {resposta}")