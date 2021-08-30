from setuptools import setup
from setuptools import find_packages

setup(
    name="Companies' ESG metrics",
    version='1.0.0',
    description='Package that allows you to find ESG ratings from Yahoo\
    Finance, MSCI, CSR Hub, S&P Global, SustainAnalytics. In addition,\
    financial information is also scraped from Yahoo Finance',
    url='https://github.com/shweta-29/Sustainability_Company_Information.git',
    author='Shweta Yadav',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium']
)
