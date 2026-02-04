import asyncio
import edge_tts
from flask import Flask, request, send_file, jsonify
import io

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts_endpoint():
    data = request.json
    # Aceita tanto 'input' (padrão n8n) quanto 'text'
    text = data.get('input') or data.get('text')
    voice = data.get('voice', 'pt-BR-FranciscaNeural')

    if not text:
        return jsonify({"error": "Texto não fornecido"}), 400

    # Cria um arquivo na Memória RAM (Buffer)
    audio_memory = io.BytesIO()

    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        # Grava pedaço por pedaço na memória
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_memory.write(chunk["data"])

    try:
        asyncio.run(generate())
        audio_memory.seek(0) # Volta a fita para o começo antes de enviar
        return send_file(audio_memory, mimetype="audio/mpeg", download_name="audio.mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
