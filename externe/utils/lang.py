# -*- coding: utf-8 -*-
class LangHelper(object):
    FUCK_NO = [
        # new line
        '\n',
        # tab
        '\t',
        # non-breaking space
        '\xa0',
        # 0 width space
        '\u200b'
    ]

    @staticmethod
    def englishize_romanian(string):
        symbols = (u"țţȚŢșşȘŞăĂîÎâÂ",
                   u"ttTTssSSaAiIaA")

        tr = {ord(a): ord(b) for a, b in zip(*symbols)}
        return string.translate(tr)

    @staticmethod
    def beautify_romanian(string):
        symbols = (u"ţşŢŞ",
                   u"țșȚȘ")
        tr = {ord(a): ord(b) for a, b in zip(*symbols)}
        return string.translate(tr)

    @staticmethod
    def sanitize(string):
        """Sanitize a string.
        Removes new lines and 0 width spaces, because fuck those.

        :param string: The string to sanitize.
        :return: A clean string.
        """
        if string:
            for this_little_shit in LangHelper.FUCK_NO:
                string = string.replace(this_little_shit, '')
        return string
