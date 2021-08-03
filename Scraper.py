import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from tqdm import tqdm 

class WebScraper():
    def __init__(self, URL):
        options = Options()
        #options.add_argument("--headless") For EC2
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(URL)
        time.sleep(2)
    
    def driver(self):
        return self.driver

    def wait_element_to_load(self, xpath):
        delay = 10  # seconds
        ignored_exceptions= (NoSuchElementException,StaleElementReferenceException,)
        try:
            time.sleep(0.5)
            myElem = WebDriverWait(self.driver, delay, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print("Loading took too much time!")

    def accept_cookies(self, xpath): # Accept cookies
        cookies_button = self.driver.find_element_by_xpath(xpath)
        WebScraper.wait_element_to_load(self, xpath)
        cookies_button.click()
        time.sleep(2)

    def convert_to_csv(self, dict_name, i,name): # Save the data into a csv file. 
        df1 = pd.DataFrame.from_dict(dict_name)
        if i==0:
                df1.to_csv(name +'.csv', index = False) 

        else:
                df1.to_csv(name +'.csv', mode = 'a', header=False, index = False) 
        return df1
    
    def empty_append(self, dict): # Append the dictionary by empty values
        for key in dict.keys():
            dict[key].append(None)
        return dict

    def find_element(self, xpath=None, class_name=None, multiple=False):
        if xpath and multiple:
            WebScraper.wait_element_to_load(self, xpath)
            return self.driver.find_elements_by_xpath(xpath)
        elif xpath and not multiple:
            WebScraper.wait_element_to_load(self, xpath)
            return self.driver.find_element_by_xpath(xpath)
        elif class_name and multiple:
            return self.driver.find_elements_by_class_name(class_name)
        elif class_name and not multiple:
            return self.driver.find_element_by_class_name(class_name)
        return None

    def initialise_search_bar(self,df,i,xpath=None, class_name=None, multiple=False):
        Company = df.loc[i]['Name']
        search_bar = WebScraper.find_element(self, xpath, class_name, multiple=False)
        search_bar.clear()
        search_bar = WebScraper.find_element(self, xpath, class_name, multiple=False)
        search_bar.send_keys(Company)   
        time.sleep(3)
        search_bar = WebScraper.find_element(self, xpath, class_name, multiple=False)
        return search_bar

    def send_request(self, xpath, request):
        # First, look for the xpath of the search_bar
        search_bar = self.find_element(xpath=xpath)
        # Then, clear and send the request
        search_bar.clear()
        search_bar.send_keys(request)
        time.sleep(1)
        # Go to the first search result
        search_bar.send_keys(Keys.DOWN)
        time.sleep(1)
        # Press Enter
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
    