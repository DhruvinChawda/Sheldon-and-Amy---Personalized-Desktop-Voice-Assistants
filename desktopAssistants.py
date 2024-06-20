import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import openai
import datetime
import random

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "I apologize sir, some error occurred."

def set_female_voice(engine):
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'zira' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def say_female(text):
    engine = pyttsx3.init()
    set_female_voice(engine)
    engine.say(text)
    engine.runAndWait()

def geminiprompt(prompt):
    from config import gemini_api_key
    import google.generativeai as genai

    genai.configure(api_key=gemini_api_key)

    text = f"OpenAI response for prompt: {prompt} \n************************************\n\n"

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(prompt)
    print(response.text)
    text += response.text

    if not os.path.exists("Gemini"):
        os.makedirs("Gemini")

    with open(f"Gemini/{prompt[0:30]}.txt", "w") as f:
        f.write(text)
    
    say(response.text)

chatStr = ""

def chat(prompt):
    from config import gemini_api_key
    import google.generativeai as genai

    global chatStr
    chatStr += f"Harry: {prompt}\n sheldon: "

    genai.configure(api_key=gemini_api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(prompt)
    say_female(response.text)

    chatStr += f"{response.text}\n"
    return response.text

if __name__ == '__main__':
    print('SHELDON AND AMY ARE HERE !!')
    say("Hello, I am Sheldon, How can I help you sir?")
    say_female("Amy present too sir")
    while True:
        say("Listening")
        print("Listening...")
        query = takecommand()
        sites = [["YouTube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"sheldon Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])

        if "Hello sheldon".lower() in query.lower():
            say("Hello sir")

        if "open music" in query:
            musicpath = "C:\\Users\\dhruv\\Downloads\\play_friends_theme_song.mp3"
            os.startfile(musicpath)

        if "sheldon time".lower() in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {strfTime}")

        if "open word".lower() in query.lower():
            path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
            say("Opening word, sir")
            os.startfile(path)

        if "turn off sheldon".lower() in query.lower():
            say("Turning off, sir")
            exit()
        if "who is the best sheldon".lower() in query.lower():
            say("You are the best sir. You are the only one and nobody is better than you, sir. I just blessed that you exist")

        if "What is your name".lower() in query.lower():
            say("Hello! I am Sheldon, created by Dhruvin Chawda")

        if "How are you sheldon".lower() in query.lower():
            say("I am great sir and now that I am talking with you, I am feeling better, sir")

        if "sheldon you there".lower() in query.lower():
            say("Yes sir")    

        if "hey sheldon".lower() in query.lower():
            geminiprompt(prompt=query)

        if "amy".lower() in query.lower():
            chat(prompt=query)
