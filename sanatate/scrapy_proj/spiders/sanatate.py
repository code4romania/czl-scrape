# -*- coding: utf-8 -*-

import scrapy
import scrapy_proj.items as items
import scrapy_proj.loaders as loaders
import re
import sys

class SanatateSpider(scrapy.Spider):
    name = 'sanatate'

    def start_requests(self):
        urls = [
            'http://www.ms.ro/acte-normative-in-transparenta/?vpage=2',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date_regex = re.compile('de\s+la\s+(\d{1,2}[-/]\d{2}[-/]\d{4})')
        email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        tel_regex = re.compile(r'[^0-9](0(?:[0-9].?){9})')
        feedback_days_regex = re.compile(r'termen.*limita.*[^[0-9]]*([0-9]{1,2}).*zi')

        for item in response.css('.panel'):
            heading = item.css('div.panel-heading')
            body = item.css('div.panel-body')
            body_text = ''.join(body.xpath('.//text()').extract()).lower()

            title = item.css('a.panel-title::text').extract_first()

            loader = loaders.ActLoader(items.ActItem())
            loader.add_value('title', title)

            contact_loader = loaders.ContactLoader(items.ContactItem())
            contact_loader.add_value('tel', tel_regex.findall(body_text))
            contact_loader.add_value('email', email_regex.findall(body_text))
            loader.add_value('contact', contact_loader.load_item())
            loader.add_value('date', date_regex.findall(body_text))
            loader.add_value('feedback_days', feedback_days_regex.findall(body_text))

            keys = ['type', 'url']
            types = body.xpath('.//a[contains(@href, ".pdf")]').xpath('text()').extract()
            urls = body.xpath('.//a[contains(@href, ".pdf")]').xpath('@href').extract()
            docs = [[types[i], urls[i]] for i in range(len(types))]
            loader.add_value('documents', [dict(zip(keys, doc)) for doc in docs])

            yield loader.load_item()

        next_pages = response.css('.pt-cv-pagination a::attr(href)').extract()
        next_pages.reverse()
        for next_page in next_pages:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
