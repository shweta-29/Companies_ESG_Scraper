from setuptools import setup
from setuptools import find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="ESGScraper",
    version='1.0.0',
    description='Package that allows you to find ESG ratings from Yahoo\
    Finance, MSCI, CSR Hub, S&P Global, SustainAnalytics. In addition,\
    financial information is also scraped from Yahoo Finance',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shweta-29/Companies_ESG_Scraper.git',
    download_url='https://github.com/shweta-29/Companies_ESG_Scraper/archive/refs/tags/v_01.tar.gz',
    author='Shweta Yadav',
    author_email='shweta.yadav2092@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'pandas', 'tqdm', 'sqlalchemy'],
    include_package_data=True,
    package_data={'': ['data/*.csv']}
)
