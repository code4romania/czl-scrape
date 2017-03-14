# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy_proj.helpers import *
from scrapy.loader.processors import *

class ContactLoader(ItemLoader):
    default_output_processor = TakeFirst()
    email_in = MapCompose(str.lower)
    tel_in = MapCompose(TextHelper.remove_non_numeric)
