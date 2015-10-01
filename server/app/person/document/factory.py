# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from person.document.util import is_valid_cpf_format, is_valid_cnpj_format
from person.document.models import CPF, CNPJ
from core.util import dict_to_struct


class InvalidDocumentException(Exception):
    pass

class CPFFactory:

    @staticmethod
    def get_or_instantiate_for_number(number):
        
        with is_valid_cpf_format(number) as cpf:
            if cpf.is_valid:
                
                instance = None

                try: 
                    instance =  CPF.objects.only('id', 'person_id').get(number=cpf.number)
                    return dict_to_struct({'instance': instance, 'exists': True })
                except CPF.DoesNotExist:
                    instance = CPF(number=cpf.number)
                    return dict_to_struct({'instance': instance, 'exists': False })

        
        raise InvalidDocumentException(_(u'O número informado não pode ser identificado como um documento válido'))



class CNPJFactory:

    @staticmethod
    def get_or_instantiate_for_number(number):

        with is_valid_cnpj_format(number) as cnpj:
            if cnpj.is_valid:

                instance = None

                try: 
                    instance = CNPJ.objects.only('id', 'person_id').get(number=cnpj.number)
                    return dict_to_struct({'instance': instance, 'exists': True })
                except CNPJ.DoesNotExist:
                    instance = CNPJ(number=cnpj.number)
                    return dict_to_struct({'instance': instance, 'exists': False })

        raise InvalidDocumentException(_(u'O número informado não pode ser identificado como um documento válido'))