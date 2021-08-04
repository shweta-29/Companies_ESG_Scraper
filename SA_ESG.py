import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import scraper
from scraper import WebScraper 

# Read Forbes dataset
df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = len(df)

# Set up the webdriver
URL = "https://www.sustainalytics.com/esg-ratings"
bot = scraper.WebScraper(URL)

temp = 0
for i in tqdm(range(data_length)):
    san = {'SA_Company': [], 'SA_ESG_Risk' : [], 'SA_Industry' :[]}
    search_bar = bot.initialise_search_bar(df,i, xpath = '///*[@id="searchInput"]')
    
    try:
        key = bot.driver.find_element_by_xpath('.//div[@class="list-group-item"]')
        key.click()
        time.sleep(3) 
        xpath ='/html/body/section[2]/section[1]/div/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span'
        esg_score = bot.driver.find_element_by_xpath(xpath)
        company = bot.driver.find_element_by_xpath('/html/body/section[2]/section[1]/div/div[1]/div[1]/div[1]/div/h2')
        industry = bot.driver.find_element_by_xpath('/html/body/section[2]/section[1]/div/div[1]/div[1]/div[2]/div[1]/p/strong')
        if temp == company:
                bot.empty_append(san) 
                
        else:
                san['SA_Company'].append(company.text) 
                san['SA_ESG_Risk'].append(esg_score.text) 
                san['SA_Industry'].append(industry.text) 
                temp = company      
    
    except NoSuchElementException:
        bot.empty_append(san) 
        continue
    
   # Save the data into a csv file 
    df1 = bot.convert_to_csv(san, i, 'San1') 





