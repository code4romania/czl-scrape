# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from crawl_dezvoltare.items import *

from bs4 import BeautifulSoup as bs
import re
from slugify import slugify
from datetime import datetime
import hashlib

class MdrapSpider(scrapy.Spider):
    name = "mdrap"
    allowed_domains = ["gov.ro"]
    start_urls = ['http://www.mdrap.gov.ro/transparenta/consultari-publice/']

    def __init__(self, token=None, *args, **kwargs):
        super(MdrapSpider, self).__init__(*args, **kwargs)
        if token:
            self.token = token

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        article_contents = soup.find('div',id='article_content').find_all('li')
        for article in article_contents:
            article_a = article.find('a')
            if article_a.text == 'Anunturi':
                break
            yield Request(url=article_a['href'], callback=self.get_category)

    def get_category(self, response):
        soup = bs(response.body, 'lxml')
        article_contents = soup.find('div',id='article_content').find_all('li')
        for article in article_contents:
            article_a = article.find('a')
            article_span = article.find('span')

            article_date = article_span.text
            regex = r"\d{2}-\d{2}-\d{4}"
            matches = re.search(regex, article_date)
            if matches:
                article_date = matches.group()

            article_date = datetime.strptime(article_date, '%d-%m-%Y').strftime('%Y-%m-%d')

            article_title = article.text.replace(article_span.text, '')
            article_slug = hashlib.md5(slugify(article.text)).hexdigest()
            article_type = article_a.text
            yield Request(
                url='http://www.mdrap.gov.ro/' + article_a['href'], 
                callback=self.get_article, 
                meta = {
                    'article_title': article_title, 
                    'article_date': article_date, 
                    'article_slug': article_slug, 
                    'article_type': article_type
                    })

    def get_article(self, response):
        item = CrawlDezvoltareItem()
        soup = bs(response.body, 'lxml')
        item['title'] = response.meta['article_title']
        item['date'] = response.meta['article_date']
        item['identifier'] = response.meta['article_slug']
        item['institution'] = 'dezvoltare'

        type_mapping = {
            'hg': 'HG',
            'lege': 'LEGE',
            'ordin': 'OM',
            'omdrapfe': 'OTHER',
            'hotarare a guvernului': 'HG',
            'ordonanta de guvern': 'OG',
            'hotarare de guvern': 'HG',
            'ordonanta de urgenta': 'OUG'
        }

        type_regex = r'HG|Lege|ORDIN|OMDRAPFE|HotarAre a guvernului'
        m = re.search(type_regex, response.meta['article_type'].replace('  ',' '), re.IGNORECASE)
        item['type'] = type_mapping[m.group().lower()]

        article_paragraphs = soup.find('div',id='article_content').find_all('p')

        item['description'] = article_paragraphs[0].text

        email_regex = r"e-mail ([\w\.@]+)"
        fax_regex = r"fax ([\w\.@]+)"
        addr_regex = r"Str. ([\w\.@\s,–]+),"
        email_search = re.search(email_regex, article_paragraphs[2].text)
        addr_search = re.search(addr_regex, article_paragraphs[2].text)
        fax_search = re.search(fax_regex, article_paragraphs[2].text)
        item['contact'] = {
            'email': email_search.groups()[0] if email_search else '',
            'addr': addr_search.groups()[0] if addr_search else '',
            'fax': fax_search.groups()[0] if fax_search else '',
        }

        feedback_regex = r"(\d+) zile"
        feedback_search = re.search(feedback_regex, article_paragraphs[3].text)
        item['feedback_days'] = feedback_search.groups()[0] if feedback_search else None

        article_documents = soup.find('div',id='article_content').find_all('li')
        item['documents'] = []
        for doc in article_documents:
            item['documents'].append({
                'type': doc.find('a').text, 
                'url': 'http://www.mdrap.gov.ro' + doc.find('a')['href']
                })

        return item