from collections import namedtuple
from core.util import normalize_text
from person.util import validate_cnpj, validate_cpf
from person.models import Person
from person.contact.models import Phone, Address
from person.contact.exceptions import PhoneValidationError, AreaCodeValidationError
from person.contact.util import validate_phone_number, validate_areacode
from person.exceptions import CPFValidationError, CNPJValidationError
from geo.util import validate_zipcode
from geo.exceptions import ZipCodeValidationError


ZOOM_RECORD_FIELDS = ("row", "person", "address", "phone")


class ZoomRecord(namedtuple('ZoomRecord_', ZOOM_RECORD_FIELDS)):

    @classmethod
    def parse(klass, row, carrier, areacode, phone_type):
        row = list(row)                                 # Make row mutable

        person = Person()
        person.name = normalize_text(row[2])

        address = Address()
        address.location = normalize_text(row[3])
        address.neighborhood = normalize_text(row[4])
        address.city = normalize_text(row[5])
        address.state = normalize_text(row[6])

        phone = Phone()
        phone.carrier = carrier
        phone.areacode = areacode
        phone.type = phone_type

        try:

            # document - try CPF
            person.document = validate_cpf(row[8][-11:])
            person.nature = Person.NATURE_CHOICES_PHYSICAL[0]

        except CPFValidationError:

            # document - try CNPJ
            person.document = validate_cnpj(row[8][-14:])
            person.nature = Person.NATURE_CHOICES_LEGAL[0]

        address.zipcode = validate_zipcode(row[7])

        phone.number = validate_phone_number(row[1])

        return klass(row, person, address, phone)

    @classmethod
    def parse_gvt(klass, row, carrier, phone_type):

        row = list(row)                                 # Make row mutable

        person = Person()
        person.name = normalize_text(row[2])

        address = Address()
        address.location = '%s %s %s' % (normalize_text(
            row[3]), normalize_text(row[4]), normalize_text(row[5]))
        address.neighborhood = normalize_text(row[6])
        address.city = normalize_text(row[8])
        address.state = normalize_text(row[9])

        phone = Phone()
        phone.carrier = carrier
        phone.type = phone_type

        try:

            # document - try CPF
            person.document = validate_cpf(row[11][-11:])
            person.nature = Person.NATURE_CHOICES_PHYSICAL[0]

        except CPFValidationError:

            # document - try CNPJ
            person.document = validate_cnpj(row[11][-14:])
            person.nature = Person.NATURE_CHOICES_LEGAL[0]

        address.zipcode = validate_zipcode(row[7])

        phone.areacode = validate_areacode(row[0])

        phone.number = validate_phone_number(row[1])

        return klass(row, person, address, phone)
