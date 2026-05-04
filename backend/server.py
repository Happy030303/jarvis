from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cohore_api import cohore_model_classify
import llm_model
from tts import speak_text, stop_speaking
import speech_recognition as sr

app = Flask(__name__, static_folder="../frontend")
CORS(app)

is_listening = False

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/listen", methods=["POST"])
def listen(): ## same what stt.py method did "def captureAudio_into_text():"
    stop_speaking()
    global is_listening
    if is_listening:
        return jsonify({"error": "Already listening"}), 409

    is_listening = True
    recogniser = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recogniser.adjust_for_ambient_noise(source, duration=0.1)
            audio = recogniser.listen(source, timeout=10, phrase_time_limit=15)

        text = recogniser.recognize_google(audio, language="en-US")
        is_listening = False
        return jsonify({"success": True, "text": text})

    except sr.WaitTimeoutError:
        is_listening = False
        return jsonify({"error": "No speech detected. Try again."}), 400
    except sr.UnknownValueError:
        is_listening = False
        return jsonify({"error": "Could not understand audio. Try again."}), 400
    except Exception as e:
        is_listening = False
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask():
    stop_speaking()
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        category = cohore_model_classify(user_text)

        if category == "GENERAL":
            response = llm_model.groq_model(user_text)
            threading.Thread(target=speak_text, args=(response,), daemon=True).start()
            return jsonify({"success": True, "category": "GENERAL", "response": response})

        elif category == "REALTIME":
            response = llm_model.realtime_query(user_text)
            if response:
                threading.Thread(target=speak_text, args=(response,), daemon=True).start()
            return jsonify({"success": True, "category": "REALTIME", "response": response or "Realtime query processed."})

        elif category == "SYSTEM":
            llm_model.system_query(user_text)
            msg = "System command executed."
            threading.Thread(target=speak_text, args=(msg,), daemon=True).start()
            return jsonify({"success": True, "category": "SYSTEM", "response": msg})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "listening": is_listening})

if __name__ == "__main__":
    print("\n JARVIS server starting on http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
