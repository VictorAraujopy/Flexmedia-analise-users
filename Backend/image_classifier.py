"""
image_classifier.py — Classificador de expressoes faciais com sklearn (P1)

Demonstra visao computacional usando dataset FER2013 ou dataset sintetico.
Treina SVM em pixels achatados (48x48 -> 2304 features).
Standalone — nao conecta com o resto do sistema.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "graficos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_SIZE = 48
CLASSES = {0: "Triste", 1: "Feliz"}


def carregar_fer2013(csv_path):
    df = pd.read_csv(csv_path)

    df_filtrado = df[df["emotion"].isin([3, 4])].copy()
    df_filtrado["label"] = df_filtrado["emotion"].map({3: 1, 4: 0})

    X = np.array([
        np.fromstring(pixels, sep=" ").astype(np.float32)
        for pixels in df_filtrado["pixels"]
    ])

    y = df_filtrado["label"].values

    print(f"[FER2013] {len(X)} imagens carregadas (Feliz: {sum(y==1)}, Triste: {sum(y==0)})")
    return X, y


def gerar_dataset_sintetico(n_samples=300):
    np.random.seed(42)
    n_each = n_samples // 2
    total_pixels = IMG_SIZE * IMG_SIZE

    feliz = np.random.normal(loc=180, scale=40, size=(n_each, total_pixels)).clip(0, 255)
    triste = np.random.normal(loc=80, scale=40, size=(n_each, total_pixels)).clip(0, 255)

    X = np.vstack([feliz, triste]).astype(np.float32)
    y = np.array([1] * n_each + [0] * n_each)

    indices = np.random.permutation(len(X))
    X, y = X[indices], y[indices]

    print(f"[SINTETICO] {len(X)} imagens geradas (Feliz: {n_each}, Triste: {n_each})")
    return X, y


def treinar_classificador(X_train, y_train):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    modelo = SVC(kernel="rbf", C=1.0, random_state=42)
    modelo.fit(X_train_scaled, y_train)

    return modelo, scaler


def avaliar_classificador(modelo, scaler, X_test, y_test):
    X_test_scaled = scaler.transform(X_test)
    y_pred = modelo.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    print(f"\nAcuracia: {acc * 100:.2f}%\n")

    print(classification_report(y_test, y_pred, target_names=["Triste", "Feliz"]))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Purples",
        xticklabels=["Triste", "Feliz"],
        yticklabels=["Triste", "Feliz"],
    )
    plt.title("Matriz de Confusao — Classificador de Imagem")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.tight_layout()

    caminho = os.path.join(OUTPUT_DIR, "matriz_confusao_imagem.png")
    plt.savefig(caminho, dpi=150)
    plt.close()

    print(f"[SALVO] {caminho}")


if __name__ == "__main__":
    print("=" * 65)
    print("  image_classifier.py — Classificador de expressoes faciais")
    print("=" * 65)
    print()

    fer_path = os.path.join(os.path.dirname(__file__), "fer2013.csv")

    if os.path.exists(fer_path):
        X, y = carregar_fer2013(fer_path)
    else:
        print("[INFO] fer2013.csv nao encontrado. Usando dataset sintetico.\n")
        X, y = gerar_dataset_sintetico()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print(f"[SPLIT] Treino: {len(X_train)} | Teste: {len(X_test)}\n")

    modelo, scaler = treinar_classificador(X_train, y_train)
    avaliar_classificador(modelo, scaler, X_test, y_test)

    print("\nPronto!")
