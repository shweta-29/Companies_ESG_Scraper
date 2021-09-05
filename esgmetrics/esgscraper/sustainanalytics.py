"""SustainAnalytics website Scrape

This script allows the user to scrape the companies' ESG ratings from the
SustainAnalytics website
Website link: "https://www.sustainalytics.com/esg-ratings"

This tool accepts Company's names list in comma separated value
file (.csv) format as input.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

The output is a .csv file with Company name and its corresponding ESG ratings
"""

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tqdm import tqdm
from .scraper import WebScraper


def append_dict(temp: str) -> str:
    ''' Append the SustainAnalytics dictionary with Company name, Industry\
        Name, and its ESG Risk rating

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
        bot.append_empty_values(san)

    else:
        san['SA_Company'].append(company.text)
        san['SA_ESG_Risk'].append(esg_score.text)
        san['SA_Industry'].append(industry.text)
        temp = company
    return temp


# Read input companies dataset
companies_filename = WebScraper._get_filename()
header_name = WebScraper._get_headername()
export_path = WebScraper._get_exportpath()
df = pd.read_csv(companies_filename)
data_length = len(df)

# Set up the webdriver
URL = "https://www.sustainalytics.com/esg-ratings"
bot = WebScraper(URL)

# Scrape the website. Extract company names and their respective ESG score
#  and store it in the dictionary
temp = 0
for i in tqdm(range(data_length)):
    san = {'SA_Company': [], 'SA_ESG_Risk': [], 'SA_Industry': []}
    # Starting the search by finding the search bar and searching for the
    #  company
    search_bar = bot.send_request_to_search_bar(
        header_name, df, i, xpath='//*[@id="searchInput"]')

    try:
        key = bot.find_element('.//div[@class="list-group-item"]')
        key.click()
        sleep(3)
        xpath = '/html/body/section[2]/section[1]/div/div[1]/div[1]/div[3]/ \
                div[1]/div[1]/div[1]/span'
        esg_score = bot.find_element(xpath)
        company = bot.find_element(
            '/html/body/section[2]/section[1]/div/div[1]/div[1]/div[1]/div/h2')
        industry = bot.find_element(
            '/html/body/section[2]/section[1]/div/div[1]/div[1]/div[2]/ \
            div[1]/p/strong')
        temp = append_dict(temp)

    except NoSuchElementException:
        bot.append_empty_values(san)

    # Save the data into a csv file
    df1 = bot.convert_dict_to_csv(san, export_path)
