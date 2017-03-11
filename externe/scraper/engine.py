import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import scraper.settings as settings


def fetch_page(page_url):
  page = requests.get(page_url, headers=settings.HEADERS)
  return bs(page.text, 'html.parser')


def extract_all_entries(content):
  for article in extract_entry(content):
    pass


def parse_page(page_url):
  content = fetch_page(page_url)
  extract_all_entries(content)


def extract_entry(content):
  tables = content.select_one('div.art').select('table')
  for table in tables:
    '''
    "identifier": "lawproposal-first-document-name-slug-or-something",
    // un identificator unic, predictibil (repetabil), pereferabil
    human-readable
    '''
    # contact

    article = Article(table)
    print('\n title: %s \n description: %s \n url: %s \n published: %s \n'
          % (article.article_type, article.description, article.documents, article.published_at))
    yield article


class Article:
  """
  Defines an article object as found on the MAE site.
  """

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

  # HG, OG, OUG, PROIECT
  article_type = None
  description = None
  documents = None
  published_at = None
  contact = None

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
    published_at = self._extract_desc_paragraph(row).split(' ')[1].replace('\xa0', ' ')

  def _extract_desc_paragraph(self, row):
    return row[2].select('td')[0].select('p')[1].text
