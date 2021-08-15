from integracao.login import Login
from lxml import html
import json


class RDLogin(Login):

    def __init__(self, http):
        super().__init__()
        self.URL_BASE = "https://accounts.rdstation.com.br/"
        self.URL_LOGIN = f"{self.URL_BASE}#?locale=pt"
        self.URLDOLOGIN = f"{self.URL_BASE}api/v1/login"
        self.http = http

    def doLogin(self):
        self.http.updateHeader(self.getHeader())
        root = html.fromstring(self.actualPage)
        token = self.get_csrf_token(root)
        self.http.updateHeader({"X-CSRF-TOKEN":token})
        payload = {
            "email": "cesarpamplonafilho@gmail.com",
            "password": "Pass@tk@1010"
        }
        _r = self.http.enviar(url=self.URLDOLOGIN, data=json.dumps(payload))
        return True


    def getHeader(self):
        return {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Host": "accounts.rdstation.com.br",
            "Origin": "https://accounts.rdstation.com.br",
            "Referer": "https://accounts.rdstation.com.br/",
            "DNT": "1",
        }

    def get_csrf_token(self, root):
        token = ''
        lista_meta = root.xpath(".//meta")
        for item in lista_meta:
            if 'csrf-token' in item.attrib['name']:
                token = item.attrib['content']
                break
        return token
