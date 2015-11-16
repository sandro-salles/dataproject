from django.db import models
from django.utils.translation import ugettext as _
from person.contact.models import Carrier

class PersonNatureContactPhoneCarrier(models.Model):

    id = models.CharField(_(u'Id'), max_length=300, primary_key=True)
    nature = models.CharField(_(u'Person Nature'), max_length=1, db_index=True)
    carrier = models.ForeignKey(Carrier)

    class Meta:
        managed = False
        db_table = 'person_nature_contact_phone_carrier'

    def __unicode__(self):
        return self.id

class ContactPhoneCarrierContactPhoneAreacode(models.Model):

    id = models.CharField(_(u'Id'), max_length=300, primary_key=True)
    carrier = models.ForeignKey(Carrier)
    areacode = models.CharField(_(u'DDD'), max_length=2)

    class Meta:
        managed = False
        db_table = 'contact_phone_carrier_contact_phone_areacode'

    def __unicode__(self):
        return self.id


class ContactPhoneAreacodeContactAddressCity(models.Model):

    id = models.CharField(_(u'Id'), max_length=300, primary_key=True)
    areacode = models.CharField(_(u'DDD'), max_length=2)
    city = models.CharField(_(u'Cidade'), max_length=200, db_index=True)

    class Meta:
        managed = False
        db_table = 'contact_phone_areacode_contact_address_city'

    def __unicode__(self):
        return self.id


class ContactAddressCityContactAddressNeighborhood(models.Model):

    id = models.CharField(_(u'Id'), max_length=300, primary_key=True)
    city = models.CharField(_(u'Cidade'), max_length=200, db_index=True)
    neighborhood = models.CharField(_(u'Bairro'), max_length=200, db_index=True)

    class Meta:
        managed = False
        db_table = 'contact_address_city_contact_address_neighborhood'

    def __unicode__(self):
        return self.id



class AddressCity(models.Model):
    city = models.CharField(_(u'Cidade'), max_length=300, primary_key=True)

    class Meta:
        managed = False
        db_table = 'contact_address_city'

    def __unicode__(self):
        return self.city


class PhoneAreacode(models.Model):
    areacode = models.CharField(_(u'DDD'), max_length=2, primary_key=True)

    class Meta:
        managed = False
        db_table = 'contact_phone_areacode'

    def __unicode__(self):
        return self.areacode
