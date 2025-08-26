import requests
import pyttsx3
import time

# 🔍 Function to fetch news from Flask backend
def fetch_news_from_backend(site="thehackernews", keyword=""):
    url = "http://localhost:5000/api/scrape"
    params = {"site": site, "keyword": keyword}
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    return data.get("articles", [])

# 🔊 Function to speak the news out loud
def speak_news(article):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    text_to_speak = f"Zero Two here with a spicy news drop! {article['title']}. {article['summary']}"
    engine.say(text_to_speak)
    engine.runAndWait()

# 🚀 Run the assistant
if __name__ == "__main__":
    print("🔐 Fetching Cybersecurity News from backend...\n")
    news = fetch_news_from_backend()
    for article in news:
        print(f"📰 Title: {article['title']}")
        print(f"📝 Summary: {article['summary']}")
        print(f"🔗 Link: {article['link']}\n")
        speak_news(article)
        time.sleep(1)  # Pause between articles
