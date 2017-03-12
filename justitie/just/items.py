# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JustPublication(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    identifier = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    institution = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    feedback_days = scrapy.Field()
    contact = scrapy.Field()
    documents = scrapy.Field()

    pass

