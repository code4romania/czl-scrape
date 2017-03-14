# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy_proj.helpers import *
from scrapy.loader.processors import *
from datetime import datetime as dt

class ActLoader(ItemLoader):
    default_output_processor = TakeFirst()
    title_in = MapCompose(TextHelper.rws, RomanianHelper.beautify_romanian)
    contact_in = Compose(TakeFirst(), lambda x: dict(x))
    date_in = MapCompose(lambda d: dt.strptime(d, '%d-%m-%Y').strftime('%Y-%m-%d'))
    feedback_days_in = MapCompose(int)
    documents_in = Identity()
    documents_out = Identity()
