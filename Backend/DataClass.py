import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

MODEL_PATH = os.path.join(os.path.dirname(__file__), "melhor_modelo.joblib")


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = df[(df["valor_sensor"] == 1) & (df["tempo_duracao"] > 10)].copy()

    X = df[["tempo_duracao"]]
    y = df["satisfacao"]

    if os.path.exists(MODEL_PATH):
        modelo = joblib.load(MODEL_PATH)
        print(f"Modelo carregado: {type(modelo).__name__}")
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
        modelo.fit(X_train, y_train)
        acuracia = accuracy_score(y_test, modelo.predict(X_test))
        print(f"AVISO: melhor_modelo.joblib nao encontrado. Usando Decision Tree (acuracia: {acuracia * 100:.2f}%)")

    df["satisfacao_prevista"] = modelo.predict(X)

    return df
