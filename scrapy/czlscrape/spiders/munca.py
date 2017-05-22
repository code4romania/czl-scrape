# coding=utf-8

import datetime
import hashlib
import re

from scrapy import Spider, Request
from scrapy.selector import Selector

from ..items import Publication
from ..utils import extract_documents
from ..utils import strip_diacritics

INDEX_URL = 'http://www.mmuncii.ro/j33/index.php/ro/transparenta/proiecte-in-dezbatere'

INITIATIVE_TYPE_RULES = [
    (r'\b(lege)\b', 'LEGE'),
    (r'\b(hotarare|hg)\b', 'HG'),
    (r'\b(ordonanta de guvern|og)\b', 'OG'),
    (r'\b(ordonanta de urgenta|oug)\b', 'OUG'),
    (r'\b(ordin de ministru|ordin|ordinul|om)\b', 'OM'),
]

PUBLISH_DATE_PATTERN = r'.*publicat pe site:?\s?(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})'

FEEDBACK_DEADLINE_DATE_PATTERN = r'.*(?:\d{1,2})\.(?:\d{1,2})\.(?:\d{4}) [-–]? (?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})\.?'

FEEDBACK_DEADLINE_DAYS_PATTERN = r'.*in termen de (?P<days>\d{1,2}) zile'

DOC_EXTENSIONS = [".docs", ".doc", ".txt", ".crt", ".xls", ".xml", ".pdf",
                  ".docx", ".xlsx", ]


def guess_initiative_type(text: str) -> str:
    text_without_diacritics = strip_diacritics(text)
    for search_pattern, publication_type in INITIATIVE_TYPE_RULES:
        if re.search(search_pattern, text_without_diacritics, re.IGNORECASE):
            return publication_type
    else:
        return "OTHER"


def extract_text(selector: Selector) -> str:
    return selector.xpath('string(.)').extract_first().strip()


def extract_date(text: str, regex: str) -> datetime:
    date_pattern_match = re.match(regex, text, re.IGNORECASE | re.DOTALL)
    if date_pattern_match:
        return datetime.date(
            int(date_pattern_match.group('year')),
            int(date_pattern_match.group('month')),
            int(date_pattern_match.group('day'))
        )


def extract_feedback_days(text: str) -> int:
    feedback_days_pattern_match = re.match(FEEDBACK_DEADLINE_DAYS_PATTERN, text,
                                           re.IGNORECASE | re.DOTALL)
    if feedback_days_pattern_match:
        return int(feedback_days_pattern_match.group('days'))


class MuncaSpider(Spider):
    name = 'munca'
    start_urls = [INDEX_URL]

    def parse(self, response):
        for entry in response.css('#adminForm > table > tbody > tr > td'):
            href = entry.css('a::attr(href)').extract_first()
            yield Request(response.urljoin(href), self.parse_entry)

    def parse_entry(self, response):
        today = datetime.date.today()

        identifier = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        title = extract_text(response.css(
            '#s5_component_wrap_inner > div.item-page > div.page-header > h2'))
        description = title
        initiative_type = guess_initiative_type(description)

        page_text = strip_diacritics(
            extract_text(response.css('div[itemprop=articleBody]')))

        publish_date = extract_date(page_text, PUBLISH_DATE_PATTERN)

        if publish_date:
            publish_date_string = publish_date.isoformat()
        else:
            publish_date_string = today.isoformat()

        feedback_date = extract_date(page_text, FEEDBACK_DEADLINE_DATE_PATTERN)
        feedback_days = extract_feedback_days(page_text)

        documents = [
            {
                'type': doc['type'],
                'url': response.urljoin(doc['url']),
            } for doc in extract_documents(
                response.css('div[itemprop=articleBody] span > a'))
        ]

        contact = {'email': 'dezbateri@mmuncii.gov.ro'}

        publication = Publication(
            identifier=identifier,
            title=title,
            institution='munca',
            description=description,
            type=initiative_type,
            date=publish_date_string,
            documents=documents,
            contact=contact
        )

        if feedback_date:
            publication['max_feedback_date'] = feedback_date.isoformat()

        if feedback_days:
            publication['feedback_days'] = feedback_days

        return publication
