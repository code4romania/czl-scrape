# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlDezvoltareItem(scrapy.Item):
    identifier = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    institution = scrapy.Field()
    issuer = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    feedback_days = scrapy.Field()
    contact = scrapy.Field()
    tel = scrapy.Field()
    email = scrapy.Field()
    documents = scrapy.Field()