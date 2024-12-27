import requests as req
from json import loads

class kanjiHiraganaConversionAPI:

    def __init__(self):
        pass

    def convertKanji_to_Hiragana(self,yahooClientID:str,text:str) -> tuple[bool,str]:
        apiURL:str = "https://jlp.yahooapis.jp/FuriganaService/V2/furigana?"
        header:dict = {
            "Content-Type":"application/json"
        }

        body:dict = {
            "id": "1234-1",
            "jsonrpc": "2.0",
            "method": "jlp.furiganaservice.furigana",
            "params": {
                "q": text,
                "grade": 1
            }
        }

        response:object = req.post(url= apiURL + "appid=" + yahooClientID, headers=header,json=body)
        responseJson:dict = loads(response.text)

        if "error" in responseJson:
            return False, responseJson["error"]["message"]

        if "Error" in responseJson:
            return False, responseJson["Error"]["Message"]


        return True, "".join([element.get("furigana",element["surface"]) for element in responseJson["result"]["word"]])


if __name__ == "__main__":
    kanjiConversion:object = kanjiHiraganaConversionAPI()
    res,convertedText = kanjiConversion.convertKanji_to_Hiragana("dj00aiZpPVM2VlRoYXFYSG51SSZzPWNvbnN1bWVyc2VjcmV0Jng9YWI-",input("here:").strip())
    print(res,convertedText)