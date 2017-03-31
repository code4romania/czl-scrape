# -*- coding: utf-8 -*-

import re
import fuzzywuzzy.fuzz as fuzz

from scrapy_proj.helpers.romanian import *

class LegalHelper(object):
    @staticmethod
    def get_type_from_title(title):
        engrol = RomanianHelper.englishize_romanian(title).lower()

        stop_pos = len(title)
        magic_keyword_search_result = re.search(r'(pentru|privind)', engrol)
        if magic_keyword_search_result != None:
            stop_pos = magic_keyword_search_result.start()

        search_space = engrol[:stop_pos]

        type_to_keywords = {
            'HG': 'hotarare',
            'OM': 'ordin',
            'LEGE': 'lege',
            'OG': 'ordonanta',
            'OUG': 'ordonanta de urgenta'
        }

        final_type = None
        max_ratio = 0

        for key in type_to_keywords:
            ratio = fuzz.ratio(type_to_keywords[key], search_space)
            if ratio > max_ratio:
                max_ratio = ratio
                final_type = key

        return final_type
