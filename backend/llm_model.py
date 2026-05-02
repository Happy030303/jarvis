from groq import Groq
import realtime
from system_script import system_command 

# 🔹 Client ek hi baar banao
client = Groq(api_key="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")

def groq_model(user_asked: str) -> str:                        #  ✅✅✅
    print("we will use groq model here")
    print(f"user_asked is: {user_asked}")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant and you have tell things not too much, not too low, just medium size explanation."},
            {"role": "user", "content": user_asked}
                    ]
                                )

    groq_response = response.choices[0].message.content.strip()
    return groq_response

# -----------------------------------------------------------------------------------------

#real time query : 

def realtime_query(user_asked: str) -> str:  # ✅ user_asked added as parameter
    print("\n\n\ncalling realtime query : \n\n")
    realtime.realtime_query(user_asked)
    

# -----------------------------------------------------------------------------------
def system_query(command ): # system query 🛠️🛠️🛠️
    print("SYSTEM CMS Is : ", command)
    system_command(command)

    




# if __name__ == "__main__":
        # we made to test this file

#     system_query("open youtube")