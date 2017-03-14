# -*- coding: utf-8 -*-

import scrapy

class ContactItem(scrapy.Item):
    tel = scrapy.Field(serializer=str)
    email = scrapy.Field(serializer=str)
