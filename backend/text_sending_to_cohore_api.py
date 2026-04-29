import cohere

co = cohere.ClientV2("liRjqw2XFpUVkNfRUBAaTC2C74BlJTrDcK0MZ7Yt")

def cohore_model_classify(user_text:str) -> str:
    prompt = f""" 
    You are an intent classifier.

    Classify the user input into ONLY one of these categories:
    - GENERAL
    - REALTIME
    - SYSTEM

    Rules:
    - GENERAL: knowledge, facts, coding, conversation, whatever you have information without going to internet to search 
    - REALTIME: live data (weather, stock, news) from internet
    - SYSTEM: commands to control device or system

    Output ONLY one word: GENERAL or REALTIME or SYSTEM.

    User input: {user_text} """
    
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.message.content[0].text.strip().upper()

    if output not in ["GENERAL", "REALTIME", "SYSTEM"]:
        return "GENERAL" 
    
    print(f"response is : {output}")

    return output












