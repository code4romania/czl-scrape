# -*- coding: utf-8 -*-

import scrapy

class ActItem(scrapy.Item):
    identifier = scrapy.Field()
    title = scrapy.Field(serializer=str)
    type = scrapy.Field()
    institution = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    feedback_days = scrapy.Field(serializer=int)
    contact = scrapy.Field()
    documents = scrapy.Field()
