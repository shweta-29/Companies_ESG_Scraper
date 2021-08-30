# Companies_Sustainability_Information

This repository is created to build a dataset of companies' financial metrics and its corresponding ESG and CSR metrics. The ESG information has been collected from 5 different publically available data analytics firm. The websites used for ESG metrics are: S&P Global, MSCI, Yahoo Finance, CSR Hub, SustainAnalytics. The website used to collect financial information is Yahoo Finance. 

Project Motivation
The motivation behind this webscraping project is to gather the publically available data on ESG and financial metrics, and decipher if there is a relation between company's financial status with its performance in Sustainability. The aim of this project is to extract the ESG and financial metrics for any given companies list.

Example dataset
An example dataset of Forbes 2021 2000 companies is provided with this package.

Package structure:

WebScraping 
    - project
        - esgscraper
            - esgdata.py
            - scraper.py
            - csrhub.py
            - snp_global.py
            - msci.py
            - sustainanalytics.py
            - yahoo.py

        - rds_uploader
            - rds_module.py

Selenium is used to scrape all the websites. Below is the information of each of the .py files:

1. esgdata.py: To begin, run this file. It will ask for these inputs: 
    1. Path of the file(.csv) that contains companies name
    2. Header name of the companies column
    3. Which website to scrape the data from: SustainAnalytics, S&P Global, CSR HUB, MSCI, Yahoo

2. scraper.py This Python file serves as an input for all the other .py files. It has a Class that includes all the methods that are used commonly in all the .py files.

3. snp_global.py : This file collects ESG score and supporting information such as Industry, Ticker, Country, Company Name from the S&P Global website.
                https://www.spglobal.com/esg/scores/

4. msci.py : This file collects ESG rating and Company name from the MSCI website. https://www.msci.com/our-solutions/esg-investing/esg-ratings/

5. csrhub.py : This file collects CSR rating and Company name from the CSR Hub website. https://www.csrhub.com/search/name/

6. sustainanalytics.py : This file collects ESG risk rating, Company and Industry name from the SustainAnalytics website. https://www.sustainalytics.com/esg-ratings

7. yahoo.py : This file collects the below information from the Yahoo Finance website (https://finance.yahoo.com/lookup):
    ESG rating, company name and financial metrics such as Market Cap, Trailing P/E, return on asset, Total Debt/Equity (mrq), Operating Cash Flow and Stock Price, Price/Book (mrq), Most Recent Quarter (mrq), Profit Margin, Op_Margin, return on equity, Diluted EPS, PayoutRatio

8. rds_module.py: Use the class RdsUploader to upload the data to SQL database. Inputs needed: DATATBASE_TYPE, DBAPI, ENDPOINT, PORT, DATABASE, USERNAME, PASSWORD. Methods: create_table, send_query, read_table, add_rows, delete_row 
 
Things to note:
1. Enter a file path that contains the file name with the extension .csv
2. Company names are extracted from each website so that the user can tally the company names with input companies names dataset 
3. Check the documentation of each script for more information

License:
MIT © Shweta Yadav

Support:
For any questions and suggestions, connect with me on LinkedIn:  http://www.linkedin.com/in/shweta-yadav1