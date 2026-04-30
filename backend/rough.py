from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/Donald_Trump"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, timeout=5)
soup = BeautifulSoup(response.text, "html.parser")

# Grab only title and paragraphs directly
title = soup.find("title").get_text()
paragraphs = soup.find_all("p")

print(f"Title: {title}\n")

count = 0

for p in paragraphs:
    text = p.get_text().strip()
    if text:
        print(text)
        count += 1
        if count == 2:  # stop after 20 lines
            break

