🚀 Totem Inteligente "Smart-Guide" - FlexMedia Challenge

Este projeto simula a arquitetura e a implementação de um **Totem Inteligente "Smart-Guide"** para o FlexMedia Challenge. O objetivo é demonstrar um pipeline completo de **Edge-to-Cloud**, integrando a coleta de dados de sensores simulados, persistência em **Oracle Database**, processamento inteligente com **Machine Learning** e visualização em um **Dashboard** analítico.

O projeto atende aos requisitos da Sprint 2 do Challenge, focando na integração funcional entre hardware e software para gerar métricas acionáveis de engajamento e utilidade.

---

## 🎯 Objetivos do Projeto

O projeto visa demonstrar a integração funcional entre os módulos, conforme os requisitos do desafio:

1. **Integração Funcional:** Conectar sensores simulados (Wokwi/ESP32) a um backend Flask e persistir dados em um banco de dados SQL (Oracle).

1. **Estrutura de Dados:** Registrar e estruturar dados de interação (`valor_sensor`, `satisfacao`, `tempo_duracao`).

1. **Inteligência de ML:** Aplicar Machine Learning Supervisionado (Árvore de Decisão) para classificar o tipo de interação do usuário.

1. **Visualização:** Criar um dashboard front-end simples (Streamlit) para acompanhar métricas de uso e os insights gerados pelo ML.

1. **Conformidade:** Garantir a anonimização dos dados na borda (Edge Computing) e a segurança na comunicação (HTTPS/TLS).

---

## 🏗️ Arquitetura e Fluxo de Dados

A solução adota um modelo **Edge-to-Cloud** dividido em três camadas principais:

### 1. Camada de Borda (Edge Computing - Wokwi/ESP32)

Responsável pela coleta de dados e anonimização.

| Componente | Função | Detalhes de Implementação |
| --- | --- | --- |
| **Hardware Simulado** | ESP32 (via Wokwi) | Utiliza um sensor PIR (presença) e um botão (interação útil). |
| **Coleta** | `sketch.ino` | O código registra o início da sessão (PIR `HIGH`) e o fim (PIR `LOW`), calculando a `tempo_duracao`. O botão registra a `satisfacao`. |
| **Comunicação** | HTTPS/TLS | Envia os dados brutos (JSON) via `POST` para a API do Backend, garantindo a segurança. |

### 2. Camada de Nuvem (Backend, Persistência e ML)

O backend centraliza a recepção, o armazenamento e a inteligência.

| Componente | Tecnologia | Arquivo | Função |
| --- | --- | --- | --- |
| **API Gateway** | Flask | `api.py` | Recebe o JSON via `POST` no endpoint `/api/dados_sensor` e valida a integridade dos dados. |
| **Persistência** | Oracle Database | `db_config.py` | Gerencia o Pool de Conexões e executa o `INSERT` na tabela `logs_sensores`. |
| **Inteligência** | Python/Scikit-learn | `DataClass.py` | Treina um modelo de Árvore de Decisão para classificar as sessões em 6 categorias de experiência (Ex: "interação longa e útil"). |

### 3. Camada de Visualização (Dashboard)

Responsável por transformar os insights do ML em métricas visuais.

| Componente | Tecnologia | Arquivo | Função |
| --- | --- | --- | --- |
| **Dashboard** | Streamlit | `dash.py` | Consome o arquivo `dados_classificados_ml.csv` para exibir KPIs, Gráfico Donut e o Gráfico de Velocímetro (Taxa de Utilidade). |

---

## ⚙️ Configuração e Execução

Para rodar o projeto, siga os passos abaixo:

### 1. Configuração do Ambiente Python (Backend e ML)

O backend e o módulo de Machine Learning são escritos em Python.

#### 1.1. Instalação de Dependências

Crie e ative um ambiente virtual (recomendado) e instale as bibliotecas necessárias:

```bash
# Crie e ative seu ambiente virtual
python3 -m venv venv
source venv/bin/activate 

# Instale as bibliotecas necessárias
# Flask, oracledb, python-dotenv (para o Backend)
# pandas, scikit-learn, streamlit, plotly (para o ML e Dashboard)
pip install flask oracledb python-dotenv pandas scikit-learn streamlit plotly
```

#### 1.2. Configuração do Banco de Dados Oracle

O projeto utiliza o Oracle Database. Crie um arquivo chamado `.env` na raiz do projeto com suas credenciais de acesso:

```
## Arquivo .env
DB_USER="seu_usuario_oracle"
DB_PASS="sua_senha_oracle"
DB_DSN="seu_host:sua_porta/seu_servico"
```

### 2. Execução do Backend (API)

O `api.py` deve ser iniciado primeiro para receber os dados do Wokwi.

```bash
python3 api.py
```

Se a conexão for bem-sucedida, o servidor Flask estará rodando em `http://0.0.0.0:5000/`.

### 3. Execução do Módulo de Machine Learning

O `DataClass.py` processa os dados brutos (simulados em `dados_ficticios.csv` ) e gera o arquivo classificado para o Dashboard.

```bash
python3 DataClass.py
```

Este script irá gerar o arquivo `dados_classificados_ml.csv`.

### 4. Execução do Dashboard

O `dash.py` inicia o painel de visualização.

```bash
streamlit run dash.py
```

O Dashboard será aberto no seu navegador, exibindo as métricas de UX.

---

## 🌐 Simulação de Sensores (Wokwi/ESP32)

A simulação do hardware é feita via Wokwi, utilizando o código `sketch.ino`.

### 1. Bibliotecas (Inclusas no Wokwi)

O código `sketch.ino` utiliza as seguintes bibliotecas do ESP32:

- `WiFi`

- `HTTPClient`

- `WiFiClientSecure`

### 2. Lógica de Envio

O `sketch.ino` envia os dados via `POST` para o endpoint da API:

- **Endpoint:** `https://<SEU_TUNNEL_URL>/api/dados_sensor`

- **Método:** `POST`

- **Corpo da Requisição (JSON ):**

   ```json
   {
       "valor_sensor": 1,
       "satisfacao": <0 ou 1>,
       "tempo_duracao": <segundos>
   }
   ```

- **Observação:** O `sketch.ino` utiliza `client.setInsecure()` para simplificar a conexão HTTPS em ambientes de simulação como o Wokwi.

