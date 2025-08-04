import requests
from bs4 import BeautifulSoup
import pyttsx3
import time

# 🔍 Function to scrape news from The Hacker News
def scrape_hacker_news_articles():
    url = "https://thehackernews.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.find_all("div", class_="body-post")[:5]  # Grab top 5 articles
    results = []

    for article in articles:
        title = article.find("h2", class_="home-title").text.strip()
        link = article.find("a")["href"]
        summary = article.find("div", class_="home-desc").text.strip()
        results.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return results

# 🔊 Function to speak the news out loud
def speak_news(article):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)

    # Optional: pick a female voice
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
    print("🔐 Fetching Cybersecurity News...\n")
    news = scrape_hacker_news_articles()

    for article in news:
        print(f"📰 Title: {article['title']}")
        print(f"📝 Summary: {article['summary']}")
        print(f"🔗 Link: {article['link']}\n")
        speak_news(article)
        time.sleep(1)  # Pause between articles
