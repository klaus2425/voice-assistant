import os
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import customtkinter as ctk
from pytube import Search
from pytube import YouTube
from datetime import datetime



# Engine, Microphone, and Recognizer
m = sr.Microphone()
r = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()


def listen():
    with m as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User: {query}")
        return query
    except Exception as e:
        return ''


def execute_command(command):
    if 'play' in command:
        play(command)

    elif 'set a reminder' in command:
        reminder()

    elif 'create a to-do list' in command:
        todo()

    elif 'search' in command:
        search(command)

    elif 'download' in command:
        download(command)
    elif 'time' in command:
        time()
    elif 'date' in command:
        date()
    else:
        speak("I'm sorry, I didn't understand that.")
        return True


def play(command):
    pos = command.index('play')
    song = command.replace(command[:pos + 4], '')
    speak(f"Playing {song}")
    link = pywhatkit.playonyt(song)


def reminder():
    speak("What should I remind you about?")
    reminder_text = listen()
    if reminder_text:
        print(f"Reminder set: {reminder_text}")


def todo():
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


def time():
    current_time = datetime.now().strftime("%I %M %p").lstrip('0')
    speak("Current time is " + current_time)


def date():
    speak(datetime.today().strftime('%A %d %B %Y'))


def start_va():
    command = listen()
    if 'exit' in command:
        start_window.quit()
        exit()
    else:
        execute_command(command)


def run_assistant():
    username = "Jaycie"
    while True:
        text = listen()
        if 'hey cali' and 'cali' in text:
            speak('Hi ' + username + ', how can I help you?')
            label.configure(text='speak')
            start_va()
            engine.runAndWait()
        if 'exit' in text:
            start_window.quit()


#GUI
start_window = ctk.CTk()
start_window.title('CaliVA')
start_window.geometry('400x600')

frame = ctk.CTkFrame(master=start_window, width=380, height=580)
frame.place(relx=0.5, rely=0.5, anchor='center')

label = ctk.CTkLabel(frame, text='CALI')
label.configure(width=150, height=200)
label.place(relx=0.5, rely=0.1, anchor='center')

def main():
    threading.Thread(target=run_assistant).start()
    start_window.mainloop()


if __name__ == '__main__':
    main()
