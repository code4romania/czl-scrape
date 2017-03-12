import requests
from bs4 import BeautifulSoup as beautiful_soup

import utils.settings as settings
from scraper.article import Article


class Extractor:
    """Extractor object, responsible for fetching data from the MAE website.
    """
    url = None
    content = None
    articles = None

    def __init__(self, url):
        self.url = url
        self.content = self._fetch_page()

    def get_all_articles(self):
        """Generates a list of all Article objects fetched from MAE.
        :return: the list of Articles
        """
        self.articles = [Article(table) for table in self._get_tables()]
        return self.articles

    def get_article_by_id(self, identifier):
        """Returns the article matching the given identifier.
        :param identifier: the id
        :return: the matching Article, or None
        """
        if not self.articles:
            self.get_all_articles()

        for a in self.articles:
            if a.identifier == identifier:
                return a

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
