import speech_recognition as sr
from urllib.parse import urlparse

def get_voice_input() -> tuple[str, str]:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Speak the website name (e.g., 'The Hacker News' or 'Cybersecurity News')...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"✅ You said: {text}")

        # Map spoken names to known URLs
        site_map = {
            "the hacker news": "https://thehackernews.com/",
            "cybersecurity news": "https://cybersecuritynews.com/"
        }

        # Try exact match first
        if text in site_map:
            url = site_map[text]
            name = urlparse(url).netloc
            return name, url
        else:
            # ✅ NEW: fuzzy keyword match
            for key, site_url in site_map.items():
                if key in text or any(word in text for word in key.split()):
                    url = site_url
                    name = urlparse(url).netloc
                    print(f"🔎 Matched '{text}' to '{key}'")
                    return name, url

            # fallback: assume user spoke a domain or URL
            if not text.startswith(("http://", "https://")):
                text = "https://" + text.replace(" ", "")
            name = urlparse(text).netloc
            return name, text


    except sr.UnknownValueError:
        print("❌ Could not understand your speech.")
    except sr.RequestError as e:
        print(f"❌ Error with Google Speech API: {e}")

    return None, None

