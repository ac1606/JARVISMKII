from playsound import playsound
import datetime
import time
import webbrowser
import speech_recognition as sr


# Import the run_gemini function from jarvisgemini.py


# Audio files
morning_sound = 'morning.wav'
afternoon_sound = 'afternoon.wav'
evening_sound = 'evening.wav'
welcome_sound = 'welcome.wav'
error_sound = 'error.wav'
standby_sound = 'standby.wav'
standbyoff_sound = 'standby2.wav'
discord_sound = 'discord.wav'
music_sound = 'music.wav'
d2l_sound = 'd2l.wav'
gmail_sound = 'gmail.wav'

# Bookmarks dictionary containing bookmark names and URLs
bookmarks = {
    'google': {'url': 'https://www.google.ca/', 'sound': 'google.wav'},
    'youtube': {'url': 'https://www.youtube.com/', 'sound': 'youtube.wav'},
    'snapchat': {'url': 'https://web.snapchat.com/', 'sound': 'snapchat.wav'},
    'chatgpt': {'url': 'https://chat.openai.com/', 'sound': 'chatgpt.wav'},
    'docs': {'url': 'https://docs.google.com/document/u/0/', 'sound': 'docs.wav'},
    'drive': {'url': 'https://drive.google.com/drive/my-drive', 'sound': 'drive.wav'},
    'whatsapp': {'url': 'https://web.whatsapp.com/', 'sound': 'whatsapp.wav'},
    'calendar': {'url': 'https://calendar.google.com/calendar/u/0/r', 'sound': 'calendar.wav'},
    'discord': {'url': 'https://web.discord.com', 'sound': 'discord.wav'},
    'youtube music': {'url': 'https://music.youtube.com', 'sound': 'music.wav'},
    'd2l': {'url': 'https://pdsb.elearningontario.ca/d2l/home', 'sound': 'd2l.wav'},
    'gmail': {'url': 'https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox', 'sound': 'gmail.wav'}
}

standby_mode = False

def play_audio(filename):
    """Play audio from the specified file."""
    playsound(filename)

def wishMe():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        play_audio(morning_sound)
        time.sleep(1)
        play_audio(welcome_sound)
    elif 12 <= hour < 18:
        play_audio(afternoon_sound)
        time.sleep(1)
        play_audio(welcome_sound)
    else:
        play_audio(evening_sound)
        time.sleep(1)
        play_audio(welcome_sound)

def open_bookmark(command):
    """Open bookmarks based on the command."""
    bookmark_name = command.split('open ')[-1].lower()
    if bookmark_name in bookmarks:
        play_audio(bookmarks[bookmark_name]['sound'])  # Play the corresponding bookmark sound
        time.sleep(1)  # Delay before opening the bookmark
        webbrowser.open_new_tab(bookmarks[bookmark_name]['url'])
        print(f"Opening {bookmark_name} in your browser.")
    else:
        play_audio(error_sound)  # Play an error sound if the bookmark is not found
        print("Sorry, I couldn't find that bookmark.")

def standby():
    global standby_mode
    standby_mode = True
    play_audio(standbyoff_sound)
    print("Standby mode activated. Waiting for 'Jarvis' trigger.")

def take_command():
    """Listen for voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=None if standby_mode else 5)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

if __name__ == "__main__":
    # Call the wishMe function to greet the user
    wishMe()

    while True:
        command = take_command()

        # Command handling logic
        if "standby" in command:
            standby()
        elif standby_mode:
            if "jarvis" in command:
                print("Exiting standby mode.")
                play_audio(standby_sound)
                standby_mode = False
            else:
                continue
        elif "open" in command:
            open_bookmark(command)
        elif "ai mode" in command:
            print("Switching to AI mode. Type 'exit' to return to Jarvis.")
        
        elif "exit" in command:
            play_audio('goodbye.wav')
            break
