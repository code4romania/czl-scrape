# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Publication(scrapy.Item):
    institution = scrapy.Field()
    identifier = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    documents = scrapy.Field()
    contact = scrapy.Field()
    feedback_days = scrapy.Field()
    max_feedback_date = scrapy.Field()
