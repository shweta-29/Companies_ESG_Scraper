import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from tqdm import tqdm 
import scraper
from scraper import WebScraper

# Set up driver
URL = "https://www.spglobal.com/esg/scores/"
bot = scraper.WebScraper(URL)

# Read Forbes dataset
df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = 2 #len(df)

# Accept cookies
cookies_xpath = '//*[@id="onetrust-accept-btn-handler"]'
bot.accept_cookies(cookies_xpath)

#Scrape the website. Extract company names and their respective ESG score
temp = 0
for i in tqdm(range(data_length)): 
    # Define dictionary  
    SnP = {'SnP_ESG_Company' : [], 'SnP_ESG_Score' : [], 'SnP_ESG_Country' : [], 'SnP_ESG_Industry' : [], 'SnP_ESG_Ticker' : []}
    try:
        search_bar = bot.initialise_search_bar(df,i, class_name = 'banner-search__input')  
        search_bar.send_keys(Keys.RETURN)
        time.sleep(4)
        xpath = '//*[@id="esg-score"]' 
        bot.wait_element_to_load(xpath)
        ESG_Company = bot.driver.find_element_by_xpath('//*[@id="company-name"]')
        if temp == ESG_Company:
           bot.empty_append(SnP)

        else:
            ESG_Score = bot.driver.find_element_by_xpath(xpath)
            SnP["SnP_ESG_Score"].append(ESG_Score.text)
            SnP["SnP_ESG_Company"].append(ESG_Company.text)
            ESG_Country = bot.driver.find_element_by_xpath('//*[@id="company-country"]')
            SnP["SnP_ESG_Country"].append(ESG_Country.text)
            ESG_Industry = bot.driver.find_element_by_xpath('//*[@id="company-industry"]')
            SnP["SnP_ESG_Industry"].append(ESG_Industry.text)
            ESG_Ticker = bot.driver.find_element_by_xpath('//*[@id="company-ticker"]')
            SnP["SnP_ESG_Ticker"].append(ESG_Ticker.text)
            temp = ESG_Company
    
    except NoSuchElementException:
        print(f'I am here {i}')
        bot.empty_append(SnP)

    df1 = bot.convert_to_csv(SnP, i, 'SnP1')  
    
   


