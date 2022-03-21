from gtts import gTTS
#from subprocess import call #MAC / Linux
from playsound import playsound #Windows

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/hello.mp3')

    #call(['afplay', 'audios/hello.mp3']) # OSX
    #call(['aplay', 'audios/hello.mp3']) # Linux
    playsound('audios/hello.mp3') # Windows

cria_audio('oi, eu sou a Rosie.')
