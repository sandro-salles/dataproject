from collections import namedtuple
from core.util import normalize_text, as_digits
from person.util import validate_cnpj, validate_cpf
from person.models import Person
from person.contact.exceptions import PhoneValidationError
from person.contact.util import validate_phone_number
from person.exceptions import CPFValidationError, CNPJValidationError
from geo.util import validate_zipcode
from geo.exceptions import ZipCodeValidationError


ZOOM_FIELDS = ("zoom_code", "phone", "name", "location",
               "neighborhood", "city", "state", "zipcode", "document", "nature", "exception")


class ZoomRecord(namedtuple('ZoomRecord_', ZOOM_FIELDS)):

    @classmethod
    def parse(klass, row):
        row = list(row)                                 # Make row mutable

        row[2] = normalize_text(row[2])                 # name
        row[3] = normalize_text(row[3])                 # location
        row[4] = normalize_text(row[4])                 # neighborhood
        row[5] = normalize_text(row[5])                 # city
        row[6] = normalize_text(row[6])                 # state

        exception = None
        nature = None

        try:
            row[1] = validate_phone_number(row[1])      # phone
            row[7] = validate_zipcode(row[7])           # zipcode
            row[8] = validate_cpf(row[8][-11:])         # document - try CPF
            nature = Person.NATURE_CHOICES_PHYSICAL[0]
        except CPFValidationError as e:

            try:

                row[8] = validate_cnpj(row[8])          # document - try CNPJ
                nature = Person.NATURE_CHOICES_LEGAL[0]

            except CNPJValidationError as e:

                exception = e

        except ZipCodeValidationError as e:

            exception = e

        except PhoneValidationError as e:

            exception = e

        row.append(nature)
        row.append(exception)

        return klass(*row)
