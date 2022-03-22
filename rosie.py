import speech_recognition as sr

def monitora_microfone():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        print("Olá fale algo")
        audio = mic.listen(source)

    try:
        print(mic.recognize_google(audio, language='pt-BR'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

monitora_microfone()
