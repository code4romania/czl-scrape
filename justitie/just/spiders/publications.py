# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor

import datetime
import locale
try:
    locale.setlocale(locale.LC_ALL, "ro_RO.UTF-8")
except:
    locale.setlocale(locale.LC_ALL, "Romanian")

from unidecode import unidecode
import re

from scrapy.loader import ItemLoader

from just.items import JustPublication


class PublicationSpider(scrapy.Spider):
    name = "publication"

    def start_requests(self):
         yield scrapy.Request(
             url="http://www.just.ro/transparenta-decizionala/acte-normative/proiecte-in-dezbatere/",
             callback=self.parse)

    def parse(self, response):
        for li_item in response.css('#content div.entry-content ul.lcp_catlist li'):
            title = li_item.css('h3.lcp_post a::text').extract_first().strip()
            text_date = li_item.css('::text').extract_first().strip()

            try:
                date_obj = datetime.datetime.strptime(text_date, '%d %B %Y')
                date = date_obj.date().isoformat()
            except ValueError:
                date = None

            paragraphs = li_item.xpath('p').xpath("string()").extract()
            description = '\n'.join(paragraphs)

            feedback_days = None
            feedback_date = self.get_feedback_date(description)
            if feedback_date:
                days_diff = feedback_date - date_obj
                feedback_days = days_diff.days

            links = li_item.css('a')
            documents = self.get_documents_from_links(links)

            item = JustPublication(
                title=title,
                type=self.get_type(title),
                identifier=self.slugify(title)[0:127],
                date=date,
                institution='justitie',
                description=description,
                documents=documents,
                contact=self.get_contacts(description),
                feedback_days=feedback_days
            )

            yield item

        paginationLinkEx = LinkExtractor(restrict_css='ul.lcp_paginator')
        pages = paginationLinkEx.extract_links(response)
        for page in pages:
            yield scrapy.Request(page.url, callback=self.parse)


        pass


    def get_feedback_date(self, text):
        text = unidecode(text.strip().lower())

        regex = re.findall(r'pana la data de (.{3,20}20\d\d)', text)
        formats = ['%d %B %Y', '%d.%m.%Y']
        for result in regex:
            for format in formats:
                try:
                    date = datetime.datetime.strptime(result, format)
                    if date:
                        return date
                except ValueError:
                    pass

    def get_contacts(self, text):
        text = unidecode(text.strip().lower())

        contact = {}

        emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{2,5})", text)
        contact['email'] = list(set(emails))

        numbers = re.findall(r'((fax|telefon)[^\d]{1,10}(\d(\d| |\.){8,11}\d))', text)
        for number in numbers:
            key = number[1]
            value = number[2].replace(' ','').replace('.', '')
            if key in contact:
                contact[key].push(value)
            else:
                contact[key] = [value]

        for k,v in contact.items():
            contact[k] = ','.join(v)

        return contact

    def get_type(self, text):
        text = unidecode(text).lower().strip()
        type = None

        stop_pos = re.search(r'(pentru|privind)', text).start()
        if stop_pos:
            text = text[0:stop_pos]

        if re.search(r'ordin', text):
            type = 'OM'

        if re.search(r'lege', text):
            type = 'LEGE'

        if re.search(r'hotarare', text):
            type = 'HG'

        if re.search(r'ordonanta', text):
            if re.search(r'urgenta', text):
                type = 'OUG'
            else:
                type = 'OG'

        return type

    def slugify(self, text):
        text = unidecode(text).lower()
        return re.sub(r'\W+', '-', text)

    def get_documents_from_links(self, links):
        valid_links = []

        for link in links:
            href = link.xpath('@href').extract_first()
            text = link.xpath('text()').extract_first()
            if href:
                if re.search(r'\.(doc|docx|csv|xml|html|txt|pdf|xls|xlsx|rar|zip)$', href, re.IGNORECASE):
                    valid_links.append({
                        'url': href,
                        'type': text
                    })

        return valid_links