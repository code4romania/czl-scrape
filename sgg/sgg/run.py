# -*- coding: utf-8 -*-

import os
import subprocess
import json
import requests 

POST_URL = "http://czl-api.code4.ro/api/publications/"
# POST_URL_DEV = "http://10.231.234.10:8000/api/publications/"

AUTH_TOKEN = os.getenv('SGG_AUTH_TOKEN', "sgg-very-secret-key")

headers = {
  'Authorization': " ".join(['Token',AUTH_TOKEN])
}

if os.path.exists("sgg.json"):
    os.remove("sgg.json")

subprocess.call(['scrapy','crawl', 'sgg_spider', '-o', 'sgg.json'])

with open("sgg.json") as fp:
    items = json.load(fp)
    for item in items: 
        r = requests.post(POST_URL, data=item, headers=headers)
        if r.status_code >= 400:
            print(json.dumps(r.json()))

print("DONE!")