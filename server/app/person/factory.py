# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from core.util import dict_to_struct
from person.models import Person, PhysicalPerson


class PersonFactory:

    @staticmethod
    def get_or_instantiate_for_document(document):

        PersonClass = document.__class__.person.field.related_model

        if document.person_id:
            return dict_to_struct({'instance': PersonClass.objects.only('id', 'name').get(id=document.person_id), 'exists': True })
        else:
            person = PersonClass()
            return dict_to_struct({'instance': person, 'exists': False })
