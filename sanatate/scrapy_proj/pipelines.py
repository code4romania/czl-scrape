# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

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
        out = json.dumps(self.items)
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
        identifier_text = '{0} {1}'.format(engrolna, item['date'])
        identifier_text_hashed = hashlib.md5(identifier_text.encode()).hexdigest()
        item['identifier'] = '{0}-{1}-{2}'.format(item['institution'], item['type'], identifier_text_hashed)
        return item

class SanatatePipelineClean(object):
    def process_item(self, item, spider):
        item['title'] = helpers.TextHelper.rws(item['title'])
        item['feedback_days'] = int(item['feedback_days'])
        item['date'] = datetime.datetime.strptime(item['date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        return item

class SanatatePipelineAPI(object):

    def open_spider(self, spider):
        self.total_items = 0
        self.total_created = 0

    def process_item(self, item, spider):

        encoded_body = json.dumps(dict(item))

        http = urllib3.PoolManager()

        r = http.request(
            'POST',
            'http://czl-api.code4.ro/api/publications/',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Token sanatate-very-secret-key'
            },
            body=encoded_body
        )

        return item
