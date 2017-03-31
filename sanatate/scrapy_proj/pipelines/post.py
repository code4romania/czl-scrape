# -*- coding: utf-8 -*-

import json
import urllib3

class SanatatePipelinePost(object):
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
