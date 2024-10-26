import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Please speak something...")
    audio_data = recognizer.listen(source)
    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"Recognized: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
