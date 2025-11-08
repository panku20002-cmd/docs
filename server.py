import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Flask and OpenAI
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Serve the HTML frontend ----------
@app.route('/')
def serve_html():
    return send_from_directory(os.getcwd(), 'jarvis_ai.html')

# ---------- GPT API endpoint ----------
@app.route('/api/gpt', methods=['POST'])
def gpt_reply():
    """
    This endpoint takes text input from frontend
    Sends it to OpenAI GPT model
    Returns text + optional speech file path
    """
    data = request.get_json()
    message = data.get("message", "")
    lang = data.get("lang", "en")

    if not message:
        return jsonify({"error": "No message received"}), 400

    try:
        # Send user message to GPT model
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful and multilingual AI assistant."},
                {"role": "user", "content": message}
            ]
        )
        reply = completion.choices[0].message.content

        # Convert GPT reply to speech (TTS)
        tts = gTTS(text=reply, lang=lang)
        speech_path = f"tts_output.mp3"
        tts.save(speech_path)

        return jsonify({
            "reply": reply,
            "speech": f"/{speech_path}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Serve generated TTS audio ----------
@app.route('/tts_output.mp3')
def serve_audio():
    return send_from_directory(os.getcwd(), "tts_output.mp3")

# ---------- Run Server ----------
if __name__ == '__main__':
    print("🚀 JarvisAI (GPT + TTS) server running on http://127.0.0.1:5000")
    app.run(debug=True)
