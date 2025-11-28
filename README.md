# 🚀 Sistema de Análise de Interação (FlexMedia)

Este projeto simula um sistema completo de coleta, análise e visualização de dados de interação em um painel digital, utilizando **Python**, **Flask** e **Oracle Database**.

---

## 🎯 Objetivo Geral

Construir um pipeline de dados que começa com a **simulação** da coleta (Wokwi), passa pelo **armazenamento** no Oracle, pela **análise** (Pessoa 3) e finaliza na **visualização** (Dashboard/Pessoa 4).

---

## 👥 Divisão de Tarefas

O projeto segue esta divisão de responsabilidades:

| Pessoa | Foco Principal | Tarefas Chave | Tecnologias Principais |
| :--- | :--- | :--- | :--- |
| **Pessoa 1** | Estrutura e Banco de Dados | Modelar e criar o DB Oracle para receber e armazenar todos os dados dos sensores. | Oracle Database, SQL |
| **Pessoa 2 (Você)** | Simulação e Coleta de Dados | Criar a simulação dos sensores e enviar dados brutos (`valor_sensor`, `satisfacao`, `tempo_duracao`) para o Banco de Dados. | Wokwi, Python, Flask, `oracledb` |
| **Pessoa 3** | Análise e Inteligência Artificial | Conectar-se ao DB, realizar a análise dos dados e aplicar Machine Learning (ML). | Python (Pandas, Scikit-learn) |
| **Pessoa 4** | Visualização e Dashboard | Desenvolver a interface visual que exibe os resultados da análise da Pessoa 3. | Python (Streamlit/Dash) |
| **Pessoa 5** | Gestão e Documentação | Coordenar o projeto, garantir o código no GitHub e documentar. | GitHub |

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **API:** Flask (Responsável pela comunicação entre o Wokwi e o DB)
*   **Banco de Dados:** Oracle Database
*   **Conexão DB:** `oracledb`
*   **Simulação:** Wokwi ou Python Scripts

---

## ⚙️ Configuração do Ambiente (Backend)

Siga estes passos para configurar e rodar o servidor da API:

### 1. Instalação de Dependências

```bash
## Crie e ative seu ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate 

## Instale as bibliotecas necessárias
pip install flask oracledb python-dotenv
```

### 2. Configuração do Banco de Dados

Crie um arquivo chamado `.env` na raiz da sua pasta `Backend` com as suas credenciais de acesso ao Oracle, que são lidas pelo `db_config.py`:

```dotenv
## Exemplo de arquivo .env
DB_USER="seu_usuario_oracle"
DB_PASS="sua_senha_oracle"
DB_DSN="seu_host:sua_porta/seu_servico"
```

### 3. Execução da API

A API deve ser iniciada primeiro, pois é o destino dos dados da Pessoa 2 (Wokwi).

```bash
python3 api.py
```

Se a conexão for bem-sucedida, o servidor Flask estará rodando em `http://0.0.0.0:5000/`.

---

## 👨‍💻 Fluxo de Dados e Endpoints

### A. Coleta de Dados (Pessoa 2)

O Wokwi envia dados brutos via `GET` para este endpoint. O `api.py` recebe a requisição e salva no `logs_sensores`.

*   **Endpoint:** `/api/dados_sensor`
*   **Método:** `GET`
*   **Parâmetros na URL:** `valor_sensor`, `satisfacao`, `tempo_duracao`
*   **URL de Exemplo para o Wokwi:**
    `http://<SEU_IP>:5000/api/dados_sensor?valor_sensor=150&satisfacao=4&tempo_duracao=120`

### B. Relatório/Dashboard (Pessoa 4)

O Dashboard consulta este endpoint para buscar o histórico completo dos dados brutos para gerar gráficos e métricas.

*   **Endpoint:** `/api/relatorio`
*   **Método:** `GET`
*   **Retorno:** JSON contendo todos os registros da tabela `logs_sensores`.
