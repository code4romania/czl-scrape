import scrapy
import re

from czlscrape.utils import guess_initiative_type
from ..items import Publication

INDEX_URL = 'http://dialogsocial.gov.ro/categorie/proiecte-de-acte-normative/'

DOC_EXTENSIONS = [
    ".docs", ".doc", ".txt", ".crt", ".xls",
    ".xml", ".pdf", ".docx", ".xlsx",
]

TYPE_RULES = [
    ("lege", "LEGE"),
    ("hotarare de guvern", "HG"),
    ("hotarare a guvernului", "HG"),
    ("ordonanta de guvern", "OG"),
    ("ordonanta de urgenta", "OUG"),
    ("ordin de ministru", "OM"),
    ("ordinul", "OM"),
]


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
        title = text_from(response.css('h1'))
        publication_type = guess_initiative_type(title, TYPE_RULES)

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

        return Publication(
            identifier=identifier,
            title=title,
            institution='dialog',
            description=text_from(article),
            type=publication_type,
            date=date,
            documents=documents,
        )


def main():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(DialogSpider)
    process.start()

if __name__ == '__main__':
    main()
