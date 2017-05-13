import scrapy
import re
from ..items import Publication

INDEX_URL = 'http://www.aippimm.ro/categorie/transparenta-decizionala---modificare-hg-96-2011/'

def text_from(sel):
    return (sel.xpath('string(.)').extract_first() or "").strip()

def guess_publication_type(text):
    text = text.lower()
    text = re.sub(r'[șş]', 's', text)
    text = re.sub(r'[țţ]', 't', text)
    text = re.sub(r'[ăâ]', 'a', text)
    text = re.sub(r'[î]', 'i', text)
    rules = [
        ("lege", "LEGE"),
        ("hotarare de guvern", "HG"),
        ("hotarare a guvernului", "HG"),
        ("hg", "HG"),
        ("ordonanta de guvern", "OG"),
        ("oug", "OUG"),
        ("ordonanta de urgenta", "OUG"),
        ("ordin de ministru", "OM"),
        ("ordinul", "OM"),
    ]
    for substr, publication_type in rules:
        if substr in text:
            return publication_type
    else:
        return "OTHER"

class AfaceriSpider(scrapy.Spider):

    name = 'afaceri'
    start_urls = [INDEX_URL]

    def parse(self, response):
        for article in response.css('.article_container'):
            link = article.css('a.lead_subcat')
            title = text_from(link)
            if not title:
                continue

            date_match = re.search(
                r'(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})$',
                text_from(article.css('ul.lead')),
            )
            date = "{year}-{month}-{day}".format(**date_match.groupdict())

            identifier = link.css('::attr(href)').extract_first().split('/')[-1]
            publication_type = guess_publication_type(title)

            documents = [
                {
                    'type': href.split('.')[-1],
                    'url': href,
                }
                for href in article.css('a.files::attr(href)').extract()
            ]

            yield Publication(
                identifier=identifier,
                title=title,
                institution='afaceri',
                description=title,
                type=publication_type,
                date=date,
                documents=documents,
            )
