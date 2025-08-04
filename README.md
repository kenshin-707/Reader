# Reader: Voice-Based News Assistant 

> Your personalized AI voice assistant for news – just say it, hear it, and stay informed.

---

## One-Line Problem Statement
People often struggle to find **relevant** and **easy-to-understand** news — this assistant delivers **only what they ask for**, in **summarized form**, and **reads it out loud**.

---

## Expected Outcome
A voice-interactive assistant that fetches **real-time news**, summarizes it, and delivers it **through speech**, based on **user commands**.

---

## Who Are the Users?

- Students and researchers 
- Journalists & analysts needing quick insights  
- Non-tech folks   
- Anyone who says: "I want news, but no clutter."

---

## What Problem Does It Solve?

- Cuts through overwhelming and jargon-heavy news  
- Saves time by summarizing key points  
- Speaks the info aloud — great for multitasking or accessibility  
- Lets users **ask exactly what they want** (e.g., "ransomware updates")  

---

## How’s It Different?

✅ Summarized + Category-Specific Cyber News  
✅ Hands-free Voice Interface  
✅ Easy-to-use GUI   
✅ Future-ready for personalization (cloned voices, offline mode)

---

## 🛠Features (Demo Scope)

-  Speech recognition for user commands  
-  News scraping from trusted sources  
-  AI-powered summarization (T5 or BART)  
-  Text-to-Speech output (gTTS / pyttsx3 / cloned voice)  
-  Simple GUI with voice button and keyword input  
-  MongoDB integration for storing news & user preferences

---

##  Tech Stack

| Layer       | Tools/Frameworks                     |
|------------|---------------------------------------|
| Frontend   | HTML, CSS, JS, Tailwind (optional UI theme) |
| Backend    | Python, Flask / FastAPI               |
| AI/ML      | Hugging Face Transformers, TTS Engines |
| Database   | MongoDB (Atlas / Local)               |
| Voice I/O  | SpeechRecognition, gTTS, pyttsx3       |
| Deployment | Render / Heroku (Backend), Vercel / GitHub Pages (Frontend) |

---

## Folder Structure

```bash
cybersentinel/
├── backend/
│   ├── app.py
│   ├── summarizer.py
│   └── scraper.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── main.js
├── database/
│   └── models.py
├── voice/
│   ├── speech_to_text.py
│   └── text_to_speech.py
└── README.md
