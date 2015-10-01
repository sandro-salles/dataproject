from contextlib import contextmanager
from core.util import dict_to_struct


@contextmanager
def is_valid_cpf_format(number):
    number = ''.join(c for c in str(number) if c.isdigit())
    yield dict_to_struct({'is_valid': (len(number) == 11), 'number': number})

@contextmanager
def is_valid_cnpj_format(number):
    number = ''.join(c for c in str(number) if c.isdigit())
    yield dict_to_struct({'is_valid': (len(number) == 14), 'number': number})
