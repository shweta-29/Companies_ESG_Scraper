""" CSR HUB website Scrape

This script allows the user to scrape the companies' CSR ratings from
the CSR HUB website. Website link: "https://www.csrhub.com/search/name/"

This tool accepts Company's names list in comma separated value
file (.csv) format as input.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

The output is a .csv file with Company name and its corresponding CSR ratings
"""

import pandas as pd
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
from .scraper import WebScraper


def _append_dict() -> dict:
    ''' Append the CSR dictionary with Company Name and its CSR score
    Returns
    -------
    dict
        The CSR dictionary
    '''
    try:
        csr_score = bot.find_element(
            '//*[@id="wrapper"]/div[3]/section[3]/div[2]/table/tbody/tr[2]/td[2]')
        csr['CSR_Ratings'].append(csr_score.text)
        company = bot.find_element(
            '//*[@id="wrapper"]/div[3]/section[3]/div[2]/table/tbody/tr[2]/td[1]/a')
        csr['CSR_Company'].append(company.text)

    except NoSuchElementException:
        bot.append_empty_values(csr)
    return csr


# Read input companies dataset

companies_filename = WebScraper._get_filename()
header_name = WebScraper._get_headername()
export_path = WebScraper._get_exportpath()
df = pd.read_csv(companies_filename)
data_length = len(df)


# Set up driver
URL = "https://www.csrhub.com/search/name/"
bot = WebScraper(URL)

# Accept cookies
cookies_xpath = '//*[@id="body-content-holder"]/div[2]/div/span[2]/button'
bot.accept_cookies(cookies_xpath)

# Scrape the website. Extract company names and their respective CSR score
i = 0
progress_bar = tqdm(total=data_length)
while i < data_length:
    csr = {'CSR_Company': [], 'CSR_Ratings': []}
    delay = 2  # seconds

    try:
        search_bar = bot.send_request_to_search_bar(
            header_name, df, i, xpath='//*[@id="search_company_names_0"]')
        search_bar.send_keys(Keys.RETURN)
        sleep(1)
        csr = _append_dict()
        # Save the data into a csv file
        df1 = bot.convert_dict_to_csv(csr, export_path)
        i += 1
    # If no element found, the page is restarted
    except NoSuchElementException:
        bot = bot.restart_driver(cookies_xpath)

    sleep(0.1)
    progress_bar.update(1)

progress_bar.close()
