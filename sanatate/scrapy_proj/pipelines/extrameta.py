# -*- coding: utf-8 -*-

import datetime
import hashlib

from scrapy_proj.helpers import *

class SanatatePipelineExtraMeta(object):
    def process_item(self, item, spider):
        item['institution'] = spider.name
        act_type = LegalHelper.get_type_from_title(item['title'])
        if act_type == None:
            raise scrapy.exceptions.DropItem
        item['type'] = act_type
        engrol = RomanianHelper.englishize_romanian(item['title']).lower()
        engrolna = TextHelper.remove_non_ascii(engrol)
        identifier_text = '{0} {1}'.format(engrolna, item['date'] if 'date' in item else 'NA')
        identifier_text_hashed = hashlib.md5(identifier_text.encode()).hexdigest()
        item['identifier'] = '{0}-{1}-{2}'.format(item['institution'], item['type'], identifier_text_hashed)
        return item
