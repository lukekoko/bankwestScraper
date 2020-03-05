import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import logging
import logging.config
from config import config

settings = config.settings
logging.config.fileConfig(
    config.settings["logger_config"], disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

chrome_options = Options()  
# chrome_options.add_argument("--headless")
chromeDriver = "./config/chromedriver"

login_page = "https://ibs.bankwest.com.au/BWLogin/rib.aspx"

def scraper():
    browser = webdriver.Chrome(executable_path=chromeDriver, options=chrome_options)
    browser.set_window_size(1080,1920)
    browser.get(login_page)

    browser.find_element_by_id("AuthUC_txtUserID").send_keys(settings['login'])
    browser.find_element_by_id("AuthUC_txtData").send_keys(settings['password'])
    browser.find_element_by_id("AuthUC_btnLogin").click()
    
    time.sleep(20)

if __name__ == "__main__":
    scraper()