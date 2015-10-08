from core.util import as_digits
from geo.exceptions import ZipCodeValidationError


def validate_zipcode(number):
    number = as_digits(number)
    if (len(number) == 8):
        return number
    else:
        raise ZipCodeValidationError('CEP invalido - (%s)' % number)
