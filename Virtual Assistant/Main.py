from googletrans import Translator
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import json
import random

NEWS_API_KEY = "b69d103332414b71854433df5086347d"  # News API key
WEATHER_API_KEY = "d04223fed8441152c99321e995162632" # replace with your API key

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
            if 'stop' in command:
                talk('Goodbye!')
                exit()
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
    elif 'translate' in command:
        command = command.replace('translate', '')
        try:
            translation = Translator.translate(command)
            print(f"{translation.origin} ({translation.src}) -> {translation.text} ({translation.dest})")
            talk(translation.text)
        except Exception as e:
            print(e)
            talk("Sorry, I couldn't translate your text.")
    elif 'set reminder' in command:
        talk('What should I remind you about?')
        reminder = take_command()
        talk('When should I remind you?')
        reminder_time = take_command()
        reminder_time = datetime.datetime.strptime(reminder_time, '%d/%m/%Y %H:%M')
        current_time = datetime.datetime.now()
        delta = reminder_time - current_time
        seconds = delta.total_seconds()
        if seconds < 0:
            talk("Sorry, I can't go back in time.")
        else:
            talk(f"Reminder set for {reminder_time}.")
            time.sleep(seconds)
            talk(f"Reminder: {reminder}")
    elif 'news' in command:
        news_url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={NEWS_API_KEY}"
        response = requests.get(news_url)
        news = json.loads(response.text)["articles"]
        article = random.choice(news)
        talk(f"Here's the latest news: {article['title']}")
        talk(article['description'])
    elif 'weather' in command:
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        api_key = WEATHER_API_KEY
        talk("Which city's weather would you like to know?")
        city_name = take_command()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            weather = data["weather"][0]["description"]
            temp = int(data["main"]["temp"] - 273.15)
            talk(f"The weather in {city_name} is {weather} and the temperature is {temp} degrees Celsius.")
        else:
            talk("Sorry, I couldn't find the weather for that city.")      
    else:
        talk('Say that again, please')


engine.say("Hello, I'm Ghost, your virtual assistant.")
engine.say("How can I help you?")
engine.runAndWait()

while (True):
    run_assistant()
