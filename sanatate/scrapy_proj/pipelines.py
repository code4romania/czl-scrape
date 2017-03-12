# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import urllib
import datetime
import helpers
import hashlib

class SanatatePipelineJSON(object):

    items = []

    def open_spider(self, spider):
        self.file = open('items.json', 'wb')
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
        # conn = http.client.HTTPSConnection("localhost", 8080)
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item
