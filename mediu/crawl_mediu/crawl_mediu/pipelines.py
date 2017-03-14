# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests

class CrawlMediuPipeline(object):
    def process_item(self, item, spider):
        doc = {
            'identifier': item['identifier'],
            'title': item['title'],
            'institution': item['institution'],
            'description': item['description'],
            'type': item['type'],
            'date': item['date'],
            'documents': item['documents'],
            'contact':item['contact'],
            'feedback_days': item['feedback_days'] 
        }

        response = requests.post('http://czl-api.code4.ro/api/publications/', headers={'Authorization': 'Token ' + spider.token }, json=doc)
        # print '---------'
        # print response
        # print response.text
        # print '---------'
        return item

