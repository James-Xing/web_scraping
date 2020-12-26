from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

session = HTMLSession()

base_url = 'https://www.amazon.com.au'

url = 'https://www.amazon.com.au/s?k=motorola+phones'

def get_data(url, session):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

soup = get_data(url=url, session=session)

phonelist = []

def get_deals(soup):
    products = soup.find_all('div', {'data-component-type':'s-search-result'})
    for product in products:
        product_name = product.find('span', {'class':'a-size-base-plus a-color-base a-text-normal'}).text.strip()
        product_link = base_url + product.find('a', {'class':'a-link-normal a-text-normal'})['href'].strip()
        try:
            current_price = float(product.find('span', {'class':'a-price-whole'}).text.replace(',','').strip()
                                 + product.find('span', {'class':'a-price-fraction'}).text.strip())
        except:
            current_price = None

        try:
            original_price = float(product.find('span', {'class':'a-offscreen'}).text.replace('$', '').replace(',','').strip())
        except:
            original_price = None
        try:
            rating = product.find('span', {'class':'a-icon-alt'}).text.strip()
        except:
            rating = ''

        phone = {
            'product_name':product_name,
            'product_link':product_link,
            'current_price':current_price,
            'original_price':original_price,
            'rating':rating
        }

        phonelist.append(phone)
    return

def get_next_page(soup):
    try:
        page = soup.find('ul', {'class':'a-pagination'})
        url = base_url + str(page.find('li', {'class':'a-last'}).find('a')['href'])
        if not page.find('li', {'class': 'a-disabled a-last'}):
            return url
        else:
            return
    except:
        return

while True:
    soup = get_data(session=session,url=url)
    get_deals(soup=soup)
    url=get_next_page(soup)
    if not url:
        break
    else:
        print('proceed to next page')

df = pd.DataFrame(phonelist)

df.to_csv('motorolla_phones.csv', index=False)





