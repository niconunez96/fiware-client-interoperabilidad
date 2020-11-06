from datetime import datetime
import requests


class FiwareApi:
    HEADERS = {'fiware-service': "openiot", 'fiware-servicepath': "/"}

    def post(self, buffer):
        data = buffer[buffer.find('#') + 1: buffer.find('\\')]
        buffer = buffer[2:buffer.find('#')]
        try:
            r = requests.post(buffer, data)
            pastebin_url = r.text
            if len(pastebin_url) == 0:
                print("{} POST  {}  Data: {}".format(datetime.now(), r, data))
                return "POST['{}']".format(data)
            else:
                print("{} Post Error: {}".format(datetime.now(), pastebin_url))
                return "POST|Error"
        except Exception:
            print("{} Hubo un error en la operación POST", datetime.now())
            return "POST|Error"

    def get(self, buffer):
        try:
            r = requests.get(
                url=buffer[2:buffer.find('\\')],
                headers=self.HEADERS,
            )
            pastebin_url = str(r.json())
            print("{} GET  {}  Data: {}".format(
                datetime.now(), r, pastebin_url,
            ))
            if(str(r).find("[200]") >= 0):
                return "GET{}".format(pastebin_url)
            else:
                return 'GET|Error'
        except Exception:
            print("Hubo un error en la operación GET")
            return "GET|Error"
