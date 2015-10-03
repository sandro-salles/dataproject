# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from person.contact.util import is_valid_brazilian_area_code, is_valid_brazilian_telephone_number, is_valid_brazilian_cellphone_number, is_valid_brazilian_zipcode
from person.contact.models import Phone, PhysicalAddress
from person.contact.util import normalize_address
from core.util import dict_to_struct, remove_spaces_and_similar
from geo.models import Street
import mmh3

class InvalidContactException(Exception):
    pass

class ZipCodeInvalidException(Exception):
    pass

class ZipCodeNotFoundException(Exception):
    pass

class PhoneFactory:

    @staticmethod
    def get_or_instantiate_for_type(type, area_code, number):
        
        country_code = Phone.COUNTRY_CODE_CHOICES_BRAZIL[0]        
        

        with is_valid_brazilian_area_code(area_code) as code:
            if code.is_valid:

                if type == Phone.TYPE_CHOICES_TELEPHONE[0]:
                    with is_valid_brazilian_telephone_number(number) as phone:
                        if phone.is_valid:
                            hash = Phone.make_hash(country_code, code.number, phone.number)
                            instance = None

                            try: 
                                instance = Phone.objects.only('id', 'carrier_id').get(hash=hash)
                                return dict_to_struct({'instance': instance, 'exists': True })
                            except Phone.DoesNotExist:
                                instance = Phone(hash=hash, type=type, country_code=country_code, area_code=code.number, number=phone.number)
                                return dict_to_struct({'instance': instance, 'exists': False })

                elif type == Phone.TYPE_CHOICES_CELLPHONE[0]:
                    with is_valid_brazilian_cellphone_number(number) as phone:
                        if phone.is_valid:
                            hash = Phone.make_hash(country_code, code.number, phone.number)
                            instance = None

                            try: 
                                instance = Phone.objects.only('id', 'carrier_id').get(hash=hash)                            
                                return dict_to_struct({'instance': instance, 'exists': True })
                            except Phone.DoesNotExist:
                                instance = Phone(hash=hash, type=type, country_code=country_code, area_code=code.number, number=phone.number)
                                return dict_to_struct({'instance': instance, 'exists': False })


        raise InvalidContactException(_(u'O número informado não parece ser um telefone/celular válido'))


    

class PhysicalAddressFactory:

    @staticmethod
    def get_or_instantiate_for_zipcode(zipcode, number, complement):
        
        

        with is_valid_brazilian_zipcode(zipcode) as code:
             if code.is_valid:
                hash = PhysicalAddress.make_hash(code.number, remove_spaces_and_similar(number), remove_spaces_and_similar(complement))
                
                instance = None
                number = remove_spaces_and_similar(number) or None
                complement = remove_spaces_and_similar(complement) or None

                try: 
                    instance = PhysicalAddress.objects.only('id').get(hash=hash)                    
                    return dict_to_struct({'instance': instance, 'exists': True })
                except PhysicalAddress.DoesNotExist:
                    try:
                        street = Street.objects.only('id').get(zipcode=code.number)
                        instance = PhysicalAddress(hash=hash, street=street, number=number, complement=complement, neighborhood=street.neighborhood, city=street.neighborhood.city, state=street.neighborhood.city.state, )
                        return dict_to_struct({'instance': instance, 'exists': False })
                    except Street.DoesNotExist:
                        raise ZipCodeNotFoundException(_(u'O CEP informado (%s) não existe na base de DNE' % zipcode))

        raise ZipCodeInvalidException(_(u'O CEP informado (%s) parece estar incorreto' % zipcode))













