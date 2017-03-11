# -*- coding: utf-8 -*-
import scrapy


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
            # print(title)
            yield {'title': title}
