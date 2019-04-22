from __future__ import print_function
import random, os, pprint, pyttsx3, json, pickle, datetime
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from pygame import mixer
import speech_recognition as sr
from pymongo import MongoClient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil.parser import parse


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

def getGevent():
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    puts('Getting the upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=3, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        puts('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        sp = decodedate(start)
        pp = "On " + sp + ", "+event['summary']
        puts(pp)

def decodedate(a):
    b = a[8:10]+'.'+a[5:7]+'.'+a[:4]
    return b

def createGevent(title,date,time,summ):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    event = {
      'summary': title,
      'description': summ,
      'start': {
        'dateTime': encodedate(date,time),
        'timeZone': 'Asia/Kolkata',
      },
      'end': {
        'dateTime': encodedate(date,time),
        'timeZone': 'Asia/Kolkata',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

def encodedate(date,time):
    d = date + ' ' + time
    e = str(parse(d))
    return (e[:10]+'T'+e[11:])

def createevent():
    puts('Say the title of your event')
    title = getSpeech();
    puts('Can you confirm your date?')
    date = input('User: ')
    puts('What time will your event be?')
    time = input('User: ')
    puts('What is the event about?')
    event = input('User: ')
    createGevent(title, date, time, event)

def getevent():
    puts('what is your date?')
    date = input('User: ')
    if not dbevent.find({"date": date}):
        puts('There are no events on the day')
    for post in dbevent.find({"date": date}):
        if post['time'] is 'all day':
            puts('On ' + post['date'] + ', event is "' + post['event']+'"')
        else:
            puts('On ' + post['date'] + ', ' + post['time'] + ' event is "' + post['event']+'"')

def getremin():
    return

def createremin():
    return

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
bye = ['bye', 'later', 'goodby']
greet = ['thanks', 'thank', 'awesome', 'great', 'good']
prob = ['I can help with your calender events', "You can ask about your day's plan"]
meet = ['event','appoin']
ok = ['ok', 'okay', 'hmm']

remi = ['remind']
creat = ['creat', 'set']

greetrep = ['your welcome', "don't mention it", 'my pleasure']
hirep = ['hi, how can i help?', 'hello, what can i do for you?']

p = True
while p:
    a = 0
    # text = input('User: ')
    text = getSpeech()
    words = tokenize(text)
    for word in words[:]:
        if word in creat and a is 0:
            createevent()
            a = 1
            continue

        elif word in meet and a is 0:
            getGevent()
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
            puts('ok, bye.')
            break

        elif word in ok and a is 0:
            a = 1
            puts("Okay :-)")

    if a is 0:
        puts(random.choice(prob))
