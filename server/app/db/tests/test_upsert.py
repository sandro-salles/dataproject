from django.test import TestCase
from person.models import Person
from person.contact.models import Phone
from django.utils.crypto import get_random_string
from django.core.exceptions import FieldDoesNotExist

from db.tests import get_n_person_instances, get_n_phone_instances, create_and_get_n_carrier_objects

import random
import copy


class UpsertTestCase(TestCase):

    def setUp(self):
        self.carriers = create_and_get_n_carrier_objects(20)

    def test_bulk_upsert_can_return_ids(self):

        length = 10
        names, documents, people = get_n_person_instances(length)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'])

        self.assertEqual(length, len(people))
        self.assertEqual(length, len([p.id for p in people if p.id]))

    def test_bulk_upsert_return_correct_ids(self):

        length = 7
        names, documents, people = get_n_person_instances(length)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'])

        db_people = Person.objects.filter(
            id__in=[p.id for p in people if p.id]).all()

        self.assertEqual(len(people), len(db_people))

        person = random.choice(people)
        db_person = Person.objects.get(id=person.id)

        self.assertEqual(person.name, db_person.name)
        self.assertEqual(person.document, db_person.document)

    def test_bulk_upsert_with_batch_size_return_correct_ids(self):

        length = 11
        names, documents, people = get_n_person_instances(length)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'], batch_size=3)

        self.assertEqual(len(people), Person.objects.filter(
            id__in=[p.id for p in people if p.id]).count())

        person = random.choice(people)
        db_person = Person.objects.get(id=person.id)

        self.assertEqual(person.name, db_person.name)
        self.assertEqual(person.document, db_person.document)

    def test_bulk_upsert_can_handle_updates(self):

        length = 11
        names, documents, people = get_n_person_instances(length)

        # copy the people list without preserving references
        people_copy = copy.deepcopy(people)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'])

        names, documents, people = get_n_person_instances(length)

        people.extend(people_copy[:2])

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'])

        self.assertEqual(len(people), Person.objects.filter(
            id__in=[p.id for p in people if p.id]).count())

        person = random.choice(people)
        db_person = Person.objects.get(id=person.id)

        self.assertEqual(person.name, db_person.name)
        self.assertEqual(person.document, db_person.document)

    def test_bulk_upsert_without_return_ids_can_insert_entries(self):

        length = 11
        names, documents, people = get_n_person_instances(length)

        people = Person.objects.bulk_upsert(
            people, return_ids=False)

        self.assertEqual(len(people), Person.objects.filter(
            document__in=documents).count())

        person = random.choice(people)
        db_person = Person.objects.get(document=person.document)

        self.assertEqual(person.name, db_person.name)

    def test_bulk_upsert_without_return_ids_can_handle_updates(self):

        length = 4
        names, documents, people = get_n_person_instances(length)

        # copy the people list without preserving references
        people_copy = copy.deepcopy(people)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'], return_ids=False)

        names, documents, people = get_n_person_instances(length)

        people.extend(people_copy[:2])

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', update_fields=['name', 'updated_at'], return_ids=False)

        documents = [p.document for p in people if p.document]

        self.assertEqual(len(people), Person.objects.filter(
            document__in=documents).count())

        person = random.choice(people)
        db_person = Person.objects.get(document=person.document)

        self.assertEqual(person.name, db_person.name)
        self.assertEqual(person.document, db_person.document)

    def test_bulk_upsert_without_return_ids_without_update_fields_can_skip_update(self):

        length = 11
        names, documents, people = get_n_person_instances(length)

        # copy the people list without preserving references
        people_copy = copy.deepcopy(people)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', return_ids=False)

        names, documents, people = get_n_person_instances(length)

        skip_people = people_copy[:2]

        for p in skip_people:
            p.name = get_random_string(length=40)

        people.extend(skip_people)

        people = Person.objects.bulk_upsert(
            people, unique_constraint='document', return_ids=False)

        self.assertEqual(0, Person.objects.filter(
            name__in=[p.name for p in skip_people]).count())

    def test_bulk_upsert_can_handle_unique_together_constraint(self):

        length = 5
        hashes, numbers, areacodes, phones = get_n_phone_instances(
            length, self.carriers)

        phones = Phone.objects.bulk_upsert(
            phones, unique_constraint=('type', 'areacode', 'number'), update_fields=['carrier', 'updated_at'])

        self.assertEqual(length, len(phones))
        self.assertEqual(length, len([p.id for p in phones if p.id]))

    def test_bulk_upsert_with_wrong_unique_constraint_name_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(FieldDoesNotExist):
            people = Person.objects.bulk_upsert(
                people, unique_constraint='wrong_document_field_name', update_fields=['name', 'updated_at'])

    def test_bulk_upsert_with_wrong_update_field_name_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(FieldDoesNotExist):
            people = Person.objects.bulk_upsert(
                people, unique_constraint='document', update_fields=['wrong_name', 'updated_at'])

    def test_bulk_upsert_with_non_unique_constraint_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(ValueError):
            people = Person.objects.bulk_upsert(
                people, unique_constraint='nature', update_fields=['name', 'updated_at'])

    def test_bulk_upsert_with_unique_constraint_on_update_fields_list_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(ValueError):
            people = Person.objects.bulk_upsert(
                people, unique_constraint='document', update_fields=['id', 'updated_at'])

    def test_bulk_upsert_with_return_ids_without_unique_constraint_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(AssertionError):
            people = Person.objects.bulk_upsert(
                people, update_fields=['id', 'updated_at'])

    def test_bulk_upsert_with_return_ids_without_update_fields_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(AssertionError):
            people = Person.objects.bulk_upsert(
                people, unique_constraint='document')

    def test_bulk_upsert_without_return_ids_with_update_fields_without_unique_constraint_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(AssertionError):
            people = Person.objects.bulk_upsert(
                people, update_fields=['id', 'updated_at'], return_ids=False)

    def test_bulk_upsert_with_nonexistent_unique_together_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(ValueError):
            people = Person.objects.bulk_upsert(
                people, unique_constraint=('a', 'b'), update_fields=['name', 'updated_at'])

    def test_bulk_upsert_with_nonexistent_unique_together_throws_exception(self):

        length = 1
        names, documents, people = get_n_person_instances(length)

        with self.assertRaises(ValueError):
            people = Person.objects.bulk_upsert(
                people, unique_constraint=('a', 'b'), update_fields=['name', 'updated_at'])

    def test_bulk_upsert_with_invalid_unique_together_throws_exception(self):

        length = 1
        hashes, numbers, areacodes, phones = get_n_phone_instances(
            length, self.carriers)

        with self.assertRaises(ValueError):
            phones = Phone.objects.bulk_upsert(
                phones, unique_constraint=('a', 'b'), update_fields=['number', 'updated_at'])
