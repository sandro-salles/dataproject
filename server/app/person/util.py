# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from core.util import as_digits
from person.exceptions import CPFValidationError, CNPJValidationError
from localflavor.br.forms import BRCPFField, BRCNPJField


def validate_cpf(number):
    number = as_digits(number)
    field = BRCPFField()

    try:
        field.clean(number)
        return number
    except ValidationError as e:
        raise CPFValidationError(e)


def validate_cnpj(number):
    number = as_digits(number)
    field = BRCNPJField()

    try:
        field.clean(number)
        return number
    except ValidationError as e:
        raise CNPJValidationError(e)
