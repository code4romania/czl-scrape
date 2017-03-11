import requests
from bs4 import BeautifulSoup as bs

import utils.constants as settings
from scraper.article import Article
from scraper.article_serializer import ArticleSerializer


class Extractor:
    """Extractor object, responsible for fetching data from the MAE website.
    """
    url = None
    content = None

    def __init__(self, url):
        self.url = url
        self.content = self._fetch_page()

    def extract_all_entries(self):
        """Generates a list of all Articles objects fetches from MAE.
        :return: the list of Articles
        """
        return [article for article in self.extract_entry()]

    def extract_entry(self):
        """Generates Article objects from the MAE table.
        :return: the next Article
        """
        tables = self.content.select_one('div.art').select('table')
        for table in tables:
            article = Article(table)
            if ArticleSerializer.is_valid(article):
                print(article.__dict__)
                yield article
            else:
                # TODO: Logging
                print("Invalid article: %s" % article)

    def _fetch_page(self):
        page = requests.get(self.url, headers=settings.HEADERS)
        return bs(page.text, 'html.parser')
