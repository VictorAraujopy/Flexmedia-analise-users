# Totem Inteligente "Smart-Guide" - FlexMedia Challenge

Pipeline completo **Edge-to-Cloud**: sensores simulados (Wokwi/ESP32) enviam dados para uma API Flask, que persiste no Oracle Database. Um modelo de Machine Learning classifica a satisfacao do usuario e um Dashboard Streamlit exibe os resultados.

---

## Estrutura do Projeto

```
Backend/
├── api.py          # API Flask - recebe dados do sensor via POST
├── db_config.py    # Conexao com Oracle (pool) + queries INSERT/SELECT
├── DataClass.py    # Pipeline de ML (Decision Tree) - classifica satisfacao
├── dash.py         # Dashboard Streamlit com graficos e KPIs
└── .env            # Credenciais do banco (NAO commitado)
```

---

## Fluxo Completo

```
Wokwi/ESP32  ──POST──>  api.py  ──INSERT──>  Oracle DB
                                                  │
                                              SELECT dados
                                                  │
                                dash.py  <──ML──  DataClass.py
                              (Streamlit)       (Decision Tree)
```

1. O **ESP32 (Wokwi)** detecta presenca (sensor PIR) e registra interacao (botao)
2. Envia via POST para `http://<IP>:5000/api/dados_sensor`
3. A **API Flask** valida e salva no **Oracle** (tabela `logs_sensores`)
4. O **Dashboard** puxa os dados do banco, passa pelo modelo de ML e exibe metricas

---

## Pre-requisitos

- Python 3.10+
- Acesso ao Oracle Database (FIAP ou outro)
- Wokwi com projeto ESP32 configurado (responsabilidade do colega de hardware)

---

## Instalacao

### 1. Clonar e criar ambiente virtual

```bash
git clone <url-do-repo>
cd Flexmedia-analise-users

python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar o `.env`

Crie o arquivo `Backend/.env` com suas credenciais:

```env
DB_USER="seu_usuario_oracle"
DB_PASS="sua_senha_oracle"
DB_DSN="oracle.fiap.com.br:1521/ORCL"
```

### 4. Criar a tabela no Oracle (se ainda nao existir)

```sql
CREATE TABLE logs_sensores (
    valor_sensor  NUMBER,
    satisfacao    NUMBER,
    tempo_duracao NUMBER
);
```

---

## Como Rodar

### Rodar a API (receber dados do Wokwi)

```bash
cd Backend
python3 api.py
```

Saida esperada:
```
[DB CONFIG] iniciando Pool de Conexoes...
[DB CONFIG] Pool de Conexoes criado com SUCESSO

--- Conexao com Oracle OK. Iniciando API... ---
 * Running on http://0.0.0.0:5000
```

A API fica escutando em `http://0.0.0.0:5000/api/dados_sensor` (POST).

### Testar a API manualmente (sem Wokwi)

Abra outro terminal e envie um POST de teste:

```bash
curl -X POST http://localhost:5000/api/dados_sensor \
  -H "Content-Type: application/json" \
  -d '{"valor_sensor": 1, "satisfacao": 1, "tempo_duracao": 45}'
```

Resposta esperada:
```json
{"mensagem": "Dados salvos com sucesso"}
```

A API tambem aceita form-data (formato comum do ESP32):
```bash
curl -X POST http://localhost:5000/api/dados_sensor \
  -d "valor_sensor=1&satisfacao=0&tempo_duracao=8"
```

### Rodar o Dashboard

```bash
cd Backend
streamlit run dash.py
```

O Streamlit abre no navegador (geralmente `http://localhost:8501`) e exibe:

- **KPIs**: total de sessoes, % satisfacao real, % satisfacao prevista pelo ML, tempo medio
- **Insights**: tempo medio de usuarios satisfeitos vs insatisfeitos
- **Grafico**: comparativo de satisfacao real vs prevista pelo modelo

---

## Endpoint da API

### `POST /api/dados_sensor`

| Campo | Tipo | Descricao |
|---|---|---|
| `valor_sensor` | number | `1` = sensor detectou presenca, `0` = sem presenca |
| `satisfacao` | number | `1` = satisfeito (botao pressionado), `0` = insatisfeito |
| `tempo_duracao` | number | Duracao da sessao em segundos |

**Respostas:**

| Codigo | Significado |
|---|---|
| `200` | Dados salvos com sucesso |
| `400` | Campos faltando, tipo invalido ou formato nao suportado |
| `500` | Falha ao salvar no banco |

---

## Modelo de Machine Learning

- **Algoritmo**: Decision Tree (Arvore de Decisao) - `sklearn.tree.DecisionTreeClassifier`
- **Feature**: `tempo_duracao` (tempo da sessao)
- **Target**: `satisfacao` (0 ou 1)
- **Filtro**: so usa sessoes onde `valor_sensor == 1` e `tempo_duracao > 10` (evita ativacoes acidentais)
- **Split**: 70% treino / 30% teste
- **Saida**: coluna `satisfacao_prevista` adicionada ao DataFrame

---

## Conexao Wokwi -> API

O ESP32 no Wokwi envia POST para a API. Para funcionar:

1. A API precisa estar rodando (`python3 api.py`)
2. Se o Wokwi estiver em nuvem, use um tunnel (ngrok, localtunnel, etc.) para expor a porta 5000
3. No `sketch.ino`, configure o endpoint: `http://<SEU_IP_OU_TUNNEL>:5000/api/dados_sensor`

O payload que o ESP32 deve enviar:
```json
{
    "valor_sensor": 1,
    "satisfacao": 0,
    "tempo_duracao": 32
}
```

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Hardware | ESP32 / Wokwi |
| API | Flask |
| Banco | Oracle Database |
| ML | scikit-learn (Decision Tree) |
| Dashboard | Streamlit + Plotly |
| Linguagem | Python 3.10 |
