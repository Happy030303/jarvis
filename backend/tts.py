import subprocess
import sys

_process = None

def speak_text(text: str):
    global _process
    stop_speaking()  # pehle purana band karo
    
    # alag python process mein bolao
    _process = subprocess.Popen([
        sys.executable, "-c",
        f"""
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)
engine.setProperty('rate', 170)
engine.say({repr(text)})
engine.runAndWait()
"""
    ])

def stop_speaking():
    global _process
    if _process and _process.poll() is None:  # chal raha hai?
        _process.kill()                        # kill karo
        _process = None