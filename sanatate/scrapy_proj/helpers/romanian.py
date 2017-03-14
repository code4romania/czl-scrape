# -*- coding: utf-8 -*-

class RomanianHelper(object):
    @staticmethod
    def englishize_romanian(string):
        symbols = (u"țţȚŢșşȘŞăǎĂîÎâÂ",
                   u"ttTTssSSaaAiIaA")

        tr = {ord(a):ord(b) for a, b in zip(*symbols)}

        return string.translate(tr)

    @staticmethod
    def beautify_romanian(string):
        symbols = (u"ǎţşŢŞ",
                   u"ățșȚȘ")
        tr = {ord(a):ord(b) for a, b in zip(*symbols)}
        return string.translate(tr)
