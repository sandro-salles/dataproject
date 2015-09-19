# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from person.document.util import is_valid_cpf_format, is_valid_cnpj_format
from person.document.models import CPF, CNPJ


class InvalidDocumentException(Exception):
    pass

class DocumentFactory:

    @staticmethod
    def get_or_instantiate_for_number(number):
        
        with is_valid_cpf_format(number) as cpf:
            if cpf.is_valid:
                try: 
                    return CPF.objects.get(number=cpf.number)
                except CPF.DoesNotExist:
                    return CPF(number=cpf.number)

        with is_valid_cnpj_format(number) as cnpj:
            if cnpj.is_valid:
                try: 
                    return CNPJ.objects.get(number=cnpj.number)
                except CNPJ.DoesNotExist:
                    return CNPJ(number=cnpj.number)


        raise InvalidDocumentException(_(u'O número informado não pode ser identificado como um documento válido'))
