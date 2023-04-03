import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 150)     # setting up new voice rate
voices = engine.getProperty('voices') # changing index, changes voices. 0 for male
engine.setProperty('voice', voices[0].id) # engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('Listening ...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'Ghost' in command:
                command = command.replace('Ghost', '')
    except:
        pass

    return command


def run_assistant():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
    elif 'date' in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        print(date)
        talk("Today is" + date)
    elif "with me" in command:
        talk("Arent you dating someone?, plus i'm dating WIFI at the moment")
    elif "joke" in command:
        talk(pyjokes.get_joke())
    else:
        talk('Say that again, please')


engine.say("Hello, I'm Ghost, your virtual assistant.")
engine.say("How can I help you?")
engine.runAndWait()

while (True):
    run_assistant()
