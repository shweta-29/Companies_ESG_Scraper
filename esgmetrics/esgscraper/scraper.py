'''This module contains a class for scraping the websites.'''

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
import pkg_resources


class WebScraper():

    '''
    This class is used to scrape a website.

    Attributes:
        URL (str): The website URL.
    '''

    def __init__(self, URL: str):
        '''
        See help(scraper) for accurate signature
        '''
        self.URL = URL
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.chrome_path = input('Please specify the chromedriver path : ')
        self.driver = webdriver.Chrome(
            executable_path=self.chrome_path, options=options)
        self.driver.get(URL)
        sleep(2)

    @classmethod
    def get_esgdata(cls):
        '''
        This function calls the _get_websitename() method and imports the\
        corresponding module
        '''
        website_name = cls._get_websitename()
        module = "esgmetrics.esgscraper." + website_name

        __import__(module)

    @staticmethod
    def _get_filename() -> str:
        '''
        This function asks the user for the filepath of the .csv file that
        lists companies name

        Returns:
            str : The input file path
        '''
        companies_filename = input('Enter the filepath of a .csv file with'
                                   + ' company names. To run on example'
                                   + ' dataset(Forbes 2020 2000 companies'
                                   + ' list), enter 0 : ')
        if companies_filename == '0':
            return pkg_resources.resource_stream(__name__, 'data/Forbes.csv')
        else:
            return companies_filename

    @staticmethod
    def _get_headername() -> str:
        '''
        This function asks the user for the name of the header in the .csv
        file that lists companies name

        Returns:
            str : The input header name
        '''
        companies_headername = input(
            'Enter the name of the header that contains the company names.To'
            + ' run on example dataset(Forbes 2020 2000 list), enter 0  : ')
        if companies_headername == '0':
            return 'Name'
        else:
            return companies_headername

    @staticmethod
    def _get_websitename() -> str:
        '''
        This function asks the user for the website name from which data is to
        be extracted

        Returns:
            str : website name
        '''
        website = input(
            'Which website to scrape the data from: MSCI (enter 1),Yahoo'
            + ' Finance (enter 2), CSRHUB (enter 3), S&P Global (enter 4)'
            + ' , SustainAnalytics (enter 5) :')
        if website == '1':
            return 'msci'
        if website == '2':
            return 'yahoo'
        if website == '3':
            return 'csrhub'
        if website == '4':
            return 'snp_global'
        if website == '5':
            return 'sustainanalytics'
        else:
            return print('Enter a number between 1 to 5')

    @staticmethod
    def _get_exportpath() -> str:
        '''
        This function asks the user for the path plus output filename where
        csv file is exported

        Returns:
            str : filepath
        '''
        export_path = input(
            'Enter the path with output csv file name where output csv file is'
            + ' to be exported. : ')
        return export_path

    def wait_element_to_load(self, xpath: str):
        '''
        This function waits until the specified xpath is accessible on the
        website

        Args:
            xpath ('str'): The xpath of the element to be located on the
            webpage

        '''
        delay = 10  # seconds
        ignored_exceptions = (NoSuchElementException,
                              StaleElementReferenceException,)
        try:
            sleep(0.5)
            WebDriverWait(self.driver, delay,
                          ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            pass

    def accept_cookies(self, xpath: str):
        '''
        This function clicks on 'Accept cookies' button on the website

        Args:
            xpath (str): The xpath of the 'Accept cookies' button
        '''
        cookies_button = self.driver.find_element_by_xpath(xpath)
        WebScraper.wait_element_to_load(self, xpath)
        cookies_button.click()
        sleep(2)

    @staticmethod
    def convert_dict_to_csv(dict_name: str, export_path: str) -> pd.DataFrame:
        '''
        This function converts the dictionary to a pandas dataframe and the
        latter is converted a csv file

        Args:
            dict_name (str): Name of the dictionary
            export_path (str) : Filepath including the outpule filename in
            which csv file is to be exported

        Returns:
            pd.DataFrame: Pandas Dataframe generated from the dictionary
        '''
        df1 = pd.DataFrame.from_dict(dict_name)
        # If the file already exists, append the new data
        if os.path.isfile(export_path + '.csv'):
            df1.to_csv(export_path + '.csv',
                       mode='a', header=False, index=False)
        else:
            df1.to_csv(export_path + '.csv', index=False)
        return df1

    @staticmethod
    def append_empty_values(dictionary: dict) -> dict:
        '''
        This function appends empty values to the dictionary

        Args:
            dict (dict): Dictionary to be appended

        Returns:
            dict: Dictionary appended with empty values
        '''
        for key in dictionary.keys():
            dictionary[key].append(None)
        return dictionary

    def find_element(self, xpath: str = None, class_name: str = None,
                     multiple: bool = False) -> WebElement:
        '''
        Given xpath or class name, this function locates the corresponding web
        element

        Args:
            xpath (str) : xpath of the web element
            class_name (str) : class name of the web element
            multiple (bool) : True if multiple elements to be located; False
            otherwise

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

    def send_request_to_search_bar(self, header_name, df: pd.DataFrame, i: int,
                                   xpath: str = None, class_name: int =
                                   None) -> WebElement:
        '''
        Given xpath or class name, this function locates the search bar
        and enters the company name

        Args:
            df (dataframe) : input pandas datframe containing Companies name
            xpath (str) : xpath of the search bar
            class_name (str) : class name of the search bar
            multiple (bool) : True if multiple elements to be located;
            False otherwise

        Returns:
            WebElement: webelement of the search bar
        '''
        Company = str(df.loc[i][header_name])
        search_bar = WebScraper.find_element(self, xpath, class_name)
        search_bar.clear()
        search_bar = WebScraper.find_element(self, xpath, class_name)
        search_bar.send_keys(Company)
        sleep(3)
        search_bar = WebScraper.find_element(self, xpath, class_name)
        return search_bar

    def restart_driver(self, cookies_xpath):
        '''
        This function restarts the website

        Args:
            xpath (str): The xpath of the 'Accept cookies' button

        Returns:
            WebScraper instance
        '''
        self.driver.quit()
        sleep(60)
        bot = WebScraper(self.URL)
        bot.accept_cookies(cookies_xpath)
        return bot
