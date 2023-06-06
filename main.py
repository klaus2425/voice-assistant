import os
import threading
import customtkinter
import speech_recognition as sr
import pyttsx3
import pywhatkit
import time
import customtkinter as ctk
import mpv
from word2number import w2n
from pytube import Search
from pytube import YouTube
from datetime import datetime
from PIL import Image

# Engine, Microphone, and Recognizer
m = sr.Microphone()
r = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')


def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()


def listen():
    with m as source:
        print("Listening...")
        action_label.configure(text='Listening...')
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        action_label.configure(text='Recognizing...')
        query = r.recognize_google(audio, language='en')
        action_label.configure(text='Recognizing...')
        print(f"User: {query}")
        return query
    except Exception as e:
        return ''


def execute_command(command):
    if 'play' in command:
        play(command)

    elif 'list' in command:
        todo()

    elif 'search' in command:
        search(command)
    elif 'reminder' in command:
        reminder()
    elif 'download' in command:
        download(command)
    elif 'time' in command:
        ask_time()
    elif 'today' in command:
        date()
    else:
        speak("I'm sorry, I didn't understand that.")
        return True


def play(command):
    pos = command.index('play')
    song = command.replace(command[:pos + 4], '')
    video = Search(song).results[0]
    action_label.configure(text=f"Playing {video.title}")
    speak(f"Playing {video.title}")
    pywhatkit.playonyt(song)



def todo():
    speak("What task would you like to add?")
    task = listen()
    todo_list = open('C:\\Users\\' + os.getlogin() + '\\Documents\\List.txt', 'w')
    count = 1
    while task:
        if task == 'stop':
            break
        todo_list.write(f'{count}. {task}\n')
        print(f"{count}Task added: {task}")
        count += 1
        speak('What else?')
        task = listen()


def reminder():
    def timer(minutes, t):
        time.sleep(minutes)
        speak(f"Hi {os.getlogin()}, you need to {t}")
    speak("What do you want me to remind you?")
    task = listen()
    speak("In how many minutes?")
    reminder_time = listen().lower().replace('minutes', '').replace('in', '').replace('minute', '').strip()
    try:
        time_num = w2n.word_to_num(reminder_time)
        time_num = 60 * time_num
        print(time_num)
        threading.Thread(target=timer, args=(time_num, task)).start()
    except:
        speak("Sorry, I didn't understand that")
        run_assistant()


def search(command):
    pos = command.index('search')
    search_query = command.replace(command[:pos + len('search')], '')
    action_label.configure(text=f"Searching for {search_query}")
    speak(f"Searching for {search_query}")
    pywhatkit.search(search_query)


def download(command):
    pos = command.index('download')
    song = command.replace(command[:pos + len('download')], '')
    video = Search(song).results[0]
    action_label.configure(text=f'Downloading {song}')
    speak('Downloading' + song)
    if YouTube(video.watch_url).streams.get_highest_resolution().download(
            'C:\\Users\\' + os.getlogin() + '\\Downloads'):  # Save download videos to Downloads folder
        speak('Download Finished')
        action_label.configure(text='Download Finished')
    else:
        speak('Download Failed')
        action_label.configure(text='Download Failed')



def ask_time():
    current_time = datetime.now().strftime("%I %M %p").lstrip('0')
    current_time_label = datetime.now().strftime("%I:%M %p").lstrip('0')
    action_label.configure(text=f'Current time is {current_time_label}')
    speak("Current time is " + current_time)


def date():
    date_today = datetime.today().strftime('%A %d %B %Y')
    speak(f"The date today is {date_today}")
    action_label.configure(text=f'The date today is {date_today}')


def start_va():
    command = listen()
    if 'exit' in command:
        speak('Goodbye!')
        start_window.quit()
        exit()
    else:
        execute_command(command)


def run_assistant():
    username = os.getlogin()
    while True:
        text = listen()
        if 'cali' in text:
            action_label.configure(text=f'Hi {username}, how can I help you?')
            speak('Hi ' + username + ', how can I help you?')
            action_label.configure(text=f'Hi {username}, how can I help you?')
            start_va()
            engine.runAndWait()
        if 'exit' in text:
            speak('Goodbye!')
            start_window.quit()
            exit()


# GUI
start_window = ctk.CTk()
start_window.title('CaliVA')
start_window.geometry('400x600')

frame = ctk.CTkFrame(master=start_window, width=380, height=580)
frame.place(relx=0.5, rely=0.5, anchor='center')

label = ctk.CTkLabel(frame, text='CALI')
label.configure(width=150, height=200, font=('Helvetica', 60, 'bold'))
label.place(relx=0.5, rely=0.1, anchor='center')

logo = ctk.CTkImage(light_image=Image.open("images/MicrophoneLogoInactive.png"),
                    dark_image=Image.open("images/MicrophoneLogoInactive.png"),
                    size=(220, 220)
                    )

logo_label = ctk.CTkLabel(frame, image=logo, text='')
logo_label.place(relx=0.5, rely=0.4, anchor='center')

action_label = customtkinter.CTkLabel(frame, text="Listening...")
action_label.configure(font=('Helvetica', 20), wraplength=300)
action_label.place(relx=0.5, rely=0.8, anchor='center')


def main():
    threading.Thread(target=run_assistant).start()
    start_window.resizable(False, False)
    start_window.iconbitmap(r'images/logo.ico')
    start_window.wm_state('zoomed')
    start_window.mainloop()


if __name__ == '__main__':
    main()
