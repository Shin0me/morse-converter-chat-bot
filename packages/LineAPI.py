import requests as req

replyUrl:str = "https://api.line.me/v2/bot/message/reply"

class LineAPI:

    def __init__(self):
        pass

    def parse_POSTrequest(self,requestData:dict) -> tuple[str,str,str]:

        event:dict = requestData.get("events",[{}])[0]

        contentProvider:str = event["message"].get("type","")
        message:str = event["message"].get("text","None").strip()
        messageType:str = event.get("type","")
        self.replyToken:str  = event.get("replyToken","None")

        self.body:dict = {
            "replyToken":self.replyToken,
        }

        return message,messageType,contentProvider

    def fetchRecievedFiles(self):
        pass


    def addCredentials(self,channelAccessToken:str) -> None:
        self.channelAccessToken = channelAccessToken

        self.header = {
        "Content-Type":"application/json",
        "Authorization":"Bearer " + self.channelAccessToken,
        }


    def addMessage_forReply(self,messageType:str,message:str = "", contentURL:str = "",audioDuration:int= 1000) -> None:

        match messageType.lower():
            case "text":
                self.body["message"] = ({
                    [
                {
                    "type":"text",
                    "text":message
                }   ]})

            case "audio":
                self.body["message"] = ({
                    "type": "audio",
                    "originalContentUrl": contentURL,
                    "duration": audioDuration
                    })


    def sendMessage(self) -> str:
        response = req.post(url=replyUrl,headers=self.header,json=self.body)
        return response.text

if __name__ == "__main__":
    line:object = LineAPI()
    line.addMessage_forReply(messageType="Audio",contentURL="hello",audioDuration=3000)