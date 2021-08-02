# Sustainability_Company_Information
This repository is created to build a dataset of Forbes 2021 2000 companies' financial metrics and ESG and CSR metrics. The ESG information has been collected from 5 
different publically available data analytics firm. The websites used for ESG metrics are: S&P Global, MSCI, Yahoo Finance, CSR Hub, SustainAnalytics. The website
used to collect financial information is Yahoo Finance.

The motivation behind this webscraping project is to gather the publically available data on ESG and financial metrics, and decipher if there is a relation between 
company's financial status with its performance in Sustainability.

The dataset generated contains 2000 rows with all the Forbes 2000 companies with 28 columns containing company info, its financial info and its ESG ratings

Selenium is used to scrape all the websites. 1_Forbes2000.py is the first file to be run. All other files can be run in any preference. Below is the information of each of the .py files:

Scraper.py
This Python file serves as an input for all the other .py files. It has a Class that includes all the methods that are used commonly in all the .py files.

1_Forbes2000.py
This file scrapes the companies name listed on Forbes 2000 website. Along with that information such as Country, Sales, Profit, Asset, and Market value of the 
companies is also collected. The output of this code is used as an input for all of the below files.

2_SP_ESG.py
This file collects ESG score and supporting information such as Industry, Ticker, Country, Company Name (to tally with input Forbes dataset) from the S&P Global website

3_MSCI_ESG.py
This file collects ESG ratings and supporting information such as Company name (to tally with input Forbes dataset) from the MSCI website

4_CSR.py
This file collects CSR ratings and supporting information such as Company name (to tally with input Forbes dataset) from the CSR Hub website

5_SA_ESG.py
This file collects ESG risk ratings and supporting information such as Company and Industry name from the SustainAnalytics website

6_Yahoo.py
This file collects ESG ratings and financial metrics such as Market Cap, P/E, return on aset, Debt/equity, Operating Cash Flow and Stock Price
from the Yahoo Finance website
