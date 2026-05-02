from gtts import gTTS
import os

def speak_text(text: str):
    tts = gTTS(text=text, lang='en')  # we are using Google text to speech 
    tts.save("output.mp3")            # gTTS sends object which has save() to save audio file save

    os.system("start output.mp3")     # Windows ke liye (auto play)



# if __name__ == "__main__":
#     speak_text("Hi my name is happy singh")