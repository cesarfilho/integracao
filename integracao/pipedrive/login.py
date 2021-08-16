from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from integracao.infraestructutre.driver import init_driver,close_driver
from integracao.login import Login
from time import sleep
from lxml import html
import json


class PipeLogin(Login):

    def __init__(self, http,dados):
        super().__init__()
        self.URL_APP_BASE = "app.pipedrive.com"
        self.URL_BASE = "https://app.pipedrive.com/auth/login/"
        self.URL_LOGIN = f"{self.URL_BASE}#?locale=pt"
        self.URLDOLOGIN = f"{self.URL_BASE}api/v1/login"
        self.http = http
        self.driver, self.pid = init_driver()
        self.wait = WebDriverWait(self.driver, 30)
        self.dados = dados

    def doLogin(self):
        self.driver.maximize_window()
        self.driver.get(self.URL_BASE)
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@name='login']")))
        username = self.driver.find_element_by_xpath("//input[@name='login']")
        password = self.driver.find_element_by_xpath("//input[@name='password']")

        username.send_keys("cesarpamplonafilho@gmail.com")
        password.send_keys("pass@tk@1010")
        self.wait.until(ec.element_to_be_clickable((By.NAME, 'submit')))
        self.driver.find_element_by_name('submit').click()

    def opensLeads(self):
        _to_leads = '/html/body/div[1]/div/div[2]/nav/a[2]'
        self.wait.until(ec.element_to_be_clickable((By.XPATH, _to_leads)))
        self.driver.find_element_by_xpath(_to_leads).click()

    def openNewLead(self):

        add_lead = "//span[contains(text(),'Adicionar lead')]/ancestor::button"
        self.wait.until(ec.element_to_be_clickable((By.XPATH, add_lead)))
        self.driver.find_element_by_xpath(add_lead).click()

    def saveNewLead(self):
        self.openNewLead()
        add_nome = '//*[@id="downshift-0-input"]'
        # _nome = f"//div[@class='cui4-input__box']/input"
        self.wait.until(ec.visibility_of_element_located((By.XPATH, add_nome)))
        self.driver.find_element_by_xpath(add_nome).send_keys(self.dados["nome"])
        print("nome passou!")
        ##############################################
        sleep(3)
        add_telefone = '//div[@data-test-key="phone"]//input'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, add_telefone)))
        self.driver.find_element_by_xpath(add_telefone).send_keys(self.dados["telefone"])
        print("telefone passou!")
        ##############################################
        add_email = '//div[@data-test-key="email"]//input'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, add_email)))
        self.driver.find_element_by_xpath(add_email).send_keys(self.dados["email"])
        print("email passou!")
        ##############################################
        _submit = '//button[@data-test="add-modals-save"]'
        self.driver.find_element_by_xpath(_submit).click()
        print("salvando!!")

        pass

    def filterLead(self):
        _filter = f"Lead {self.dados['nome']}"
        selbox = f'//div[contains(text(),"{_filter}")]'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, selbox)))
        self.driver.find_element_by_xpath(selbox).click()
        print("selecionou!")

    def excluirLead(self):
        _filter = "@data-testid='MenuLeadActions_Button'"
        _selOption = f"//span[{_filter}]/button"
        self.wait.until(ec.visibility_of_element_located((By.XPATH, _selOption)))
        self.driver.find_element_by_xpath(_selOption).click()
        # print("abriu opções")
        # sleep(1)
        _filter = "text(),'Excluir lead'"
        _selExcluir = f"//span[contains({_filter})]"
        self.wait.until(ec.visibility_of_element_located((By.XPATH, _selExcluir)))
        self.driver.find_element_by_xpath(_selExcluir).click()
        # print("abriu Excluir")
        # sleep(1)
        _filter1 = 'Tem certeza de que deseja excluir este lead?'
        _filter2 = "//button[contains(text(),'Excluir')]"
        _filter3 =f"//*[text()='Excluir']"
        _filter4 =f"//*[text()='{_filter1}']"

        # self.wait.until(ec.visibility_of_element_located((By.XPATH, _filter4)))
        self.driver.find_element_by_xpath(_filter3).click()
        print("confirma Excluir")

        print("se foi!")


    def save(self):
        self.doLogin()
        self.opensLeads()
        self.openNewLead()
        self.saveNewLead()

    def delete(self):
        self.doLogin()
        self.opensLeads()
        self.filterLead()
        self.excluirLead()

    def saveAndDelete(self):
        self.doLogin()
        self.opensLeads()
        self.openNewLead()
        self.saveNewLead()
        self.opensLeads()
        self.filterLead()
        self.excluirLead()


        # self.wait.until(ec.element_to_be_clickable((By.ID, _nome)))
        # self.driver.find_element_by_xpath(_nome).click()
        # add_lead = "//span[contains(text(),'Adicionar lead')]/ancestor::button"
        # self.wait.until(ec.element_to_be_clickable((By.XPATH, add_lead)))
        # self.driver.find_element_by_xpath(add_lead).click()

