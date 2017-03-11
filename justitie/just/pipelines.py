# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json

from items import JustPublication
import logging

API_KEY = 'justitie-very-secret-key'
API_PUBLICATIONS = 'http://czl-api.code4.ro/api/publications/'

class JustPublicationsToApiPipeline(object):
    def process_item(self, item, spider):

        if type(item) != JustPublication:
            return item

        r = requests.post(API_PUBLICATIONS, json=dict(item), headers={'Authorization': 'Token %s' % (API_KEY,) } )

        return item
