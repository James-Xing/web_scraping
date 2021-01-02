from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd


session = HTMLSession()

url = 'https://www.amazon.com/SanDisk-MicroSDXC-Nintendo-Switch-SDSQXAO-128G-GNCZN/product-reviews/B07KXQX3S3/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'

r = session.get(url, headers = {'user_agent':user_agent})

soup = BeautifulSoup(r.content, 'html.parser')

reviews = soup.find_all('div', {'data-hook':'review'})

for review in reviews:
    reviewer = review.find('span', {'class':'a-profile-name'})
    rating = review.find('i', {'data-hook':'review-star-rating'})
    title = review.find('a',{'data-hook':'review-title'})
    review_data = review.find('span', {'data-hook':'review-date'})
    print(reviewer, rating, title, review_data)

