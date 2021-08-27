"""Yahoo Finance website Scrape

This script allows the user to scrape the ESG ratings from the Yahoo Finance website
of each of the Forbes 2020 2000 companies
Website link: "https://finance.yahoo.com/lookup"

This tool accepts Company's names list in comma separated value 
file (.csv) format as input.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

The output is a .csv file with Company name and its corresponding finance statistics and ESG ratings
"""

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from tqdm import tqdm 
from scraper import WebScraper 

def append_finance_data(temp : str,company_name : str) -> str:
    '''
    Append the Yahoo Finance dictionary with each company's Financial statistics
    
    Parameters
    ----------
    temp : str
    The previous company name appended to the dictionary

    company_name : str
    The company name to be searched

    Returns
    -------
    str
        The latest company name appended to the dictionary
    ''' 
    if temp == company_name:
        bot.append_empty_values(fin)
    
    else:
        xpath_stats_button = '//*[@data-test="STATISTICS"]'
        bot.wait_element_to_load(xpath_stats_button)
        statistics_button = bot.find_element(xpath_stats_button)
        sleep(1)
        statistics_button.click()
        xpath_stats = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[2]/td[2]'
        bot.wait_element_to_load(xpath_stats)
        
        quar = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[1]/div/div/table/tbody/tr[2]/td[2]')
        pm = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td[2]')
        op = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[2]/td[2]')
        roa = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[3]/div/div/table/tbody/tr[1]/td[2]')
        roe = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[3]/div/div/table/tbody/tr[2]/td[2]')
        eps = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div/table/tbody/tr[7]/td[2]')
        cf = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[1]/td[2]')
        d2e = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[4]/td[2]')
        por = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[6]/td[2]')
        st_p = bot.find_element('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')

        fin["fin_Company"].append(company_name)
        xpath_mcap = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]'
        mcap = bot.find_element(xpath_mcap)
        bot.wait_element_to_load(xpath_mcap)
        fin["Market Cap"].append(mcap.text)
        xpath_pe = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]'
        pe = bot.find_element(xpath_pe)
        bot.wait_element_to_load(xpath_pe)
        fin["Trailing P/E"].append(pe.text)
        pb = bot.find_element('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]')
        fin["Price/Book (mrq)"].append(pb.text)
        fin["Most Recent Quarter (mrq)"].append(quar.text)
        fin["Profit Margin"].append(pm.text)
        fin["Op_Margin"].append(op.text)
        fin["ROA"].append(roa.text)
        fin["ROE"].append(roe.text)
        fin["Diluted EPS"].append(eps.text)
        fin["Operating_CashFlow"].append(cf.text)
        fin["Total Debt/Equity (mrq)"].append(d2e.text)
        fin["PayoutRat"].append(por.text)
        fin["Stock Price"].append(st_p.text)
        print('3')
        temp = company_name 
    return temp

def append_esg_data():
    '''
    Append the Yahoo Finance dictionary with each company's ESG rating
    ''' 
    try:
        #xpath_button_esg = '//*[@id="quote-nav"]/ul/li[11]/a'
        xpath_button_esg = '//*[@id="quote-nav"]/ul/li[11]/a/span'
        #xpath_button_esg = '//*[@data-test="SUSTAINABILITY"]'
        bot.wait_element_to_load(xpath_button_esg)
        button = bot.find_element(xpath_button_esg)
        button.click()
        xpath_esg = '//div[@class="Fz(36px) Fw(600) D(ib) Mend(5px)"]' 
        bot.wait_element_to_load(xpath_esg)
        esg = bot.find_element(xpath_esg)
        fin["ESG"].append(esg.text)
        print('4')

    except NoSuchElementException:
        fin["ESG"].append(None)

def append_dict(temp : str):
    '''
    Append the Yahoo Finance dictionary with each company's Financial statistics and ESG rating
    
    Parameters
    ----------
    temp : str
    The previous company name appended to the dictionary

    Returns
    -------
    str
        The latest company name appended to the dictionary
    '''     
    try: 
        xpath = '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1' 
        bot.wait_element_to_load(xpath)
        company_xpath = bot.find_element(xpath)
        company_name = company_xpath.text
        print('1')
        temp = append_finance_data(temp, company_name)
        append_esg_data()
        return company_name
                
    except NoSuchElementException:
        bot.append_empty_values(fin)

df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = len(df)

# Set up driver
URL = "https://finance.yahoo.com/lookup"
bot = WebScraper(URL)

# Accept cookies
cookies_xpath = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button'
bot.accept_cookies(cookies_xpath)

#Scrape the website. Extract company names and their respective CSR score
temp = 0
i = 106 
progress_bar = tqdm(total=data_length)
while i < data_length:
    print(i)
    fin = {'fin_Company': [], 'Market Cap':[],'Trailing P/E': [], 'Price/Book (mrq)': [], 'Most Recent Quarter (mrq)':[], 'Profit Margin':[], 'Op_Margin' : [], 'ROA': [], 'ROE': [], 'Diluted EPS' : [], 'Operating_CashFlow' : [], 'Total Debt/Equity (mrq)': [], 'PayoutRat' :[], 'Stock Price': [], 'ESG' : []}
    Company = df.loc[i]['Name']
    class_name = ' Bdrs(0) Bxsh(n)! Fz(s) Bxz(bb) D(ib) Bg(n) Pend(5px) Px(8px) Py(0) H(30px) Lh(30px) Bd O(n):f O(n):h Bdc($seperatorColor) Bdc($linkColor):f Bdc($c-fuji-punch-a):inv C($negativeColor):in M(0) Pstart(10px) Bxz(bb) Bgc(white) W(100%) H(32px)! Lh(32px)! Ff($yahooSansFinanceFont)'           
    try: 
        #Starting the search by finding the search bar and searching for the company
        xpath = f'//*[@class="{class_name}"]'
        sleep(3)
        bot.wait_element_to_load(xpath)
        search_bar = bot.find_element(xpath)
        bot.wait_element_to_load(xpath)
        search_bar.clear()
        search_bar = bot.find_element(xpath)
        bot.wait_element_to_load(xpath)
        search_bar.send_keys(Company)
        sleep(5)
        search_bar = bot.find_element(xpath)
        bot.wait_element_to_load(xpath)
        search_bar.send_keys(Keys.DOWN)
        search_bar = bot.find_element(xpath)
        bot.wait_element_to_load(xpath)
        search_bar.send_keys(Keys.RETURN)
        sleep(4)
        append_dict(temp)
        df1 = bot.convert_dict_to_csv(fin, 'Yahoo_Finance') 
        i += 1    
    
    except NoSuchElementException: 
        # If the webpage changes, the driver is restarted
        print('Restarting the driver')
        bot.driver.quit()
        sleep(60)
        bot = WebScraper(URL)
        bot.accept_cookies(cookies_xpath)
    
    print('6')
    sleep(1)
    progress_bar.update(1)

progress_bar.close()

                
