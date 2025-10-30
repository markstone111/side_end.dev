import os
import json
import datetime
import csv
import time
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
# import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import threading
import queue
import base64  #for encoding audio files as base64 strings

#initialize Text-to-Speech Engine
tts_engine = pyttsx3.init()

#create a Queue for TTS tasks
tts_queue = queue.Queue()

def speak_worker():
    """Worker thread to process text-to-speech tasks."""
    while True:
        text = tts_queue.get()
        if text is None:  # Exit signal
            break
        tts_engine.say(text)
        tts_engine.runAndWait()
        tts_queue.task_done()

#start the TTS worker thread
threading.Thread(target=speak_worker, daemon=True).start()

def speak(text):
    """Convert text to speech using gTTS and autoplay it in the browser."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        audio_file = open("response.mp3", "rb")
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        st.components.v1.html(audio_html, height=0)

        #reemove the temporary file
        time.sleep(1)
    
    #     os.remove("response.mp3")
    # except Exception as e:
    #     st.write(f"Error during text-to-speech: {e}")
        try:
            os.remove("response.mp3")
        except PermissionError:
            #file is in uuse; skip deletion
            pass
    except Exception as e:
        st.write(f"Error during text-to-speech: {e}")
        

def recognize_speech_with_sounddevice():
    """Capture audio using sounddevice and recognize it."""
    duration = 5  # seconds
    samplerate = 16000
    st.write("Listening... Speak now!")

    try:
        # record audio
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()  # wait for recording to finish
        audio_data = (audio_data * 32767).astype(np.int16)  # convert to int16 for speech_recognition
        
        recognizer = sr.Recognizer()
        audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)
        user_input = recognizer.recognize_google(audio)
        st.write(f"**You said:** {user_input}")
        return user_input
    except Exception as e:
        st.write(f"Error recognizing speech: {e}")
        return None

#SSL setup for downloading NLTK data
ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

#load intents file
file_path = os.path.abspath("./intents.json")
with open(file_path, "r", encoding="utf-8") as file:
    intents = json.load(file)

#inittialize vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

#preprocess data for training
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

#train the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

#func to generate chatbot responses
def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I'm sorry, I don't understand that."

#Streamlit App
CHAT_LOG_FILE = "chat_log.csv"

def save_chat_log(user_input, bot_response):
    """Save the chat log to a CSV file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_LOG_FILE, "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([user_input, bot_response, timestamp])

def main():
    st.set_page_config(page_title="Intents-based Chatbot", layout="wide")
    st.title("Intents-based Chatbot")

    #Sidebar menu
    menu = ["Home", "History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Chat with the Bot")

        # Ensure tht chat log file exists
        if not os.path.exists(CHAT_LOG_FILE):
            with open(CHAT_LOG_FILE, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["User", "Bot", "Time"])

        #Select Input Method
        input_method = st.radio("Choose your input method:", ("Type", "Speak"))

        if input_method == "Type":
            user_input = st.text_input("You: ", placeholder="Type your message here...")
        elif input_method == "Speak":
            if st.button("Click to Speak"):
                user_input = recognize_speech_with_sounddevice()
            else:
                user_input = None

        if user_input:
            bot_response = chatbot(user_input)
            st.write(f"**ChatBot:** {bot_response}")
            save_chat_log(user_input, bot_response)

            #Speak the bot's response
            speak(bot_response)

            #exit conditiom
            if bot_response.lower() in ['goodbye', 'bye', 'exit', 'quit']:
                st.write("ChatBot: Goodbye! Have a great day!")
                speak("Goodbye! Have a great day!")
                st.stop()

    elif choice == "History":
        st.subheader("Chat History")

        if os.path.exists(CHAT_LOG_FILE):
            with open(CHAT_LOG_FILE, "r", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  #skiping the header row
                for row in csv_reader:
                    st.markdown(f"**User:** {row[0]}  ")
                    st.markdown(f"**Bot:** {row[1]}  ")
                    st.caption(f"**Time:** {row[2]}")
                    st.markdown("---")
        else:
            st.write("No chat history available.")

    elif choice == "About":
        st.subheader("About the Chatbot")
        st.write("This chatbot is designed to understand and respond to user intents using machine learning.")
        st.markdown("### Features:")
        st.write("- Trained on predefined patterns and responses.")
        st.write("- Provides responses based on classified intents.")
        st.write("- Logs chat history for reference.")

        st.markdown("### Future Enhancements:")
        st.write("- **Expand Dataset:** Include more intents and responses.")
        st.write("- **Advanced NLP Models:** Utilize models like BERT or GPT for improved understanding.")
        st.write("- **Multi-language Support:** Interact in multiple languages.")
        st.write("- **Sentiment Analysis:** Make responses emotionally aware.")
        st.write("- **Voice Integration:** Enable voice-based interaction.")
        st.write("- **Personalization:** Provide tailored responses based on user preferences.")
        st.write("- **Continuous Learning:** Improve through user feedback.")

        st.markdown("### GitHub Repository:")
        st.write("[Chatbot Repository](https://github.com/markstone111)")

if __name__ == "__main__":
    main()

