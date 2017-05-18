import re

from scrapy.selector import SelectorList

DIACRITICS_RULES = [
    (r'[șş]', 's'),
    (r'[ȘŞ]', 'S'),
    (r'[țţ]', 't'),
    (r'[ȚŢ]', 'T'),
    (r'[ăâ]', 'a'),
    (r'[ĂÂ]', 'A'),
    (r'[î]', 'i'),
    (r'[Î]', 'I'),
]

ROMANIAN_MONTHS = {
    'ianuarie': 1,
    'februarie': 2,
    'martie': 3,
    'aprilie': 4,
    'mai': 5,
    'iunie': 6,
    'iulie': 7,
    'august': 8,
    'septembrie': 9,
    'octombrie': 10,
    'noiembrie': 11,
    'decembrie': 12,
}

DOC_EXTENSIONS = [".docs", ".doc", ".txt", ".crt", ".xls", ".xml", ".pdf",
                  ".docx", ".xlsx", ]


def guess_initiative_type(text: str, rules: list) -> str:
    """
    Try to identify the type of a law initiative from its description.

    Use a best guess approach. The rules are provided by the caller as a list
    of tuples. Each tuple is composed of a search string and the initiative
    type it matches to.
    :param text: the description of the initiative
    :param rules: the rules of identification expressed as a list of tuples
    :return: the type of initiative if a rule matches; "OTHER" if no rule
    matches
    """
    text = strip_diacritics(text)

    for search_string, initiative_type in rules:
        if search_string in text:
            return initiative_type
    else:
        return "OTHER"


def strip_diacritics(text: str) -> str:
    """
    Replace all diacritics in the given text with their regular counterparts.
    :param text: the text to look into
    :return: the text without diacritics
    """
    result = text
    for search_pattern, replacement in DIACRITICS_RULES:
        result = re.sub(search_pattern, replacement, result)
    return result


def romanian_month_number(text: str) -> int:
    """
    Return the number of the given month identified by its Romanian name.
    :param text: the name of the month in Romanian
    :return: the number of the month if the month name is recognized,
    otherwise None
    """
    return ROMANIAN_MONTHS.get(text.lower())


def extract_documents(selector_list: SelectorList):
    """
    Extract white-listed documents from CSS selectors.

    Generator function. Search for links to white-listed document types and
    return all matching ones. Each entry has two properties. "type" contains
    the link text, "url" contains the link URL.

    :param selector_list: a SelectorList
    :return: a generator
    """
    for link_selector in selector_list:
        url = link_selector.css('::attr(href)').extract_first()
        if any(url.endswith(ext) for ext in DOC_EXTENSIONS):
            yield {
                'type': link_selector.css('::text').extract_first(),
                'url': url,
            }
