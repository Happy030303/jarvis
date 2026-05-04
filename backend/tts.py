import subprocess
import sys
import threading

_lock    = threading.Lock()
_process = None   # the running pyttsx3 subprocess


def speak_text(text: str):
    """Stop whatever is playing, then speak new text in a fresh subprocess."""
    stop_speaking()          # kill previous first

    global _process
    script = f"""
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)
engine.setProperty('rate', 170)
engine.say({repr(text)})
engine.runAndWait()
"""
    with _lock:
        _process = subprocess.Popen(
            [sys.executable, "-c", script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def stop_speaking():
    """Immediately kill the TTS subprocess — stops audio mid-sentence."""
    global _process
    with _lock:
        if _process and _process.poll() is None:
            _process.kill()
            _process.wait()   # wait for OS to fully release audio device
        _process = None