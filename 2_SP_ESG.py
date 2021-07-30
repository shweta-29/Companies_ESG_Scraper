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

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(options=options) #For EC2 run
#driver = webdriver.Chrome('./chromedriver',options=options) #For VS code run

# Wait for the page to load
def wait_element_to_load(xpath):
    delay = 10  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Loading took too much time!")

# Read Forbes dataset
df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = len(df)

# Set up the webdriver
URL = "https://www.spglobal.com/esg/scores/"
driver.get(URL)

# Accept cookies
xpath = '//*[@id="onetrust-accept-btn-handler"]'
wait_element_to_load(xpath)
cookies_button = driver.find_element_by_xpath(xpath)
cookies_button.click()   

#Scrape the website. Extract company names and their respective ESG score
temp = 0
for i in tqdm(range(data_length)): 
    # Define dictionary  
    SnP = {'SnP_ESG_Company' : [], 'SnP_ESG_Score' : [], 'SnP_ESG_Country' : [], 'SnP_ESG_Industry' : [], 'SnP_ESG_Ticker' : []}
    try:
        Company = df.loc[i]['Name']
        search_bar = driver.find_element_by_class_name('banner-search__input')
        search_bar.clear()
        search_bar = driver.find_element_by_class_name('banner-search__input')
        search_bar.send_keys(Company)   
        search_bar.send_keys(Keys.RETURN)
        time.sleep(4)
        xpath = '//*[@id="esg-score"]' 
        wait_element_to_load(xpath)
        ESG_Company = driver.find_element_by_xpath('//*[@id="company-name"]')
        if temp == ESG_Company:
            SnP["SnP_ESG_Score"].append(None)
            SnP["SnP_ESG_Company"].append(None)
            SnP["SnP_ESG_Country"].append(None)
            SnP["SnP_ESG_Industry"].append(None)
            SnP["SnP_ESG_Ticker"].append(None)
        else:
            ESG_Score = driver.find_element_by_xpath(xpath)
            SnP["SnP_ESG_Score"].append(ESG_Score.text)
            SnP["SnP_ESG_Company"].append(ESG_Company.text)
            ESG_Country = driver.find_element_by_xpath('//*[@id="company-country"]')
            SnP["SnP_ESG_Country"].append(ESG_Country.text)
            ESG_Industry = driver.find_element_by_xpath('//*[@id="company-industry"]')
            SnP["SnP_ESG_Industry"].append(ESG_Industry.text)
            ESG_Ticker = driver.find_element_by_xpath('//*[@id="company-ticker"]')
            SnP["SnP_ESG_Ticker"].append(ESG_Ticker.text)
            temp = ESG_Company
    
    except NoSuchElementException:
        print(f'I am here {i}')
        SnP["SnP_ESG_Score"].append(None)
        SnP["SnP_ESG_Company"].append(None)
        SnP["SnP_ESG_Country"].append(None)
        SnP["SnP_ESG_Industry"].append(None)
        SnP["SnP_ESG_Ticker"].append(None)
    
    # Save the data into a csv file. 
    df1 = pd.DataFrame.from_dict(SnP)
    if i==0:
            df1.to_csv('2_SnP.csv', index = False) 

    else:
            df1.to_csv('2_SnP.csv', mode = 'a', header=False, index = False) 
    
    #ProgressBar
    if i % 100 == 0:
        p = i/20
        print(f'Completed {p} percent')


