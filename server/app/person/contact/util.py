# -*- coding: utf-8 -*-

from core.util import normalize_text, as_digits
from memoize import memoize


def is_valid_brazilian_area_code(number):
    number = as_digits(number)
    return ((len(number) == 2), number)


def is_valid_brazilian_telephone_number(number):
    number = as_digits(number)
    return ((len(number) == 8), number)


def is_valid_brazilian_cellphone_number(number):
    number = as_digits(number)
    return ((len(number) == 8 or len(number) == 9), number)


def is_valid_brazilian_zipcode(number):
    number = as_digits(number)
    return ((len(number) == 8), number)


def normalize_address(address):
    return normalize_text(address)