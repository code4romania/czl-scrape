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

from just.items import JustPublication

class TineretSpider(scrapy.Spider):
    name = "tineret"

    def start_requests(self):
         yield scrapy.Request(
             url="http://mts.ro/proiecte-legislative-in-dezbatere-publica/",
             callback=self.parse)

    def parse(self, response):
        articleLinks = LinkExtractor(restrict_css='div.main > div.article')
        pages = articleLinks.extract_links(response)
        for page in pages:
            yield scrapy.Request(page.url, callback=self.parse_article)

    def parse_article(self, response):
        article_node = response.css('div.main>div.article')

        title = article_node.css('h3.article-title::text').extract_first().strip()
        title = self.get_title(title)

        text_date = article_node.css('span.date::text').extract_first().strip()
        try:
            date_obj = datetime.datetime.strptime(text_date, '%d.%m.%Y')
            date = date_obj.date().isoformat()
        except ValueError:
            date = None

        content_node = article_node.css('div.article-content')
        paragraphs = content_node.xpath('*').xpath("string()").extract()
        description = '\n'.join(paragraphs)

        feedback_days = None
        feedback_date = self.get_feedback_date(description)
        if feedback_date:
            days_diff = feedback_date - date_obj
            feedback_days = days_diff.days

        links = content_node.css('a')
        documents = self.get_documents_from_links(links)

        item = JustPublication(
            title=title,
            type=self.get_type(title),
            identifier=self.slugify(title)[0:127],
            date=date,
            institution='tineret',
            description=description,
            documents=documents,
            contact=self.get_contacts(description),
            feedback_days=feedback_days
        )

        print(item.items())

    def get_feedback_date(self, text):
        formats = ['%d %B %Y', '%d.%m.%Y']
        text = unidecode(text.strip().lower())

        phrase = re.search(r'data limita.*((\d\d?\.\d\d?\.20\d\d)|(\d\d?\s[a-z]+\s20\d\d))', text)
        if phrase:
            date = re.search(r'(\d\d?\.\d\d?\.20\d\d)|(\d\d?\s[a-z]+\s20\d\d)', phrase.group(0))

            if date:
                date = date.group(0)
                for format in formats:
                    try:
                        result = datetime.datetime.strptime(date, format)
                        if result:
                            return result
                    except ValueError:
                        pass

    def get_contacts(self, text):
        text = unidecode(text.strip().lower())

        contact = {}

        emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{2,5})", text)
        contact['email'] = list(set(emails))

        numbers = re.findall(r'((fax|telefon|tel)[^\d]{1,10}(\d(\d| |\.){8,11}\d))', text)
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

    def get_title(self, text):
        idx = 0
        parts = text.split()
        for i in range(len(parts)):
            if len(parts[i]) > 1:
                idx = i
                break

        text = '%s %s' % (''.join(parts[:idx]), ' '.join(parts[idx:]))
        return text

    def get_type(self, text):
        text = unidecode(text).lower().strip()
        type = None

        stop_pos = re.search(r'(pentru|privind)', text)
        if stop_pos:
            text = text[0:stop_pos.start()]

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