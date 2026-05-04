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

# ── Global state ──
_listen_lock   = threading.Lock()
_current_listen_thread = None
_listening     = False

def _set_listening(val: bool):
    global _listening
    _listening = val

# ── Routes ──

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


@app.route("/stop", methods=["POST"])
def stop():
    """Kill any active speech immediately."""
    stop_speaking()
    return jsonify({"success": True})


@app.route("/listen", methods=["POST"])
def listen():
    """
    ONE-SHOT listen:  frontend calls this once per mic click.
    Stops any ongoing speech first, then records a single utterance.
    it just turns voice into text and sends to html, then html code sends it to /ask endpoint which send to cohore api
    """
    stop_speaking()          # kill whatever Jarvis was saying
    _set_listening(True)

    recogniser = sr.Recognizer()
    recogniser.energy_threshold = 300   # lower = more sensitive
    recogniser.dynamic_energy_threshold = True

    recogniser.pause_threshold = 2      # 0.8 tha, ab 1.5s silence ke baad khatam hoga
    recogniser.phrase_threshold = 0.1     # choti awaaz bhi capture ho
    recogniser.non_speaking_duration = 1.5  # pause ke baad itna aur sune

    try:
        with sr.Microphone() as source:
            # Quick noise calibration — 0.3s is enough
            recogniser.adjust_for_ambient_noise(source, duration=0.3)
            # timeout=5  → give up after 5s of silence
            # phrase_time_limit=12 → max 12s of speech
            audio = recogniser.listen(source, timeout=5, phrase_time_limit=20)

        text = recogniser.recognize_google(audio, language="en-US")
        _set_listening(False)
        return jsonify({"success": True, "text": text})

    except sr.WaitTimeoutError:
        _set_listening(False)
        return jsonify({"error": "No speech detected. Try again."}), 400
    except sr.UnknownValueError:
        _set_listening(False)
        return jsonify({"error": "Could not understand audio. Try again."}), 400
    except Exception as e:
        _set_listening(False)
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    stop_speaking()          # stop any previous speech before processing new query

    data      = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # ── Classify intent ── # sending user asked to cohore api
        category = cohore_model_classify(user_text)

        if category == "GENERAL":
            response = llm_model.groq_model(user_text)
            threading.Thread(target=speak_text, args=(response,), daemon=True).start() # threading ma "speak_text() method" or "response return" ek shaat ho raha hai
            return jsonify({"success": True, "category": "GENERAL", "response": response})

        elif category == "REALTIME":
            response = llm_model.realtime_query(user_text)
            if response:
                threading.Thread(target=speak_text, args=(response,), daemon=True).start() # threading ma "speak_text() method" or "response return" ek
            return jsonify({
                "success": True,
                "category": "REALTIME",
                "response": response or "Realtime query processed."
            })

        elif category == "SYSTEM":
            llm_model.system_query(user_text)
            msg = "System command executed."
            threading.Thread(target=speak_text, args=(msg,), daemon=True).start()  # threading ma "speak_text() method" or "response return" ek
            return jsonify({"success": True, "category": "SYSTEM", "response": msg})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "listening": _listening})


if __name__ == "__main__":
    print("\n  JARVIS server starting on http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

    # server.py is working .......