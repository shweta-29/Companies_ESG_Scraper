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
from tqdm import tqdm # I added a progress bar that looks nice

# Set up the webdriver
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")

# Read Forbes dataset
df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = len(df)

# Open Website 
def start_website():
    driver = webdriver.Chrome('./chromedriver',options=options) #For VS code run
    # driver = webdriver.Chrome(options=options) #For EC2 run
    URL = "https://www.csrhub.com/search/name/"
    driver.get(URL)
    time.sleep(1)
    cookies_button = driver.find_element_by_xpath('//*[@id="body-content-holder"]/div[2]/div/span[2]/button')
    cookies_button.click()
    time.sleep(1)
    return driver

driver = start_website()
Access_xpath = '/html/body/pre'
#Scrape the website. Extract company names and their respective CSR score
for i in tqdm(range(data_length)):
    csr = {'CSR_Company': [], 'CSR_Ratings' : []}
    delay = 2  # seconds
         
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, Access_xpath)))

    except TimeoutException:
        pass

    Company = df.loc[i]['Name']
    search_bar = driver.find_element_by_xpath('//*[@id="search_company_names_0"]')
    search_bar.clear()
    search_bar.send_keys(Company)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)
    
    try:
        csr_score = driver.find_element_by_xpath('//*[@id="wrapper"]/div[3]/section[3]/div[2]/table/tbody/tr[2]/td[2]')
        csr['CSR_Ratings'].append(csr_score.text) 
        company = driver.find_element_by_xpath('//*[@id="wrapper"]/div[3]/section[3]/div[2]/table/tbody/tr[2]/td[1]/a')
        csr['CSR_Company'].append(company.text)    

    # If no element found, that means the page rejected your requests
    # You will restart the chromedriver
    except NoSuchElementException:
        print(f'Could not find company: {Company}')
        print('Restarting the driver')
        driver.quit()
        time.sleep(120)
        driver = start_website()
        # If you reached this exception, you couldn't find the info for this company
        # So we need to move back 1 iteration to retry this company
        i -= 1
        continue
        
    
    df1 = pd.DataFrame.from_dict(csr) 

    if i==0:
        df1.to_csv('4_CSR_ESG.csv', index = False) 

    else:
        df1.to_csv('4_CSR_ESG.csv', mode = 'a', header=False, index = False) 

# Save the data into a csv file

df2 = pd.read_csv('4_CSR_ESG.csv', index_col = 0)
df2.to_excel('4_CSR_ESG.xlsx')






