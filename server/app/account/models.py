# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, SlugModel
from polymorphic import PolymorphicModel


class Account(SlugModel, DatableModel):

    class Meta:
        verbose_name = _('Conta')
        verbose_name_plural = _('Contas')

    def __unicode__(self):
        return self.name

class Corporation(SlugModel, DatableModel):
    account = models.ForeignKey(Account)

    class Meta:
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')

    def __unicode__(self):
        return self.name


class User(PolymorphicModel, SlugModel, DatableModel):
    account = models.ForeignKey(Account)

    class Meta:
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')

    def __unicode__(self):
        return self.name


class CorporateUser(User):
    corporation = models.ForeignKey(Corporation)

    class Meta:
        verbose_name = _(u'Usuário Corporativo')
        verbose_name_plural = _(u'Usuários Corporativos')

    def __unicode__(self):
        return self.name


