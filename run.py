from integracao.infraestructutre.http_access import HttpAccess
from integracao.rdstation.login import RDLogin
from integracao.rdstation.lead import RDLead
from integracao.pipedrive.login import PipeLogin

http = HttpAccess()

class AutomacaoLead(object):

    def logarSistemas(self):
        # rdlogin = RDLogin(http)
        # rdlogin.login()

        dados = {
            "nome": "Jose Pinto Coelho",
            "email": "cesarpamplonafiho@gmail.com",
            "telefone": "4878451221"
        }
        pplogin = PipeLogin(http, dados)
        pplogin.delete()
        # pplogin.saveAndDelete()



    def submetInformacoesIniciais(self):
        pass
        # sub = RDLead(http)
        # sub.getPageNewLead()
        # sub.saveLead()



    def run(self):
        self.logarSistemas()
        self.submetInformacoesIniciais()

if __name__ == "__main__":
    aut = AutomacaoLead()
    aut.run()