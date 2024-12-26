from pydub import AudioSegment
from flask import Flask,request,Response,send_file
from json import load
from packages.LineAPI import LineAPI

#from sys import exit
from time import sleep

from os import environ,getcwd
from os.path import join
from dotenv import load_dotenv



def load_env() -> str:
    load_dotenv("/etc/secrets/.env")
    channelAccessToken:str = environ["channelAccessToken"]

    return channelAccessToken


def japaneseToMorseSound_converter(message:str) -> tuple[str,int]:
    exportedMorseSignalsPath:str = "converted_morse_signals.mp3"
    morseAudio:object = AudioSegment.silent(duration=0)
    morseTable:dict = {}
    singleUnitDuration:int =  60 # *0.001 sec

    print("loading morse signal assets")
    morse_long:object = AudioSegment.from_file("morse_long.mp3") #!   0.18 sec
    morse_short:object = AudioSegment.from_file("morse_short.mp3")#!  0.06 sec
    morseSignals:list = [morse_short,morse_long]
    morse_space:object = AudioSegment.silent(duration=singleUnitDuration) #! 0.06 sec

    print("loading japanese-morse conversion table")
    with open("japanese-morse_table.json","r",encoding="utf-8") as f:
        morseTable = load(f)

    if not message:
        print("text should be written in the message!!")
        return

    print(f"requestedMessage:{message}")

    for index,letter in enumerate(message):
        morseList:list  =morseTable.get(letter,[])
        if len(morseList) == 0:
            return

        print(f"Now generating morse signals for {letter}({index+1}/{len(message)})")
        for signal in morseList:
            try:
                morseAudio += morseSignals[signal]
            except Exception as e:
                print(f"interruption occured. Error:{e}")
                break
            morseAudio += morse_space

    audioDuration:int = len(morseAudio)
    morseAudio.export(exportedMorseSignalsPath,format="mp3")
    return exportedMorseSignalsPath,audioDuration



app:object = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():

    if request.method == "POST":
        line:object = LineAPI()
        message,contentType = line.parse_POSTrequest(request.get_json())
        morseAudioPath,audioDuration = japaneseToMorseSound_converter(message.strip())
        absoluteAudioPath:str = join(getcwd(),morseAudioPath)

        channelAccessToken:str = load_env()
        line.addCredentials(channelAccessToken)
        line.addMessage_forReply(messageType="audio",contentURL=absoluteAudioPath,audioDuration=audioDuration)
        response:str = line.sendMessage()
        print(absoluteAudioPath)
        print(response)


    else:
        pass
        """ requestMessage:str = str(request.args.get("message"," "))
        morseAudioPath,audioDuration = japaneseToMorseSound_converter(requestMessage.strip())
        absoluteAudioPath:str = join(getcwd(),morseAudioPath)
        print("This method is not allowed. POST is only accessible.")
        return send_file(absoluteAudioPath)"""

    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0")