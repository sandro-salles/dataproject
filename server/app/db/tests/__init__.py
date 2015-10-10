from person.models import Person
from person.contact.models import Phone, Carrier
from django.utils.crypto import get_random_string
import random

def get_n_person_instances(n):

    names = []
    documents = []
    people = []

    for i in xrange(n):
        names.append(get_random_string(length=40))
        documents.append(get_random_string(length=14))
        people.append(Person(name=names[i], document=documents[i]))

    return (names, documents, people)


def create_and_get_n_carrier_objects(n):
    return [Carrier.objects.get_or_create(name=get_random_string(length=200))[0] for i in xrange(n)]


def get_n_phone_instances(n, carriers):

    types = []
    carriers = carriers or create_and_get_n_carrier_objects(20)
    numbers = []
    areacodes = []
    hashes = []
    phones = []

    for i in xrange(n):
        types.append(random.choice(Phone.TYPE_CHOICES)[0])
        carriers.append(random.choice(carriers))
        numbers.append(get_random_string(length=9))
        areacodes.append(random.choice(Phone.AREACODE_CHOICES)[0])
        hashes.append(Phone.make_hash(types[i], areacodes[i], numbers[i]))
        phones.append(Phone(type=types[i], carrier=carriers[i], number=numbers[
                      i], areacode=areacodes[i], hash=hashes[i]))

    return (hashes, numbers, areacodes, phones)
