import json
from os import remove

import speech_recognition as sr
from gtts import gTTS
#from subprocess import call     # MAC / LINUX
from playsound import playsound # WINDOWS
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser


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

    elif 'toca' in trigger and 'stratovarius' in trigger:
        playlists('stratovarius')

    elif 'tempo agora' in trigger:
        previsao_tempo(tempo=True)

    elif 'temperatura hoje' in trigger:
        previsao_tempo(minmax=True)

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

def playlists(album):
    if album == '':
        browser.open('https://open.spotify.com/track/1IaQLINjiOCSv4INrrv0aS?si=2ebe0b2533f040c5')
    elif album == 'stratovarius':
        browser.open('https://open.spotify.com/track/6i79bRJSNbFkHU6wVsqVWY?si=80918ba9f20549af')

def previsao_tempo(tempo=False, minmax=False):
    #https://api.openweathermap.org/data/2.5/weather?q=C%C3%A2ndido%20Mota&appid=59eca70c674af8e32b001b32f0b1f491&units=metric&lang=pt
    site = get('https://api.openweathermap.org/data/2.5/weather?id=3467542&appid=59eca70c674af8e32b001b32f0b1f491&units=metric&lang=pt')
    clima = site.json()
    #print(json.dumps(clima, indent=4))
    temperatura = clima['main']['temp']
    minima = clima['main']['temp_min']
    maxima = clima['main']['temp_max']
    descricao = clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}'
    if minmax:
        mensagem = f'Mínima de {minima} e máxima de {maxima}'
    cria_audio(mensagem)


def main():
    while(True):
        monitora_audio()

main()

#previsao_tempo(True, True)