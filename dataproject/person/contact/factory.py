# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from person.contact.util import is_valid_brazilian_area_code, is_valid_brazilian_telephone_number, is_valid_brazilian_cellphone_number
from person.contact.models import Phone


class InvalidContactException(Exception):
    pass

class PhoneFactory:

    @staticmethod
    def get_or_instantiate_for(area_code, number):
        
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


        raise InvalidContactException(_(u'O número informado não pode ser identificado como um documento válido'))
