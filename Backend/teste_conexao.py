import oracledb

# Suas credenciais da FIAP colocadas direto no código
MEU_USUARIO = "rm567109"
MINHA_SENHA = "fiap26"
# Adicionada a porta 1521 e o serviço ORCL, que são o padrão da faculdade
MEU_HOST = "oracle.fiap.com.br:1521/ORCL"

try:
    print("Tentando conectar no Oracle da FIAP...")

    conexao = oracledb.connect(
        user=MEU_USUARIO,
        password=MINHA_SENHA,
        dsn=MEU_HOST
    )

    print("✅ DEU CERTO! O banco está vivo e logamos com sucesso!")
    conexao.close()

except Exception as e:
    print(f"❌ DEU ERRO. O motivo foi: {e}")