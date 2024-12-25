from pydub import AudioSegment
from flask import Flask,request,Response
from json import load


def japaneseToMorseSound_converter(message:str) -> str:
    exportedMorseSignalsPath:str = "converted_morse_signals.mp3"
    morseAudio:object = None
    morseTable:dict = {}

    morse_long = AudioSegment.from_mp3("morse_long.mp3")
    morse_short = AudioSegment.from_mp3("morse_short.mp3")
    morseSignals:list = [morse_short,morse_long]
    morse_space = AudioSegment.from_mp3("morse_space.mp3")

    with open("japanese-morse table.json","r") as f:
        morseTable = load(f)

    for letter in message:
        for signal in morseTable.get(letter,[]):

            if len(signal) > 0:
                morseAudio + = morseSignals[signal]
            else:
                break
        morseAudio += morse_space

    morseAudio.export(exportedMorseSignalsPath,format="mp3")
    return exportedMorseSignalsPath


app:object = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
    requestMessage:str = str(request.args.get("message"))
    print(requestMessage)
    morseAudioPath:str = japaneseToMorseSound_converter(requestMessage)


    return f"message is {requestMessage}"


if __name__ == "__main__":
    app.run(host="0.0.0.0")