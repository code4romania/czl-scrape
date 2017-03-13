# -*- coding: utf-8 -*-

import json
import urllib3
import datetime
import hashlib
import logging
import scrapy_proj.helpers as helpers

class SanatatePipelineJSON(object):
    items = []
    def open_spider(self, spider):
        self.file = open('items.json', 'w')
        self.items = []
    def close_spider(self, spider):
        out = json.dumps(self.items).encode().decode('unicode_escape')
        self.file.write(out)
        self.file.close()
    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

class SanatatePipelineExtraMeta(object):
    def process_item(self, item, spider):
        item['institution'] = spider.name
        act_type = helpers.LegalHelper.get_type_from_title(item['title'])
        if act_type == None:
            raise scrapy.exceptions.DropItem
        item['type'] = act_type
        engrol = helpers.RomanianHelper.englishize_romanian(item['title']).lower()
        engrolna = helpers.TextHelper.remove_non_ascii(engrol)
        identifier_text = '{0} {1}'.format(engrolna, item['date'] if 'date' in item else 'NA')
        identifier_text_hashed = hashlib.md5(identifier_text.encode()).hexdigest()
        item['identifier'] = '{0}-{1}-{2}'.format(item['institution'], item['type'], identifier_text_hashed)
        return item

class SanatatePipelineAPI(object):
    def open_spider(self, spider):
        with open('credentials.json') as credentials_file:
            self.credentials = json.load(credentials_file)
    def process_item(self, item, spider):
        http = urllib3.PoolManager()
        r = http.request(
            'POST',
            self.credentials['endpoint'],
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.credentials['authorization']
            },
            body=json.dumps(dict(item))
        )
        return item
