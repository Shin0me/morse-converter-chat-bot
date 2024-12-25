from pydub import AudioSegment
from flask import Flask,request,Response,send_file
from json import load


def japaneseToMorseSound_converter(message:str) -> str:
    exportedMorseSignalsPath:str = "converted_morse_signals.mp3"
    morseAudio:object = None
    morseTable:dict = {}
    
    print("loading morse signal assets")
    morse_long = AudioSegment.from_mp3("morse_long.mp3")
    morse_short = AudioSegment.from_mp3("morse_short.mp3")
    morseSignals:list = [morse_short,morse_long]
    morse_space = AudioSegment.from_mp3("morse_space.mp3")
    
    print("loading japanese-morse conversion table")
    with open("japanese-morse table.json","r") as f:
        morseTable = load(f)

    for index,letter in enumerate(message):
        print(f"Now generating morsw signals for {letter}({index+1}/{len(message)})")
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


    return send_file(morseAudioPath, as_attachment=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0")