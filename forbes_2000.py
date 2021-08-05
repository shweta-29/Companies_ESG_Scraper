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
URL = "https://www.forbes.com/lists/global2000/#173f1d785ac0"
bot = scraper.WebScraper(URL)
        
# Extract path of all the rows in the table
def table_info_extract():
    table_xpath = '//*[@id="row-4"]/div/ul/li/div/div/table'
    bot.wait_element_to_load(table_xpath)
    table = bot.driver.find_element_by_xpath(table_xpath)
    body = table.find_element_by_tag_name('tbody')
    rows = body.find_elements_by_tag_name('tr')
    return rows

#Scrape all the 100 rows on a page. Eveyry 16th row has an ad, so skip that
def scraper(rows):
   
    count = 0
    n = 106
    for row in tqdm(rows[:n]): #106
         # Define dictionary
        forbes = {'Rank': [], 'Name': [], 'Country': [], 'Sales': [],
          'Profit': [], 'Assets': [], 'Market Value': []}
        count += 1
        if count % 16 !=0:   
            info = row.find_elements_by_tag_name('td')
            forbes['Rank'].append(info[0].text)
            forbes['Name'].append(info[1].text)
            forbes['Country'].append(info[2].text)
            forbes['Sales'].append(info[3].text)
            forbes['Profit'].append(info[4].text)
            forbes['Assets'].append(info[5].text)
            forbes['Market Value'].append(info[6].text)
            print(forbes)
            df1 = bot.convert_to_csv(forbes, row)  
    return forbes, df1

# Click next page
def next_page_scrape(forbes):
    next_page = bot.driver.find_element_by_xpath('//*[@id="row-4"]/div/ul/li/div/div/div[2]/div/div/ul/li[11]/a')
    bot.driver.execute_script("arguments[0].click();", next_page)                                        
    rows = table_info_extract()
    forbes = scraper(rows)
    
# Accept cookies
cookies_xpath = '//*[@id="truste-consent-button"]'
bot.accept_cookies(cookies_xpath)

# 1st page run
rows = table_info_extract()
forbes = scraper(rows)
# Save the data into a csv file


# Run Page 2 to 20th
pages = 20
for i in range(1,pages): #20
    next_page_scrape(forbes)

