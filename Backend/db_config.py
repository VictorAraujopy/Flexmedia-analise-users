import pandas as pd
import oracledb

# --- CREDENCIAIS DA FIAP (QUE FUNCIONARAM NO TESTE) ---
MEU_USUARIO = "rm567109"
MINHA_SENHA = "fiap26"
MEU_HOST = "oracle.fiap.com.br:1521/ORCL"

# 1. CRIAR O POOL DE CONEXÃO (Pra não travar se tiver muitos acessos)
try:
    pool = oracledb.create_pool(
        user=MEU_USUARIO,
        password=MINHA_SENHA,
        dsn=MEU_HOST,
        min=2,
        max=5,
        increment=1
    )
    print("✅ Pool de conexão com Oracle criado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao criar o pool do Oracle: {e}")
    pool = None


# 2. FUNÇÃO PARA BUSCAR OS DADOS (O Dashboard vai chamar essa)
def buscar_logs():
    """Busca os dados reais do banco para alimentar a Inteligência Artificial."""
    if not pool:
        print("Erro: Banco de dados não conectado.")
        return pd.DataFrame()

    try:
        with pool.acquire() as connection:
            # Puxa os dados da tabela
            query = "SELECT * FROM logs_sensores"
            df_logs = pd.read_sql(query, con=connection)
            print(f"✅ Dados extraídos! {len(df_logs)} linhas encontradas.")
            return df_logs

    except Exception as e:
        print(f"❌ [DB ERRO - SELECT] Falha ao buscar dados: {e}")
        return pd.DataFrame()


# 3. FUNÇÃO PARA INJETAR OS DADOS (A que a sua API já usa)
def salvar_log_sensor(dados):
    """Injeta novos logs no banco de dados."""
    if not pool:
        return

    sql = "INSERT INTO logs_sensores (valor_sensor, status_sensor, tempo_duracao) VALUES (:1, :2, :3)"

    dados_para_banco = (
        dados.get('valor_sensor', 0),
        dados.get('status_sensor', 0),
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