from os import remove

import speech_recognition as sr
from gtts import gTTS
#from subprocess import call     # MAC / LINUX
from playsound import playsound # WINDOWS
from requests import get
from bs4 import BeautifulSoup


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
                    responde('feedback')
                    executa_comandos(trigger)
                    ### executar os comandos
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    playsound('audios/' + arquivo + '.mp3')  # Windows

def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/resposta.mp3')
    print('Rosie: ', mensagem)
    playsound('audios/resposta.mp3') # Windows
    remove('audios/resposta.mp3')

def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('Comando Inválido', mensagem)
        responde('comandoInvalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:5]:
        mensagem = item.title.text
        cria_audio(mensagem)




def main():
    while(True):
        monitora_audio()

#main()

ultimas_noticias()