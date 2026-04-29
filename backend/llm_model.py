from groq import Groq
from web_script import web_search

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


def realtime_query(user_asked: str) -> str:  # ✅ user_asked added as parameter

    print("groq model web scraping started : \n")

    raw_data = web_search(user_asked)  # ✅ fetch web data first

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. You will receive raw scraped web data. Your job is to extract only the direct answer to the user's question from that data. Reply in one or two clean sentences like a human assistant would. Example: 'The current president of the USA is Donald Trump.' Do not mention sources, URLs, or Wikipedia. Just answer directly."},
            {"role": "user", "content": f"User asked: {user_asked}\n\nRaw web data:\n{raw_data}"}
        ]
    )

    groq_response = response.choices[0].message.content.strip()  # ✅ fixed typo choicesp -> choices
    print(groq_response)
    return groq_response
    


def system_query(command ): # system query 🛠️🛠️🛠️
    print("")
    pass




if __name__ == "__main__":
    

    with open("output.txt","r") as f:
        user_asked = f.read()
    # groq_model(user_asked)
    realtime_query("who is the president of america")