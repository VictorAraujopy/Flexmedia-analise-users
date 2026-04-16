# 🗄️ Documentação do Banco de Dados — FlexMedia

## 1. Tabela: logs_sensores

### DDL (Estrutura da Tabela)
```sql
CREATE TABLE logs_sensores (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    valor_sensor    NUMBER(1),
    tempo_duracao   NUMBER,
    satisfacao      NUMBER(1),
    timestamp       TIMESTAMP DEFAULT SYSTIMESTAMP
);
```

### Descrição dos Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | NUMBER | Identificador único da sessão |
| valor_sensor | NUMBER(1) | 1 = sensor ativado, 0 = inativo |
| tempo_duracao | NUMBER | Tempo da sessão em segundos |
| satisfacao | NUMBER(1) | 1 = satisfeito, 0 = insatisfeito |
| timestamp | TIMESTAMP | Data e hora do registro |

---

## 2. Tabela: logs_interacoes

### DDL (Estrutura da Tabela)
```sql
CREATE TABLE logs_interacoes (
    id               NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo_interacao   VARCHAR2(10),
    conteudo         VARCHAR2(500),
    resposta_sistema VARCHAR2(1000),
    timestamp        TIMESTAMP DEFAULT SYSTIMESTAMP
);
```

### Descrição dos Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | NUMBER | Identificador único da interação |
| tipo_interacao | VARCHAR2 | Tipo: texto, voz ou botao |
| conteudo | VARCHAR2 | Pergunta ou input do usuário |
| resposta_sistema | VARCHAR2 | Resposta gerada pelo chatbot |
| timestamp | TIMESTAMP | Data e hora da interação |

---

## 3. Como os dados alimentam o Dashboard

- `logs_sensores` → alimenta os KPIs, gráficos temporais e o modelo ML
- `logs_interacoes` → alimenta as métricas de engajamento (pizza, ranking, tempo médio)

## 4. Como os dados alimentam o Modelo ML

O modelo Decision Tree usa as colunas `valor_sensor` e `tempo_duracao`
para prever a coluna `satisfacao`. Quanto maior o tempo de duração,
maior a chance de satisfação.