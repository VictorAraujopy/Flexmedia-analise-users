import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # Filtra apenas interações válidas:
    # valor_sensor == 1 → sensor detectou presença
    # tempo_duracao > 10 → evita ativações acidentais
    df = df[(df["valor_sensor"] == 1) & (df["tempo_duracao"] > 10)].copy()

    # X = o que o modelo analisa
    # y = o que ele aprende a prever

    X = df[["tempo_duracao"]]
    y = df["satisfacao"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
    modelo.fit(X_train, y_train)

    acuracia = accuracy_score(y_test, modelo.predict(X_test))
    print(f"Acurácia do modelo: {acuracia * 100:.2f}%")

    # modelo prevê satisfação pra cada linha
    df["satisfacao_prevista"] = modelo.predict(X)

    return df