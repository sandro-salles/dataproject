# -*- coding: utf-8 -*-

import unicodedata
import string
from collections import namedtuple

def replace_diacritics(text):
    try:
        text = unicode(text or "", 'utf-8')
    except TypeError:
        pass

    try:
        text = ''.join((c for c in unicodedata.normalize(
            'NFKD', text) if unicodedata.category(c) != 'Mn'))

    except UnicodeEncodeError:

        text = ''.join((c for c in unicodedata.normalize(
            'NFD', text) if unicodedata.category(c) != 'Mn'))

    return filter(lambda x: x in string.printable, text)


def remove_spaces_and_similar(text):
    return " ".join((text or "").split()).strip()


def normalize_text(text):
    return remove_spaces_and_similar(replace_diacritics(text)).upper()


def as_digits(text):
    return ''.join(c for c in str(text) if c.isdigit())

