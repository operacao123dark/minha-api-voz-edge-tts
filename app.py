import asyncio
import edge_tts
from flask import Flask, request, send_file, jsonify
import tempfile
import os

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts_endpoint():
    data = request.json
    text = data.get('input') or data.get('text')
    voice = data.get('voice', 'pt-BR-FranciscaNeural')

    if not text:
        return jsonify({"error": "Texto não fornecido"}), 400

    # Cria arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()

    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_file.name)

    try:
        asyncio.run(generate())
        return send_file(temp_file.name, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Limpeza é feita pelo sistema operacional ou na próxima reinicialização do container
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
