import pandas as pd
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def run_pipeline(df):
    """
    Recebe o DataFrame do banco de dados, aplica as regras de negócio,
    treina o modelo de ML, salva o CSV e retorna o DataFrame classificado.
    """
    print("Iniciando o pipeline de dados no DataClass...")

    # 1. Tratar coluna (caso venha do banco como 'util')
    if "util" in df.columns:
        df = df.rename(columns={"util": "teve_duvida"})

    # 2. Corrigir e aplicar a Regra de Negócio
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
        # BUG CORRIGIDO AQUI: Adicionada a condição exata para moderada e inútil
        elif class_tempo == "uso moderado" and row["teve_duvida"] == 0:
            return "interação moderada e inútil"
        elif class_tempo == "uso baixo" and row["teve_duvida"] == 1:
            return "interação rápida mas útil"
        else:
            return "interação rápida e inútil"

    # Aplica a regra para criar o Target (y)
    df["class_experiencia"] = df.apply(classificar_experiencia_regras, axis=1)

    # 3. Preparar Features e Treinar a Árvore de Decisão
    features = ["tempo_interacao", "teve_duvida"]
    X = df[features]
    y = df["class_experiencia"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    # Avaliar e printar acurácia para fins de log/documentação da Sprint
    acuracia = accuracy_score(y_test, clf.predict(X_test))
    print(f"Acurácia do modelo: {acuracia * 100:.2f}%")

    # 4. Gerar as previsões da IA no DataFrame completo
    df["classificacao_ia"] = clf.predict(X)

    # 5. Corrigir o Path e Salvar CSV de forma segura
    # Path(__file__).parent garante que o CSV seja salvo na mesma pasta deste script,
    # independente de onde o terminal chamou o comando 'streamlit run'
    base_dir = Path(__file__).parent.resolve()
    caminho_csv = base_dir / "dados_classificados_ml.csv"

    # Exportar e salvar
    df_export = df[["tempo_interacao", "teve_duvida", "classificacao_ia"]]
    df_export.to_csv(caminho_csv, index=False)
    print(f"Arquivo CSV gerado com sucesso em: {caminho_csv}")

    # 6. Retorna o DataFrame completo para o dash.py renderizar os gráficos
    return df