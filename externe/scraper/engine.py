import requests
import re
from datetime import date, timedelta
from bs4 import BeautifulSoup as bs

import scraper.settings as settings


class Extractor:

  url = None
  content = None

  def __init__(self, url):
    self.url = url
    self.content = self._fetch_page()

  def _fetch_page(self):
    page = requests.get(self.url, headers=settings.HEADERS)
    return bs(page.text, 'html.parser')

  def extract_all_entries(self):
    for article in self.extract_entry():
      pass

  def extract_entry(self):
    tables = self.content.select_one('div.art').select('table')
    for table in tables:
      article = Article(table)
      print('\n title: %s \n description: %s \n urls: %s \n published: %s \n debate_until: %s \n'
            % (article.article_type, article.description,
               article.documents, article.published_at, article.debate_until))
      yield article


class Article:
  """
  Defines an article object as found on the MAE site.
  """
  DATE_REGX = r'(\d+)\s([a-zA-Z]*)\s(\d{4})'
  TIMEDELTA_REGX = '(timp\sde\s([0-9]+)\szile)'
  DESCRIPTION_FMT = '{0} {1}'
  CONTACT_REGX = dict(
    MAIL=r'e-mail:?(.*?@.*?\..*?)(?:\s|\.|,)',
    PHONE=r'telefon:?\s*((\d+\s?)*)(,|\s|\.)?',
    FAX=r'fax:?\s*((\d+\s?)*)(,|\s|\.)?',
    ADDRESS=r'adresa poştală a (.*? cod(:|\s)?\d+)',
    # ADDRESS=r'adresa poştală a (.*)\.'
  )

  def __init__(self, table):
    """
    Builds an Article object from a given HTML table row
    :param table: the table.
    :return: the current object.
    """
    try:
      tr = table.select('tr')
      self._build_contact(tr)
      self._build_documents(tr)
      self._extract_article_type(tr)
      self._extract_description(tr)
      # Need published_at for debate_until
      self._extract_published_at(tr)
      self._extract_debate_until(tr)
    except Exception:
      print('Unable to build article from table')

  article_type = None # HG, OG, OUG, PROIECT
  description = None
  documents = None
  published_at = None
  debate_until = None
  contact = None
  institution = settings.INSTITUTION

  def _build_contact(self, row):
    """
    Builds a contact dict from a given table.
    :param table: the given table row
    :return: None
    """
    contact_paragraph = row[2].select('p')[0].text
    self.contact = dict()
    for field in ['MAIL', 'PHONE', 'FAX', 'ADDRESS']:
      aux = re.search(self.CONTACT_REGX[field], contact_paragraph)
      if aux:
        self.contact[field.lower()] = aux.group(1).strip()
      else:
        print('Unable to match %s for pargaraph: %s' % (field.lower(), contact_paragraph))


  def _build_documents(self, row):
    """
    Builds the documents dict from a given table.
    :param row: the given table row
    :return: None
    """
    self.documents = [
      dict(
        type='Decizie - anexa',
        url=row[0].select('td')[0].select('a')[0].attrs['href']
      ),
      dict(
        type='Nota de fundamentare - anexa',
        url=row[1].select('td')[0].select('a')[0].attrs['href']
      )
    ]

  def _extract_article_type(self, row):
    """
    extracts and sets the title from a given HTML table row
    :param row: the given table row
    :return: String
    """
    type = row[0].find_all('a')[0].text
    if type in settings.TYPES:
      self.article_type = settings.TYPES[type]
    else:
      print("%s not defined as article type" % type)
    return type

  def _extract_description(self, row):
    """
    extracts and sets the description from a given HTML table row
    :param table: the given table row
    :return: None
    """
    #TODO here
    art_type = self._extract_article_type(row).lower().capitalize()
    desc_text = row[0].find_all('a')[1].text.rstrip('\n')
    self.description = self.DESCRIPTION_FMT.format(art_type, desc_text)

  def _extract_published_at(self, row):
    """
    extracts and sets the published_at attribute from a given HTML table row.
    :param row: the given table row
    :return: None
    """
    published_text = row[-1].find_all('p')[-1].text
    match = re.search(self.DATE_REGX, published_text)
    if match:
      self.published_at = self._build_date_from_match(match)

  def _extract_debate_until(self, row):
    """
    extracts and sets the debate_until attribute from a given HTML table row.
    :param row: the given table row
    :return: None
    """
    desc_text = row[-1].find_all('p')[0].text
    match = re.search(self.DATE_REGX, desc_text)
    if match:
      self.debate_until = self._build_date_from_match(match)
      # In case no direct date is provided, try timedelta.
    else:
      delta_match = re.search(self.TIMEDELTA_REGX, desc_text)
      delta = delta_match.group(2)
      self.debate_until = self.published_at + timedelta(days=int(delta))

  def _build_date_from_match(self, match):
    month = settings.MONTHS.get(match.group(2).strip())
    if not month:
      print('Unable to match month for date string: %s' % match.group(0))
    else:
      return date(
        year=int(match.group(3)), month=int(month), day=int(match.group(1))
      )
