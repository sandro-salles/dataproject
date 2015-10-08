# -*- coding: utf-8 -*-
from person.contact.exceptions import AreaCodeValidationError, PhoneValidationError
from person.contact.models import Phone
from core.util import as_digits

AREA_CODES = [choice[0] for choice in Phone.AREACODE_CHOICES]


def validate_areacode(number):
    number = as_digits(number)
    if (int(number) in AREA_CODES):
        return number
    else:
        raise AreaCodeValidationError('Codigo DDD invalido - (%s)' % number)


def validate_phone_number(number):
    number = as_digits(number)
    length = len(number)
    if (length == 8 or length == 9):
        return number
    else:
        raise PhoneValidationError(
            'Numero de telefone invalido - (%s)' % number)
