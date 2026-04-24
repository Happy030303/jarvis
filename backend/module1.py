from faster_whisper import WhisperModel
import speech_recognition as sr
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def capture_audio():
    """Captures audio from microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n--- Listening ---")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return audio
        except Exception as e:
            print(f"Capture Error: {e}")
            return None

def save_audio_to_file(audio_data, base_name="temp_audio"):
    """Saves raw audio to a temporary WAV file."""
    if audio_data is None: return None
    
    counter = 1
    while os.path.exists(f"{base_name}{counter}.wav"):
        counter += 1
    
    file_name = f"{base_name}{counter}.wav"
    try:
        with open(file_name, "wb") as f:
            f.write(audio_data.get_wav_data())
        return file_name
    except Exception as e:
        print(f"Save Error: {e}")
        return None

def transcribe_and_clean(file_path):
    """Converts audio to text, saves it to 'stored_text', and deletes the audio file."""
    if not os.path.exists(file_path): return None

    try:
        # Load Whisper model (Tiny version)
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        
        # Transcription
        segments, _ = model.transcribe(file_path, beam_size=5)
        text_result = " ".join([segment.text for segment in segments]).strip()
        
        if text_result:
            # Create stored_text directory if it doesn't exist
            folder_name = "stored_text"
            os.makedirs(folder_name, exist_ok=True)
            
            # Save the text to a .txt file
            text_file_name = os.path.join(folder_name, os.path.basename(file_path).replace(".wav", ".txt"))
            with open(text_file_name, "w") as f:
                f.write(text_result)
            print(f"Success: Text stored in {text_file_name}")
        
        # Delete the audio file after work is done
        os.remove(file_path)
        print(f"Cleanup: Deleted temporary audio file {file_path}")
        
        return text_result
    except Exception as e:
        print(f"Processing Error: {e}")
        return None

if __name__ == "__main__":
    # Step 1: Capture
    audio = capture_audio()
    
    if audio:
        # Step 2: Save temporary file
        temp_file = save_audio_to_file(audio)
        
        if temp_file:
            # Step 3: Transcribe, Save Text, and Cleanup Audio
            final_text = transcribe_and_clean(temp_file)
            
            if final_text:
                print(f"\nFinal Speech-to-Text: {final_text}")
            else:
                print("Failed to transcribe audio.")
    else:
        print("Mic Capture failed.")
