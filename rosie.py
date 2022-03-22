import speech_recognition as sr
#from subprocess import call     # MAC / LINUX
from playsound import playsound # WINDOWS


##### CONFIGURAÇÕES #####
hotword = 'rose'

with open('./credenciais/assistentevirtual.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        while(True):
            mic.adjust_for_ambient_noise(source)
            print("Aguardando o Comando: ")
            audio = mic.listen(source)
            print(mic.recognize_google(audio, language='pt-BR'))
            try:
                trigger = mic.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()

                if hotword in trigger:
                    print('Comando: ', trigger)
                    responde('hello')
                    ### executar os comandos
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    playsound('audios/' + arquivo + '.mp3')  # Windows





def main():
    monitora_audio()

main()

