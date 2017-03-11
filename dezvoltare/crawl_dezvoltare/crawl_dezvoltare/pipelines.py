# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests


class CrawlDezvoltarePipeline(object):
    def process_item(self, item, spider):
        response = requests.post('http://czl-api.code4.ro/api/publications/', headers={'Authorization': 'Token ' + spider.token }, data=item)
        print '***********'
        print '***********'
        print response
        print response.text
        print '***********'
        print '***********'
        return item


