import hashlib
from urllib.parse import quote
import re
from datetime import date, timedelta

import logging

from utils.lang import LangHelper
from utils.settings import *


class Article:
    """Defines an article object as found on the MAE site.
    """

    #: Constants
    ANEXA = ' - ANEXA'
    DATE_REGX = r'(\d+)\s([a-zA-Z]*)\s(\d{4})'
    TIMEDELTA_REGX = '(timp\sde\s([0-9]+)\szile)'
    DESCRIPTION_FMT = '{0} {1}'
    CONTACT_REGX = dict(
        email=r'\s(([a-zA-Z0-9\._]|\.)*?@[a-zA-Z]*?\.[a-zA-Z]*?)(?:\s|\.|,)',
        tel=r'(?:tel|telefon)\s?:?\s*((\d+(?:\s|-|\.)?)+)(,|\s|\.)?',
        addr=r'adresa poştală\s?a?\s*(.*?\scod(:|\s)?\d+)',
    )

    identifier = None
    article_type = None
    title = None
    documents = None
    published_at = None
    feedback_days = None
    contact = None

    def __init__(self, table=None):
        """
        Builds an Article object from a given HTML table row
        :param table: the table.
        :return: the current object.
        """
        if table:
            tr = table.select('tr')
            self._extract_article_type(tr)
            self._extract_title(tr)
            self._extract_published_at(tr)
            self._generate_id()
            self._build_contact(tr)
            self._build_documents(tr)
            self._extract_feedback_days(tr)

    def __str__(self):
        return ('identifier: %s\ntitle: %s\npublished_at: %s\ndocuments: %s\ncontact:%s',
                self.identifier, self.title, self.published_at, self.documents,
                self.contact)

    def _generate_id(self):
        """Generates and sets the identifier.
        :return: None
        """
        if self.article_type and self.title:
            self.identifier = '%s-%s' % (
                self.article_type, hashlib.md5(self.title.encode()).hexdigest()
            )
        else:
            logging.error(
                'Failed to generate id for type: %s, title: %s, published_at: %s',
                self.article_type, self.title, self.published_at
            )

    def _build_contact(self, row):
        """Builds and sets the contact dict.
        :param row: the given table row
        :return: None
        """
        contact_paragraph = row[-1].select('p')[0].text
        self.contact = dict()
        for field in self.CONTACT_REGX.keys():
            aux = re.search(self.CONTACT_REGX[field], contact_paragraph)
            if aux and aux.group(1).strip():
                self.contact[field.lower()] = LangHelper.sanitize(aux.group(1).strip())
            else:
                logging.warning(
                    'Unable to match %s for identifier: %s', field, self.identifier
                )

    def _build_documents(self, row):
        """Builds the documents attribute.
        :param row: the given table row
        :return: None
        """
        t1 = self.article_type + self.ANEXA if self.article_type else None
        t2 = (LangHelper.sanitize(row[1].find('td').text) + self.ANEXA
              if len(row) >= 2 else None)

        t1_url = quote(row[0].find('td').find('a').attrs['href'])
        t2_url = quote(row[1].find('td').find('a').attrs['href'])

        self.documents = [dict(type=t1, url=URLS['mae_base'] + t1_url)]
        if t2:
            self.documents.append(dict(type=t2, url=URLS['mae_base'] + t2_url))

    def _extract_article_type(self, row):
        """Extracts and sets the title attribute.
        :param row: the given table row
        :return: str
        """
        article_type = LangHelper.sanitize(row[0].find_all('a')[0].text.strip())
        article_type = LangHelper.englishize_romanian(article_type)
        self.article_type = TYPES.get(article_type)
        if not self.article_type:
            self.article_type = TYPES.get('OTHER')
        return self.article_type

    def _extract_title(self, row):
        """Extracts and sets the description attribute.
        :param row: the given table row
        :return: None
        """
        art_type = self._extract_article_type(row).lower().capitalize()
        desc_text = row[0].find_all('a')[1].text
        self.title = LangHelper.sanitize(
            self.DESCRIPTION_FMT.format(art_type, desc_text)
        )
        self.title = LangHelper.sanitize(re.sub(' +', ' ', self.title).strip())

    def _extract_published_at(self, row):
        """Extracts and sets the published_at attribute.
        :param row: the given table row
        :return: None
        """
        published_text = row[-1].find_all('p')[-1].text
        match = re.search(self.DATE_REGX, published_text)
        if match:
            self.published_at = self._build_date_from_match(match)

    def _extract_feedback_days(self, row):
        """Extracts and sets the debate_until attribute
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

    @staticmethod
    def _build_date_from_match(match):
        month = MONTHS.get(match.group(2).strip())
        return date(
            year=int(match.group(3)), month=int(month),
            day=int(match.group(1))
        )
