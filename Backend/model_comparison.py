"""
model_comparison.py — Comparacao de 4 modelos de ML (P1)

Fluxo:
  1. Puxa dados do Oracle via db_config
  2. Filtra e separa treino/teste (mesma logica do DataClass.py)
  3. Treina: Decision Tree, Random Forest, KNN, XGBoost
  4. Compara: accuracy, precision, recall, F1-score
  5. Salva o melhor modelo em melhor_modelo.joblib
"""

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier

import db_config


def carregar_e_filtrar_dados():
    db_config.init_db_pool()
    df = db_config.get_dados_sensor()

    df = df[(df["valor_sensor"] == 1) & (df["tempo_duracao"] > 10)].copy()

    if df.empty:
        print("[ERRO] Nenhum dado valido encontrado no banco.")
        return None, None, None, None

    print(f"[DADOS] {len(df)} registros validos encontrados")
    print(f"[DADOS] Distribuicao de satisfacao:\n{df['satisfacao'].value_counts().to_string()}\n")

    X = df[["tempo_duracao"]]
    y = df["satisfacao"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print(f"[SPLIT] Treino: {len(X_train)} | Teste: {len(X_test)}\n")

    return X_train, X_test, y_train, y_test


def treinar_modelos(X_train, y_train):
    modelos = {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            eval_metric="logloss",
            random_state=42,
            verbosity=0
        ),
    }

    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        print(f"[TREINO] {nome} treinado com sucesso")

    print()
    return modelos


def comparar_modelos(modelos, X_test, y_test):
    resultados = []

    for nome, modelo in modelos.items():
        y_pred = modelo.predict(X_test)

        resultados.append({
            "Modelo": nome,
            "Acuracia": round(accuracy_score(y_test, y_pred), 4),
            "Precisao": round(precision_score(y_test, y_pred, zero_division=0), 4),
            "Recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
            "F1": round(f1_score(y_test, y_pred, zero_division=0), 4),
        })

    tabela = pd.DataFrame(resultados)

    print("=" * 65)
    print("         COMPARACAO DE MODELOS — FlexMedia Sprint 4")
    print("=" * 65)
    print(tabela.to_string(index=False))
    print("=" * 65)

    return tabela


def salvar_melhor_modelo(modelos, tabela_comparacao):
    idx_melhor = tabela_comparacao["F1"].idxmax()
    nome_melhor = tabela_comparacao.loc[idx_melhor, "Modelo"]
    f1_melhor = tabela_comparacao.loc[idx_melhor, "F1"]

    modelo_melhor = modelos[nome_melhor]

    caminho = os.path.join(os.path.dirname(__file__), "melhor_modelo.joblib")
    joblib.dump(modelo_melhor, caminho)

    print(f"\n[RESULTADO] Melhor modelo: {nome_melhor} (F1: {f1_melhor})")
    print(f"[SALVO] {caminho}")

    return nome_melhor


if __name__ == "__main__":
    print("=" * 65)
    print("  model_comparison.py — Treinamento e comparacao de modelos")
    print("=" * 65)
    print()

    X_train, X_test, y_train, y_test = carregar_e_filtrar_dados()

    if X_train is None:
        print("Sem dados suficientes. Verifique o banco Oracle.")
        exit(1)

    modelos = treinar_modelos(X_train, y_train)
    tabela = comparar_modelos(modelos, X_test, y_test)
    salvar_melhor_modelo(modelos, tabela)

    print("\nPronto! Agora rode evaluation.py pra gerar os graficos.")
