# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from items import JustPublication

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.just.ro/transparenta-decizionala/acte-normative/proiecte-in-dezbatere/?lcp_page0=1",
            callback=self.parse)

    def parse(self, response):
        for li_item in response.css('#content div.entry-content ul.lcp_catlist li'):
            title = li_item.css('h3.lcp_post a::text').extract_first()
            item = JustPublication(title=title)
            yield item
        pass
