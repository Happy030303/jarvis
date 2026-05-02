from ddgs import DDGS
import requests
from groq import Groq

client = Groq(api_key="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")


# ──────────────────────────────────────────────
# ROUTER — Groq decide karega kaunsa source use ho
# ──────────────────────────────────────────────

def decide_source(user_asked: str) -> str:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a query classifier.
Decide if the user's question needs:
- "wikipedia"  → for history, definitions, static facts (things that never change)
- "web"        → for ANYTHING that involves current, latest, now, today, live data, current leaders, prices, scores, news, weather

IMPORTANT: If the question asks about who is CURRENTLY holding a position (president, prime minister, CEO etc.) always return "web" because this changes over time.

Return ONLY one word: wikipedia OR web
No explanation, no punctuation, nothing else."""
            },
            {
                "role": "user",
                "content": user_asked
            }
        ]
    )

    decision = response.choices[0].message.content.strip().lower()
    print(f"🧠 Router decision: {decision}")
    return decision


# ──────────────────────────────────────────────
# SOURCE 1 — Wikipedia API (static facts)
# ──────────────────────────────────────────────

def get_wikipedia_summary(query: str) -> str:

    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:  # wikipedia ne block kiya ya page nahi mila
        return ""

    data = response.json()
    return data.get("extract", "")  # clean summary return karo


# ──────────────────────────────────────────────
# SOURCE 2 — DuckDuckGo (live web data)
# ──────────────────────────────────────────────

def get_web_data(query: str) -> str:

    with DDGS() as search:
        results = list(search.text(query, max_results=3))  # top 3 results lo

    if not results:
        return ""

    combined = ""
    for result in results:
        combined += result['body'] + "\n"  # sirf summary text lo

    return combined


# ──────────────────────────────────────────────
# GROQ — Raw data ko clean answer mein convert karo
# ──────────────────────────────────────────────

def refine_with_groq(user_asked: str, raw_data: str) -> str:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful voice assistant like Jarvis.
Read the raw data and give a short, clean, natural answer in 2-3 sentences maximum.
Sound natural — like "The current president of the USA is Donald Trump, who took office on January 20, 2025."
Never mention Wikipedia, sources, or URLs.
Never give long explanations.
Just answer the question directly and clearly."""
            },
            {
                "role": "user",
                "content": f"User asked: {user_asked}\n\nRaw data:\n{raw_data}"
            }
        ]
    )

    return response.choices[0].message.content.strip()


# ──────────────────────────────────────────────
# MAIN — Sab kuch connect karo
# ──────────────────────────────────────────────

def realtime_query(user_asked: str) -> str:

    print(f"\n🔍 Query: {user_asked}")

    # Step 1 — decide karo kaunsa source chahiye
    source = decide_source(user_asked)

    # Step 2 — sahi source se raw data lo
    if source == "wikipedia":
        print("📖 Using Wikipedia API")
        raw_data = get_wikipedia_summary(user_asked)

        # agar wikipedia ne kuch nahi diya toh "web" pe fallback karo
        if not raw_data:
            print("⚠️ Wikipedia failed — falling back to web search")
            raw_data = get_web_data(user_asked)
    else:
        print("🌐 Using Web Search")
        raw_data = get_web_data(user_asked)

    # Step 3 — Groq se refine karo
    answer = refine_with_groq(user_asked, raw_data)

    print(f"🤖 Jarvis: {answer}\n")
    return answer


# ──────────────────────────────────────────────
# TEST
# ──────────────────────────────────────────────

# if __name__ == "__main__":
#     realtime_query("what is photosynthesis")       # web
#     realtime_query("who is the prime minister of India") # web
#     realtime_query("what is quantum physics")            # wikipedia
#     realtime_query("latest IPL 2025 score")              # web
#     realtime_query("who is Elon Musk")                   # wikipedia