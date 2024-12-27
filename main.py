from pydub import AudioSegment
from flask import Flask,request,Response,send_file
from json import load
from packages.LineAPI import LineAPI

#from sys import exit
from time import sleep

from os import environ,getcwd
from os.path import join
from dotenv import load_dotenv

exportedMorseAudioName:str = "converted_morse_signals.mp3"
relativePath:str = str(join(getcwd(),exportedMorseAudioName))
absoluteAudioPath:str = "https://morse-signal-converter-bot.onrender.com" + relativePath


def load_env() -> str:
    load_dotenv("/etc/secrets/.env")
    channelAccessToken:str = environ["channelAccessToken"]

    return channelAccessToken


def japaneseToMorseSound_converter(message:str) -> tuple[str,int]:
    morseAudio:object = AudioSegment.silent(duration=0)
    morseTable:dict = {}
    singleUnitDuration:int =  180 # *0.001 sec

    print("loading morse signal assets")
    morse_long:object = AudioSegment.from_file("morse_long.mp3") #!   0.18 sec
    morse_short:object = AudioSegment.from_file("morse_short.mp3")#!  0.06 sec
    morseSignals:list = [morse_short,morse_long]
    morse_space:object = AudioSegment.silent(duration=singleUnitDuration) #! 0.18 sec

    print("loading japanese-morse conversion table")
    with open("japanese-morse_table.json","r",encoding="utf-8") as f:
        morseTable = load(f)

    if not message:
        print("Request should not be blank")
        return None,None

    print(f"requestedMessage:{message}")

    for index,letter in enumerate(message):
        morseList:list  = morseTable.get(letter,[])
        if len(morseList) == 0:
            print("Request text includes an invalid character")
            return None,None

        print(f"Now generating morse signals for {letter}({index+1}/{len(message)})")
        for signal in morseList:
            try:
                morseAudio += morseSignals[signal]
            except Exception as e:
                print(f"interruption occured. Error:{e}")
                break
            morseAudio += morse_space

    audioDuration:int = len(morseAudio)
    morseAudio.export(exportedMorseAudioName,format="mp3")
    return exportedMorseAudioName,audioDuration



app:object = Flask(__name__)

@app.route("/app_script/wakeup",methods=["GET"])
def wakeUpCallHandling():
    return Response(status=200)


@app.route(relativePath,methods=["GET","POST"])
def returnMorseAudio():
    return send_file(exportedMorseAudioName,as_attachment=True)


@app.route("/",methods=["GET","POST"])
def main():

    if request.method == "POST":
        line:object = LineAPI()
        message,contentType = line.parse_POSTrequest(request.get_json())
        morseAudioPath,audioDuration = japaneseToMorseSound_converter(message.strip().upper())

        channelAccessToken:str = load_env()
        line.addCredentials(channelAccessToken)
        line.addMessage_forReply(messageType="audio",contentURL=absoluteAudioPath,audioDuration=audioDuration)
        response:str = line.sendMessage()
        print(absoluteAudioPath)
        print(response)


    else:
        return "GET method is not available.\nTry POST method from the LINE official bot: 'https://lin.ee/zTGOWML'"

    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0")