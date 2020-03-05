import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import logging
import logging.config
import pathlib
from config import config
import pandas as pd

settings = config.settings
logging.config.fileConfig(
    config.settings["logger_config"], disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

def browserConfig():
    logger.info("Configuring browser")
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    prefs = {
        'download.default_directory' : str(pathlib.Path('./downloads/').resolve()),
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chromeDriver = "./config/chromedriver"

    browser = webdriver.Chrome(executable_path=chromeDriver, options=chrome_options)
    browser.set_window_size(1080,1920)
    return browser

def scraper():
    logger.info("Starting")
    browser = browserConfig()
    browser.get(settings['url'])

    logger.info("Logging in")
    browser.find_element_by_id("AuthUC_txtUserID").send_keys(settings['login'])
    browser.find_element_by_id("AuthUC_txtData").send_keys(settings['password'])
    browser.find_element_by_id("AuthUC_btnLogin").click()

    browser.find_element_by_link_text(settings['account']).click()
    browser.find_element_by_tag_name('html').send_keys(Keys.END)

    logger.info("Downloading")
    browser.find_element_by_id("_ctl0_ContentButtonsRight_btnExport").click()
    logger.info("Download finished")
    time.sleep(5)

def readCSV():
    csvFiles = pathlib.Path('./downloads').glob("*.csv")
    removeList = ['NAR', 'TFC', 'TFD']
    columns = ['Transaction Date', 'Narration', 'Debit', 'Credit', 'Balance', 'Transaction Type']
    for file in csvFiles:
        initDF = pd.read_csv(file)
        filteredDF = initDF[columns]
        df = filteredDF[~filteredDF['Transaction Type'].isin(removeList)]
        print(df['Credit'].sum())

if __name__ == "__main__":
    # scraper()
    readCSV()