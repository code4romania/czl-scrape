# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import urllib
import helpers

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
        return item

class SanatatePipelineClean(object):

    def process_item(self, item, spider):
        item['title'] = helpers.TextHelper.rws(item['title'])
        return item

class SanatatePipelineAPI(object):

    def open_spider(self, spider):
        # conn = http.client.HTTPSConnection("localhost", 8080)
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item
