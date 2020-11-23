# -*- coding: utf-8 -*-:
import csv
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.item import Item, Field

class FclSpider(scrapy.Spider):
    name = 'fcl'
    allowed_domains = ['firstclasslearning.co.uk']
    base_url = 'https://www.firstclasslearning.co.uk/find-a-centre?postcode='

    def start_requests(self):
		with open("city.csv", "rU") as f:
			reader = csv.DictReader(f)
			for line in reader:
				city = line.pop('city')
				url = base_url + city
				request = Request(url)
				request.meta['city'] = city
				yield request


    def parse(self, response):
        item = Item()
		l = ItemLoader(item=item, response=response)

