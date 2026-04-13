# Documentação da Interface — Smart-Guide

## 1. Visão Geral

A interface do Smart-Guide é composta por dois módulos principais: o `chatbot.py`, responsável pela lógica de respostas, e o `totem_interface.py`, responsável pela tela interativa do totem. Juntos, eles permitem que o visitante interaja com o totem via texto digitado ou botões de seleção, recebendo respostas automáticas em tempo real.

---

## 2. Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `chatbot.py` | Motor de respostas por intenções |
| `totem_interface.py` | Interface Streamlit do totem |
| `api.py` | Endpoints que conectam interface e banco |
| `db_config.py` | Persistência das interações no Oracle |

---

## 3. Fluxo de Dados

```
Visitante
   ↓ digita texto ou clica em botão
totem_interface.py
   ↓ POST /api/interacao
api.py
   ↓ chama chatbot.processar(texto)
chatbot.py
   ↓ retorna (resposta, categoria)
api.py
   ↓ salva no Oracle via db_config.salvar_interacao()
   ↓ retorna resposta para o Streamlit
totem_interface.py
   ↓ exibe resposta no histórico de conversa
Visitante
```

---

## 4. chatbot.py

Motor de respostas baseado em intenções. Cada intenção possui uma lista de palavras-chave, uma resposta e uma categoria.

### Intenções disponíveis

| Intenção | Palavras-chave | Categoria |
|---|---|---|
| Banheiro | banheiro, wc, sanitário, toalete | localizacao |
| Saída | saída, sair, porta, saida | localizacao |
| Wi-Fi | wifi, wi-fi, internet, rede, senha | informacao |
| Estacionamento | estacionamento, carro, vaga, estacionar | localizacao |
| Horário | horário, horario, abre, fecha, funcionamento | informacao |

### Função principal

```python
def processar(texto: str) -> tuple[str, str]:
```

Recebe o texto do visitante e retorna uma tupla `(resposta, categoria)`. Se nenhuma intenção for identificada, retorna a categoria `desconhecido`.

---

## 5. totem_interface.py

Interface Streamlit com layout em duas áreas:

- **Sidebar (esquerda):** botões de perguntas rápidas e campo de texto para dúvidas livres
- **Área principal (direita):** histórico de conversa em balões, com `st.chat_input` fixo no rodapé

### Tipos de interação

| Tipo | Como é gerado |
|---|---|
| `botao` | Visitante clica em uma das opções rápidas |
| `texto` | Visitante digita livremente no campo de chat |

---

## 6. Endpoints da API

### POST /api/interacao

Recebe o texto do visitante, processa via chatbot e salva no banco.

**Request:**

```json
{
  "texto": "onde fica o banheiro",
  "tipo": "texto"
}
```

**Response:**

```json
{
  "resposta": "O banheiro fica no corredor B, ao lado da loja 12.",
  "categoria": "localizacao"
}
```

### GET /api/recomendacao

Retorna uma sugestão com base no perfil do visitante. Integração com modelo ML da P1 pendente.

**Parâmetro:** `?perfil=longa` | `curta` | `util` | `padrao`

**Response:**

```json
{
  "recomendacao": "Que tal visitar a ala de tecnologia?",
  "perfil": "longa"
}
```

---

## 7. Como Executar

**Terminal 1 — API:**

```bash
cd Backend
python api.py
```

**Terminal 2 — Interface:**

```bash
cd Backend
streamlit run totem_interface.py
```

Acessar em `http://localhost:8501`.

---

## 8. Dados Salvos no Banco

Cada interação é registrada na tabela `logs_interacoes` com os seguintes campos:

| Campo | Descrição |
|---|---|
| `tipo_interacao` | `texto`, `voz` ou `botao` |
| `conteudo` | Mensagem enviada pelo visitante |
| `resposta_sistema` | Resposta gerada pelo chatbot |
| `categoria` | Categoria da intenção identificada |
| `timestamp` | Data e hora da interação |