from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividades (descricao, data_realizacao)
            VALUES (%s, %s)
            """,
            (data['descricao'], data['data_realizacao'])
        )
        conn.commit()
        return jsonify({"message": "Atividade criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['GET'])
def read_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividades WHERE id_atividade = %s", (id_atividade,))
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade[0],
            "descricao": atividade[1],
            "data_realizacao": atividade[2]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividades
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (data['descricao'], data['data_realizacao'], id_atividade)
        )
        conn.commit()
        return jsonify({"message": "Atividade atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM atividades WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        return jsonify({"message": "Atividade deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)