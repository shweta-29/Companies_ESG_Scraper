import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from tqdm import tqdm 
import scraper
from scraper import WebScraper

# Read Forbes dataset
df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = 2 #len(df)

# Set up the webdriver
URL = "https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/"
bot = scraper.WebScraper(URL)

# Accept cookies
cookies_xpath = '//*[@id="portlet_mscicookiebar_WAR_mscicookiebar"]/div/div[2]/div/div/div[1]/div/button[1]'
bot.accept_cookies(cookies_xpath)

#Scrape the website. Extract company names and their respective ESG score
temp = 0
for i in tqdm(range(data_length)): 
        # Define dictionary
        msci = {'MSCI_Company': [], 'MSCI_ESG' : []}
        search_bar = bot.initialise_search_bar(df,i, xpath = '//*[@id="_esgratingsprofile_keywords"]')  
        search_bar.send_keys(Keys.DOWN, Keys.RETURN)
        time.sleep(4)

        try: 
                xpath ='//*[@id="_esgratingsprofile_esg-ratings-profile-header"]/div[2]/div[1]/div[2]/div'
                esg_score = bot.driver.find_element_by_xpath(xpath)
                company = bot.driver.find_element_by_xpath('//*[@id="_esgratingsprofile_esg-ratings-profile-header"]/div[1]/div[1]')
                if temp == company:
                        bot.empty_append(msci)
                        
                else:
                        msci['MSCI_Company'].append(company.text) 
                        msci['MSCI_ESG'].append(esg_score.get_attribute('class')) 
                        temp = company      

        except NoSuchElementException:
                print(f'I am here {i}')
                bot.empty_append(msci)
                
        # Save the data into a csv file 
        df1 = bot.convert_to_csv(msci, i, 'msci1')  







