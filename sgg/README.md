# Secretariatul General al Guvernului

## Tehnologie
Python3, virtualenv, scrapy


## Instructiuni

Install `Python3` and `virtualenv`

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd sgg 
    scrapy crawl sgg_spider -o sgg.json

## Exceptii