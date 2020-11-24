import csv
import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.firstclasslearning.co.uk/find-a-centre?postcode=london'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

#Contact information is in Json
script = str(soup.find_all('script')[0])[51:-9]
json_obj = json.loads(script)

#Extract center information, which is a list of dictionaries
centers = json_obj.get('props').get('pageProps').get('centres')

#We only need 5 columns, and ingore the rest

csv_columns = ['centreName', 'centreManagerName','centreEmail','centreTelephoneNumber','centreMobileNumber']
csv_file = "center.csv"
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore')
        writer.writeheader()
        for data in centers:
            writer.writerow(data)
except IOError:
    print("I/O error")

