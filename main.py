# Install All require libraries using pip 
import webbrowser as browser
import speech_recognition as sr
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import time
import pygame
import os

# Inlude your news api
newsapi = ""

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running while the music plays
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Wait for 1 second to avoid high CPU usage
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def Aiprocess(command):
    # Use this using your chatgpt plus api
    client = OpenAI(
        api_key="")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Echo skilled in general task like Alexa."},
            {
                "role": "user",
                "content": "What is coding."
            }
        ]
    )
    return(completion.choices[0].message.content)


def process_command(c):
    if "open google" in c.lower():
        browser.open("https://www.google.com/")
    elif "open youtube" in c.lower():
        browser.open("https://www.youtube.com/")
    elif "open facebook" in c.lower():
        browser.open("https://www.facebook.com/")
    elif "open linkedin" in c.lower():
        browser.open("https://pk.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        browser.open(link)
    elif "news" in c.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Get the list of articles
            articles = data.get('articles', [])

            for article in articles:
                print(article["title"])
                speak(article["title"])
    elif "ai" in c.lower():
        output =Aiprocess(c)
        speak(output)
    else:
        speak("Could Not Understand Your Request")

    

if(__name__ == "__main__"):
    speak("Intializing Echo....")
    while True:
        # Listen For Wake Word Echo
        # obtain audio from michrophone
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            # Give Command to echo
            with sr.Microphone() as source: 
                print("Listening....")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if(word.lower() == "echo"):
                speak("Ya How may i help you")
                with sr.Microphone() as source: 
                    print("Echo Active!....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(command)
                    process_command(command)
        except Exception as e:
            print(e)