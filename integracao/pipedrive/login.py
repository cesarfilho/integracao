from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from integracao.infraestructutre.driver import init_driver,close_driver
from integracao.login import Login
from time import sleep
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
        self.driver, self.pid = init_driver()
        self.wait = WebDriverWait(self.driver, 30)

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
        # _to_leads = '/html/body/div[1]/div/div[2]/nav/a[2]'
        # self.wait.until(ec.element_to_be_clickable((By.XPATH, _to_leads)))
        # self.driver.find_element_by_xpath(_to_leads).click()
        # add_lead = "//span[contains(text(),'Adicionar lead')]/ancestor::button"
        # self.wait.until(ec.element_to_be_clickable((By.XPATH, add_lead)))
        # self.driver.find_element_by_xpath(add_lead).click()
        self.openNewLead()
        self.saveLead()

    def openNewLead(self):
        _to_leads = '/html/body/div[1]/div/div[2]/nav/a[2]'
        self.wait.until(ec.element_to_be_clickable((By.XPATH, _to_leads)))
        self.driver.find_element_by_xpath(_to_leads).click()
        add_lead = "//span[contains(text(),'Adicionar lead')]/ancestor::button"
        self.wait.until(ec.element_to_be_clickable((By.XPATH, add_lead)))
        self.driver.find_element_by_xpath(add_lead).click()

    def saveLead(self):

        add_nome = '//*[@id="downshift-0-input"]'
        # _nome = f"//div[@class='cui4-input__box']/input"
        self.wait.until(ec.visibility_of_element_located((By.XPATH, add_nome)))
        nome = self.driver.find_element_by_xpath(add_nome)
        nome.send_keys("Cesar Filho")
        ##############################################
        add_telefone = '//div/h3'
        # self.wait.until(ec.visibility_of_element_located((By.XPATH, add_telefone)))
        telefone = self.driver.find_element_by_xpath(add_telefone)
        telefone.send_keys("4899606656")
        ##############################################
        add_email = '//div[text="E-mail"]//input'
        # _nome = f"//div[@class='cui4-input__box']/input"
        # self.wait.until(ec.visibility_of_element_located((By.XPATH, add_email)))
        email = self.driver.find_element_by_xpath(add_email)
        email.send_keys("cesarpamplonafilho@gmail.com")


        ##############################################
        # add_nome = '//*[@id="downshift-0-input"]'
        # _nome = f"//div[@class='cui4-input__box']/input"
        # self.wait.until(ec.visibility_of_element_located((By.XPATH, add_nome)))
        # nome = self.driver.find_element_by_xpath(add_nome)
        # nome.send_keys("Cesar Filho")
        pass



        # self.wait.until(ec.element_to_be_clickable((By.ID, _nome)))
        # self.driver.find_element_by_xpath(_nome).click()
        # add_lead = "//span[contains(text(),'Adicionar lead')]/ancestor::button"
        # self.wait.until(ec.element_to_be_clickable((By.XPATH, add_lead)))
        # self.driver.find_element_by_xpath(add_lead).click()
