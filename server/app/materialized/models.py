from django.db import models
from django.utils.translation import ugettext as _
from person.contact.models import Carrier


class Filter(models.Model):

    id = models.IntegerField(_(u'Id'), primary_key=True)
    nature = models.CharField(_(u'Natureza da pessoa'), max_length=1, db_index=True)
    state = models.CharField(_(u'Estado'), max_length=1, db_index=True)
    carrier = models.ForeignKey(Carrier)
    areacode = models.CharField(_(u'DDD'), max_length=2, db_index=True)
    city = models.CharField(_(u'Cidade'), max_length=200, db_index=True)
    neighborhood = models.CharField(_(u'Bairro'), max_length=200, db_index=True)

    class Meta:
        managed = False
        db_table = 'materialized_filter'

    def __unicode__(self):
        return self.id