# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, DirtyModel
from person.models import Person
import reversion
import mmh3
from memoize import memoize

@reversion.register
class Document(DatableModel):

    TYPE_CHOICES_CPF  = ('CPF', _(u'CPF'))
    TYPE_CHOICES_RG  = ('RG', _(u'RG'))
    TYPE_CHOICES_CNPJ  = ('CNPJ', _(u'CNPJ'))
    TYPE_CHOICES = (TYPE_CHOICES_CPF, TYPE_CHOICES_RG, TYPE_CHOICES_CNPJ)

    type = models.CharField(_('Tipo do Documento'), max_length=6, choices=TYPE_CHOICES)
    number = models.CharField(_(u'Número'), max_length=30, unique=True)
    issuer = models.CharField(_(u'Órgão Emissor'), max_length=300, blank=True)
    hash = models.IntegerField(_('Hash'), unique=True, editable=False)

    person = models.ForeignKey(Person)

    
    @staticmethod
    @memoize()
    def make_hash(type, number):
        return mmh3.hash('%s%s' % (type, number))

    def save(self, *args, **kwargs):
        self.hash = Document.make_hash(self.type, self.number)
        super(Document, self).save(*args, **kwargs)

    class Meta:
        verbose_name        = _("Documento Pessoal")
        verbose_name_plural = _("Documentos Pessoais")

    def __unicode__(self):
        return self.number