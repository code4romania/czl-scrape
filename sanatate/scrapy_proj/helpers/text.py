# -*- coding: utf-8 -*-

import re

class TextHelper(object):

    @staticmethod
    def remove_non_ascii(string):
        return re.sub(r'[^\x00-\x7F]+', ' ', string)

    @staticmethod
    def remove_non_numeric(string):
        return re.sub('[^0-9]+', '', string)

    @staticmethod
    def rws(str):
        if str:
            return ' '.join(str.split())
        else:
            return None

    @staticmethod
    def titleize(string):
        if string:
            return string.title()
        else:
            return None
