import os
from groq import Groq

client = Groq(api_key="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")
ALLOWED_COMMANDS = {
    "open youtube"      : "start https://www.youtube.com",
    "open whatsapp"     : "start https://web.whatsapp.com",
    "open telegram"     : "start https://web.telegram.org",
    "open chrome"       : "start chrome.exe",
    "open brave"        : "start brave.exe",
    "open notepad"      : "start notepad.exe",
    "open calculator"   : "start calc.exe",
    "open spotify"      : "start https://www.spotify.com",
    "open instagram"    : "start https://www.instagram.com",
    "open github"       : "start https://www.github.com",
    "open vs code"      : "start code.exe",

    # close commands
    "close chrome"      : "taskkill /f /im chrome.exe",
    "close brave"       : "taskkill /f /im brave.exe",
    "close notepad"     : "taskkill /f /im notepad.exe",
    "close calculator"  : "taskkill /f /im calculator.exe",
    "close spotify"     : "taskkill /f /im spotify.exe",
    "close vs code"     : "taskkill /f /im code.exe",
    "close telegram"    : "taskkill /f /im telegram.exe",
    "close whatsapp"    : "taskkill /f /im whatsapp.exe",
}


def system_command(user_commmand: str) -> str:  # system query 🛠️🛠️🛠️

    print(f"🖥️ System user_commmand received: {user_commmand}")

    # Groq ko allowed commands ki list bhejo
    allowed_keys = "\n".join(ALLOWED_COMMANDS.keys())

    # Groq sirf key return karega — koi user_commmand generate nahi karega
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"""You are a user_commmand classifier.
        Your only job is to match the user's request to one of these exact keys:

        {allowed_keys}

        Rules:
        - Return ONLY the matching key, nothing else.
        - No explanation, no punctuation, no extra words.
        - If nothing matches, return exactly: unknown
        """},
            {"role": "user", "content": user_commmand}
        ]
    )

    # Groq ka response lo
    matched_key = response.choices[0].message.content.strip().lower()
    print(f"🔑 Matched key: {matched_key}")

    # Dictionary mein dhundho
    if matched_key in ALLOWED_COMMANDS:
        os_command = ALLOWED_COMMANDS[matched_key]  # actual windows user_commmand
        print(f"✅ Executing: {os_command}")
        os.system(os_command)  # windows ko user_commmand do
        return f"Done: {matched_key}"
    
    else:
        print("❌ Command not recognized.")
        return "Sorry, I cannot perform that system user_commmand."


# if __name__ == "__main__":
#     system_query("open spotif")