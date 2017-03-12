import logging
import requests
from bs4 import BeautifulSoup as beautiful_soup

import utils.settings as settings
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

    def get_all_articles(self):
        """Generates a list of all Article objects fetched from MAE.
        :return: the list of Articles
        """
        return [article for article in self.extract_entry()]

    def extract_entry(self):
        """Article generator.
        Returns the next article from the given page.

        :return: the next Article
        """
        for table in self._get_tables():
            article = Article(table)
            if ArticleSerializer.is_valid(article):
                print(article.__dict__)
                yield article
            else:
                logging.warning("Invalid article: %s", article)

    def get_identifier_list(self):
        """Extracts a list of identifiers of the latest articles.
        :return: list
        """
        latest = []
        for table in self._get_tables():
            tr = table.select('tr')
            article = Article()
            article._extract_article_type(tr)
            article._extract_title(tr)
            article._generate_id()
            latest.append(article.identifier)
        return latest

    def _fetch_page(self):
        page = requests.get(self.url, headers=settings.HEADERS)
        return beautiful_soup(page.text, 'html.parser')

    def _get_tables(self):
        return self.content.select_one('div.art').select('table')
