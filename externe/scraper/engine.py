import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import scraper.settings as settings


class Extractor():

  url = None
  
  def __init__(url):
    self.url = url

  def fetch_page():
    page = requests.get(self.url, headers=settings.HEADERS)
    return bs(page.text, 'html.parser')

  def parse_page():
    content = fetch_page()
    extract_all_entries(content)

  def extract_all_entries(content):
    for article in extract_entry(content):
      pass

  def extract_entry(content):
    tables = content.select_one('div.art').select('table')
    for table in tables:
      article = Article(table)
      print('title: %s \n urls: %s \n published: %s \n\n'
            % (article.article_type, article.documents, article.published_at))
      yield article


class Article:
  """
  Defines an arctile object as found on the MAE site.
  """
  def __init__(self, table):
    """
    Builds an Article object from a given HTML table.
    :param table: the table.
    :return: the current object.
    """
    self._build_contact(table)
    self._build_documents(table)
    self._extract_title(table)
    self._extract_description(table)
    self._extract_published_at(table)

  article_type = None # HG, OG, OUG, PROIECT
  description = None
  documents = None
  published_at = None
  contact = None
  institution = settings.INSTITUTION


  def _extract_type(self, table):
    """
    extracts and process the type from a given HTML table.
    :param table: the given table
    :return: None
    """
    type = t.select('tr')[0].select('td > p')[0].text
    if type in settings.TYPES:
      self.article_type = settings.TYPES['type']
    else:
      print("Type is not annotated")

  def _build_contact(self, table):
    """
    Builds a contact dict from a given table.
    :param table: the given table
    :return: None
    """
    pass

  def _build_documents(self, table):
    """
    Builds the documents dict from a given table.
    :param table: the given table
    :return: None
    """
    self.documents = [
      dict(
        type='Decizie - anexa',
        url=table.select('tr')[0].select('td > p > a')[0].attrs['href']
      ),
      dict(
        type='Nota de fundamentare - anexa',
        url=table.select('tr')[1].select('td > p > a')[0].attrs['href']
      )
    ]

  def _extract_title(self, table):
    """
    extracts the title from a given HTML table.
    :param table: the given table
    :return: None
    """
    self.article_type = table.select('tr')[0].select('td')[0].text.strip().replace('\n', ' ')

  def _extract_description(self, table):
    """
    extracts the description from a given HTML table.
    :param table: the given table
    :return: None
    """
    self.description = None

  def _extract_published_at(self, table):
    """
    extracts the published_at attribute from a given HTML table.
    :param table: the given table
    :return: None
    """
    published_at = table.select('tr')[2].select('td')[0].select('p')[1].text\
      .split(' ')[1].replace('\xa0', ' ')
