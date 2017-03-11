# -*- coding: utf-8 -*-
import scrapy


class SanatateSpider(scrapy.Spider):
    name = "sanatate"
    allowed_domains = ["www.ms.ro"]
    start_urls = ['http://www.ms.ro/']

    def parse(self, response):
        pass
