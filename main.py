from pydub import AudioSegment
from flask import Flask, request, Response, send_file
from json import load
from packages.LineAPI import LineAPI

# from sys import exit
from time import sleep

from os import environ, getcwd
from os.path import join
from dotenv import load_dotenv

from packages.HiraganaConversionAPI import HiraganaConversionAPI
from packages.kanjiHiraganaConversionAPI import kanjiHiraganaConversionAPI

exportedMorseAudioName: str = "converted_morse_signals.mp3"
relativePath: str = str(join(getcwd(), exportedMorseAudioName))
absoluteAudioPath: str = "https://morse-signal-converter-bot.onrender.com" + relativePath
spaceSymbols: list = [" ", "　"]  # ! [english space, japanese space]


def load_env() -> tuple[str, str]:
    load_dotenv("/etc/secrets/.env")
    channelAccessToken: str = environ["channelAccessToken"]
    yahooClientID: str = environ["yahooClientID"]

    return channelAccessToken, yahooClientID


def japaneseToMorseSound_converter(message: str) -> tuple[str, int, str]:
    morseAudio: object = AudioSegment.silent(duration=0)
    morseTable: dict = {}
    singleUnitDuration: int = 60  # *0.001 sec

    print("loading morse signal assets")
    morse_long: object = AudioSegment.from_file("morse_long.mp3")  # !   0.18 sec
    morse_short: object = AudioSegment.from_file("morse_short.mp3")  # !  0.06 sec
    morseSignals: list = [morse_short, morse_long]
    morse_letterTransition: object = AudioSegment.silent(duration=singleUnitDuration * 2)  # ! 0.12 sec
    morse_space: object = AudioSegment.silent(duration=singleUnitDuration * 3)  # ! 0.18 sec

    print("loading japanese-morse conversion table")
    with open("japanese-morse_table.json", "r", encoding="utf-8") as f:
        morseTable = load(f)

    if not message:
        print("Request should not be blank")
        return None, None, "RequestMessageEmptyError"

    print(f"requestedMessage:{message}")

    for index, letter in enumerate(message):
        if letter in spaceSymbols:
            morseAudio += morse_space
            continue

        morseList: list = morseTable.get(letter, [])
        if len(morseList) == 0:
            print("Request text includes an invalid character")
            return None, None, f"InvalidCharacterError"

        print(f"Now generating morse signals for {letter}({index+1}/{len(message)})")
        for signal in morseList:
            try:
                morseAudio += morseSignals[signal]
            except Exception as e:
                print(f"interruption occured. Error:{e}")
                break
            morseAudio += morse_letterTransition

    audioDuration: int = len(morseAudio)
    morseAudio.export(exportedMorseAudioName, format="mp3")
    return exportedMorseAudioName, audioDuration, ""


app: object = Flask(__name__)


@app.route("/app_script/wakeup", methods=["GET"])
def wakeUpCallHandling():
    return Response(status=200)


@app.route(relativePath, methods=["GET", "POST"])
def returnMorseAudio():
    return send_file(exportedMorseAudioName, as_attachment=True)


@app.route("/", methods=["GET", "POST"])
def main():

    if request.method == "POST":
        channelAccessToken, yahooClientID = load_env()
        line: object = LineAPI()
        line.addCredentials(channelAccessToken)

        message, contentType = line.parse_POSTrequest(request.get_json())

        #! convert the requested message into the appropriate format
        kanjiConversion:object = kanjiHiraganaConversionAPI()
        hiraganaConversion:object = HiraganaConversionAPI()

        modifiedMessage:str = hiraganaConversion.katakana_hiragana_conversion(message)
        res, modifiedMessage = kanjiConversion.convertKanji_to_Hiragana(yahooClientID,modifiedMessage)

        if not res:
            line.addMessage_forReply(messageType="text",message=f"漢字ひらがな変換APIのリクエストが不正です。\nError:{modifiedMessage}")
            response: str = line.sendMessage()
            return

        morseAudioPath, audioDuration, error = japaneseToMorseSound_converter(modifiedMessage.upper())

        match error:
            case "RequestMessageEmptyError":
                line.addMessage_forReply(messageType="text", message="文章を打ち込んで下さい。")

            case "InvalidCharacterError":
                line.addMessage_forReply(messageType="text", message="認識できない文字が含まれています。")

            case _:
                line.addMessage_forReply(messageType="audio", contentURL=absoluteAudioPath, audioDuration=audioDuration)

        response: str = line.sendMessage()
        print(response)

    else:
        return "GET method is not available.\nTry POST method from the LINE official bot: 'https://lin.ee/zTGOWML'"

    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
