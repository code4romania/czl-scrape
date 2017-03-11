# -*- coding: utf-8 -*-
import scrapy


class MdrapSpider(scrapy.Spider):
    name = "mdrap"
    allowed_domains = ["http://www.mdrap.gov.ro/"]
    start_urls = ['http://http://www.mdrap.gov.ro//']

    def parse(self, response):
        pass
