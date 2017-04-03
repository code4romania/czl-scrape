# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy.exceptions import DropItem
import requests

API_URL = 'http://czl-api.code4.ro/api/publications/'
API_TOKEN = os.environ['API_TOKEN']

class UploadPipeline(object):

    def process_item(self, item, spider):
        self.upload(item)
        return item

    def upload(self, item):
        headers = {'Authorization': 'Token ' + API_TOKEN}
        resp = requests.post(API_URL, json=dict(item), headers=headers)
        if resp.status_code == 400:
            if re.search(r'Integrity Error: Key .* already exists', resp.text):
                return
        if resp.status_code != 201:
            msg = "Failed to upload publication: {!r}".format(resp)
            raise RuntimeError(msg)


class PublicationValidatorPipeline(object):

    REQUIRED_FIELDS = [
        'identifier',
        'title',
        'institution',
        'description',
        'type',
        'date',
    ]

    def process_item(self, item, spider):
        for field in self.REQUIRED_FIELDS:
            if not item.get(field):
                raise DropItem("Missing field {}".format(field))
        return item
