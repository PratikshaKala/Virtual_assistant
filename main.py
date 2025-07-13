import speech_recognition as sr   # Imports the speech_recognition module used to convert voice to text.
import webbrowser  # Used to open websites in your default browser.
import pyttsx3   # Used for text-to-speech output (your assistant will "speak").
import musicLibrary   # A custom module that maps song names to YouTube/Spotify links.
import requests    # Used to send HTTP requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()  # # Initialize TTS engine
newsapi = "{NewsApI key}"

def speak(text):
    engine.say(text)  # Add text to speech queue
    engine.runAndWait()     # Starts speaking

def processCommand(command):    # Main function to process the user’s spoken command.
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]   # eg.play sky fall --> ['play','skyfall'] --> it will choose[1] that is skyfall
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in command.lower():
        response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey= {Your newsAPI key}")   # Sends an API request to fetch India’s top headlines using NewsAPI.
        if response.status_code == 200:     # Checks if the HTTP request to the News API was successful.
                                            # 200 is the standard "OK" status code in HTTP.
                                            # If not 200, the request likely failed (e.g. invalid API key, no internet).
            data = response.json()   #Parses the response body (which is in JSON format) into a Python dictionary called data.
            # Extract the articles
            articles = data.get("articles", [])    #Extracts the list of news articles from the data dictionary.If "articles" key doesn't exist, it safely returns an empty list []

            for i, article in enumerate(articles[:10], 1):  # limit to top 10
                speak(f"{i}. {article['title']}")   # Uses speak() function to read out the article title.

    else:
        # add a feature(optional)
        pass


if __name__ == "__main__":      # Main program loop...starts the assistant by announcing "Initializing..."
    speak("Intializing.....")
    # Listen for the wake word-"hello"
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if(word.lower()=="hello"):
                speak("Yeah")


                # Listen for actual command
            with sr.Microphone() as source:
                print("Your virtual assistant is active...")
                audio = r.listen(source)
                command = r.recognize_google(audio)
                processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e)) # Catches any runtime errors (speech timeout, microphone issue, etc.) and prints them.
     