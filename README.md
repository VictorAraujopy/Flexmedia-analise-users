# 🤖 Totem Inteligente "Smart-Guide" FlexMedia
O Totem Inteligente "Smart-Guide" FlexMedia é uma solução de análise de experiência do usuário desenvolvida para museus e exposições culturais.

---

## 🤝 Responsabilidades da Equipe

| Membro | Responsabilidade Principal |
| :--- | :--- |
| Jonathan Gomes Ribeiro Franco | Estrutura e Banco de Dados |
| Pedro Zanon Castro | Simulação e Coleta de Dados |
| Filipe Marques Previato | Análise e Inteligência Artificial |
| Victor Araujo Ferreira | Visualização e Dashboard |
| Jacqueline Nanami Matushima | Gestão, Documentação e Vídeo | 

---

## O Desafio
Exposições carecem de métricas objetivas e em tempo real para avaliar a eficácia do conteúdo e do layout, resultando em decisões de curadoria subjetivas.

 💡 A Solução Smart-Guide
O Smart-Guide resolve isso implementando uma arquitetura Edge-to-Cloud com Machine Learning. Nossa solução converte a presença física e a interação em dados quantificáveis, permitindo:

* **Classificação Inteligente**: Classificar cada sessão como útil ou inútil (fricção).

* **Insights Acionáveis**: Gerar métricas de Taxa de Utilidade e Potencial de Abandono que a curadoria pode usar para otimizar o espaço e aumentar o engajamento do público.

O Smart-Guide transforma o totem em uma poderosa ferramenta de Business Intelligence para o setor cultural.

### Nossos Diferenciais

| Característica | Detalhamento |
| :--- | :--- |
| **Engajamento Inteligente** | Personaliza rotas e conteúdos com base na atenção e interesse do visitante. |
| **Privacidade por Design (LGPD)** | Processamento de dados anônimos na borda (**Edge Computing**), descartando imagens e enviando apenas metadados criptografados. |
| **Geração de Insights Acionáveis**| Utiliza Machine Learning para classificar as interações e gerar métricas (Taxa de Utilidade, Duração Média e Heatmaps de Fricção) para a curadoria. |

---

## 🏗️ Arquitetura da Solução

A solução é **modular e escalável**, seguindo o princípio de processamento na borda (**Edge**) antes da persistência na **Nuvem**.

### 1. Edge Computing (Hardware & Coleta)

* **Dispositivo:** ESP32-CAM (simulado via Wokwi).
* **Ação:** O Sensor PIR (presença) e o Botão (interação) ativam o microcontrolador. O dispositivo analisa a atenção, **anonimiza os dados (descarte de imagem)** e calcula a duração da sessão.
* **Comunicação:** Envio de metadados via HTTPS/TLS para a API Gateway na Nuvem.

### 2. Nuvem (Backend e Processamento)

* **API Gateway:** Implementado em **Python/Flask**, responsável por receber os dados via POST.
* **Armazenamento:** **Oracle SQL** (simulação) para persistência inicial e centralizada dos dados de interação.
* **Processamento ML:** Script `DataClass.py` que aplica um modelo de **Árvore de Decisão** para rotular as sessões (Ex: "Interação longa e útil").

### 3. Visualização (Dashboard)

* **Tecnologia:** **Streamlit** (Python).
* **Função:** Consome o CSV com os dados classificados pelo ML e exibe métricas-chave para a curadoria, como a Taxa de Utilidade, Duração Média e distribuição das 6 categorias de experiência.

---

## ⚙️ Tecnologias Principais

| Camada | Ferramenta | Uso no Projeto |
| :--- | :--- | :--- |
| **Hardware / Edge** | ESP32, Wokwi | Simulação da coleta de dados e Edge Computing (Anonimização). |
| **Backend / API** | Python, Flask | Criação do *endpoint* para recebimento seguro de dados. |
| **Armazenamento** | Oracle SQL | Persistência e gerenciamento centralizado dos dados brutos. |
| **Inteligência / IA** | Python, Scikit-learn | Modelo de Árvore de Decisão para classificação de UX. |
| **Visualização** | Streamlit | Dashboard interativo e analítico para a Curadoria. |

---

## 🔒 Segurança e Privacidade (LGPD)
O Totem Smart-Guide foi focado sob o princípio de Privacidade por Design, garantindo a conformidade com a LGPD.

* **Anonimização e Edge Computing**: Para proteger o usuário, o processamento de dados ocorre na borda (no ESP32). A imagem bruta é descartada localmente, e a nuvem recebe apenas metadados não identificáveis, como a duração e o tipo de interação.

* **Comunicação Criptografada**: A transmissão dos metadados entre o Totem e a API é feita exclusivamente por canais seguros, utilizando TLS/HTTPS, assegurando a integridade e confidencialidade dos dados em trânsito.

* **Autenticação**: A comunicação é protegida por API Keys, garantindo que apenas os Totens autorizados possam enviar dados ao sistema.
---

## ✅ Entregáveis

### O vídeo de demonstração do fluxo de dados (Coleta → SQL → Análise ML → Dashboard) pode ser acessado no link abaixo.

**[▶️ Vídeo de Demonstração](https://youtu.be/IsyxFJXJOS8?si=Tn-UwoW30bB2KLrI)**

### A descrição detalhada da arquitetura Edge-to-Cloud, o fluxo de dados (Entrada → Processamento → Saída) e os prints de execução estão disponíveis na documentação técnica completa em PDF:

[📁 Acessar Documentação Técnica Completa](./DocTec.FlexMedia-FIAP.pdf)


