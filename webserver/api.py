from datetime import datetime

class API:

    def __init__(self, content):
        self.content = content.decode('utf-8')

    def runJSON(self, json_request):

        return

    def run(self):

        text = "hello world<br>"

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

        text += timestampStr + "<br>"
        text += "<p>"
        text += self.content
        text += "</p>"
        return text


