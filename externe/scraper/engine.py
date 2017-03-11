import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import scraper.settings as settings


class Extractor:

  url = None
  content = None

  def __init__(self, url):
    self.url = url

  def fetch_page(self):
    page = requests.get(self.url, headers=settings.HEADERS)
    self.content = bs(page.text, 'html.parser')

  def parse_page(self):
    self.fetch_page()
    self.extract_all_entries()

  def extract_all_entries(self):
    for article in self.extract_entry():
      pass

  def extract_entry(self):
    tables = self.content.select_one('div.art').select('table')
    for table in tables:
      article = Article(table)
      print('title: %s \n urls: %s \n published: %s \n\n'
            % (article.article_type, article.documents, article.published_at))
      yield article


class Article:
  """
  Defines an article object as found on the MAE site.
  """
  DATE_REGX = '[0-9]{2}(.*)[0-9]{4}'
  DESCRIPTION_FMT = '{0} {1}'

  def __init__(self, table):
    """
    Builds an Article object from a given HTML table.
    :param table: the table.
    :return: the current object.
    """
    try:
      tr = table.select('tr')
      self._build_contact(tr)
      self._build_documents(tr)
      self.article_type = self._extract_article_type(tr)
      self._extract_description(tr)
      self._extract_published_at(tr)
    except Exception:
      print('Unable to build article from table')

  article_type = None # HG, OG, OUG, PROIECT
  description = None
  documents = None
  published_at = None
  contact = None
  institution = settings.INSTITUTION

  def _build_contact(self, row):
    """
    Builds a contact dict from a given table.
    :param table: the given table row
    :return: None
    """
    pass

  def _build_documents(self, row):
    """
    Builds the documents dict from a given table.
    :param row: the given table row
    :return: None
    """
    self.documents = [
      dict(
        type='Decizie - anexa',
        url=row[0].select('td > p > a')[0].attrs['href']
      ),
      dict(
        type='Nota de fundamentare - anexa',
        url=row[1].select('td > p > a')[0].attrs['href']
      )
    ]

  def _extract_article_type(self, row):
    """
    extracts the title from a given HTML table.
    :param row: the given table row
    :return: String
    """
    return row[0].find_all('strong')[0].text

  def _extract_description(self, row):
    """
    extracts the description from a given HTML table.
    :param table: the given table row
    :return: None
    """
    art_type = self._extract_article_type(row).lower().capitalize()
    desc_text = row[0].find_all('strong')[1].text
    self.description = self.DESCRIPTION_FMT.format(art_type, desc_text)

  def _extract_published_at(self, row):
    """
    extracts the published_at attribute from a given HTML table.
    :param row: the given table row
    :return: None
    """
    desc_paragraph = self._extract_desc_paragraph(row)
    match = re.search(self.DATE_REGX, desc_paragraph)
    # self.published_at = .split(' ')[1].replace('\xa0', ' ')

  def _extract_desc_paragraph(self, row):
    return row[2].select('td')[0].select('p')[1].text
