import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm 
import scraper
from scraper import WebScraper 

df = pd.read_csv('Forbes.csv', index_col = 0)
data_length = len(df)

# Open Website 
def start_website():
    # Set up the webdriver
    URL = "https://finance.yahoo.com/lookup"
    bot = scraper.WebScraper(URL)
    #Accept cookies
    cookies_xpath = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button'
    bot.accept_cookies(cookies_xpath)
    return bot, bot.driver

bot, driver = start_website()

#Scrape the website. Extract company names and their respective CSR score
temp = 0
for i in tqdm(range(data_length)): #range(data_length)
    fin = {'fin_Company': [], 'Market Cap':[],'Trailing P/E': [], 'Price/Book (mrq)': [], 'Most Recent Quarter (mrq)':[], 'Profit Margin':[], 'Op_Margin' : [], 'ROA': [], 'ROE': [], 'Diluted EPS' : [], 'Operating_CashFlow' : [], 'Total Debt/Equity (mrq)': [], 'PayoutRat' :[], 'Stock Price': [], 'ESG' : []}
    Company = df.loc[i]['Name']
    class_name = ' Bdrs(0) Bxsh(n)! Fz(s) Bxz(bb) D(ib) Bg(n) Pend(5px) Px(8px) Py(0) H(30px) Lh(30px) Bd O(n):f O(n):h Bdc($seperatorColor) Bdc($linkColor):f Bdc($c-fuji-punch-a):inv C($negativeColor):in M(0) Pstart(10px) Bxz(bb) Bgc(white) W(100%) H(32px)! Lh(32px)! Ff($yahooSansFinanceFont)'           
    try: 
        xpath = f'//*[@class="{class_name}"]'
        #time.sleep(3)
        bot.wait_element_to_load(xpath)
        search_bar = driver.find_element_by_xpath(xpath)
        #time.sleep(4)
        bot.wait_element_to_load(xpath)
        search_bar.clear()
        search_bar = driver.find_element_by_xpath(xpath)
        bot.wait_element_to_load(xpath)
        search_bar.send_keys(Company)
        #time.sleep(5)
        bot.wait_element_to_load(xpath)
        search_bar.send_keys(Keys.DOWN, Keys.RETURN)
        time.sleep(3)
        
        try: 
            xpath = '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1' 
            bot.wait_element_to_load(xpath)
            company_xpath = driver.find_element_by_xpath(xpath)
            company = company_xpath.text
            if temp == company:
                bot.empty_append(fin)
                continue
            else:
            
                xpath_stats_button = '//*[@data-test="STATISTICS"]'
                bot.wait_element_to_load(xpath_stats_button)
                statistics_button = driver.find_element_by_xpath(xpath_stats_button)
                statistics_button.click()
                xpath_stats = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[2]/td[2]'
                bot.wait_element_to_load(xpath_stats)
                mcap = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]')
                pe = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]')
                pb = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]')
                quar = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[1]/div/div/table/tbody/tr[2]/td[2]')
                pm = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td[2]')
                op = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[2]/td[2]')
                roa = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[3]/div/div/table/tbody/tr[1]/td[2]')
                roe = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[3]/div/div/table/tbody/tr[2]/td[2]')
                eps = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div/table/tbody/tr[7]/td[2]')
                cf = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[6]/div/div/table/tbody/tr[1]/td[2]')
                d2e = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[4]/td[2]')
                por = driver.find_element_by_xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[6]/td[2]')
                st_p = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')

                fin["fin_Company"].append(company)
                fin["Market Cap"].append(mcap.text)
                fin["Trailing P/E"].append(pe.text)
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

                temp = company         

        except NoSuchElementException:
            bot.empty_append(fin)
            pass

        try:
            #xpath_button_esg = '//*[@id="quote-nav"]/ul/li[11]/a'
            xpath_button_esg = '//*[@id="quote-nav"]/ul/li[11]/a/span'
            #xpath_button_esg = '//*[@data-test="SUSTAINABILITY"]'
            bot.wait_element_to_load(xpath_button_esg)
            button = driver.find_element_by_xpath(xpath_button_esg)
            button.click()
            xpath_esg = '//div[@class="Fz(36px) Fw(600) D(ib) Mend(5px)"]' 
            bot.wait_element_to_load(xpath_esg)
            esg = driver.find_element_by_xpath(xpath_esg)
            fin["ESG"].append(esg.text)

        except NoSuchElementException:
            fin["ESG"].append(None)
            pass
    
    except NoSuchElementException: 
        print(f'Could not find company: {Company}')
        print('Restarting the driver')
        #i -= 1
        bot.empty_append(fin)
        driver.quit()
        time.sleep(60)
        driver = start_website()
        continue
    
    # Save the data into a csv file 
    df1 = bot.convert_to_csv(fin, i, 'Fin1') 
 

                
