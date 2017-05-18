# coding=utf-8

import datetime
import re

from scrapy import Spider, Request

from ..items import Publication
from ..utils import extract_documents

INDEX_URL = 'https://www.senat.ro/LegiProiect.aspx'


class SenatSpider(Spider):
    name = 'senat'
    start_urls = [INDEX_URL]

    def parse(self, response):
        for entry in response.css('#GridViewProiecte tr > td:nth-child(2) a'):
            href = entry.css('a::attr(href)').extract_first()
            yield Request(response.urljoin(href), self.parse_entry)

    def parse_entry(self, response):
        identifier = response.css(
            '#ctl00_B_Center_ctl06_viewFisa_lblNr::text').extract_first()
        description = response.css(
            '#ctl00_B_Center_ctl06_grdTitlu_ctl02_Label1::text').extract_first()
        title = description
        date_string = response.css(
            '#ctl00_B_Center_ctl06_grdDerulare_ctl02_Label1::text').extract_first()
        date_match = re.match(
            '^(?P<day>\d{1,2})\-(?P<month>\d{1,2})\-(?P<year>\d{4})$',
            date_string)
        if date_match:
            date = datetime.date(
                int(date_match.group('year')),
                int(date_match.group('month')),
                int(date_match.group('day')),
            )
        else:
            date = datetime.date.today()

        documents = [
            {
                'type': re.sub('^[^a-zA-Z]+', '', doc['type'], 1),
                'url': re.sub('\\\\', '/', response.urljoin(doc['url'])),
            } for doc in extract_documents(response.css(
                '#ctl00_B_Center_Accordion1 div.accrdContent a'))
        ]

        contact = {
            'tel': '021 315 8942',
            'email': 'infopub@senat.ro',
        }

        return Publication(
            identifier=identifier,
            title=title,
            institution='senat',
            description=description,
            type='LEGE',
            date=date.isoformat(),
            documents=documents,
            contact=contact
        )
