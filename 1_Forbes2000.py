import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from time import sleep
from scraper import Web_scrape

# Wait for the page to load
def wait_element_to_load(xpath): 
        delay = 10  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print("Loading took too much time!")
        
# Extract path of all the rows in the table
def table_info_extract():
    table_xpath = '//*[@id="row-4"]/div/ul/li/div/div/table'
    wait_element_to_load(table_xpath)
    table = driver.find_element_by_xpath(table_xpath)
    body = table.find_element_by_tag_name('tbody')
    rows = body.find_elements_by_tag_name('tr')
    return rows

#Scrape all the 100 rows on a page. Eveyry 16th row has an ad, so skip that
def scraper(forbes, rows):
    count = 0
    for row in rows[:106]: 
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
    return forbes

# Click next page
def next_page_scrape(forbes):
    next_page = driver.find_element_by_xpath('//*[@id="row-4"]/div/ul/li/div/div/div[2]/div/div/ul/li[11]/a')
    driver.execute_script("arguments[0].click();", next_page)                                        
    rows = table_info_extract()
    forbes = scraper(forbes, rows)
    
# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome('./chromedriver',options=options)
URL = "https://www.forbes.com/lists/global2000/#173f1d785ac0"
driver.get(URL)

# Accept cookies
cookies_xpath = '//*[@id="truste-consent-button"]'
wait_element_to_load(cookies_xpath)
cookies_button = driver.find_element_by_xpath(cookies_xpath)
cookies_button.click()

# Define dictionary
forbes = {'Rank': [], 'Name': [], 'Country': [], 'Sales': [],
          'Profit': [], 'Assets': [], 'Market Value': []}

# 1st page run
rows = table_info_extract()
forbes = scraper(forbes, rows)  

# Run Page 2 to 20th
for i in range(1,20): 
    next_page_scrape(forbes)

# Save the data into a csv file
df = pd.DataFrame.from_dict(forbes)
df.to_csv('Forbes.csv')
df.to_excel('Forbes.xlsx')


