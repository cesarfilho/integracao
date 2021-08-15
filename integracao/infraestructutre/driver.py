import logging
import os
import random
import tempfile
from time import time
from seleniumwire import webdriver
from selenium.webdriver.common import service
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_binary

logger = logging.getLogger(__name__)


def init_driver(pid=None, *args, **kwargs):
    """
    if debug:
        driver = webdriver.Chrome()
        return driver, driver.service.process.pid
        # return webdriver.Chrome()
    """
    try:
        if pid is not None:
            os.system('kill -9 {}'.format(pid))
    except Exception as e:
        print(e)
    finally:
        print("############################ INICIANDO DRIVER #############################")
        _path = os.getcwd()
        chrome_options = webdriver.ChromeOptions()
        # display = Display(size=(1024, 768), visible=True)
        # display.start()
        download_dir = "/tmp/crawler_docs"
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                   "download.default_directory": download_dir,
                   "download.extensions_to_open": "applications/pdf",
                   'plugins.plugins_disabled': ['Chrome PDF Viewer'],
                   'plugins.always_open_pdf_externally': True}
        chrome_options.add_experimental_option("prefs", profile)
        chrome_options.add_argument('--no-sandbox')
        options = {}
        proxy = random.choice([True, False, True, True, True, False])

        # chrome_options.add_argument(f'--proxy-server={ProxyMesh().get_proxy()["http"]}')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--window-size=1920x1080')
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--log-level=0")
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--disable-gpu')

        try:
            print(_path)
            path = "/home/cesarfilho/miniconda3/envs/franq/lib/python3.9/site-packages/chromedriver_binary/chromedriver"
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
            # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/home/johann/chromedriver",
            #                           seleniumwire_options=options, )

        except Exception as err:
            print(err)
            raise err
        return driver, driver.service.process.pid

def dispose_driver(driver):
    driver.quit()


def close_driver(driver):
    driver.close()


def check_webdriver_reachable(driver, callback=None, pid=None, *args, **kwargs):
    try:
        e = driver.current_url
        logger.info('Driver is reachable with current url at ' + str(e))
        return driver, driver.service.process.pid
    except Exception as e:
        logger.warning("Selenium WebDriver not recheable. Restarting... {}".format(e))
        driver, pid = init_driver(pid=pid)
        if callback is not None:
            callback(driver)
        return driver, pid


def driver_ready(driver):
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')


def reset_driver(driver, callback=None):
    try:
        close_driver(driver)
    except Exception as e:
        logger.warning("Selenium WebDriver could not close... Error: {}".format(e))
    finally:
        driver = init_driver()
        if callback is not None:
            callback(driver)
        return driver


class Service(service.Service):
    """
    Object that manages the starting and stopping of PhantomJS
    """
    def __init__(self, executable_path, port=0, service_args=None, log_path=None):
        """
        Creates a new instance of the Service

        :Args:
         - executable_path : Path to PhantomJS binary
         - port : Port the service is running on
         - service_args : A List of other command line options to pass to PhantomJS
         - log_path: Path for PhantomJS service to log to
        """
        self.service_args = service_args
        if self.service_args is None:
            self.service_args = []
        else:
            self.service_args = service_args[:]
        if not log_path:
            log_path = "ghostdriver.log"
        if not self._args_contain("--cookies-file="):
            self._cookie_temp_file_handle, self._cookie_temp_file = tempfile.mkstemp()
            self.service_args.append(
                "--cookies-file=" + self._cookie_temp_file)
        else:
            self._cookie_temp_file = None

        service.Service.__init__(
            self, executable_path, port=port, log_file=open(log_path, 'w'))

    def _args_contain(self, arg):
        return len(list(filter(lambda x: x.startswith(arg), self.service_args))) > 0

    def command_line_args(self):
        return self.service_args + ["--webdriver=%d" % self.port]

    @property
    def service_url(self):
        """
        Gets the url of the GhostDriver Service
        """
        return "http://localhost:%d/wd/hub" % self.port

    def send_remote_shutdown_command(self):
        if self._cookie_temp_file:
            os.close(self._cookie_temp_file_handle)
            os.remove(self._cookie_temp_file)


class WebDriverService(RemoteWebDriver):
    def __init__(self, command_executor=None, capabilities=None, debug=False):
        if command_executor is None:
            command_executor = "http://localhost:4444/wd/hub"

        if capabilities is None:
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            # options.add_argument("--disable-gpu")
            options.add_argument("--screen-size=1200x800")
            options.add_argument("--enableVNC=true")
            capabilities = options.to_capabilities()

        super().__init__(command_executor=command_executor, desired_capabilities=capabilities)


    def wait_for_page_load(self, timeout=30):
        init = time()
        status = 'loading'
        while status != 'complete':
            status = self.execute_script("return document.readyState;")
            if (time() - init) > timeout:
                raise Exception("timed out while waiting for page to load")
