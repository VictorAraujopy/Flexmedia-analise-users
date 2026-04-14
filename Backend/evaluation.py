"""
evaluation.py — Gera graficos de avaliacao do melhor modelo (P1)

Carrega melhor_modelo.joblib e gera:
  1. Matriz de confusao (PNG)
  2. Classification report (TXT)
  3. Curva de aprendizado (PNG)

Tudo salvo em Backend/graficos/
"""

import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import learning_curve

import model_comparison

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "graficos")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def gerar_matriz_confusao(modelo, X_test, y_test):
    y_pred = modelo.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Insatisfeito", "Satisfeito"],
        yticklabels=["Insatisfeito", "Satisfeito"],
    )
    plt.title("Matriz de Confusao")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.tight_layout()

    caminho = os.path.join(OUTPUT_DIR, "matriz_confusao.png")
    plt.savefig(caminho, dpi=150)
    plt.close()

    print(f"[SALVO] {caminho}")


def gerar_relatorio_classificacao(modelo, X_test, y_test):
    y_pred = modelo.predict(X_test)

    relatorio = classification_report(
        y_test, y_pred,
        target_names=["Insatisfeito", "Satisfeito"]
    )

    print("\n" + relatorio)

    caminho = os.path.join(OUTPUT_DIR, "classification_report.txt")
    with open(caminho, "w") as f:
        f.write(relatorio)

    print(f"[SALVO] {caminho}")


def gerar_curva_aprendizado(modelo, X, y):
    train_sizes, train_scores, val_scores = learning_curve(
        modelo, X, y,
        cv=5,
        scoring="f1",
        train_sizes=np.linspace(0.2, 1.0, 5),
        random_state=42
    )

    train_mean = train_scores.mean(axis=1)
    val_mean = val_scores.mean(axis=1)

    plt.figure(figsize=(8, 5))
    plt.plot(train_sizes, train_mean, "o-", label="Treino", color="#3b82f6")
    plt.plot(train_sizes, val_mean, "o-", label="Validacao", color="#ef4444")
    plt.fill_between(train_sizes, train_mean - train_scores.std(axis=1),
                     train_mean + train_scores.std(axis=1), alpha=0.1, color="#3b82f6")
    plt.fill_between(train_sizes, val_mean - val_scores.std(axis=1),
                     val_mean + val_scores.std(axis=1), alpha=0.1, color="#ef4444")
    plt.title("Curva de Aprendizado")
    plt.xlabel("Tamanho do conjunto de treino")
    plt.ylabel("F1-Score")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    caminho = os.path.join(OUTPUT_DIR, "curva_aprendizado.png")
    plt.savefig(caminho, dpi=150)
    plt.close()

    print(f"[SALVO] {caminho}")


if __name__ == "__main__":
    print("=" * 65)
    print("  evaluation.py — Gerando graficos de avaliacao")
    print("=" * 65)
    print()

    modelo_path = os.path.join(os.path.dirname(__file__), "melhor_modelo.joblib")

    if not os.path.exists(modelo_path):
        print("[ERRO] melhor_modelo.joblib nao encontrado. Rode model_comparison.py primeiro.")
        exit(1)

    modelo = joblib.load(modelo_path)
    print(f"[OK] Modelo carregado: {type(modelo).__name__}\n")

    X_train, X_test, y_train, y_test = model_comparison.carregar_e_filtrar_dados()

    if X_train is None:
        print("Sem dados suficientes.")
        exit(1)

    X_full = np.vstack([X_train, X_test])
    y_full = np.concatenate([y_train, y_test])

    gerar_matriz_confusao(modelo, X_test, y_test)
    gerar_relatorio_classificacao(modelo, X_test, y_test)
    gerar_curva_aprendizado(modelo, X_full, y_full)

    print(f"\nTodos os graficos salvos em: {OUTPUT_DIR}")
