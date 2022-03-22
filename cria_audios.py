from gtts import gTTS
#from subprocess import call #MAC / Linux
from playsound import playsound #Windows

nome_arquivo = 'comandoInvalido'

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/' + nome_arquivo + '.mp3')

    #call(['afplay', 'audios/hello.mp3']) # OSX
    #call(['aplay', 'audios/hello.mp3']) # Linux
    playsound('audios/' + nome_arquivo + '.mp3') # Windows

cria_audio('Ops, não sei te informar')
