# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from crawl_mediu.items import *

from bs4 import BeautifulSoup as bs
import re
from slugify import slugify
from datetime import datetime
import hashlib
from unidecode import unidecode 


class MmediuSpider(scrapy.Spider):
    name = "mmediu"
    allowed_domains = ["gov.ro"]
    start_urls = ['http://www.mmediu.gov.ro/categories/view/proiecte-de-acte-normative/41/page:1']
    page = 2
    first_day_of_year = datetime.now().replace(month=1,day=1, hour=0, minute=0, second=0)

    def __init__(self, token=None, *args, **kwargs):
        super(MmediuSpider, self).__init__(*args, **kwargs)
        if token:
            self.token = token

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        continue_crawl = True
        all_pubs = soup.find_all('article')

        for pub in all_pubs:
            pub_date_str = pub.find('div', class_="date").text.strip()
            pub_date = datetime.strptime(pub_date_str, '%d %b %Y')
            if pub_date < self.first_day_of_year:
                continue_crawl = False
            else:
                pub_title = pub.find('h3', class_='title').find('a')['title']
                pub_date_new = pub_date.strftime('%Y-%m-%d')
                pub_href = 'http://www.mmediu.gov.ro' + pub.find('h3', class_='title').find('a')['href']

                yield Request(
                    url=pub_href, 
                    callback=self.get_article, 
                    meta={
                        'title': pub_title,
                        'date': pub_date_new,
                        'md5': hashlib.md5(slugify(pub_title)).hexdigest()
                    })
        if response.status == 200 and continue_crawl:
            next_url = self.start_urls[0][:-1] + str(self.page)
            self.page += 1
            yield Request(url=next_url)


    def get_article(self, response):
        item = CrawlMediuItem()
        soup = bs(response.body, 'lxml')
        item['title'] = response.meta['title']
        item['date'] = response.meta['date']
        item['identifier'] = response.meta['md5']
        item['institution'] = 'mediu'

        type_mapping = {
            "Proiectul de OM": "OM",
            "Proiectul de Ordonanta de urgenta": "OUG",
            "Proiectul de HG": "HG",
            "Proiectul de Hotarare": "HG",
            "Proiectul de LEGE ": "LEGE",
            "Proiectul de Ordin de Ministru": "OM"
        }

        type_found = False
        for key in type_mapping.keys():
            if key in unidecode(item['title']):
                type_found = True
                item['type'] = type_mapping[key]
        if not type_found:
                item['type'] = 'OTHER'

        article_paragraphs = soup.find('div', class_='text').find_all('p')

        item['description'] = article_paragraphs[0].text

        contact_paragraph = unidecode(article_paragraphs[3].text)

        email_regex = r"[eE]-?mail:* ([\w\.@]+)"
        fax_regex = r"fax:? ([\w\.@]+)"
        tel_regex = r"[telefon/fax:]+ ([\d\.()]+)"
        addr_regex = r"Str. ([\w\.@\s,–]+),"

        email_search = re.search(email_regex, contact_paragraph)
        addr_search = re.search(addr_regex, contact_paragraph)
        fax_search = re.search(fax_regex, contact_paragraph)
        tel_search = re.search(tel_regex, contact_paragraph)

        item['contact'] = {
            'email': email_search.groups()[0] if email_search else '',
            'addr': addr_search.groups()[0] if addr_search else '',
            'fax': fax_search.groups()[0] if fax_search else '',
            'tel': tel_search.groups()[0] if tel_search else '',
        }

        feedback_regex = r"(\d+) zile"
        feedback_search = re.search(feedback_regex, article_paragraphs[2].text)
        item['feedback_days'] = feedback_search.groups()[0] if feedback_search else None

        article_documents = article_paragraphs[1].find_all('a')
        item['documents'] = []
        for doc in article_documents:
            item['documents'].append({
                'type': doc.text, 
                'url': 'http://www.mdrap.gov.ro' + doc['href']
                })

        return item