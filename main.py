import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
import customtkinter
from pytube import Search
from pytube import YouTube

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")





def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, 0.2)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User: {query}")
        return query
    except Exception as e:
        speak("Please say that again")
        return None


def execute_command(command):
    if 'play' in command:
        play(command)

    elif 'set a reminder' in command:
        reminder(command)

    elif 'create a to-do list' in command:
        todo(command)

    elif 'search' in command:
        search(command)

    elif 'download' in command:
        download(command)

    elif 'exit' in command:
        window.close()

    else:
        speak("I'm sorry, I didn't understand that.")


def play(command):
    pos = command.index('play')
    song = command.replace(command[:pos + 4], '')
    speak(f"Playing {song}")
    link = pywhatkit.playonyt(song)


def reminder(command):
    speak("What should I remind you about?")
    reminder_text = listen()
    if reminder_text:
        print(f"Reminder set: {reminder_text}")


def todo(command):
    speak("What task would you like to add?")
    task = listen()
    while task:
        if task == 'stop':
            break
        print(f"Task added: {task}")
        speak('What else?')
        task = listen()


def search(command):
    pos = command.index('search')
    search_query = command.replace(command[:pos + len('search')], '')
    speak(f"Searching for {search_query}")
    pywhatkit.search(search_query)


def download(command):
    pos = command.index('download')
    song = command.replace(command[:pos + len('download')], '')
    video = Search(song).results[0]
    speak('Downloading' + song)
    if YouTube(video.watch_url).streams.get_highest_resolution().download(
            'C:\\Users\\' + os.getlogin() + '\\Downloads'):  # Save download videos to Downloads folder
        speak('Download Finished')
    else:
        speak('Download Failed')


def main():
    while True:
        command = listen()
        if 'exit' in command:
            break
        if command:
            execute_command(command)

if __name__ == '__main__':
    main()
