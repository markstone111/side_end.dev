# 📚 Intent-Based ChatBot

This is an **Intent-Based ChatBot** built with **Python**, **NLTK**, **scikit-learn**, **SpeechRecognition**, **SoundDevice**, and **Streamlit** for an interactive web interface.  
It supports both **text input** and **voice input**, and it responds with text and **text-to-speech audio output**.  
All conversations are logged in a CSV file for history and reference.

---

## 🚀 Features

- ✅ **Intent Classification:** Uses TF-IDF vectorization and Logistic Regression to classify user inputs into predefined intents.
- ✅ **Voice Input:** Record voice input using your microphone with `sounddevice` and `speech_recognition`.
- ✅ **Text-to-Speech (TTS):** The chatbot responds with speech using `pyttsx3` (offline TTS) and `gTTS` for in-browser playback.
- ✅ **Chat History:** All interactions are saved to a `chat_log.csv` file, viewable in the **History** tab.
- ✅ **Streamlit Interface:** Clean UI with tabs for **Home**, **History**, and **About**.

---

## 🗂️ Project Structure

📂 Project Root

├── chatBot.py # Main chatbot app

├── intents.json # Intent patterns & responses

├── chat_log.csv # Chat history log (auto-created)

├── response.mp3 # Temporary audio file for TTS

└── other files...

---

## ⚙️ Requirements

- Python 3.x
- `nltk`
- `scikit-learn`
- `streamlit`
- `sounddevice`
- `SpeechRecognition`
- `pyttsx3`
- `gtts`
- `numpy`

---

## 📌 Important: Audio Limitations on Streamlit Cloud

⚠️ **Note:** This chatbot uses **local audio input and output** (`sounddevice`, `speech_recognition`, `pyttsx3`), which **requires microphone and speaker hardware**.  
**Streamlit Cloud does not support this**, as remote servers do not have audio hardware or PortAudio installed.

✅ **To use voice features, run this app locally on your own machine.**

---

## 💻 How to Run Locally

**1️⃣ Clone this repository**
```bash
git clone https://github.com/markstone111/side_end.dev.git
cd ChatBot(Intent-Based)
```

**2️⃣ Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
# Activate the virtual environment:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

**4️⃣ Run the chatbot**
```bash
streamlit run chatBot.py
```





🗣️ How to Use
Home Tab:
Choose Type to chat by typing, or Speak to record audio input (local only).

History Tab:
View your entire conversation log with timestamps.

About Tab:
Learn about the project, features, and planned enhancements.



👋 Author
Built with ❤️ by Nikunj Maheshwari — side_end.dev
- https://nikunjmaheshwari.vercel.app
