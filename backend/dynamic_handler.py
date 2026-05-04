import os
from groq import Groq

client = Groq(api_key="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")

def youtube_handler(user_command: str)-> str:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a YouTube URL builder.

                Given the user's request, return ONLY a single YouTube URL. Nothing else. No explanation, no punctuation, no extra words.

                - If the user wants to open a creator's channel → return: https://www.youtube.com/@ChannelHandle
                - If the user wants to search something → return: https://www.youtube.com/results?search_query=query+words+here

                Rules:
                - Return the raw URL only.
                - No markdown, no brackets, no explanation.
                """
            },
            {
                "role": "user",
                "content": user_command
            }
        ]
    )

    url = response.choices[0].message.content.strip()
    print(f"🔗 Generated URL : {url}")
    
    return url

def google_handler(user_command: str)-> str:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a Google URL builder.

                Given the user's request, return ONLY a single Google URL. Nothing else. No explanation, no punctuation, no extra words.

                
                - If the user wants to search something on Google → return: https://www.google.com/search?q=query+words+here

                Rules:
                - Return the raw URL only.
                - No markdown, no brackets, no explanation.
                """
            },
            {
                "role": "user",
                "content": user_command
            }
        ]
    )

    url = response.choices[0].message.content.strip()
    print(f"🔗 Generated URL : {url}")
    
    return url
    


if __name__ == "__main__":
    while True:
        user_input = input("\n🎬 YouTube Command : ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        youtube_handler(user_input)