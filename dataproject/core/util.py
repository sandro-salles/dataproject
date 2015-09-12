import unicodedata

def replace_diacritics(text):
    try:
        text = unicode(text, 'utf-8')
    except TypeError:
        pass
    return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
