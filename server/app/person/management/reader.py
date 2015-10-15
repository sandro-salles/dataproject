from collections import namedtuple
from core.util import normalize_text
from person.util import validate_cnpj, validate_cpf
from person.models import Person
from person.contact.models import Phone, Address
from person.contact.exceptions import PhoneValidationError
from person.contact.util import validate_phone_number
from person.exceptions import CPFValidationError, CNPJValidationError
from geo.util import validate_zipcode
from geo.exceptions import ZipCodeValidationError


ZOOM_FIELDS = ("row", "person", "address", "phone", "exception")


class ZoomRecord(namedtuple('ZoomRecord_', ZOOM_FIELDS)):

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

        exception = None

        try:

            # document - try CPF
            person.document = validate_cpf(row[8][-11:])
            person.nature = Person.NATURE_CHOICES_PHYSICAL[0]

        except CPFValidationError as e:

            try:

                # document - try CNPJ
                person.document = validate_cnpj(row[8][-14:])
                person.nature = Person.NATURE_CHOICES_LEGAL[0]

            except CNPJValidationError as e:

                exception = e

        person.hash = Person.make_hash(person.name, person.document)

        try:
            address.zipcode = validate_zipcode(row[7])
            address.hash = Address.make_hash(address.zipcode, address.location)

        except ZipCodeValidationError as e:

            exception = e

        try:

            phone.number = validate_phone_number(row[1])
            phone.hash = Phone.make_hash(
                phone.type, phone.areacode, phone.number)

        except PhoneValidationError as e:

            exception = e

        return klass(row, person, address, phone, exception)
