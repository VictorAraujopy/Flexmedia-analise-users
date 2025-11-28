from flask import Flask, jsonify, request
import db_config 

app = Flask(__name__)

@app.route ('/api/dados_sensor', methods=['POST'])
def receber_dados_sensor():
    dados = request.json
    
    if not dados or 'valor_sensor' not in dados or 'satisfacao' not in dados or 'tempo_duracao' not in dados:
        return jsonify({"erro": "Dados incompletos"}), 400
    
    print(f"\n[API] Dados recebidos: {dados}")

    db_config.salvar_log_sensor(dados)

    return jsonify({"mensagem": "Dados salvos com sucesso"}), 200



if __name__ == '__main__':

    if db_config.init_db_pool():
        print("\n--- Conexão com Oracle OK. Iniciando API... ---")
        print(app.url_map)
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Erro crítico ao conectar no banco. Verifique .env")
    

