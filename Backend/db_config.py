import oracledb
import os
from dotenv import load_dotenv 

load_dotenv()

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
    
    sql = """ 
        INSERT INTO logs_sensores (valor_sensor, satisfacao, tempo_duracao)
        VALUES (:1, :2, :3) 
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
    except Exception as e:
        print(f"[DB ERRO - INSERT]: {e}")
        