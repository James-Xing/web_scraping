# -*- coding: utf-8 -*-
import scrapy


class FclSpider(scrapy.Spider):
    name = 'fcl'
    allowed_domains = ['firstclasslearning.co.uk']
    start_urls = ['http://firstclasslearning.co.uk/']

    def parse(self, response):
        pass
