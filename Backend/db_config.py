import pandas as pd
import oracledb

# --- CREDENCIAIS FIAP ---
MEU_USUARIO = "rm567109"
MINHA_SENHA = "fiap26"
MEU_HOST = "oracle.fiap.com.br:1521/ORCL"

pool = None

# ============================================================
# 1. Criar Pool Oracle
# ============================================================
def init_db_pool():
    global pool
    try:
        pool = oracledb.create_pool(
            user=MEU_USUARIO,
            password=MINHA_SENHA,
            dsn=MEU_HOST,
            min=1,
            max=5,
            increment=1
        )
        print("✅ Pool Oracle criado com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao criar o pool Oracle: {e}")
        return False


# ============================================================
# 2. Buscar dados → DataFrame
# ============================================================
def buscar_logs():
    if pool is None:
        print("❌ Pool não iniciado!")
        return pd.DataFrame()

    try:
        with pool.acquire() as connection:
            query = "SELECT * FROM logs_sensores"
            df = pd.read_sql(query, con=connection)

        print(f"🔎 {len(df)} registros carregados do banco.")

        # Padroniza nomes para o pipeline (IMPORTANTE)
        df = df.rename(columns={
            "tempo_duracao": "tempo_interacao",
            "satisfacao": "teve_duvida"
        })

        # Converte tipos para evitar erros no pipeline
        df["tempo_interacao"] = df["tempo_interacao"].astype(float)
        df["teve_duvida"] = df["teve_duvida"].astype(int)

        return df

    except Exception as e:
        print(f"❌ ERRO NO SELECT: {e}")
        return pd.DataFrame()


# ============================================================
# 3. Inserir dados vindos da API
# ============================================================
def salvar_log_sensor(dados):
    if pool is None:
        print("❌ Pool não iniciado!")
        return

    sql = "INSERT INTO logs_sensores (valor_sensor, satisfacao, tempo_duracao) VALUES (:1, :2, :3)"

    dados_para_banco = (
        dados.get('valor_sensor', 0),
        dados.get('satisfacao', 0),
        dados.get('tempo_duracao', 0)
    )

    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, dados_para_banco)
                connection.commit()
        print(f"✅ [DB INSERT] Log injetado com sucesso!")
    except Exception as e:
        print(f"❌ [DB ERRO - INSERT] Erro ao injetar dados: {e}")