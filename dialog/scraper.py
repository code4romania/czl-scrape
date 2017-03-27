import scrapy
import re
import requests
import os

API_URL = 'http://czl-api.code4.ro/api/publications/'
API_TOKEN = os.environ['API_TOKEN']

INDEX_URL = 'http://dialogsocial.gov.ro/categorie/proiecte-de-acte-normative/'

DOC_EXTENSIONS = [
    ".docs", ".doc", ".txt", ".crt", ".xls",
    ".xml", ".pdf", ".docx", ".xlsx",
]

def upload(doc):
    headers = {'Authorization': 'Token ' + API_TOKEN}
    resp = requests.post(API_URL, json=doc, headers=headers)
    if resp.status_code == 400:
        if re.search(r'Integrity Error: Key .* already exists', resp.text):
            return
    assert resp.status_code == 201

def text_from(sel):
    return sel.xpath('string(.)').extract_first().strip()

class DialogSpider(scrapy.Spider):

    name = 'dialog'
    start_urls = [INDEX_URL]

    def parse(self, response):
        for article in response.css('#content article.post'):
            href = article.css('.entry-title a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(href), self.parse_article)

    def parse_article(self, response):
        article = response.css('#content article.post')[0]

        id_value = article.css('::attr(id)').extract_first()
        identifier = re.match(r'post-(\d+)', id_value).group(1)

        date = (
            article.css('time.entry-date::attr(datetime)')
            .extract_first()[:10]
        )

        # remove <div class="fb-comments"> and everything below
        to_remove = article.css('.fb-comments')[0].root
        while to_remove is not None:
            next_to_remove = to_remove.getnext()
            to_remove.getparent().remove(to_remove)
            to_remove = next_to_remove

        documents = [
            {
                'type': href.split('.')[-1],
                'url': href,
            }
            for href in article.css('a::attr(href)').extract()
            if any(href.endswith(ext) for ext in DOC_EXTENSIONS)
        ]

        doc = {
            'identifier': identifier,
            'title': text_from(response.css('h1')),
            'institution': 'dialog',
            'description': text_from(article),
            'type': '',
            'date': date,
            'documents': documents,
        }
        print('result:', doc)
        #upload(doc)

def main():
    from scrapy.crawler import CrawlerProcess, Crawler
    process = CrawlerProcess()
    process.crawl(DialogSpider)
    process.start()

if __name__ == '__main__':
    main()
