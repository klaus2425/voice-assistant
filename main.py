import speech_recognition as sr
import pyttsx3
import pywhatkit
import PySimpleGUI as sg


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User: {query}")
        return query
    except Exception as e:
        print("Please say that again...")
        return None


def execute_command(command):
    if 'play' in command:
        song = command.replace('play', '')
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'set a reminder' in command:
        speak("What should I remind you about?")
        reminder_text = listen()
        if reminder_text:
            # Implement your reminder logic here
            # You can use libraries like datetime, pickle, or a database to store reminders
            print(f"Reminder set: {reminder_text}")

    elif 'create a to-do list' in command:
        speak("What task would you like to add?")
        task = listen()
        if task:
            # Implement your to-do list logic here
            # You can store tasks in a list or a file
            print(f"Task added: {task}")

    elif 'search' in command:
        search_query = command.replace('search', '')
        speak(f"Searching for {search_query}")
        pywhatkit.search(search_query)

    else:
        speak("I'm sorry, I didn't understand that.")


def main():
    sg.theme('LightGreen')

    layout = [[sg.Text('Assistant:', size=(15, 1)), sg.Text('', key='-OUTPUT-')],
              [sg.Button('Start'), sg.Button('Exit')]]

    window = sg.Window('AI Voice Assistant', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == 'Start':
            window['-OUTPUT-'].update("Listening...")
            command = listen()
            if command:
                window['-OUTPUT-'].update(command)
                execute_command(command)

    window.close()


if __name__ == '__main__':
    main()