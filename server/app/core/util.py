# -*- coding: utf-8 -*-

import unicodedata


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
    return ''.join(c for c in str(text) if c.isdigit())


def disable_auto_now(*models):
    """Turns off the auto_now and auto_now_add attributes on a Model's fields,
    so that an instance of the Model can be saved with a custom value.
    """
    for model in models:
        for field in model._meta.local_fields:
            if hasattr(field, 'auto_now') and field.auto_now:
                field.auto_now = False
                setattr(field, 'auto_now_disabled', True)


def enable_auto_now(*models):
    """Turns off the auto_now and auto_now_add attributes on a Model's fields,
    so that an instance of the Model can be saved with a custom value.
    """
    for model in models:
        for field in model._meta.local_fields:
            if hasattr(field, 'auto_now_disabled'):
                field.auto_now = True
                delattr(field, 'auto_now_disabled')
