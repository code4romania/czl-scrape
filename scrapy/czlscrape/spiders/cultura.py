# coding=utf-8

import datetime
import hashlib
import re

from scrapy import Spider, Request
from scrapy.selector import Selector

from ..items import Publication
from ..utils import extract_documents
from ..utils import romanian_month_number
from ..utils import strip_diacritics

INDEX_URL = 'http://www.cultura.ro/proiecte-acte-normative'

PUBLISH_DATE_PATTERN = re.compile(r'''
^                                           # beginning of string
(?P<day>\d{1,2})                            # day is one or two digits
\s                                          # whitespace
(?P<ro_month>\w*)                           # name of the month in Romanian
\s                                          # whitespace
(?P<year>\d{4})                             # year is 4 digits
$                                           # end of string
''', flags=re.VERBOSE)

FEEDBACK_DEADLINE_DATE_PATTERN = re.compile(r'''
.*                                          # can start anywhere
(?:pana\ la\ data(?:\ de)?)                 # the relevant prefix
\                                           # space
(?P<day>\d{1,2})                            # day is one or two digits
\.                                          # separator is dot
(?P<month>\d{1,2})                          # month is one or two digits
\.                                          # separator is dot
(?P<year>\d{4})                             # year is 4 digits
.*                                          # anywhere in the string
''', flags=re.DOTALL | re.VERBOSE)

FEEDBACK_CONTACT_FAX_PATTERN = re.compile(r'''
.*                                          # can start anywhere
fax                                         # the relevant prefix
:?                                          # optional colon
\s?                                         # optional whitespace
(?:la\ (?:numar(?:ul)?|nr\.?))?             # optional prefix
\s?                                         # optional whitespace
(\S*)                                       # fax number
.*                                          # anywhere in the string
''', flags=re.DOTALL | re.VERBOSE)

FEEDBACK_CONTACT_EMAIL_PATTERN = re.compile(r'''
.*                                          # can start anywhere
e-mail:?                                    # the relevant prefix
\s?                                         # optional whitespace
(\S*)                                       # email address
.*                                          # anywhere in the string
''', flags=re.DOTALL | re.VERBOSE)

FEEDBACK_CONTACT_RULES = [
    ('fax', FEEDBACK_CONTACT_FAX_PATTERN),
    ('email', FEEDBACK_CONTACT_EMAIL_PATTERN),
]

INITIATIVE_TYPE_RULES = [
    (r'\b(lege)\b', 'LEGE'),
    (r'\b(hotarare|hg)\b', 'HG'),
    (r'\b(ordonanta de guvern|og)\b', 'OG'),
    (r'\b(ordonanta de urgenta|oug)\b', 'OUG'),
    (r'\b(ordin de ministru|ordin|ordinul|om)\b', 'OM'),
]


def remove_html_tag(selector: Selector, tag: str) -> Selector:
    dom_element = selector.root
    html_tag_selector = selector.xpath(tag)
    if html_tag_selector:
        dom_element.remove(html_tag_selector[0].root)
    return selector


def extract_text(selector: Selector) -> str:
    return selector.xpath('string(.)').extract_first().strip()


def collapse_blank_lines(text: str) -> str:
    lines = re.sub("\n\s*\n{2,}", "\n\n", text).split("\n\n")
    return "\n\n".join(line.strip() for line in lines)


def guess_initiative_type(text: str) -> str:
    text_without_diacritics = strip_diacritics(text)
    for search_pattern, publication_type in INITIATIVE_TYPE_RULES:
        if re.search(search_pattern, text_without_diacritics, re.IGNORECASE):
            return publication_type
    else:
        return "OTHER"


def cleanup_initiative_text(selector: Selector) -> str:
    selector_copy = selector
    for tag in ['ul', 'a']:
        selector_copy = remove_html_tag(selector_copy, tag)
    text = extract_text(selector_copy)
    text = re.sub(r'(Fisiere|Fișiere|Anexe)[^:]*:', '', text)
    text = collapse_blank_lines(text)
    return text


def extract_publish_date(selector: Selector) -> datetime:
    date_pattern_match = PUBLISH_DATE_PATTERN.match(extract_text(selector))

    if date_pattern_match:
        return datetime.date(
            int(date_pattern_match.group('year')),
            romanian_month_number(date_pattern_match.group('ro_month')),
            int(date_pattern_match.group('day'))
        )


class CulturaSpider(Spider):
    name = 'cultura'
    start_urls = [INDEX_URL]

    def parse(self, response):
        for entry in response.css('#recomended-articles .recommended-title'):
            href = entry.css('a::attr(href)').extract_first()
            yield Request(response.urljoin(href), self.parse_entry)

    def parse_entry(self, response):
        today = datetime.datetime.today()

        identifier = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        title = extract_text(response.css(
            '#block-continutprincipalpagina .post-content > h1 > span'))
        initiative_type = guess_initiative_type(title)
        initiative_text_selector = response.css(
            '#block-continutprincipalpagina .node__content.clearfix > div')[0]

        publish_date = extract_publish_date(
            response.css('#block-continutprincipalpagina .post-created'))
        if publish_date:
            publish_date_string = publish_date.isoformat()
        else:
            publish_date_string = today.isoformat()

        documents = [
            {
                'type': doc['type'],
                'url': response.urljoin(doc['url']),
            } for doc in
            extract_documents(initiative_text_selector.css('ul > li > a, a'))
        ]

        description = cleanup_initiative_text(initiative_text_selector)
        description_without_diacritics = strip_diacritics(description)

        max_feedback_date_string = None
        feedback_date_match = FEEDBACK_DEADLINE_DATE_PATTERN.match(description_without_diacritics)

        if feedback_date_match:
            max_feedback_date_string = datetime.date(
                int(feedback_date_match.group('year')),
                int(feedback_date_match.group('month')),
                int(feedback_date_match.group('day'))
            ).isoformat()

        contact = {}
        for contact_type, contact_pattern in FEEDBACK_CONTACT_RULES:
            contact_match = contact_pattern.match(description_without_diacritics)

            if contact_match:
                contact[contact_type] = contact_match.group(1).rstrip('.,')

        publication = Publication(
            identifier=identifier,
            title=title,
            institution='cultura',
            description=description,
            type=initiative_type,
            date=publish_date_string,
            documents=documents,
            contact=contact
        )
        if max_feedback_date_string:
            publication['max_feedback_date'] = max_feedback_date_string

        return publication
