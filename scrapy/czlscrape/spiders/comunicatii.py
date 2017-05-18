import hashlib
import os
from datetime import datetime

import logging
from scrapy import Spider
from scrapy.crawler import CrawlerProcess

from czlscrape.utils import guess_initiative_type
from czlscrape.items import Publication

INSTITUTION = 'comunicatii'
WRAPPER_XPATH = '//div/div[3]/div/div/div[2]/div/div/div/div/div'
NO_TYPE = "OTHER"
TYPE_RULES = [
    ("proiect de lege", "LEGE"),
    ("lege nr.", "LEGE"),
    ("proiect de hotarare", "HG"),
    ("hotarare pentru", "HG"),
    ("hotarare nr.", "HG"),
    ("ordonanta pentru", "OG"),
    ("ordonanta privind", "OG"),
    ("ordonanta de urgenta", "OUG"),
    ("ordin de ministru", "OM"),
    ("ordinul", "OM"),
]


def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()


def is_title(node):
    text_list = node.xpath('span/text()').extract()
    if not text_list:
        text_list = node.xpath('text()').extract()
    if text_list:
        if guess_initiative_type(text_list[0], TYPE_RULES) != NO_TYPE:
            return True
    return False


def is_document(node):
    if node.xpath('a/@href'):
        return True
    return False


def is_current_item_complete(current_item, processed_ids):
    if current_item and current_item['identifier'] not in processed_ids:
        processed_ids.append(current_item['identifier'])
        logger.debug(
            '\ntitle: %s\ntype: %s\ndate: %s \ndocuments: %s '
            '\nidentifier: %s' % (
                current_item['title'], current_item['type'],
                current_item['date'], current_item['documents'],
                current_item['identifier']
            )
        )
        return True
    return False


def extract_documents(node, current_item):
    for url in node.xpath('a/@href').extract():
        doc = {
            'type': url.split('.')[-1],
            'url': url,
        }
        current_item['documents'].append(doc)


def extract_title(node):
    try:
        return node.xpath('span/text()').extract()[0]
    except IndexError:
        return node.xpath('text()').extract()[0]


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class ComunicatiiSpider(Spider):
    name = "comunicatii"
    start_urls = [
        'http://www.comunicatii.gov.ro/?page_id=3517',
    ]

    def parse(self, response):
        current_item = None
        processed_ids = list()
        for node in (response.xpath(WRAPPER_XPATH)[0]
                     .xpath('child::node()').xpath('//p')):

            if is_title(node):
                # New title node means new article. Check and post the old one.
                if is_current_item_complete(current_item, processed_ids):
                    yield current_item

                title = extract_title(node)
                article_type = guess_initiative_type(title, TYPE_RULES)
                current_item = Publication(
                    identifier=generate_id(node.extract()),
                    title=title,
                    type=article_type,
                    institution=INSTITUTION,
                    date=datetime.utcnow().date(),
                    documents=list()
                )

            if is_document(node):
                if not (current_item and current_item.get('title')):
                    logger.warning(
                        'Found documents with null current_item or no title.'
                    )
                extract_documents(node, current_item)


def main():
    process = CrawlerProcess()
    process.crawl(ComunicatiiSpider)
    process.start()

if __name__ == '__main__':
    main()
