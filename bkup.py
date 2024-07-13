import os
import openai
import speech_recognition as sr
from gtts import gTTS
from os import path

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "afternoon.wav")

# Set up OpenAI API key from system environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the recognizer

def listen_command():

    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

        try:
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))


    # with sr.Microphone() as source:
    # with open("afternoon.wav","rb") as audio:
        
        
        # print("Listening...",source)
        # audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            # command = recognizer.recognize_google("ALOHA")
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None

def get_response(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": command},
            ]
        )
        return response.choices[0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"Error: {e}")
        return "I'm sorry, I encountered an error."

def speak_response(response):
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # Use `afplay` to play the mp3 file on macOS

if __name__ == "__main__":

    # recognizer = sr.Recognizer()
    # r = sr.Recognizer()

    # with sr.AudioFile(AUDIO_FILE) as source:
    #     audio = r.record(source)

    # try:
    #     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    # except sr.UnknownValueError:
    #     print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))

    print("OpenAI API key loaded successfully")
    command = listen_command()
    if command:
        response = get_response(command)
        print(response)
        speak_response(response)
