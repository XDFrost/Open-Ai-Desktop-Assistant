import win32com.client                      # Provides interaction with COM (Microsoft Component Object Model) on Windows;
                                            # COM is a binary interface standard that allows the components to communicate with each other
import speech_recognition as sr
import webbrowser                           # Will be used to interact with web browser
import openai
import os                                   # Used to interact with software components of the system
from fuzzywuzzy import fuzz                 # Uses fuzzy logic to convert something into a meaningful input
import datetime
import subprocess                           # Used to run system applications
from config import apikey
import random


speaker = win32com.client.Dispatch("SAPI.SpVoice")                      # win32.client provides the function to work with COM; Dispatch method forms a connection between the specified program and COM; SAPI.SpVoice is a voice object, Speech API or SAPImakes our computer able to speak

# replace 1 with 0 for male voice

speaker.Voice = speaker.GetVoices().Item(1)                             

chatStr = ""
def chat(query):
    global chatStr
    openai.api_key = apikey
    
    #todo: Change User with your name
    
    chatStr+=f"User: {query}\n Jarvis: "                                # Appends user's querry to chatStr
    
    response = openai.Completion.create(                                # Makes a call to OpenAI API's completion endpoint
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    print(response["choices"][0]["text"])                               # response contains the API's response, choices is a list with generated choices from API, 0 is used to retrieve 1st choice, text is used to retreive generated text from the specified choice
    chatStr+=f"{response['choices'][0]['text'] }\n"                     # Appends generated text
    speaker.Speak(response["choices"][0]["text"] )
    

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"                 # Will contain the prompt given by the user
    
    response = openai.Completion.create(                                # Makes a call to OpenAI API's completion endpoint
    model="text-davinci-003",
    prompt=prompt,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    print(response["choices"][0]["text"])                               # response contains the API's response, choices is a list with generated choices from API, 0 is used to retrieve 1st choice, text is used to retreive generated text from the specified choice
    text+=response["choices"][0]["text"]                                # Appends the words in the text together
    
    if not os.path.exists("Openai"):                                    # if a directory named Openai doesn't exists, then os.mkdir() makes one
        os.mkdir("Openai")
        
    with open(f"Openai/prompt - {random.randint(1, 23234367890)}", "w") as f:                            # Makes and opens a file with name the (prompt - a random number between 1 and the specified one) in write only mode
        f.write(text)                                                                                    # writes the text with generated response in that file
    

def takeCommand():                                                      # Function that takes mic input
    r = sr.Recognizer()                                                 # Recognizes the speech
    with sr.Microphone() as source:                                     # Microphone class access audio inputs; source specifies that we are using microphone for audio input
        r.pause_threshold = 0.5                                         # Speech recognizer will stop recording after a pause of 0.5 seconds is detected
        audio = r.listen(source)                                        # listen captures audio inputs from source
        
        try:                                                            # if our software won't recognize input, it'll say Error occured during recognition, this is why we are using try, except block
            print("Recognizing...")
            query = r.recognize_google(audio, language = "en-in")       # User inputs will be recognized and stored in query
            print(f"User said: {query}")                                # For debugging
            return query
        
        except Exception as e:
            return "Error occured during recognition"
        
while True:
    print("Enter the word/words that computer will speak: ")
    s = 'Hello I am your personal assistant, what can I do for you?'
    speaker.Speak(s)                                                    # Speak is a special command provided by speaker object that converts text to speech
    
    while True:
        print("listening...")
        query = takeCommand()
        if "open" in query and "website" not in query: 
            words = query.split()                                       # splits the query inzx to a list of individual words
            website_index = words.index("open") + 1                     # finds the index of word open in list and add 1 to get next index
            website = words[website_index]
            speaker.Speak(f"Opening {website}")
            url = f"https://{website}.com"
            webbrowser.open(url)
                    
        elif "play music" in query.lower():
            speaker.Speak("Listing Music")
            
            # todo: Add your music folder path here
            
            musicFolder = r"D:\Projects\Open AI Desktop Assistant (PYTHON)"                   # Specified path for music folder
            musicFiles = []
            for file in os.listdir(musicFolder):                                                  # os.listdir retrives all files from the specified directory
                if file.endswith(".mp3"):
                    musicFiles.append(file)
            
            print("Music files:")
            for i, musicFile in enumerate(musicFiles, start=1):
                print(f"{i}. {musicFile}")
            
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speaker.Speak("Please say the name of the music file you want to play.")
                audio = r.listen(source)
            
            try:
                query = r.recognize_google(audio, language="en-in")
                query = query.lower()
                best_match_ratio = 0
                selectedFile = None
                for musicFile in musicFiles:
                    match_ratio = fuzz.ratio(query, musicFile.lower())                            # fuzz.ratio is used to calculate the similarity between two strings
                    if match_ratio > best_match_ratio:
                        best_match_ratio = match_ratio
                        selectedFile = musicFile
                
                if selectedFile is not None:
                    speaker.Speak(f"Playing {selectedFile}")
                    musicPath = os.path.join(musicFolder, selectedFile)                           # this statement joins the music folder path and selected file path
                    os.startfile(musicPath)
                else:
                    speaker.Speak("Music file not found.")
            except sr.UnknownValueError:
                speaker.Speak("Sorry, I could not understand your command.")
            except sr.RequestError:
                speaker.Speak("Sorry, I am having trouble accessing the speech recognition service.")
                
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")                               # strftime arguement converts the original datetime format to the specified format
            speaker.Speak(f"The time is {strfTime}")
            
        elif "start" in query and len(query.split()) > 1:
            words = query.split()                                                                 # words contains the individual words after query is split
            app_name = " ".join(words[1:])                                                        # contains the name of app
            speaker.Speak(f"Opening {app_name.capitalize()}")
            
            try:
                subprocess.run(f"start {app_name.capitalize()}", shell=True)                      # Subprocess module is used to run applications using python
            except Exception as e:
                speaker.Speak("Failed to open the application.")
        
        elif "Using AI".lower() in query.lower() or "Using Artificial Intelligence".lower() in query.lower():                 
            ai(prompt = query)
        
        else:
            response = chat(query)
            