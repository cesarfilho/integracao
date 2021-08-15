from lxml import html
import urllib
import json


class RDLead(object):

    def __init__(self, http):
        self.http = http

        self.URL_APP_END = "app.rdstation.com.br"
        self.URL_APP_BASE = f"https://{self.URL_APP_END}"
        self.URL_ACCOUNTS_END = "accounts.rdstation.com.br"
        self.URL_ACCOUNTS_BASE = f"https://{self.URL_ACCOUNTS_END}"
        self.URL_APP_LOGIN = f"{self.URL_APP_BASE}/login"
        self.URL_APP_HOME = f"{self.URL_APP_BASE}/home"
        self.URL_APP_CALBACK = f"{self.URL_APP_BASE}/auth/callback"
        self.URL_APP_PAGE_LEADS = f"{self.URL_APP_BASE}/leads"
        self.URL_APP_PAGE_SUBMIT_INICIAL = f"{self.URL_APP_BASE}/leads/novo"

        self.page_new_lead = None

    def getPageNewLead(self):

        self.http.updateHeader(self.getHeader())
        self.http.updateHeader({
            "Host": self.URL_ACCOUNTS_END,
            "Referer": f"{self.URL_ACCOUNTS_BASE}/?locale=pt-BR"
        })
        _subscritions = self.http.buscar(url=f"{self.URL_ACCOUNTS_BASE}/subscriptions", allow_redirects=False)
        ##################
        root = html.fromstring(self.http.responseData(_subscritions))
        link = self.get_link(root)
        self.http.updateHeader(self.getHeader())
        self.http.updateHeader({
            "Host": self.URL_APP_END,
            "Referer": f"{self.URL_ACCOUNTS_BASE}/subscriptions"
        })
        _marketing = self.http.buscar(url=f"{link}", allow_redirects=False)
        ##############################
        self.http.updateHeader(self.getHeader())
        link = _marketing.headers._store["location"][1]
        self.http.updateHeader({
            "Host": self.URL_APP_END,
            "Referer": f"{self.URL_ACCOUNTS_BASE}/subscriptions"
        })
        _login = self.http.buscar(url=f"{link}", allow_redirects=False)
        ################################
        self.http.updateHeader(self.getHeader())
        link = urllib.parse.unquote(_login.headers._store["location"][1])
        self.http.updateHeader({
            "Host": self.URL_ACCOUNTS_END,
            "Referer": f"{self.URL_ACCOUNTS_BASE}/subscriptions"
        })
        _callback = self.http.buscar(url=f"{link}", allow_redirects=False)
        #####################################
        link = urllib.parse.unquote(_callback.headers._store["location"][1])
        self.http.updateHeader({
            "Host": self.URL_APP_END,
            "Referer": f"{self.URL_ACCOUNTS_BASE}/subscriptions"
        })
        _conta = self.http.buscar(url=f"{link}", allow_redirects=False)

        ##################################
        link = urllib.parse.unquote(_conta.headers._store["location"][1])
        _home = self.http.buscar(url=f"{link}", allow_redirects=False)

        self.http.updateHeader({
            "Host": self.URL_APP_END,
            "Referer": f"{self.URL_APP_PAGE_LEADS}"
        })

        _novo = self.http.buscar(url=self.URL_APP_PAGE_SUBMIT_INICIAL, allow_redirects=False)
        self.page_new_lead = _novo
        return self.http.responseData(_novo)

    def get_link(self, root):
        link = root.xpath(".//ul/li/a[contains(text(),'Acessar Marketing')]")[0].attrib["href"]
        return link

    def getHeader(self):
        return {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip,deflate,br",
            "Content-Type": "application/json",
            "DNT": "1"
        }

    def saveLead(self):
        root = html.fromstring(self.http.responseData(self.page_new_lead))
        authenticity_token = self.get_auth_token(root)

        payload = {
            "utf8": urllib.parse.unquote("%E2%9C%93"),
            "authenticity_token": f"{authenticity_token}",
            "source": "teste02",
            "lead[name]": "Cesar+Filho2",
            "lead[email]": "cesarpamplonafilho2@gmail.com",
            "lead[job_title]": "",
            "lead[lead_info_attributes][personal_phone]": "48996069487",
            "lead[lead_info_attributes][mobile_phone]": "",
            "lead[lead_info_attributes][twitter]": "",
            "lead[lead_info_attributes][facebook]":	"",
            "lead[lead_info_attributes][linkedin]": "",
            "lead[lead_info_attributes][website]": "",
            "lead[uf]":	"",
            "lead[open_city]": "",
            "lead[company_attributes][leads_manager_id]": "362843",
            "lead[company_attributes][name]": "",
            "lead[company_attributes][company_sector_id]": "",
            "lead[company_attributes][size]": "",
            "lead[company_attributes][email]": "",
            "lead[company_attributes][site]": "",
            "lead[company_attributes][twitter]": "",
            "lead[company_attributes][facebook]": "",
            "lead[company_attributes][phone]":	"",
            "lead[company_attributes][address]": "",
            "lead[user_id]": "",
            "lead[bio]": "",
            "commit": "Salvar",
        }
        self.http.updateHeader(self.getHeader())
        self.http.updateHeader({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Host": self.URL_APP_END,
            "Origin": self.URL_APP_BASE,
            "Referer": f"{self.URL_APP_PAGE_SUBMIT_INICIAL}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1"
        })
        del self.http.http.headers._store['x-csrf-token']

        _novo = self.http.enviar(url=self.URL_APP_PAGE_LEADS, data=payload, allow_redirects=False)
        print(_novo)

    def get_auth_token(self, root):
        authenticity_token = root.xpath(".//form/input[contains(@name,'authenticity_token')]")[0].attrib["value"]
        return authenticity_token


