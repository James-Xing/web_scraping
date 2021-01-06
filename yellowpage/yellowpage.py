from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

restaurant_list = []

def get_data(url):

    session = HTMLSession()

    r = session.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    return soup


def extract_data(soup):
    items = soup.find_all('div', {'class':'listing listing-search listing-data'})

    for item in items:

        try:
            title = item.find('a', {'class':'listing-name'}).text.strip()
        except:
            title = ''
        
        try:
            phone_number = item.find('span', {'class':'contact-text'}).text.strip()
        except:
            phone_number = ''
        
        try:
            email = item.find('a', {'class':'contact contact-main contact-email'})['data-email']
        except:
            email = ''

        to_return = {
            'title': title,
            'phone_number': phone_number,
            'email': email
        }

        restaurant_list.append(to_return)

    return

for i in range(1, 10):
    url = f"https://www.yellowpages.com.au/search/listings?clue=Restaurant&eventType=pagination&locationClue=Newcastle%2C+NSW+2300&pageNumber={i}"
    soup = get_data(url=url)
    extract_data(soup)

    if not soup.find('a', {'class':'pagination navigation'}):
        break
    else:
        print('scrape a new page')


df = pd.DataFrame(restaurant_list)

df.to_csv('yp.csv', index = False)