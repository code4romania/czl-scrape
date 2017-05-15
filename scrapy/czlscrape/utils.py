import re


def guess_publication_type(text, rules):
    text = text.lower()
    text = re.sub(r'[șş]', 's', text)
    text = re.sub(r'[țţ]', 't', text)
    text = re.sub(r'[ăâ]', 'a', text)
    text = re.sub(r'[î]', 'i', text)

    for substr, publication_type in rules:
        if substr in text:
            return publication_type
    else:
        return "OTHER"
