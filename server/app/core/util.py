import unicodedata
from collections import namedtuple


def dict_to_struct(dictionary):
    return namedtuple('Struct', dictionary.keys())(*dictionary.values())

def replace_diacritics(text):
    try:
        text = unicode(text or "", 'utf-8')
    except TypeError:
        pass
    return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))

def remove_spaces_and_similar(text):
    return " ".join((text or "").split()).strip()

def normalize_text(text):
    return remove_spaces_and_similar(replace_diacritics(text)).upper()

def as_digits(text):
    return ''.join(c for c in text if c.isdigit())