from flask import Flask, jsonify, request
import db_config 

app = Flask(__name__)

@app.route('/api/dados_sensor', methods=['POST'])
def receber_dados_sensor():
    # Aceita JSON ou form-data (comum em Wokwi/ESP32)
    if request.is_json:
        dados = request.json
    elif request.form:
        dados = request.form.to_dict()
    else:
        print(f"\n[API] Content-Type não suportado: {request.content_type}")
        print(f"[API] Body bruto: {request.data}")
        return jsonify({"erro": "Envie JSON ou form-data"}), 400

    campos = ['valor_sensor', 'satisfacao', 'tempo_duracao']
    faltando = [c for c in campos if c not in dados]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios faltando: {faltando}"}), 400

    # Converte pra float (form-data vem como string)
    try:
        for campo in campos:
            dados[campo] = float(dados[campo])
    except (ValueError, TypeError):
        return jsonify({"erro": f"Campo '{campo}' deve ser numérico"}), 400

    print(f"\n[API] Dados recebidos: {dados}")

    if not db_config.salvar_log_sensor(dados):
        return jsonify({"erro": "Falha ao salvar no banco"}), 500

    return jsonify({"mensagem": "Dados salvos com sucesso"}), 200



if __name__ == '__main__':

    if db_config.init_db_pool():
        print("\n--- Conexão com Oracle OK. Iniciando API... ---")
        print(app.url_map)
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    else:
        print("Erro crítico ao conectar no banco. Verifique .env")
    

