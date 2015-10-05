from core.util import as_digits
from memoize import memoize

def is_valid_brazilian_zipcode(number):
    number = as_digits(number)
    return ((len(number) == 8), number)