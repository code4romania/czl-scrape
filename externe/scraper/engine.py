import requests
from bs4 import BeautifulSoup as bs
import scraper.settings as settings
from scraper.article import Article


class Extractor:
  """
  Extractor object, responsible for grabbing data from the MAE website.
  """
  url = None
  content = None

  def __init__(self, url):
    self.url = url
    self.content = self._fetch_page()

  def extract_all_entries(self):
    return [article for article in self.extract_entry()]

  def extract_entry(self):
    tables = self.content.select_one('div.art').select('table')
    for table in tables:
      article = Article(table)
      print('\n title: %s \n description: %s \n urls: %s \n published: %s \n feedback_days: %s \n'
            % (article.article_type, article.title,
               article.documents, article.published_at, article.feedback_days))
      yield article

  def _fetch_page(self):
    page = requests.get(self.url, headers=settings.HEADERS)
    return bs(page.text, 'html.parser')
