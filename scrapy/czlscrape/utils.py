import re

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


def guess_publication_type(text, rules):
    text = strip_diacritics(text)

    for substr, publication_type in rules:
        if substr in text:
            return publication_type
    else:
        return "OTHER"


def strip_diacritics(text: str) -> str:
    result = text
    for search_pattern, replacement in DIACRITICS_RULES:
        result = re.sub(search_pattern, replacement, result)
    return result


def romanian_month_number(text: str) -> int:
    return ROMANIAN_MONTHS.get(text.lower())
