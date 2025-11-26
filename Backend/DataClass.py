import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# 1. Carregar o arquivo (que agora tem colunas: tempo_interacao, util)
df = pd.read_csv(r"data/dados_ficticios.csv")

# Renomear a coluna 'util' para 'teve_duvida' para manter o padrão
df = df.rename(columns={"util": "teve_duvida"})

# 2. Aplicar a Regra de Negócio (Isso cria a "classificacao_real" ou "Target")
def classificar_experiencia_regras(row):
    if row["tempo_interacao"] < 20:
        class_tempo = "uso baixo"
    elif row["tempo_interacao"] < 60:
        class_tempo = "uso moderado"
    else:
        class_tempo = "uso intenso"
    
    if class_tempo == "uso intenso" and row["teve_duvida"] == 1:
        return "interação longa e útil"
    elif class_tempo == "uso intenso" and row["teve_duvida"] == 0:
        return "interação longa e inútil"
    elif class_tempo == "uso moderado" and row["teve_duvida"] == 1:
        return "interação moderada e útil"
    elif class_tempo == "uso baixo" and row["teve_duvida"] == 1:
        return "interação rápida mas útil"
    else:
        return "interação rápida e inútil"

df["class_experiencia"] = df.apply(classificar_experiencia_regras, axis=1)

print("Dados carregados e rotulados com sucesso!")

# 3. Preparar Features (Removemos 'tipo_clique' pois não existe mais no input)
features = ["tempo_interacao", "teve_duvida"]
X = df[features]
y = df["class_experiencia"]

# Separação Treino e Teste (para validar a acurácia)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("Treinando o modelo de Árvore de Decisão...")
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Avaliar precisão
previsoes_teste = clf.predict(X_test)
acuracia = accuracy_score(y_test, previsoes_teste)
print(f"Acurácia do modelo: {acuracia * 100:.2f}%")

# 4. Gerar o CSV Final
# Importante: Como você quer transformar a lista inteira, vamos aplicar a IA no dataframe TODO
df["classificacao_ia"] = clf.predict(X)

# Selecionar apenas as colunas que você pediu
df_export = df[["tempo_interacao", "teve_duvida", "classificacao_ia"]]

df_export.to_csv("dados_classificados_ml.csv", index=False)

print("\n--- PROCESSO CONCLUÍDO ---")
print("Arquivo gerado: dados_classificados_ml.csv")
print(df_export.head()) # Mostra as primeiras linhas para conferir