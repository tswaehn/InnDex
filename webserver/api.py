from datetime import datetime
import json

class API:

    content = ""

    def __init__(self, content):
        self.content = content.decode('utf-8')

    def __runJSON(self):
        text = ""

        try:
            jsonObj = json.loads(self.content)

            if 'command' in jsonObj:
                text += self.__exec( jsonObj['command'])
            else:
                text += "no command found"
        except:
            text = 'request error'

        return text

    def run(self):

        text = "hello world<br>"

        text += self.__get_timstamp()
        text += self.__dbg_request()

        data = self.__runJSON()
        jsonData = {'log': text, 'data': data}
        jsonStr = json.dumps(jsonData)

        print(jsonStr)
        return jsonStr

    def __get_timstamp(self):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        return "<p>" + timestampStr + "</p>"

    def __dbg_request(self):
        text = "<p>"
        text += self.content
        text += "</p>"
        return text

    def __exec(self, command):

        text = ""
        text += "trying to execute " + command
        cmds = {
            'config': self.__cmd_read_config
        }
        func = cmds.get(command, self.__cmd_invalid)
        text += func()
        return text


    def __cmd_invalid(self):
        return "invalid cmd"

    def __cmd_read_config(self):
        return "read config"
