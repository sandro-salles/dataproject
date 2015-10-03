from contextlib import contextmanager
from core.util import dict_to_struct, normalize_text, as_digits

@contextmanager
def is_valid_brazilian_area_code(number):
    number = as_digits(number)
    yield dict_to_struct({'is_valid': (len(number) == 2), 'number': number})

@contextmanager
def is_valid_brazilian_telephone_number(number):
    number = as_digits(number)
    yield dict_to_struct({'is_valid': (len(number) == 8), 'number': number})

@contextmanager
def is_valid_brazilian_cellphone_number(number):
    number = as_digits(number)
    yield dict_to_struct({'is_valid': (len(number) == 8 or len(number) == 9), 'number': number})

@contextmanager
def is_valid_brazilian_zipcode(number):
    number = as_digits(number)
    yield dict_to_struct({'is_valid': (len(number) == 8), 'number': number})

def normalize_address(address):
    return normalize_text(address)