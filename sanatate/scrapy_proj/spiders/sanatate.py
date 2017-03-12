# -*- coding: utf-8 -*-
import scrapy
import scrapy_proj.items
import re

class SanatateSpider(scrapy.Spider):
    name = "sanatate"

    def start_requests(self):
        urls = [
            'http://www.ms.ro/acte-normative-in-transparenta/?vpage=1',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date_regex = re.compile('\d{1,2}[-/]\d{2}[-/]\d{4}')
        email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        tel_regex = re.compile(r'(0?([0-9].?){9})')
        deadline_regex = re.compile(r'termen.*limita.*[^[0-9]]*([0-9]{1,2}).*zi')

        for item in response.css('.panel'):
            heading = item.css('div.panel-heading')
            body = item.css('div.panel-body')
            body_text = ''.join(body.xpath('.//text()').extract())

            documents_anchors = body.xpath('.//a[contains(@href, ".pdf")]')
            documents = []

            for anchor in documents_anchors:
                href = anchor.xpath('.//@href').extract_first()
                name = anchor.xpath('.//text()').extract_first()
                documents.append({
                    'type': name,
                    'url': response.urljoin(href)
                })

            title = item.css('a.panel-title::text').extract_first()
            contact_tel = tel_regex.search(body_text).group(0)
            contact_email = email_regex.search(body_text).group(0)
            start_date = date_regex.search(body_text).group(0)
            feedback_days = int(deadline_regex.search(body_text.lower()).group(1))

            contact = {
                'name': body.xpath('.//p[contains(text(), "Contact")]/text()').re_first(r'Contact:\s*(.*)'),
                'email': contact_email,
                'tel' : contact_tel
            }

            anchors = body.css('a')

            for anchor in anchors:
                href = anchor.css('::attr(href)').extract()

            yield scrapy_proj.items.ActItem(
                title = title,
                contact = contact,
                documents = documents,
                date = start_date,
                feedback_days = feedback_days
            )

        next_pages = response.css('.pt-cv-pagination a::attr(href)').extract()
        next_pages.reverse()
        for next_page in next_pages:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
