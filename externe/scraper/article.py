import re
from datetime import date, timedelta
import scraper.settings as settings


class Article:
  """
  Defines an article object as found on the MAE site.
  """
  ANEXA = ' - ANEXA'
  DATE_REGX = r'(\d+)\s([a-zA-Z]*)\s(\d{4})'
  TIMEDELTA_REGX = '(timp\sde\s([0-9]+)\szile)'
  DESCRIPTION_FMT = '{0} {1}'
  CONTACT_REGX = dict(
    email=r'\s(([a-zA-Z0-9\._]|\.)*?@[a-zA-Z]*?\.[a-zA-Z]*?)(?:\s|\.|,)',
    tel=r'(?:tel|telefon)\s?:?\s*((\d+(?:\s|-|\.)?)+)(,|\s|\.)?',
    fax=r'fax\s?:?\s*((\d+(?:\s|-|\.)?)+)(,|\s|\.)?',
    addr=r'adresa poştală\s?a?\s*(.*?\scod(:|\s)?\d+)',
    # ADDRESS=r'adresa poştală a (.*)\.'
  )

  def __init__(self, table):
    """
    Builds an Article object from a given HTML table row
    :param table: the table.
    :return: the current object.
    """
    tr = table.select('tr')
    self._extract_article_type(tr)
    self._extract_title(tr)
    self._build_contact(tr)
    self._build_documents(tr)
    # published_at should be
    self._extract_published_at(tr)
    self._extract_feedback_days(tr)

  # HG, OG, OUG, PROIECT
  article_type = None
  title = None
  documents = None
  published_at = None
  feedback_days = None
  contact = None

  def _build_contact(self, row):
    """
    Builds a contact dict from a given table.
    :param row: the given table row
    :return: None
    """
    print('--------------------------------------')
    contact_paragraph = row[-1].select('p')[0].text
    self.contact = dict()
    for field in self.CONTACT_REGX.keys():
      aux = re.search(self.CONTACT_REGX[field], contact_paragraph)
      if aux and aux.group(1).strip():
        self.contact[field.lower()] = aux.group(1).strip()
      else:
        # TODO: logger for these
        print(
          'Unable to match %s for paragraph: %s' % (field, contact_paragraph)
        )
    for k, v in self.contact.items():
      print('%s - %s' % (k, v))
    print('--------------------------------------')

  def _build_documents(self, row):
    """
    Builds the documents dict from a given table.
    :param row: the given table row
    :return: None
    """
    t1 = self.article_type + self.ANEXA if self.article_type else None
    t2 = (self._sanitize(row[1].find('td').text) + self.ANEXA
          if len(row) >= 2 else None)

    t1_url = row[0].find('td').find('a').attrs['href']
    t2_url = row[1].find('td').find('a').attrs['href']

    self.documents = [
      dict(type=t1, url=settings.MAE_BASE_URL + t1_url)
    ]
    if t2:
      self.documents.append(
        dict(type=t2, url=settings.MAE_BASE_URL + t2_url)
      )

  def _extract_article_type(self, row):
    """
    extracts and sets the title from a given HTML table row
    :param row: the given table row
    :return: String
    """
    article_type = self._sanitize(row[0].find_all('a')[0].text.strip())
    if article_type in settings.TYPES:
      self.article_type = settings.TYPES.get(article_type)
    else:
      # TODO: logger
      print("%s not defined as article type" % article_type)
    return article_type

  def _extract_title(self, row):
    """
    extracts and sets the description from a given HTML table row
    :param row: the given table row
    :return: None
    """
    art_type = self._extract_article_type(row).lower().capitalize()
    desc_text = row[0].find_all('a')[1].text.rstrip('\n')
    self.title = self.DESCRIPTION_FMT.format(art_type, desc_text)

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

  def _extract_feedback_days(self, row):
    """
    extracts and sets the debate_until attribute from a given HTML table row.
    :param row: the given table row
    :return: None
    """
    feedback_date = None
    desc_text = row[-1].find_all('p')[0].text
    match = re.search(self.DATE_REGX, desc_text)
    if match:
      feedback_date = self._build_date_from_match(match)
      # In case no direct date is provided, try timedelta.
    else:
      delta_match = re.search(self.TIMEDELTA_REGX, desc_text)
      if delta_match:
        delta = delta_match.group(2)
        feedback_date = self.published_at + timedelta(days=int(delta))
    if feedback_date:
      self.feedback_days = (feedback_date - self.published_at).days

  def _build_date_from_match(self, match):
    month = settings.MONTHS.get(match.group(2).strip())
    if not month:
      print('Unable to match month for date string: %s' % match.group(0))
    else:
      return date(
        year=int(match.group(3)), month=int(month), day=int(match.group(1))
      )

  def _sanitize(self, string):
    if string:
      return string.replace('\n', '').replace('\u200b', '')
