import subprocess
import sys
import threading
import os
import signal

_lock    = threading.Lock()
_process = None


def speak_text(text: str):
    stop_speaking()
    global _process
    script = f"""
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
voice_index = 3 if len(voices) > 3 else 0
engine.setProperty('voice', voices[voice_index].id)
engine.setProperty('rate', 170)
engine.say({repr(text)})
engine.runAndWait()
"""
    with _lock:
        _process = subprocess.Popen(
            [sys.executable, "-c", script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # ← Windows pe clean kill
        )


def stop_speaking():
    global _process
    with _lock:
        if _process and _process.poll() is None:
            _process.kill()
            _process.wait()
        _process = None