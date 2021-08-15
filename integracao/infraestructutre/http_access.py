import requests
import random
from integracao.infraestructutre.agents import agents_list

class HttpAccess(object):

    def __init__(self):
        self.http = requests.Session()
        self.updateHeader({"user-agent": agents_list[random.randrange(len(agents_list))]})

    def buscar(self, url, allow_redirects=True,verify=False):
        try:
            return self.http.get(url=url, verify=verify, allow_redirects=allow_redirects)
        except Exception as e:
            print(e)

    def enviar(self, url, data, allow_redirects=True,verify=False):
        try:
            self.updateHeader({"user-agent": agents_list[random.randrange(len(agents_list))]})
            # if isinstance(data, dict):
            #     return self.http.post(url=url, json=data, verify=verify, allow_redirects=allow_redirects)
            # else:
            return self.http.post(url=url, data=data, verify=verify, allow_redirects=allow_redirects)
        except Exception as e:
            print(e)

    def updateHeader(self, dados):
        if isinstance(dados, dict):
            self.http.headers.update(dados)
        else:
            raise "Error data"

    def responseData(self, rootHtml):
        if "text" in rootHtml.headers._store["content-type"][1]:
            return rootHtml.text
        elif "json" in rootHtml.headers._store["content-type"][1]:
            return rootHtml.text
        else:
            return rootHtml.content