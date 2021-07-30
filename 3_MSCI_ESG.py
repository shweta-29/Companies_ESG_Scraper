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
# driver = webdriver.Chrome(options=options) #For EC2 run
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
driver = webdriver.Chrome('./chromedriver',options=options) #For VS code run
URL = "https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/"
driver.get(URL)

# Accept cookies
xpath = '//*[@id="portlet_mscicookiebar_WAR_mscicookiebar"]/div/div[2]/div/div/div[1]/div/button[1]'
wait_element_to_load(xpath)
cookies_button = driver.find_element_by_xpath(xpath)
cookies_button.click()
time.sleep(2)

#Scrape the website. Extract company names and their respective ESG score
temp = 0
for i in tqdm(range(data_length)): 
        # Define dictionary
        msci = {'MSCI_Company': [], 'MSCI_ESG' : []}

        Company = df.loc[i]['Name']
        search_bar = driver.find_element_by_xpath('//*[@id="_esgratingsprofile_keywords"]')
        search_bar.clear()
        search_bar = driver.find_element_by_xpath('//*[@id="_esgratingsprofile_keywords"]')
        search_bar.send_keys(Company)
        time.sleep(2)
        search_bar = driver.find_element_by_xpath('//*[@id="_esgratingsprofile_keywords"]')
        search_bar.send_keys(Keys.DOWN, Keys.RETURN)
        time.sleep(4)

        try: 
                xpath ='//*[@id="_esgratingsprofile_esg-ratings-profile-header"]/div[2]/div[1]/div[2]/div'

                esg_score = driver.find_element_by_xpath(xpath)
                company = driver.find_element_by_xpath('//*[@id="_esgratingsprofile_esg-ratings-profile-header"]/div[1]/div[1]')
                if temp == company:
                        msci['MSCI_Company'].append(None)
                        msci['MSCI_ESG'].append(None)
                        
                else:
                        msci['MSCI_Company'].append(company.text) 
                        msci['MSCI_ESG'].append(esg_score.get_attribute('class')) 
                        temp = company      

        except NoSuchElementException:
                print(f'I am here {i}')
                msci['MSCI_ESG'].append(None) 
                msci['MSCI_Company'].append(None) 
                

        # Save the data into a csv file. 
        df1 = pd.DataFrame.from_dict(msci)  
        if i==0:
                df1.to_csv('3_MSCI.csv', index = False) 

        else:
                df1.to_csv('3_MSCI.csv', mode = 'a', header=False, index = False) 









