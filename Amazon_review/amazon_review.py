from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

review_list = []

def get_data(url):

    session = HTMLSession()

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'

    r = session.get(url, headers = {'user_agent':user_agent})

    soup = BeautifulSoup(r.content, 'html.parser')

    return soup

def extract_data(soup):

    reviews = soup.find_all('div', {'data-hook':'review'})

    for item in reviews:

        review = {
            'reviewer': item.find('span', {'class':'a-profile-name'}),
            'rating': item.find('i', {'data-hook':'review-star-rating'}),
            'title': item.find('a',{'data-hook':'review-title'}),
            'review_data': item.find('span', {'data-hook':'review-date'})
        }

        review_list.append(review) 

    return reviews   


for i in range(1, 10):
    url = f"https://www.amazon.com/Motorola-Unlocked-T-Mobile-MetroPCS-XT2019-2/product-reviews/B083PSRMQ4/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={i}"
    soup = get_data(url)
    extract_data(soup)
    print(len(review_list))
    if not soup.find('li', {'class':'a-disabled a-last'}):
        pass
    else:
        break


df = pd.DataFrame(review_list)

df.to_csv('amazon_review.csv', index = False)
    



        




