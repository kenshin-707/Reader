from flask import Flask, request, jsonify, send_file
import asyncio
import scraper
from gtts import gTTS

app = Flask(__name__)
last_news_text = ""  # store last scraped text for audio

@app.route("/scrape")
def scrape_api():
    global last_news_text
    site = request.args.get("site", "thehackernews")
    results = asyncio.run(scraper.scrape(site))
    
    # Save news for audio output
    last_news_text = " ".join([item["title"] for item in results])
    
    return jsonify({"site": site, "news": results})

@app.route("/audio")
def audio_api():
    global last_news_text
    if not last_news_text:
        return "No news scraped yet.", 400
    
    tts = gTTS(text=last_news_text, lang="en")
    tts.save("news.mp3")
    return send_file("news.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
