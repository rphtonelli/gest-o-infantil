from flask import Flask, request, jsonify
import Util.bd as bd
import base64
from log_config import registrar_evento
import psycopg2
from psycopg2 import sql, Error

app = Flask(__name__)

@app.route('/atividade_aluno', methods=['POST'])
def create_atividade_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("CREATE", mensagem="Falha na conexão com o banco de dados", sucesso=False)
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade_aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (data['id_atividade'], data['id_aluno'])
        )
        conn.commit()
        registrar_evento("CREATE", aluno_id=data['id_aluno'], sucesso=True, mensagem="Relação Atividade-Aluno criada com sucesso")
        return jsonify({"message": "Relação Atividade-Aluno criada com sucesso"}), 201
    except Error as e:
        conn.rollback()
        registrar_evento("CREATE", aluno_id=data['id_aluno'], sucesso=False, mensagem=f"Erro ao inserir relação: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
def read_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("READ", aluno_id=id_aluno, sucesso=False, mensagem="Falha na conexão com o banco de dados")
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s",
            (id_atividade, id_aluno)
        )
        relacao = cursor.fetchone()
        if relacao is None:
            registrar_evento("READ", aluno_id=id_aluno, sucesso=False, mensagem="Relação não encontrada")
            return jsonify({"error": "Relação Atividade-Aluno não encontrada"}), 404
        
        registrar_evento("READ", aluno_id=id_aluno, sucesso=True, mensagem="Relação encontrada com sucesso")
        return jsonify({
            "id_atividade": relacao[0],
            "id_aluno": relacao[1]
        }), 200
    except Error as e:
        registrar_evento("READ", aluno_id=id_aluno, sucesso=False, mensagem=f"Erro ao buscar relação: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("DELETE", aluno_id=id_aluno, sucesso=False, mensagem="Falha na conexão com o banco de dados")
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s",
            (id_atividade, id_aluno)
        )
        conn.commit()
        registrar_evento("DELETE", aluno_id=id_aluno, sucesso=True, mensagem="Relação deletada com sucesso")
        return jsonify({"message": "Relação Atividade-Aluno deletada com sucesso"}), 200
    except Error as e:
        conn.rollback()
        registrar_evento("DELETE", aluno_id=id_aluno, sucesso=False, mensagem=f"Erro ao deletar relação: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)