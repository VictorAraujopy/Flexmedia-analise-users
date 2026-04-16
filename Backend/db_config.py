import oracledb
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

pool = None 

def init_db_pool():
    global pool
    try:
        print("[DB CONFIG] iniciando Pool de Conexões...")
        pool = oracledb.create_pool(user=DB_USER, password=DB_PASS, dsn=DB_DSN, min=2, max=5, increment=1)
        print("[DB CONFIG] Pool de Conexões criado com SUCESSO")
        return True
    except Exception as e:
        print(f"[DB CONFIG] ERRO AO CRIAR POOL: {e}")
        return False
    
def salvar_log_sensor(dados):

    """
        (INSERT) Salva os dados brutos: valor_sensor, satisfacao e tempo_duracao.
    """

    if pool is None:
        print("[DB ERRO] Pool não inicializado")
        return
    
    sql = """ 
        INSERT INTO logs_sensores (valor_sensor, satisfacao, tempo_duracao, timestamp)
        VALUES (:1, :2, :3, SYSTIMESTAMP) 
    """
    
    dados_para_banco = (
        dados.get('valor_sensor', 0), 
        dados.get('satisfacao', 0),  
        dados.get('tempo_duracao', 0),
    )   
   

    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, dados_para_banco)
                connection.commit()
        print(f"[DB INSERT] Log salvo: {dados_para_banco}")
        return True
    except Exception as e:
        print(f"[DB ERRO - INSERT]: {e}")
        return False

def salvar_interacao(dados):
    if pool is None:
        print("[DB ERRO] Pool não inicializado")
        return False

    sql = """
        INSERT INTO logs_interacoes (tipo_interacao, conteudo, resposta_sistema, categoria, timestamp)
        VALUES (:1, :2, :3, :4, SYSTIMESTAMP)
    """

    dados_para_banco = (
        dados.get('tipo_interacao', 'texto'),
        dados.get('conteudo', ''),
        dados.get('resposta_sistema', ''),
        dados.get('categoria', 'desconhecido'),
    )

    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, dados_para_banco)
                connection.commit()
        print(f"[DB INSERT] Interação salva: {dados_para_banco}")
        return True
    except Exception as e:
        print(f"[DB ERRO - INSERT interacao]: {e}")
        return False

def get_dados_sensor():
    sql = "SELECT valor_sensor, satisfacao, tempo_duracao, timestamp FROM logs_sensores"

    if pool is None:
        print("[DB ERRO] Pool não inicializado")
        return pd.DataFrame(columns=["valor_sensor", "satisfacao", "tempo_duracao", "timestamp"])

    try:

        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()

        return pd.DataFrame(rows, columns=["valor_sensor", "satisfacao", "tempo_duracao", "timestamp"])

    except Exception as e:
        print(f"[DB ERRO - SELECT]: {e}")
        return pd.DataFrame(columns=["valor_sensor", "satisfacao", "tempo_duracao", "timestamp"])

def get_interacoes(tipo=None):
    if pool is None:
        print("[DB ERRO] Pool não inicializado")
        return pd.DataFrame(columns=["tipo_interacao", "conteudo", "resposta_sistema", "timestamp"])

    if tipo:
        sql = "SELECT tipo_interacao, conteudo, resposta_sistema, timestamp FROM logs_interacoes WHERE tipo_interacao = :1 ORDER BY timestamp DESC"
        params = [tipo]
    else:
        sql = "SELECT tipo_interacao, conteudo, resposta_sistema, timestamp FROM logs_interacoes ORDER BY timestamp DESC"
        params = []

    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=["tipo_interacao", "conteudo", "resposta_sistema", "timestamp"])
    except Exception as e:
        print(f"[DB ERRO - SELECT interacoes]: {e}")
        return pd.DataFrame(columns=["tipo_interacao", "conteudo", "resposta_sistema", "timestamp"])

if __name__ == "__main__":
    if init_db_pool():
        print("Conexão OK! Pode abrir o dash.")
    else:
        print("Erro na conexão. Verifica o .env")