from setuptools import setup
from setuptools import find_packages

setup(
    name="Companies_ESG_metrics",
    version='1.2',
    description='Package that allows you to find ESG ratings from Yahoo\
    Finance, MSCI, CSR Hub, S&P Global, SustainAnalytics. In addition,\
    financial information is also scraped from Yahoo Finance',
    url='https://github.com/shweta-29/Companies_ESG_Scraper.git',
    download_url='https://github.com/shweta-29/Companies_ESG_Scraper/archive/refs/tags/v_01.tar.gz',
    author='Shweta Yadav',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'pandas', 'tqdm', 'sqlalchemy']
)
