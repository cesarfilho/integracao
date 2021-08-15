

class Login(object):

    def __init__(self):
        self.actualPage = None

    def doLogin(self):
        _r = self.http.enviar(self.URL_LOGIN)
        return _r

    def pageLogin(self):
        try:
            _r = self.http.buscar(self.URL_LOGIN)
            self.actualPage = self.http.responseData(_r)
        except Exception as e:
            print(e)
            return False

        return True

    def login(self):
        # self.pageLogin()
        self.doLogin()





