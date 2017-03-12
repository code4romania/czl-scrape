import scrapy
import re
import requests
import os

API_URL = 'http://czl-api.code4.ro/api/publications/'
API_TOKEN = os.environ['API_TOKEN']

INDEX_URL = 'http://www.cdep.ro/pls/proiecte/upl_pck2015.lista?cam=2&anp=2017'

def upload(doc):
    headers = {'Authorization': 'Token ' + API_TOKEN}
    resp = requests.post(API_URL, json=doc, headers=headers)
    if resp.status_code == 400:
        if re.search(r'Integrity Error: Key .* already exists', resp.text):
            return
    assert resp.status_code == 201

class EducatieSpider(scrapy.Spider):

    name = 'cdep'
    start_urls = [INDEX_URL]

    def parse(self, response):
        for tr in response.css('.grup-parlamentar-list > table > tbody > tr'):
            href = tr.css('a::attr(href)').extract_first()
            url = response.urljoin(href)
            yield scrapy.Request(url, self.parse_proposal)

    def parse_proposal(self, response):
        cale_txt = ' '.join(t.extract() for t in response.css('.cale *::text'))
        plx_code = 'pl-x ' + re.search(r'pl-x\s+(\S+)', cale_txt.lower()).group(1)
        title = response.css('.detalii-initiativa h4::text').extract_first()

        table = response.css('#olddiv > table')[-1]
        for td in table.css('td'):
            td_text = (td.css('::text').extract_first() or '').strip()
            m = re.match(r'^(\d{2})\.(\d{2})\.(\d{4})$', td_text)
            if m:
                date = '{}-{}-{}'.format(m.group(3), m.group(2), m.group(1))
                break

        documents = []

        for pdf_link in response.css('.program-lucru-detalii a'):
            target = pdf_link.css('::attr(target)').extract_first() or ''
            if target.lower() != 'pdf':
                continue
            pdf_href = pdf_link.css('::attr(href)').extract_first()
            pdf_url = response.urljoin(pdf_href)
            label_tds = pdf_link.xpath('../../td')
            pdf_label = ' '.join(
                td.css('::text').extract_first()
                for td in label_tds[1:]
            ).strip()
            documents.append({
                'type': pdf_label,
                'url': pdf_url,
            })

        doc = {
            'identifier': plx_code,
            'title': title,
            'institution': 'cdep',
            'description': '',
            'type': 'LEGE',
            'date': date,
            'documents': documents,
        }
        upload(doc)

def main():
    from scrapy.crawler import CrawlerProcess, Crawler
    process = CrawlerProcess()
    process.crawl(EducatieSpider)
    process.start()

if __name__ == '__main__':
    main()
