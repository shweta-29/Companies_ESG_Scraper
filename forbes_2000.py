"""Forbes 2000 website scrape

This script allows the user to scrape the Forbes 2020 comapnies from the 
Forbes website
Website link: "https://www.forbes.com/lists/global2000/#173f1d785ac0"

The output is a comma separated value file (.csv) with Forbes 2000 
Companies name and their financial information
"""

from tqdm import tqdm 
from scraper import WebScraper

# Set up driver
URL = "https://www.forbes.com/lists/global2000/#173f1d785ac0"
bot = WebScraper(URL)

# Extract path of all the rows in the table
def table_info_extract() -> list:
    """
    Get the xpath of all the rows containing the company information in the webpage
    
    Returns
    -------
    list
        A list with element containing the xpath of a company on the Forbes webpage
    """
    table_xpath = '//*[@id="row-4"]/div/ul/li/div/div/table'
    bot.wait_element_to_load(table_xpath)
    table = bot.find_element(table_xpath)
    body = table.find_element_by_tag_name('tbody')
    rows = body.find_elements_by_tag_name('tr')
    return rows

def append_dict(rows: list) -> dict :
    '''
    Append the Forbes dictionary with Company Name, Forbes rank, country 
    and financial information such as Sales, Profit, Assets, market value
    
    Parameters
    ----------
    rows : list
        The xpath of all the rows to get the company information from.

    Returns
    -------
    dict
        A dictionary containing Forbes 2020 Companies information        
    '''
    count = 0
    n = 106
    for row in tqdm(rows[:n]): #106
          # Define dictionary
        forbes = {'Rank': [], 'Name': [], 'Country': [], 'Sales': [],
          'Profit': [], 'Assets': [], 'Market Value': []}
        count += 1
        if count % 16 !=0:   #Scrape all the 100 rows on a page. Eveyry 16th row has an ad, so skip that
            info = row.find_elements_by_tag_name('td')
            forbes['Rank'].append(info[0].text)
            forbes['Name'].append(info[1].text)
            forbes['Country'].append(info[2].text)
            forbes['Sales'].append(info[3].text)
            forbes['Profit'].append(info[4].text)
            forbes['Assets'].append(info[5].text)
            forbes['Market Value'].append(info[6].text)
    return forbes 

# Click next page
def move_to_next_page():
    next_page = bot.find_element('//*[@id="row-4"]/div/ul/li/div/div/div[2]/div/div/ul/li[11]/a')
    bot.driver.execute_script("arguments[0].click();", next_page)                                        

# Accept cookies
cookies_xpath = '//*[@id="truste-consent-button"]'
bot.accept_cookies(cookies_xpath)

# 1st page run
rows = table_info_extract()
forbes = append_dict(rows)
# Save the data into a csv file
bot.convert_dict_to_csv(forbes,'forbes_list') 


# Run Page 2 to 20th
pages = 20
for i in range(1,pages): #20
    move_to_next_page() 
    rows = table_info_extract()
    forbes = append_dict(rows)
    bot.convert_dict_to_csv(forbes,'forbes_list')                                    


