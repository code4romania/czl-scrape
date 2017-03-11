# -*- coding: utf-8 -*-
import scrapy

import datetime
import locale
locale.setlocale(locale.LC_ALL, "ro_RO.UTF-8")

from unidecode import unidecode
import re

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
            title = li_item.css('h3.lcp_post a::text').extract_first().strip()
            text_date = li_item.css('::text').extract_first().strip()

            date = datetime.datetime.strptime(text_date, '%d %B %Y')
            date = date.date().isoformat()

            item = JustPublication(
                title=title,
                identifier=self.slugify("%s-%s" % (text_date, title) ),
                date=date
            )

            self.logger.info(item.items())

            yield item
        pass

    def slugify(self, text):
        text = unidecode(text).lower()
        return re.sub(r'\W+', '-', text)