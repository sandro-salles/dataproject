from django.core.exceptions import ValidationError


class AreaCodeValidationError(ValidationError):

    def __init__(self, message=None):
        super(AreaCodeValidationError, self).__init__(
            message or 'Codigo DDD invalido')


class PhoneValidationError(ValidationError):

    def __init__(self, message=None):
        super(PhoneValidationError, self).__init__(
            message or 'Numero de telefone invalido')


class TelephoneValidationError(ValidationError):

    def __init__(self, message=None):
        super(TelephoneValidationError, self).__init__(
            message or 'Numero de telefone fixo invalido')


class CellphoneValidationError(ValidationError):

    def __init__(self, message=None):
        super(CellphoneValidationError, self).__init__(
            message or 'Numero de telefone celular invalido')
