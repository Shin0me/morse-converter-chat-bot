from pydub import AudioSegment
from flask import Flask,request,Response
from json import load

app:object = Flask(__name__)

def japaneseToMorseSound_converter(message:str) -> str:
    morse_long = AudioSegment.from_mp3("morse_long.mp3")
    morse_short = AudioSegment.from_mp3("morse_short.mp3")
    morseSounds:list = [morse_short,morse_long]
    morse_space = AudioSegment.from_mp3("morse_space.mp3")
    convertedFile:object = None
    morseTable:dict = {}

    with open("japanese-morse table.json","r") as f:
        morseTable = load(f)


    for letter in message:
        for signal in morseTable.get(letter,""):
            pass



@app.route("/",methods=["GET","POST"])
def main():
    requestMessage:str = str(request.args.get("message"))
    print(requestMessage)
    japaneseToMorseSound_converter(requestMessage)


    return f"message is {requestMessage}"


if __name__ == "__main__":
    app.run(host="0.0.0.0")