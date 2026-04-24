# 1. Necessary libraries import kar rahe hain.
from faster_whisper import WhisperModel  # AI model for speech-to-text
import speech_recognition as sr           # Mic handling ke liye
import logging                            # Logging updates
import os                                 # File path management

# 2. Setup logging to keep terminal output clean.
logging.basicConfig(level=logging.INFO, format='%(message)s')

def capture_audio():
    # 5. Recognizer object banaya jo sound process karega.
    recognizer = sr.Recognizer()
    
    # 6. Mic ko source ki tarah open kiya.
    with sr.Microphone() as source:
        print("\n--- Mic Testing ---")
        print("i am listening...")
        
        try:
            # 7. Background noise adjust karna (0.5 sec).
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # 8. Mic se awaaz sunna (max 10 sec recording).
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Done listening!")
            # 9. Raw audio data return karna.
            return audio
            
        except sr.WaitTimeoutError:
            print("Error: No speech detected (Timeout).")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def save_audio_to_file(audio_data, base_name="audio"):
    # 12. Check karna ki audio data hai ya nahi.
    if audio_data is None:
        return None

    # 13. Available filename dhundna (audio1, audio2...).
    counter = 1
    while os.path.exists(f"{base_name}{counter}.wav"):
        counter += 1
    
    file_name = f"{base_name}{counter}.wav"

    try:
        # 14. File mein WAV data write karna.
        with open(file_name, "wb") as f:
            f.write(audio_data.get_wav_data())
        
        print(f"Audio saved successfully as: {file_name}")
        # 15. File path return karna.
        return file_name
    except Exception as e:
        print(f"Failed to save audio file: {e}")
        return None

def transcribe_audio(file_path):
    # 18. Check karna ki file exist karti hai.
    if not os.path.exists(file_path):
        return None

    print(f"Converting audio to text...")
    
    try:
        # 19. Whisper model load karna (Tiny version is fast).
        model = WhisperModel("tiny", device="cpu", compute_type="int8")

        # 20. Audio file ko text mein convert karna (Forcing English 'en').
        # Agar aap Hindi bolna chahte hain toh 'hi' bhi kar sakte hain.
        segments, info = model.transcribe(file_path, beam_size=5, language="en")

        print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

        # 21. Saare sentence segments ko ek string mein jodna.
        text_result = ""
        for segment in segments:
            text_result += segment.text + " "
        
        text_result = text_result.strip()

        if text_result:
            # 22. Text ko 'stored_text' folder mein save karna.
            folder_name = "stored_text"
            os.makedirs(folder_name, exist_ok=True)
            text_file_name = os.path.join(folder_name, os.path.basename(file_path).replace(".wav", ".txt"))
            with open(text_file_name, "w") as f:
                f.write(text_result)
            print(f"Success: Text stored in {text_file_name}")

        # Note: Audio file deletion removed as requested.
        print(f"File Kept: You can listen to {file_path} for quality check.")

        return text_result
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

# 3. Main execution yahan se start hoti hai.
if __name__ == "__main__":
    # 4. Step 1: Voice capture karo.
    audio_captured = capture_audio()
    
    # 10. Agar awaaz mil gayi:
    if audio_captured:
        # 11. Step 2: Audio ko save karo.
        file_path = save_audio_to_file(audio_captured)
        
        # 16. Agar file save ho gayi:
        if file_path:
            # 17. Step 3: Audio ko text mein badlo.
            text = transcribe_audio(file_path)
            
            # 23. Final Result dikhao.
            if text:
                print(f"\n--- Result ---")
                print(f"You said: {text}")
            else:
                print("Failed to convert audio to text.")
    else:
        print("Process failed at Mic Capture.")
