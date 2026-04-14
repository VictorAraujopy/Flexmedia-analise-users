# Documentacao de IA — FlexMedia Sprint 4

## 1. Modelos Testados

Todos treinados com os mesmos dados (`logs_sensores`), mesmo filtro (`valor_sensor == 1`, `tempo_duracao > 10`) e mesmo split (70/30, `random_state=42`).

| Modelo | Descricao |
|---|---|
| Decision Tree | Arvore de decisao simples com profundidade maxima 5. Modelo original do projeto. |
| Random Forest | Conjunto de 100 arvores que votam juntas. Reduz overfitting. |
| KNN | Classifica baseado nos 5 vizinhos mais proximos. Abordagem nao-parametrica. |
| XGBoost | Gradient boosting com 100 rodadas. Cada arvore corrige erros da anterior. |

### Tabela de Resultados

| Modelo | Acuracia | Precisao | Recall | F1-Score |
|---|---|---|---|---|
| Decision Tree | - | - | - | - |
| Random Forest | - | - | - | - |
| KNN | - | - | - | - |
| XGBoost | - | - | - | - |

> **Nota:** Preencher com os valores reais apos rodar `model_comparison.py`.

### Criterio de Escolha

O modelo com maior **F1-Score** foi selecionado como melhor modelo. F1 foi escolhido ao inves de accuracy porque equilibra precision e recall, sendo mais confiavel em datasets potencialmente desbalanceados.

## 2. Como o Modelo e Usado

1. `model_comparison.py` treina os 4 modelos e salva o melhor em `melhor_modelo.joblib`
2. `DataClass.py` carrega o `.joblib` e usa para predicoes no dashboard
3. Se o arquivo `.joblib` nao existir, `DataClass.py` treina um Decision Tree como fallback

```
model_comparison.py  -->  melhor_modelo.joblib  -->  DataClass.py  -->  dash.py
     (treina)                 (arquivo)              (carrega)        (exibe)
```

## 3. Metricas de Avaliacao

Geradas pelo `evaluation.py`:

- **Matriz de Confusao:** `graficos/matriz_confusao.png`
- **Classification Report:** `graficos/classification_report.txt`
- **Curva de Aprendizado:** `graficos/curva_aprendizado.png`

### Como interpretar

- **Matriz de confusao:** diagonal = acertos, fora da diagonal = erros
- **Curva de aprendizado:** se as linhas de treino e validacao convergem, o modelo esta saudavel. Se divergem, ha overfitting.

## 4. Classificador de Imagens

Modulo standalone (`image_classifier.py`) que demonstra visao computacional.

### Pipeline

1. Carrega dataset FER2013 (expressoes faciais 48x48 pixels) ou gera dataset sintetico
2. Filtra duas classes: Feliz e Triste (classificacao binaria)
3. Achata cada imagem de 48x48 para vetor de 2304 features
4. Normaliza com StandardScaler
5. Treina SVM com kernel RBF
6. Avalia com accuracy e matriz de confusao

### Por que SVM?

SVM com kernel RBF funciona bem para classificacao de pixels achatados em sklearn. StandardScaler e obrigatorio porque SVM e sensivel a escala dos dados.

### Resultado

- Matriz de confusao salva em `graficos/matriz_confusao_imagem.png`
- Este modulo nao se integra ao dashboard — e uma prova de conceito de visao computacional

## 5. Limitacoes Conhecidas

- **Feature unica:** o modelo de satisfacao usa apenas `tempo_duracao`. Mais features (tipo de interacao, horario) melhorariam a precisao.
- **Dataset pequeno:** poucos registros no Oracle podem causar overfitting.
- **Classificador de imagem usa pixels achatados:** uma CNN (rede neural convolucional) seria mais apropriada, mas foge do escopo do sklearn.
- **FER2013 e um dataset proxy:** nao sao imagens reais do totem.

## 6. Como Reproduzir

```bash
cd Backend

# 1. Treinar e comparar modelos
python model_comparison.py

# 2. Gerar graficos de avaliacao
python evaluation.py

# 3. Rodar classificador de imagem
python image_classifier.py

# Os graficos ficam em Backend/graficos/
```
