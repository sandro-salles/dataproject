# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from core.util import dict_to_struct
from person.document.factory import DocumentFactory
from person.models import Person


class PersonFactory:

    @staticmethod
    def get_or_instantiate_for_document(document):
                  
        if document.person_id:
            return dict_to_struct({'instance': document.person, 'exists': True })
        else:
            person = document._meta.get_field('person').rel.to()
            return dict_to_struct({'instance': person, 'exists': False })

    @staticmethod
    def get_or_instantiate_for_document_number(number):
        
        return PersonFactory.get_or_instantiate_for_document(DocumentFactory.get_or_instantiate_for_number(number).instance)
