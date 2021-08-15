from integracao.login import Login
from lxml import html
import json


class PipeLogin(Login):

    def __init__(self, http):
        super().__init__()
        self.URL_APP_BASE = "app.pipedrive.com"
        self.URL_BASE = "https://app.pipedrive.com/auth/login/"
        self.URL_LOGIN = f"{self.URL_BASE}#?locale=pt"
        self.URLDOLOGIN = f"{self.URL_BASE}api/v1/login"
        self.http = http

    def doLogin(self):
        self.http.updateHeader(self.getHeader())
        root = html.fromstring(self.actualPage)
        hash = self.get_hash(root)
        verify = self.get_verify(root)
        self.http.updateHeader({
            "host": self.URL_APP_BASE
        })
        payload = {
            "hash": f"{hash}",
            "pipe-verify": f"{verify}",
            "login": "cesarpamplonafilho@gmail.com",
            "password": "Pass@tk@1010"
        }
        _r = self.http.enviar(url=self.URLDOLOGIN, data=payload)
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

    def get_hash(self, root):
        hash = ''
        lista_meta = root.xpath(".//input[contains(@name,'hash')]")
        for item in lista_meta:
            if 'csrf-token' in item.attrib['name']:
                token = item.attrib['content']
                break
        return token
        pass

    def get_verify(self, root):
        pass
