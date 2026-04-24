# 1. First, the necessary libraries are imported.
import speech_recognition as sr  # To handle microphone input
import logging                 # For logging messages
import os                      # To check for existing files

# 2. Setup logging to show messages in the terminal.
logging.basicConfig(level=logging.INFO, format='%(message)s')

def capture_audio():
    # 5. Inside capture_audio, we create a Recognizer object.
    recognizer = sr.Recognizer()
    
    # 6. Open the system's microphone as the microphone. and "with" will close it automatically
    with sr.Microphone() as microphone:
        print("\n--- Mic Testing ---")
        print("i am listening...") 
        
        try:
            # 7. Listen to silence for 0.5s to filter out background noise.
            recognizer.adjust_for_ambient_noise(microphone, duration=0.5)
            
            # 8. Actually record the user's voice (up to 10 seconds).
            audio = recognizer.listen(microphone, timeout=5, phrase_time_limit=10)
            
            print("Done listening!")
            # 9. Return the captured audio data back to the main block.
            return audio 
            
        except sr.WaitTimeoutError:
            print(f"Error: No speech detected (Timeout).")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def save_audio_to_file(audio_data, base_name="audio"):
    # 12. Check if we actually got audio data.
    if audio_data is None:
        return None

    # 13. Check the folder to see which filenames are already taken.
    counter = 1
    # 14. Loop through names (audio1.wav, audio2.wav...) until an available one is found.
    while os.path.exists(f"{base_name}{counter}.wav"):
        counter += 1
    
    # 15. Create the final filename (e.g., 'audio1.wav').
    file_name = f"{base_name}{counter}.wav"

    try:
        # 16. Open a new file and write the raw audio data into WAV format.
        with open(file_name, "wb") as f:
            f.write(audio_data.get_wav_data()) 
        
        print(f"Audio saved successfully as: {file_name}")
        # 17. Return the filename to the main block.
        return file_name 
    except Exception as e:
        print(f"Failed to save audio file: {e}")
        return None

# 3. Execution starts here because this script is run directly.
if __name__ == "__main__":
    # 4. Call capture_audio() to start the microphone.
    audio_captured = capture_audio()
    
    # 10. If audio was captured successfully, proceed to save it.
    if audio_captured:
        # 11. Call save_audio_to_file() with the captured audio.
        file_path = save_audio_to_file(audio_captured)
        
        # 18. Final confirmation message.
        if file_path:
            print(f"Process complete: File is ready at {file_path}")
    else:
        print("Process failed at Mic Capture.")
