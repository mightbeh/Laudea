import random, os, urllib3, pprint, pyttsx3, json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from pygame import mixer
import speech_recognition as sr
from pymongo import MongoClient

# initialize tts
engine = pyttsx3.init()
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# prepare Stemming
ps = PorterStemmer()
# prepare MongoDB
client = MongoClient('localhost', 27017)
db = client['Laudea']
dbevent = db['event']
dbremin = db['reminder']


def getSpeech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("User: ")
        audio = r.listen(source, phrase_time_limit=3)
    try:
        response = str(r.recognize_google(audio))
        print(response)
        return response
    except:
        print("Try Again")
        response = getSpeech()
    return response


def tokenize(x):
    y = x.lower()
    word = word_tokenize(y)
    print(word)
    return stopWord(word)

def stopWord(x):
    stop_words = set(stopwords.words("english"))
    filtered_sentence = [w for w in x if w not in stop_words]
    print(filtered_sentence)
    return stemming(filtered_sentence)

def stemming(x):
    words = []
    for w in x: words.append(ps.stem(w))
    print(words)
    return words


def getevent():
    puts('Can you confirm your date?')
    date = input('User: ')
    for post in dbevent.find({"date": date}):
        if post['time'] is 'all day':
            puts('On ' + post['date'] + ', the reminder is ' + post['event'])
        else:
            puts('On ' + post['date'] + ', ' + post['time'] + ' the reminder is ' + post['event'])

def createevent():
    puts('Can you confirm your date?')
    date = input('User: ')
    puts('What time will your event be?')
    time = input('User: ')
    puts('What is the event about?')
    event = input('User: ')
    push(date, time, event)
    puts('Event saved as ' + event)

def getremin()

def createremin()


def push(date, time, event):
    data = {
        "date": date,
        "time": time,
        "event": event
    }
    dbevent.insert_one(data)


def puts(text):
    print('Bot: ' + text)
    engine.say(text)
    engine.runAndWait()


hi = ['hi', 'hello', 'hey']
bye = ['bye', 'later']
greet = ['thanks', 'thank', 'awesome', 'great', 'good']
prob = ['I can help with your calender events for now.', "You can ask about your day's plan"]
meet = ['event','appoin']
ok = ['ok', 'okay', 'hmm']

remi = ['remind']
create = ['creat', 'set']

greetrep = ['your welcome;)', "don't mention it :)", 'my pleasure (^_^)']
hirep = ['hi, how can i help?', 'hello, what can i do for you?']

p = True
while p:
    a = 0
    # text = input('User: ')
    text = getSpeech()
    words = tokenize(text)
    for word in words[:]:
        if word in creat and a is 0:
            if word in meet:
                createevent()
            elif word in remi:
                creatremin()
            a = 1
            continue

        elif word in meet and a is 0:
            getevent()
            a = 1
            continue

        elif word in remi and a is 0:
            getremin()
            a = 1
            continue

        elif word in hi and a is 0:
            puts(random.choice(hirep))
            a = 1
            continue

        elif word in greet and a is 0:
            puts(random.choice(greetrep))
            a = 1
            continue

        elif word in bye and a is 0:
            a = 1
            p = False
            break

        elif word in ok and a is 0:
            a = 1
            puts("Okay :-)")

    if a is 0:
        puts(random.choice(prob))