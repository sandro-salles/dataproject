import unicodedata
from collections import namedtuple


def dict_to_struct(dictionary):
    return namedtuple('Struct', dictionary.keys())(*dictionary.values())

def replace_diacritics(text):
    try:
        text = unicode(text, 'utf-8')
    except TypeError:
        pass
    return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))

def remove_spaces_and_similar(text):
    return " ".join(text.split())

def sanitize_text(text):
    return remove_spaces_and_similar(replace_diacritics(text)).strip().upper()