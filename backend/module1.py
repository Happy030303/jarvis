# ╔══════════════════════════════════════════════════════════════╗
# ║  JARVIS MODULE 1: SPEECH TO TEXT (HINGLISH VERSION)          ║
# ║  Focus: Understanding the 'What', 'Why', and 'Returns'       ║
# ╚══════════════════════════════════════════════════════════════╝

# ================================================================
# SECTION: EXTERNAL TOOLS (IMPORTS)
# ================================================================

# [faster_whisper]: Ye hamara "Offline Brain" hai jo audio sunta hai. 
# Kyun: Taki bina internet ke bhi humari aawaz text mein badal sake.
from faster_whisper import WhisperModel 

# [speech_recognition]: Mic hardware se baat karne ke liye zaruri hai.
# Kyun: Ye Python ko batata hai ki mic kab on karna hai aur kab off.
import speech_recognition as sr 

# [logging]: Background messages ko control karne ke liye.
# Kyun: Taki terminal par faltu ki errors na dikhein, sirf hamare kaam ki cheezein dikhein.
import logging 

# [os]: Operating System se baat karne ke liye.
# Kyun: Files save karne aur folders banane (audio/stored_text) ke liye iski zarurat hai.
import os 

# [re]: Regular Expressions (Pattern matching).
# Kyun: Ye check karne ke liye ki text mein Hindi characters hain ya nahi.
import re 

# [indic_transliteration]: Script conversion tools.
# Kyun: Hindi (Devanagari) script ko English letters (Hinglish) mein badalne ke liye.
from indic_transliteration import sanscript 
from indic_transliteration.sanscript import transliterate 

# Terminal output ko saaf rakhne ke liye sirf Warnings dikhao.
logging.basicConfig(level=logging.WARNING, format='%(message)s')

# ================================================================
# SECTION: GLOBAL AI MODEL INITIALIZATION
# ================================================================

print("Whisper model load ho raha hai... (sirf ek baar)")

# [WHISPER_MODEL]: Is line par AI model actually RAM mein load hota hai.
# Mode: "base" (balance of speed and accuracy).
# Device: "cpu" (taaki kisi bhi computer par chal sake).
# Compute: "int8" (memory bachane ke liye numbers ko chota rakhta hai).
WHISPER_MODEL = WhisperModel("base", device="cpu", compute_type="int8")

print("Model ready hai!\n")


# ================================================================
# SECTION: FUNCTION DEFINITIONS (Ye sirf yahan define ho rahe hain)
# ================================================================

def has_devanagari(text):
    """
    KAAM: Check karna ki kya word mein Hindi characters hain.
    KYUN: Taki hume pata chale ki kis word ko English script mein badalna hai.
    RETURN: True (agar Hindi hai) ya False (agar nahi hai).
    """
    return bool(re.search(r'[\u0900-\u097F]', text))


def capture_audio(mic_index=24):
    """
    KAAM: Microphone se awaaz record karna.
    KYUN: User ki commands ko capture karke computer tak pahunchana.
    PARAM: mic_index (Kaunsa mic use karna hai).
    RETURN: AudioData object (Raw sound bytes).
    """
    recognizer = sr.Recognizer() # Brain of microphone interaction.
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print(f"--- Sun raha hoon... (Mic Index: {mic_index}) ---")
            
            # 0.5 sec background noise measure karke usse "minus" karta hai.
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Actually audio record karna shuru karta hai.
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Awaaz capture ho gayi!")
            return audio
    except Exception as e:
        print(f"Mic error: {e}")
        return None


def save_audio_to_file(audio_data, base_name="audio"):
    """
    KAAM: Raw audio bytes ko .wav file mein badalna.
    KYUN: Whisper AI ko audio sunane ke liye file ka hona zaruri hai.
    RETURN: File path string (Jaise 'audio1.wav').
    """
    if audio_data is None: return None

    # Folder create karna agar nahi hai toh.
    os.makedirs("audio", exist_ok=True)

    # Naya filename dhoondna taaki purani file overwrite na ho.
    counter = 1
    while os.path.exists(os.path.join("audio", f"{base_name}{counter}.wav")):
        counter += 1
    file_name = os.path.join("audio", f"{base_name}{counter}.wav")

    try:
        # Binary mode ('wb') mein sound data save karna.
        with open(file_name, "wb") as f:
            f.write(audio_data.get_wav_data())
        print(f"Audio file save hui: {file_name}")
        return file_name
    except Exception as e:
        print(f"File save error: {e}")
        return None


def transcribe_audio(file_path):
    """
    KAAM: .wav file ko sun kar usse text mein badalna.
    KYUN: Computer ko batana ki user ne kya bola.
    RETURN: Raw text string (Jaise 'नमस्ते').
    """
    if not os.path.exists(file_path): return None

    print("Whisper audio sun raha hai...")
    try:
        # AI actually transcribing...
        segments, info = WHISPER_MODEL.transcribe(file_path, beam_size=5, task="transcribe")
        
        # Alag alag tukdon (segments) ko jod kar ek sentence banana.
        raw_text = " ".join(segment.text for segment in segments).strip()
        return raw_text
    except Exception as e:
        print(f"Transcription error: {e}")
        return None


def convert_to_hinglish(raw_text):
    """
    KAAM: Hindi script (Devanagari) ko English script (Roman) mein badalna.
    KYUN: Readability behtar karne ke liye aur coding flows mein asani ke liye.
    RETURN: Final Hinglish string.
    """
    if not raw_text: return None

    words = raw_text.split() # Sentence ko ek ek word mein todna.
    result_words = []

    for word in words:
        # Check karna ki word Hindi hai ya nahi.
        if has_devanagari(word):
            # Hindi word ko English letters mein convert karna.
            roman_word = transliterate(word, sanscript.DEVANAGARI, sanscript.ITRANS)
            result_words.append(roman_word)
        else:
            # Agar pehle se English hai toh waisa hi rehne do.
            result_words.append(word)

    return " ".join(result_words)


def save_text(text, audio_file_path):
    """
    KAAM: Final output ko ek .txt file mein save karna.
    KYUN: Taki future mein record rahe ki user ne kya bola tha.
    RETURN: None.
    """
    os.makedirs("stored_text", exist_ok=True)
    base_name = os.path.basename(audio_file_path).replace(".wav", ".txt")
    text_file_path = os.path.join("stored_text", base_name)
    
    try:
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text save hua: {text_file_path}")
    except Exception as e:
        print(f"Text save error: {e}")


# ================================================================
# SECTION: MAIN EXECUTION BLOCK (Yahan se asli kaam shuru hota hai)
# ================================================================

if __name__ == "__main__":
    
    # 1. Mic se awaaz lena.
    audio = capture_audio(mic_index=24)
    
    if audio:
        # 2. Awaaz ko file mein save karna.
        file_path = save_audio_to_file(audio)
        
        if file_path:
            # 3. AI ko audio file sunana aur text lena.
            raw_text = transcribe_audio(file_path)
            print(f"Raw AI Output: {raw_text}")
            
            # 4. Hindi ko Hinglish mein badalna.
            hinglish_text = convert_to_hinglish(raw_text)
            
            if hinglish_text:
                # 5. Final text ko save karna.
                save_text(hinglish_text, file_path)
                
                # 6. Screen par result dikhana.
                print(f"\n{'='*40}")
                print(f"FINAL HINGLISH: {hinglish_text}")
                print(f"{'='*40}")

