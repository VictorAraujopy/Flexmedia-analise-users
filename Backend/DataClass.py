
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv(r"data/dados_ficticios.csv")


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
print(f"Total de linhas: {len(df)}")


le = LabelEncoder()
df["tipo_clique_encoded"] = le.fit_transform(df["tipo_clique"])


features = ["tempo_interacao", "teve_duvida", "tipo_clique_encoded"]
X = df[features]
y = df["class_experiencia"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


print("Treinando o modelo de Árvore de Decisão...")
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Avaliar precisão
previsoes = clf.predict(X_test)
acuracia = accuracy_score(y_test, previsoes)
print(f"Acurácia do modelo nos dados de teste: {acuracia * 100:.2f}%")



df_export = X_test.copy()
df_export["classificacao_real"] = y_test        
df_export["classificacao_ia"] = previsoes       

df_export["tipo_clique"] = le.inverse_transform(df_export["tipo_clique_encoded"])

df_export.to_csv("dados_classificados_ml.csv", index=False)

print("\n--- PROCESSO CONCLUÍDO ---")
print("Arquivos gerados:")
print("3. dados_classificados_ml.csv (Use este no seu Dashboard)")