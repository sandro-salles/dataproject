# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django_hstore import hstore


class State(models.Model):
    name = models.CharField(_('Nome'), max_length=300, db_index=True)
    abbreviation = models.CharField(_(u'Abreviação'), db_index=True, max_length=2)

    class Meta:
        verbose_name        = _("Estado")
        verbose_name_plural = _("Estados")

    def __unicode__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State)
    name = models.CharField(_('Nome'), db_index=True, max_length=600)
    
    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 600,
            }
        },
        {
            'name': 'j_state_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 300,
            }
        },
        {
            'name': 'j_state_abbreviation',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 2,
            }
        },
    ], editable=False)

    objects = hstore.HStoreManager()

    class Meta:
        verbose_name        = _("Cidade")
        verbose_name_plural = _("Cidades")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.json = {'j_name': self.name, 'j_state_name': self.state.name, 'j_state_abbreviation': self.state.abbreviation}
        super(City, self).save(*args, **kwargs)


class Neighborhood(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(_('Nome'), db_index=True, max_length=600)
    
    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 600,
            }
        },
        {
            'name': 'j_city_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 600,
            }
        }
    ], editable=False)

    objects = hstore.HStoreManager()

    class Meta:
        verbose_name        = _("Bairro")
        verbose_name_plural = _("Bairro")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.json = {'j_name': self.name, 'j_city_name': self.city.name}
        super(Neighborhood, self).save(*args, **kwargs)
