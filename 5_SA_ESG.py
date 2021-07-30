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
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
# driver = webdriver.Chrome(options=options) #For EC2 run
driver = webdriver.Chrome('./chromedriver',options=options) #For VS code run
URL = "https://www.sustainalytics.com/esg-ratings"
driver.get(URL)
time.sleep(1)

temp = 0
for i in tqdm(range(data_length)):
    san = {'SA_Company': [], 'SA_ESG_Risk' : [], 'SA_Industry' :[]}
    Company = df.loc[i]['Name']
    search_bar = driver.find_element_by_xpath('//*[@id="searchInput"]') 
    search_bar.clear()
    search_bar.send_keys(Company)
    time.sleep(3)
    
    try:
        key = driver.find_element_by_xpath('.//div[@class="list-group-item"]')
        key.click()
        time.sleep(3) 
        xpath ='/html/body/section[2]/section[1]/div/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/span'
        esg_score = driver.find_element_by_xpath(xpath)
        company = driver.find_element_by_xpath('/html/body/section[2]/section[1]/div/div[1]/div[1]/div[1]/div/h2')
        industry = driver.find_element_by_xpath('/html/body/section[2]/section[1]/div/div[1]/div[1]/div[2]/div[1]/p/strong')
        if temp == company:
                san['SA_Company'].append(None)
                san['SA_ESG_Risk'].append(None)
                san['SA_Industry'].append(None)
                
        else:
                san['SA_Company'].append(company.text) 
                san['SA_ESG_Risk'].append(esg_score.text) 
                san['SA_Industry'].append(industry.text) 
                temp = company      
    
    except NoSuchElementException:
        print(f'I am here {i}')
        san['SA_Company'].append(None)
        san['SA_ESG_Risk'].append(None)
        san['SA_Industry'].append(None)
        continue
    
    df1 = pd.DataFrame.from_dict(san) 
    
    if i==0:
        df1.to_csv('SA_ESG.csv', index = False) 

    else:
        df1.to_csv('SA_ESG.csv', mode = 'a', header=False, index = False) 





