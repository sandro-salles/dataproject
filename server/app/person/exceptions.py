# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError


class CPFValidationError(ValidationError):
    pass


class CNPJValidationError(ValidationError):
    pass


class ZipCodeValidationError(ValidationError):
    pass
