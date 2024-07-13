import os
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv

# Set up OpenAI API key from system environment variable
# openai.api_key = os.getenv('OPENAI_API_KEY')
load_dotenv()

client = OpenAI()

# Initialize the recognizer
recognizer = sr.Recognizer()

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None

def get_response(command):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": command},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "I'm sorry, I encountered an error."

def speak_response(response):
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # Use `afplay` to play the mp3 file on macOS

if __name__ == "__main__":
    print("OpenAI API key loaded successfully")
    command = listen_command()
    if command:
        response = get_response(command)
        print(response)
        speak_response(response)
