# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_proj.helpers import *
from scrapy.loader import ItemLoader
from scrapy.loader.processors import *
from datetime import datetime as dt

class ContactItem(scrapy.Item):
    name = scrapy.Field(serializer=str)
    tel = scrapy.Field(serializer=str)
    email = scrapy.Field(serializer=str)

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

class ContactLoader(ItemLoader):
    default_output_processor = TakeFirst()
    email_in = MapCompose(str.lower)
    tel_in = MapCompose(TextHelper.remove_non_numeric)

class ActLoader(ItemLoader):
    default_output_processor = TakeFirst()
    title_in = MapCompose(TextHelper.rws, RomanianHelper.beautify_romanian)
    contact_in = Compose(TakeFirst(), lambda x: dict(x))
    date_in = MapCompose(lambda d: dt.strptime(d, '%d-%m-%Y').strftime('%Y-%m-%d'))
    feedback_days_in = MapCompose(int)
    documents_in = Identity()
    documents_out = Identity()
