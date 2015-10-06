from collections import namedtuple
from core.util import normalize_text, as_digits
from person.util import validate_cnpj, validate_cpf
from person.exceptions import CPFValidationError, CNPJValidationError
from geo.util import validate_zipcode
from geo.exceptions import ZipCodeValidationError


ZOOM_FIELDS = ("zoom_code", "phone", "name", "location",
               "neighborhood", "city", "state", "zipcode", "document", "exceptions")


class ZoomRecord(namedtuple('ZoomRecord_', ZOOM_FIELDS)):

    @classmethod
    def parse(klass, row):
        row = list(row)                                 # Make row mutable
        row[1] = as_digits(row[1])                      # phone
        row[2] = normalize_text(row[2])                 # name
        row[3] = normalize_text(row[3])                 # location
        row[4] = normalize_text(row[4])                 # neighborhood
        row[5] = normalize_text(row[5])                 # city
        row[6] = normalize_text(row[6])                 # state

        exception = None

        try:

            row[7] = validate_zipcode(row[7])           # zipcode
            row[8] = validate_cpf(row[8][-11:])         # document - try CPF

        except CPFValidationError as e:

            try:

                row[8] = validate_cnpj(row[8])          # document - try CNPJ

            except CNPJValidationError as e:

                e.message = 'Numero de CPF/CNPJ invalido (%s)' % row[8]
                exception = e

        except ZipCodeValidationError as e:

            e.message = 'CEP invalido (%s)' % row[7]
            exception = e


        row.append(exception)

        return klass(*row)
