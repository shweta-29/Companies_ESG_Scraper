import time
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm 
import scraper
from scraper import WebScraper

# Read Forbes dataset
df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = 2 #len(df)

# Open Website 
def start_website():
    URL = "https://www.csrhub.com/search/name/"
    bot = scraper.WebScraper(URL)
    cookies_xpath = '//*[@id="body-content-holder"]/div[2]/div/span[2]/button'
    bot.accept_cookies(cookies_xpath)
    return bot, bot.driver

bot, driver = start_website()

#Scrape the website. Extract company names and their respective CSR score
for i in tqdm(range(data_length)):
    csr = {'CSR_Company': [], 'CSR_Ratings' : []}
    delay = 2  # seconds
        
    try:
        search_bar = bot.initialise_search_bar(df,i, xpath = '//*[@id="search_company_names_0"]')
        search_bar.send_keys(Keys.RETURN)
        time.sleep(1)  

        try:
            csr_score = driver.find_element_by_xpath('//*[@id="wrapper"]/div[3]/section[3]/div[2]/table/tbody/tr[2]/td[2]')
            csr['CSR_Ratings'].append(csr_score.text) 
            company = driver.find_element_by_xpath('//*[@id="wrapper"]/div[3]/section[3]/div[2]/table/tbody/tr[2]/td[1]/a')
            csr['CSR_Company'].append(company.text) 
        
        except NoSuchElementException:
            print(f'Could not find company at location: {i}')
            bot.empty_append(csr) 

    # If no element found, that means the page rejected your requests. You will restart the chromedriver
    except NoSuchElementException:
        print('Restarting the driver')
        i -= 1 
        driver.quit()
        time.sleep(120)
        driver = start_website()
        continue

    # Save the data into a csv file 
    df1 = bot.convert_to_csv(csr, i, 'CSI1') 
            
    






