# -*- coding: utf-8 -*-

from core.util import as_digits
from localflavor.br.forms import BRCPFField, BRCNPJField
from memoize import memoize

def is_valid_cpf_number(number):
    number = as_digits(number)
    field = BRCPFField()

    try:
        field.clean(number)
        is_valid = True
    except:
        is_valid = False

    return (is_valid, number)


def is_valid_cnpj_number(number):
    number = as_digits(number)
    field = BRCNPJField()

    try:
        field.clean(number)
        is_valid = True
    except:
        is_valid = False

    return (is_valid, number)
