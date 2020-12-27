import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

starting_url = 'https://www.ebay.com.au/sch/i.html?_nkw=tempered+glass+iphone+11&LH_ItemCondition=1000&Compatible%2520Model=For%2520Apple%2520iPhone%252011&rt=nc&Features=Tempered%2520Glass&_dcat=58540&_pgn=1'
product_listings = []

def get_data(url):

    headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    r = requests.get(url=url, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def extract_info(soup):
    products = soup.find_all('div', {'class': 's-item__info clearfix'})
    for product in products:
        try:
            title = product.find('h3', {'class':'s-item__title'}).text.strip()
        except:
            title = ''
        try:
            link = product.find('a', {'class':'s-item__link'})['href']
        except:
            link = ''
        try:
            price = product.find('span', {'class':'s-item__price'}).text.replace('AU $', '').strip()
        except:
            price = None
        try:
            product_info = product.find('span', {'class':'s-item__sme s-item__smeInfo'}).text.strip()
        except:
            product_info = ''
        try:
            brand = product.find('div', {'class':'s-item__subtitle'}).text.replace('Brand new', '').replace('· ', '').strip()
        except:
            brand = ''

        single_product = {
            'title':title,
            'link':link,
            'price':price,
            'product_info':product_info,
            'brand':brand
        }

        product_listings.append(single_product)
    return

def get_nextpage(soup, current_url):
    if not current_url:
        return
    try:
        next_url = soup.find('a', {'class': 'pagination__next'})['href']
    except:
        next_url = None
        return
    if next_url == current_url:
        next_url = None
        return
    return next_url

url = starting_url
while url:
    print('extracting information from a new page')
    soup = get_data(url=url)
    extract_info(soup=soup)
    url = get_nextpage(soup=soup, current_url=url)
    sleep(5)

df = pd.DataFrame(product_listings)
df.to_csv('ebay.csv', index=False)

