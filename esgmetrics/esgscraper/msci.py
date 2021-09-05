"""
MSCI website Scrape

This script allows the user to scrape the companies' ESG ratings from the MSCI
website. Website link:
"https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/"

This tool accepts Company's names list in comma separated value
file (.csv) format as input.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

The output is a .csv file with Company name and its corresponding ESG ratings
"""

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from tqdm import tqdm
from .scraper import WebScraper


def _append_dict(temp: str) -> str:
    ''' Append the MSCI dictionary with Company Name and its MSCI ESG rating

    Parameters
    ----------
    temp : str
    The previous company name appended to the dictionary

    Returns
    -------
    str
            The latest company name appended to the dictionary
    '''
    if temp == company:
        bot.append_empty_values(msci)

    else:
        msci['MSCI_Company'].append(company.text)
        msci['MSCI_ESG'].append(esg_score.get_attribute('class'))
        temp = company
    return temp


# Read input companies dataset
companies_filename = WebScraper._get_filename()
header_name = WebScraper._get_headername()
export_path = WebScraper._get_exportpath()
df = pd.read_csv(companies_filename)
data_length = len(df)

# Set up the webdriver
URL = "https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg\
        -ratings-corporate-search-tool/"
bot = WebScraper(URL)

# Accept cookies on the website
cookies_xpath = '//*[@id="portlet_mscicookiebar_WAR_mscicookiebar"]/div/div[2]/ \
                div/div/div[1]/div/button[1]'
bot.accept_cookies(cookies_xpath)

# Extract company names and their ESG score and store it in the dictionary
temp = 0
for i in tqdm(range(data_length)):
    msci = {'MSCI_Company': [], 'MSCI_ESG': []}
    # Starting the search by finding the search bar & searching for the company
    search_bar = bot.send_request_to_search_bar(
        header_name, df, i, xpath='//*[@id="_esgratingsprofile_keywords"]')
    search_bar.send_keys(Keys.DOWN, Keys.RETURN)
    sleep(4)

    try:
        xpath = '//*[@id="_esgratingsprofile_esg-ratings-profile-header"]/div[2]/div[1]/div[2]/div'
        esg_score = bot.find_element(xpath)
        company = bot.find_element(
            '//*[@id="_esgratingsprofile_esg-ratings-profile-header"]/div[1]/div[1]')
        temp = _append_dict(temp)

    except NoSuchElementException:
        bot.append_empty_values(msci)

    # Save the data into a csv file
    df1 = bot.convert_dict_to_csv(msci, export_path)
