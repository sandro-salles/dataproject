# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from person.contact.util import is_valid_brazilian_area_code, is_valid_brazilian_telephone_number, is_valid_brazilian_cellphone_number, is_valid_brazilian_zipcode
from person.contact.models import Phone, Telephone, Cellphone, PhysicalAddress
from person.contact.util import normalize_address
from core.util import dict_to_struct, remove_spaces_and_similar
from geo.models import Street

class InvalidContactException(Exception):
    pass

class PhoneFactory:

    @staticmethod
    def get_or_instantiate_for(area_code, number):
        
        with is_valid_brazilian_area_code(area_code) as code:
            if code.is_valid:

                with is_valid_brazilian_telephone_number(number) as telephone:
                    if telephone.is_valid:
                        instance = None

                        try: 
                            instance = Telephone.objects.get(country_code=Phone.COUNTRY_CODE_CHOICES_BRAZIL, area_code=code.number, number=telephone.number)
                            return dict_to_struct({'instance': instance, 'exists': True })
                        except Telephone.DoesNotExist:
                            instance = Telephone(country_code=Phone.COUNTRY_CODE_CHOICES_BRAZIL, area_code=code.number, number=telephone.number)
                            return dict_to_struct({'instance': instance, 'exists': False })

                        

                with is_valid_brazilian_cellphone_number(number) as cellphone:
                    if cellphone.is_valid:
                        instance = None

                        try: 
                            instance = Cellphone.objects.get(country_code=Phone.COUNTRY_CODE_CHOICES_BRAZIL, area_code=code.number, number=cellphone.number)
                            return dict_to_struct({'instance': instance, 'exists': True })
                        except Cellphone.DoesNotExist:
                            instance = Cellphone(country_code=Phone.COUNTRY_CODE_CHOICES_BRAZIL, area_code=code.number, number=cellphone.number)
                            return dict_to_struct({'instance': instance, 'exists': False })


        raise InvalidContactException(_(u'O número informado não parece ser um telefone/celular válido'))



class PhysicalAddressFactory:

    @staticmethod
    def get_or_instantiate_for_zipcode(zipcode, number, complement):
        
        with is_valid_brazilian_zipcode(zipcode) as code:
             if code.is_valid:
                
                instance = None
                number = remove_spaces_and_similar(number) or None
                complement = remove_spaces_and_similar(complement) or None

                try: 
                    instance = PhysicalAddress.objects.get(street__zipcode=code.number, number=number, complement=complement)
                    return dict_to_struct({'instance': instance, 'exists': True })
                except PhysicalAddress.DoesNotExist:
                    street = Street.objects.get(zipcode=code.number)
                    instance = PhysicalAddress(street=street, number=number, complement=complement)
                    return dict_to_struct({'instance': instance, 'exists': False })
                except Street.DoesNotExist:
                    pass

        raise InvalidContactException(_(u'O CEP informado parece estar incorreto'))













