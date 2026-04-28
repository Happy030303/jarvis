# 1. Python starts by loading all the necessary tools (Libraries).
from faster_whisper import WhisperModel
import speech_recognition as sr
import logging
import os
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# 2. Setup logging to keep terminal output clean.
logging.basicConfig(level=logging.WARNING, format='%(message)s')

# 3. Print the first startup message.
print("Whisper model load ho raha hai... (sirf ek baar)")

# 4. Load the AI model into RAM globally. This happens immediately during script load.
WHISPER_MODEL = WhisperModel("base", device="cpu", compute_type="int8")

# 5. Confirm the model is ready.
print("Model ready hai!\n")

# NOTE: Functions below are just "defined" here. Python remembers them but 
# DOES NOT run their code until they are called in Step 8, 15, 21, etc.

def has_devanagari(text):
    # 31. Inside the loop, it checks if a word has Hindi characters.
    return bool(re.search(r'[\u0900-\u097F]', text))

def capture_audio(mic_index=None):
    # 9. Inside capture_audio, the Recognizer (Brain) is created.
    recognizer = sr.Recognizer()
    try:
        # 10. Open the system's default microphone.
        with sr.Microphone(device_index=mic_index) as source:
            print(f"--- Sun raha hoon... (Default Mic) ---")
            # 11. Listen to silence for 0.5s to filter background noise.
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # 12. Actually record the user's voice.
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Awaaz capture ho gayi!")
            # 13. Return the captured audio data back to the main block.
            return audio
    except Exception as e:
        print(f"Mic error: {e}")
        return None

def save_audio_to_file(audio_data, base_name="audio"):
    # 16. Check if we actually got audio data.
    if audio_data is None: return None

    # [FIX] Folder name set to 'audio'. 
    # Python script jis folder mein hai (backend/), usi ke andar ye folder banega.
    folder_name = "audio"
    os.makedirs(folder_name, exist_ok=True)

    # 17. Find an available filename (audio1, audio2...).
    counter = 1
    while os.path.exists(os.path.join(folder_name, f"{base_name}{counter}.wav")):
        counter += 1
    file_name = os.path.join(folder_name, f"{base_name}{counter}.wav")

    try:
        # 18. Save the raw data into a physical .wav file.
        with open(file_name, "wb") as f:
            f.write(audio_data.get_wav_data())
        print(f"Audio file save hui: {os.path.abspath(file_name)}")
        # 19. Return the path of the saved file to the main block.
        return file_name
    except Exception as e:
        print(f"File save error: {e}")
        return None

def transcribe_audio(file_path):
    # 22. Verify the file exists before transcribing.
    if not os.path.exists(file_path): return None

    print("Whisper audio sun raha hai...")
    try:
        # 23. AI turns audio bytes into text.
        segments, info = WHISPER_MODEL.transcribe(file_path, beam_size=5, task="transcribe")
        # 24. Join sentence segments into one raw text.
        raw_text = " ".join(segment.text for segment in segments).strip()
        # 25. Return the raw text back to main block.
        return raw_text
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def convert_to_hinglish(raw_text):
    # 27. Safety check for empty text.
    if not raw_text: return None

    # 28. Split the sentence into individual words.
    words = raw_text.split()
    result_words = []

    # 29. Loop through each word.
    for word in words:
        # 30. Check if the word is Hindi (This jumps to step 31 defined above).
        if has_devanagari(word):
            # 32. If Hindi, transliterate it to Roman script (English alphabet).
            roman_word = transliterate(word, sanscript.DEVANAGARI, sanscript.ITRANS)
            result_words.append(roman_word)
        else:
            # 33. If already English, keep it as-is.
            result_words.append(word)

    # 34. Join everything back into a Hinglish sentence.
    return " ".join(result_words)

def save_text(text, audio_file_path):
    # [FIX] Folder name set to 'stored_text'.
    folder_name = "stored_text"
    os.makedirs(folder_name, exist_ok=True)
    # 36. Match text filename with audio filename.
    base_name = os.path.basename(audio_file_path).replace(".wav", ".txt")
    text_file_path = os.path.join(folder_name, base_name)
    try:
        # 37. Save the final result permanently.
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text save hua: {os.path.abspath(text_file_path)}")
    except Exception as e:
        print(f"Text save error: {e}")

# 6. Global execution reaches here. This is where the script officially "starts" running.
if __name__ == "__main__":
    # 7. Print the action message.
    print("Action shuru!\n")

    # 8. STEP 1: Call capture_audio() to start the microphone.
    audio_data = capture_audio()
    
    # 14. After returning from Step 13, check if we have data.
    if audio_data:
        # 15. STEP 2: Call save_audio_to_file() with the captured audio.
        audio_file = save_audio_to_file(audio_data)

        # 20. After returning from Step 19, check if file is ready.
        if audio_file:
            # 21. STEP 3: Call transcribe_audio() to let AI hear the file.
            raw_text = transcribe_audio(audio_file)
            
            # 26. After returning from Step 25, call the Hinglish converter.
            final_text = convert_to_hinglish(raw_text)

            # 35. STEP 5: If conversion worked, save the text file.
            if final_text:
                save_text(final_text, audio_file)
                # 38. Final result displayed to the user.
                print(f"\nFINAL HINGLISH: {final_text}")
