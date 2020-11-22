import requests
from bs4 import BeautifulSoup
import pandas as pd


def getpage(url):
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException:
        return None
    return BeautifulSoup(req.text, 'html.parser')


base_url = "http://eoddata.com/stocklist/NASDAQ/"
codes = []
names = []
close_prices = []
trading_volumes = []

#The current code stops at stocks starting 'C'. Change to 'Z' for a complete dataset

for letter in [chr(x) for x in range(ord('A'), ord('C') + 1)]:

    url = base_url + letter + '.htm'
    bs = getpage(url)

    if bs is not None:
        stock_elements = []
        table = bs.find('div', {'id': 'ctl00_cph1_divSymbols'})
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                element = td.text
                stock_elements.append(element)


    for i in range(0, len(stock_elements), 10):
        codes.append(stock_elements[i])
        names.append(stock_elements[i + 1])
        close_prices.append(stock_elements[i + 4])
        trading_volumes.append(stock_elements[i + 5])

stocks = pd.DataFrame(index=None)
stocks['code'] = codes
stocks['name'] = names
stocks['close'] = close_prices
stocks['volume'] = trading_volumes

stocks.set_index('code', inplace=True)

stocks.to_csv('stocks.csv')

