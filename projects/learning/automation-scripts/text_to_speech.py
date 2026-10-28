
#Convert to Speech

# Install first: pip install pyttsx3

import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

text_to_speech("Hello, this is Python automating your tasks!")

