import speech_recognition as sr
import pyttsx3
import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "your name" in command:
        speak("I am your personal voice assistant.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I'm sorry, I can't help with that.")
    return True

def main():
    speak("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = listen()
        if not respond_to_command(command):
            break

if __name__ == "__main__":
    main()