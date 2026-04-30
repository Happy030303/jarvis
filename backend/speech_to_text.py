import speech_recognition as sr
from text_sending_to_cohore_api import cohore_model_classify
import llm_model 
from text_to_speech import speak_text
def captureAudio_into_text():

    recogniser = sr.Recognizer()
    try:

        with sr.Microphone() as source:
            print("Chup raho (noise adjust ho raha hai)")
            recogniser.adjust_for_ambient_noise(source, duration=2)

            print("Ab bolo...")
            audio = recogniser.listen(source)

         # 🔹 AudioData → WAV file convert

        wav_data = audio.get_wav_data()

        # 🔹 File me write karna
        with open("output.wav", "wb") as f: # file making
            f.write(wav_data)

        print("Audio file saved as output.wav")


        # STT

        text = recogniser.recognize_google(audio, language="en-US")
        
        with open("output.txt", "w") as w:
            w.write(text)

            print("Captured!")


            
    except Exception as e : 
        print("error is : ",e)

   




if __name__ == "__main__":

    print(" program started : ")
    captureAudio_into_text()
    print("audio is converted into text : ")

    with open("output.txt", "r", encoding="utf-8") as f : 
        user_asked = f.read()

    print(f"\n\ntext is : {user_asked} \n\n")

    #---------------------------------------------------------------------
#module 2 : cohore api usage
    print("let's call cohore api to classify our promtp from text")
    
    response = cohore_model_classify(user_asked)

    print(f"we got response : {response}") # classify response : "GENERAL", "REALTIME", "SYSTEM"


#---------------------------------------------------------------------------
# module 3 : groq model   
   
    if response == "GENERAL":
        print("calling general query : \n\n ")
        groq_response = llm_model.groq_model(user_asked)
        print("\n\n\ngroq response is : ",groq_response)
        speak_text(groq_response)
        print("groq work is done .✅✅✅")
        
    elif response == "REALTIME":
        print("calling realtime query ")
        llm_model.realtime_query()
        print("real time query has responded ✅✅✅")

    elif response == "SYSTEM":
        print("system")
        llm_model.system_query(user_asked)
        print("system commdn is executed ✅✅✅")
        

