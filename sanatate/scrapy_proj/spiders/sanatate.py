# -*- coding: utf-8 -*-
import scrapy

# temporary remove whitespace function
def rws(str):
    if str:
        return ' '.join(str.split())
    else:
        return None

class SanatateSpider(scrapy.Spider):
    name = "sanatate"

    def start_requests(self):
        urls = [
            'http://www.ms.ro/acte-normative-in-transparenta/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for title in response.css('.panel-group div.panel-heading a::text').extract():
            yield {'title': rws(title)}

        next_pages = response.css('.pt-cv-pagination a::attr(href)').extract()
        next_pages.reverse()
        for next_page in next_pages:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
