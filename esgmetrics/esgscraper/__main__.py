"""

This script allows the user to scrape the ESG, CSR ratings and financial
metrics of the companies from the following websites: SustainAnalytics,
S&P Global, CSR HUB, MSCI, Yahoo Finance

This tool accepts Company's names list in comma separated value
file (.csv) format as input.

The output is a .csv file with Company name and its corresponding ESG/
CSR ratings/Financial Metrics

To run on example dataset (Forbes.csv provided with this package), enter 0
for Companies filename and Header Name

This script will ask the user to input a number that pertains to the website
from which the information has to be scraped
"""
from .scraper import WebScraper

WebScraper.get_esgdata()
