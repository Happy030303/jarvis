You can save this in your project documentation as your **Architectural Guidelines**.

---

**Q1: The Prompting Trap (Chunking)** How will you frame your prompt to the LLM to ensure it only writes the code for Module 1 (Audio Input) and doesn't try to write the entire Jarvis system at once?

**A1:** I will explicitly tell the LLM: "Now I am just making this chunk of my whole project that is my step 1, to take voice as input from the mic and convert it into text. Let us make this logic inside the function `convertVoiceIntoText()`." This enforces the Single Responsibility Principle and keeps the LLM focused on one specific task.

---

**Q2: Multi-Intent Routing (The Cohere Challenge)** If a user gives two commands at once (e.g., "Mute PC and tell me the weather"), how will your system handle it?

**A2:** We will handle this using Python's `asyncio` (Asynchronous I/O). First, the Cohere prompt must be instructed to return a list of multiple intents if necessary (e.g., `['System_Action', 'Web_Search']`). Then, the Python script will loop through this list and trigger the required functions asynchronously so they run efficiently without blocking each other.

---

**Q3: The Infinite Loop (Microphone Logic)** How do you prevent the microphone from listening to Jarvis's own TTS output (`edge-tts`) and feeding it back into the system in an infinite loop?

**A3:** We will implement a "State Flag" logic. We will create a boolean variable in the code (e.g., `is_jarvis_speaking = False`). When `edge-tts` starts speaking, this flag changes to `True`. The microphone module will be programmed to ignore all audio (deaf mode) while this flag is `True`. Once Jarvis finishes speaking, it resets to `False` and listens again.

---

**Q4: Scraping Resilience (HTML Changes)** If a website changes its HTML tags, your `BeautifulSoup` scraper will crash. How do we prevent this architectural risk?

**A4:** We will adopt an "API-First" approach. Instead of scraping HTML, we will use free APIs (like OpenWeather or financial APIs) that provide structured JSON data. If an API is unavailable and scraping is the only option, we will wrap the scraper in robust `try/except` blocks. If the HTML tags change, Jarvis will catch the error and gracefully say, "Sir, the data source format has changed," instead of crashing.

---

**Q5: Security Protocol (The Vault Leak)** Before pushing your code to a GitHub repository, what must you do to ensure your API keys aren't stolen?

**A5:** I will add the `.env` file (and any other credential files like `api.txt`) to the `.gitignore` file immediately. This ensures that sensitive API keys are kept strictly local and are never uploaded or leaked to the internet.

---

**Q6: The "Done" Criteria (Validation)** What is the specific testing strategy to prove that Module 1 (`convertVoiceIntoText`) is successfully built and ready?

**A6:** Module 1 is only considered "Done" when it passes these three physical tests:

1. It accurately transcribes normal speech to text on the screen within 3 seconds.
2. It successfully filters out ambient background noise (like a TV in the other room) and captures the user's voice.
3. It automatically detects silence when the user stops speaking and ends the recording block without freezing the Python script.

---

This document is your shield against bad code
