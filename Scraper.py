'''
This module contains a class for scraping the websites.
'''

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
import os
from typing import Optional

class WebScraper():
    '''
    This class is used to scrape a website.

    Attributes:
        URL (str): The website URL.
    '''
    def __init__(self, URL : str) :
        '''
        See help(scraper) for accurate signature
        '''        
        options = Options()
        #options.add_argument("--headless") For EC2
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(URL)
        sleep(2)

    def wait_element_to_load(self, xpath : str):
        '''
        This function waits until the specified xpath is accessible on the website

        Args:
            xpath ('str'): The xpath of the element to be located on the webpage

        '''
        delay = 10  # seconds
        ignored_exceptions= (NoSuchElementException,StaleElementReferenceException,)
        try:
            sleep(0.5)
            WebDriverWait(self.driver, delay, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print("Loading took too much time!")

    def accept_cookies(self, xpath : str): 
        '''
        This function clicks on 'Accept cookies' button on the website

        Args:
            xpath (str): The xpath of the 'Accept cookies' button
        '''
        cookies_button = self.driver.find_element_by_xpath(xpath)
        WebScraper.wait_element_to_load(self, xpath)
        cookies_button.click()
        sleep(2)

    def convert_dict_to_csv(self, dict_name : str, csv_name : str) -> pd.DataFrame: 
        '''
        This function converts the dictionary to a pandas dataframe and the latter is 
        converted a csv file

        Args:
            dict_name (str): Name of the dictionary
            name (str): Name to be given to the csv file

        Returns:
            pd.DataFrame: Pandas Dataframe generated from the dictionary
        '''
        df1 = pd.DataFrame.from_dict(dict_name)
        # If the file already exists, append the new data
        if os.path.isfile(csv_name + '.csv'):
            df1.to_csv(csv_name + '.csv', mode='a', header=False, index=False)
        else:
            df1.to_csv(csv_name + '.csv', index=False)
        return df1
    
    def append_empty_values(self, dict : dict) -> dict: 
        '''
        This function appends empty values to the dictionary

        Args:
            dict (dict): Dictionary to be appended

        Returns:
            dict: Dictionary appended with empty values
        '''
        for key in dict.keys():
            dict[key].append(None)
        return dict

    def find_element(self, xpath : str = None, class_name : str = None, 
                     multiple : bool = False) -> Optional[WebElement]:
        '''
        Given xpath or class name, this function locates the corresponding web element

        Args:
            xpath (str) : xpath of the web element
            class_name (str) : class name of the web element
            multiple (bool) : True if multiple elements to be located; False otherwise

        Returns:
            WebElement: element on the website
        '''
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

    def send_request_to_search_bar(self, df : pd.DataFrame, i : int, xpath : str = None, 
                                   class_name : int = None) -> WebElement :
        '''
        Given xpath or class name, this function locates the search bar and enters
        the company name

        Args:
            df (dataframe) : input pandas datframe containing Companies name
            xpath (str) : xpath of the search bar
            class_name (str) : class name of the search bar
            multiple (bool) : True if multiple elements to be located; False otherwise

        Returns:
            WebElement: webelement of the search bar
        '''
        Company = df.loc[i]['Name']
        search_bar = WebScraper.find_element(self, xpath, class_name)
        search_bar.clear()
        search_bar = WebScraper.find_element(self, xpath, class_name)
        search_bar.send_keys(Company)   
        sleep(3)
        search_bar = WebScraper.find_element(self, xpath, class_name)
        return search_bar

