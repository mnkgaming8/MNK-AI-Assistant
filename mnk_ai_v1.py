import os
import pyttsx3
import speech_recognition as sr
import pyautogui
import requests
import json
import time
from googletrans import Translator

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # Speed

# Initialize Translator
translator = Translator()

# DeepSeek API Key
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"  # <-- Put your key here

# Function to speak
def speak(text):
    print("MNK:", text)
    engine.say(text)
    engine.runAndWait()

# Function to listen from mic
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("User:", query)
    except Exception as e:
        speak("I didn't understand. Please repeat.")
        return ""
    return query

# Call DeepSeek R1 API
def ask_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"  # <-- Put your key url here
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",  # or r1 model if you have
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content']
    return answer

# Translate text to any language
def translate_text(text, target_lang):
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Execute system commands (expand later)
def execute_command(command):
    if "open notepad" in command.lower():
        speak("Opening Notepad.")
        os.system("notepad")
    elif "shutdown" in command.lower():
        speak("Shutting down.")
        os.system("shutdown /s /t 1")
    elif "screenshot" in command.lower():
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot taken.")
    else:
        speak("Command not found!")

# Main loop
def main():
    speak("Hello, I am MNK, your AI assistant.")
    while True:
        query = listen()

        if query == "":
            continue

        if "exit" in query.lower() or "stop" in query.lower():
            speak("Goodbye!")
            break

        # Simple system commands
        if any(cmd in query.lower() for cmd in ["open", "shutdown", "screenshot"]):
            execute_command(query)
            continue

        # Handle languages (Example: Translate into Urdu)
        if "translate" in query.lower():
            speak("Please say the text you want to translate.")
            text_to_translate = listen()
            translated = translate_text(text_to_translate, 'ur')  # Urdu example
            speak(f"The translation is: {translated}")
            continue

        # Ask DeepSeek for answer
        answer = ask_deepseek(query)
        speak(answer)

if __name__ == "__main__":
    main()
