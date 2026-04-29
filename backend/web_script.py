from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from llm_model import realtime_query


def scrape_page(url: str) -> str:
    """Goes inside a URL and pulls clean readable text."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
        return "\n".join(lines[:80])

    except Exception as e:
        return f"Could not scrape: {e}"


def web_search(query: str) -> str:

    print(f"🔍 Searching: {query}")

    with DDGS() as search:
        results = list(search.text(query, max_results=3))

    if not results:
        return "No results found on internet."

    all_content = ""

    for i, result in enumerate(results, 1):
        print(f"📌 Scraping result {i}: {result['title']}")
        page_text = scrape_page(result['href'])

        all_content += f"\n\nSource {i}: {result['title']}\n"
        all_content += f"URL: {result['href']}\n"
        all_content += f"{page_text}\n"
        all_content += "=" * 40

    return all_content


def realtime_query(user_asked: str) -> str:

    result = web_search(user_asked)
    # print(result)
    return result


if __name__ == "__main__":
    user_asked = "who is the president of USA"
    result = realtime_query(user_asked)

    response = realtime_query(user_asked)
    print("the answer is : ",response)



