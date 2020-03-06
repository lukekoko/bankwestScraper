from config import config
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import logging
import logging.config
import pathlib
import pandas as pd
import numpy as np
import sqlalchemy
import sys

# setting up logging
settings = config.settings
logging.config.fileConfig(
    config.settings["logger_config"], disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

def browserConfig():
    logger.info("Configuring browser")
    # adding options to web browser
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    # create download folder if doesn't exist
    pathlib.Path('./downloads/').mkdir(exist_ok=True)
    prefs = {
        'download.default_directory' : str(pathlib.Path('./downloads/').resolve()),
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chromeDriver = settings['chrome_driver']

    browser = webdriver.Chrome(executable_path=chromeDriver, options=chrome_options)
    return browser

def scraper():
    logger.info("Starting scraper")
    browser = browserConfig()
    browser.set_window_size(1024,768)
    browser.get(settings['url'])

    logger.info("Logging in")
    browser.find_element_by_id("AuthUC_txtUserID").send_keys(settings['login'])
    browser.find_element_by_id("AuthUC_txtData").send_keys(settings['password'])
    browser.find_element_by_id("AuthUC_btnLogin").click()

    browser.find_element_by_link_text(settings['account']).click()

    logger.info("Downloading")
    browser.find_element_by_id("_ctl0_ContentButtonsRight_btnExport").send_keys(Keys.ENTER)
    logger.info("Download finished")
    time.sleep(5)

def readCSV():
    logger.info("Starting read csv")
    csvFiles = pathlib.Path('./downloads').glob("*.csv")
    transactionsToRemove = ['NAR', 'TFC', 'TFD']
    columns = ['account', 'date', 'description', 'transactionType', 'balance', 'transactionAmount']
    transactionTypes = {
        'WDC': 'Debit',
        'WDL': 'Debit', 
        'DEP': 'Credit',
        'WDI': 'Debit'
    }
    for file in csvFiles:
        logger.info('Reading csv file: {}'.format(str(file).split('\\')[1]))
        initDF = pd.read_csv(file)
        logger.info('Processing data')
        # renaming column names
        initDF.rename(columns = {'Transaction Date': 'date', 'Narration': 'description', 'Transaction Type': 'transactionType', 'Balance': 'balance'}, inplace=True)
        # removing unneeded transactions
        df = initDF[~initDF['transactionType'].isin(transactionsToRemove)]
        # mapping transaction codes with names
        df = df.replace({'transactionType': transactionTypes})
        # creating new columns for account, ammount and converting date to datetime object
        df['account'] = df['BSB Number'] + ' ' + df['Account Number'].astype(str)
        df['transactionAmount'] = df[['transactionType', 'Debit', 'Credit']].apply(transactionTypeCheck, axis=1)
        df['date'] = pd.to_datetime(df['date'])
        # filtering based on needed columns
        exportDF = df[columns]
        # Inserting data into database
        successful = insertIntoDB(exportDF)
        if successful:
            logger.info('Removing csv file')
            file.unlink()
        else:
            logger.error('Data was not imported')


def transactionTypeCheck(row):
    # checking for type of transaction
    if (row['transactionType'] == 'Debit'):
        return row['Debit']
    else:
        return row['Credit']

def insertIntoDB(df):
    try:
        logger.info('Connecting to database')
        connectionString = '{}://{}:{}@{}:{}/{}'.format(settings['sql_type'], settings['sql_user'], settings['sql_pass'], settings['sql_host'], settings['sql_port'], settings['sql_database'])
        engine = sqlalchemy.create_engine(connectionString)
        engine.connect()
    except sqlalchemy.exc.OperationalError:
        logger.error('Could not connect to database')
        return False
    try: 
        logger.info('Inserting data into database')
        # inserting dataframe into temp database table
        df.to_sql('temp', engine, if_exists='replace', index=False)
        with engine.begin() as conn:
            # query to insert temp table into main transactions table to ensure no duplicate entries are entered
            sqlQuery = """
                INSERT INTO transactions (account, date, description, transactionType, balance, transactionAmount)
                SELECT t1.account, t1.date, t1.description, t1.transactionType, t1.balance, t1.transactionAmount FROM temp t1 WHERE NOT EXISTS 
                (SELECT 1 FROM transactions t2 WHERE t1.date = t2.date AND t1.description = t2.description AND t1.balance = t2.balance AND t1.transactionAmount = t2.transactionAmount)
            """
            conn.execute(sqlQuery)
        return True
    except (sqlalchemy.exc.OperationalError, sqlalchemy.exc.IntegrityError):
        logger.error('Could not insert into database')
        return False

if __name__ == "__main__":
    scraper()
    readCSV()