""" S&P Global website Scrape

This script allows the user to scrape the companies' ESG ratings from the S&P
Global website
Website link: "https://www.spglobal.com/esg/scores/"

This tool accepts Company's names list in comma separated value
file (.csv) format as input.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

The output is a .csv file with Company name and its corresponding ESG ratings
"""

import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tqdm import tqdm
from .scraper import WebScraper


def append_dict(temp: str) -> str:
    ''' Append the dictionary with Company name, Industry, Country, Ticker\
    and ESG rating

    Parameters
    ----------
    temp : str
    The previous company name appended to the dictionary

    Returns
    -------
    str
        The latest company name appended to the dictionary
    '''
    if temp == ESG_Company:
        bot.append_empty_values(SnP)

    else:
        ESG_Score = bot.find_element(xpath)
        SnP["SnP_ESG_Score"].append(ESG_Score.text)
        SnP["SnP_ESG_Company"].append(ESG_Company.text)
        ESG_Country = bot.find_element('//*[@id="company-country"]')
        SnP["SnP_ESG_Country"].append(ESG_Country.text)
        ESG_Industry = bot.find_element('//*[@id="company-industry"]')
        SnP["SnP_ESG_Industry"].append(ESG_Industry.text)
        ESG_Ticker = bot.find_element('//*[@id="company-ticker"]')
        SnP["SnP_ESG_Ticker"].append(ESG_Ticker.text)
        temp = ESG_Company
        return temp


# Read input companies dataset
companies_filename = WebScraper._get_filename()
header_name = WebScraper._get_headername()
export_path = WebScraper._get_exportpath()
df = pd.read_csv(companies_filename)
data_length = len(df)

# Set up driver
URL = "https://www.spglobal.com/esg/scores/"
bot = WebScraper(URL)

# Accept cookies
cookies_xpath = '//*[@id="onetrust-accept-btn-handler"]'
bot.accept_cookies(cookies_xpath)

# Scrape the website. Extract company names and their respective ESG score
temp = 0
for i in tqdm(range(data_length)):
    SnP = {'SnP_ESG_Company': [], 'SnP_ESG_Score': [],
           'SnP_ESG_Country': [], 'SnP_ESG_Industry': [], 'SnP_ESG_Ticker': []}

    try:
        # Starting the search by finding the search bar and searching for the
        #  company
        search_bar = bot.send_request_to_search_bar(
            header_name, df, i, class_name='banner-search__input')
        search_bar.send_keys(Keys.RETURN)
        sleep(4)
        xpath = '//*[@id="esg-score"]'
        bot.wait_element_to_load(xpath)
        ESG_Company = bot.find_element('//*[@id="company-name"]')
        temp = append_dict(temp)

    except NoSuchElementException:
        bot.append_empty_values(SnP)

    df1 = bot.convert_dict_to_csv(SnP, export_path)
