import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio, language="en-US")  # Use Google's API
            print(f"Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            print("Speech service unavailable.")
            return ""

