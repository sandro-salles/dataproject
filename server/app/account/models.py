# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, SluggableModel
from authentication.models import User as SystemUser
from polymorphic import PolymorphicModel
from django.utils.functional import cached_property

DEFAULT_SYSTEM_USER_ID = 1

class AuditableModel(DatableModel):
    deleted_by = models.ForeignKey(SystemUser, related_name="deleted_%(class)s", null=True, blank=True)
    created_by = models.ForeignKey(SystemUser, related_name="created_%(class)s", default=DEFAULT_SYSTEM_USER_ID)
    updated_by = models.ForeignKey(SystemUser, related_name="updated_%(class)s", default=DEFAULT_SYSTEM_USER_ID)

    class Meta:
        abstract = True

class Feature(SluggableModel, DatableModel):
    description = models.TextField(_('Descricao'), max_length=14, unique=True)

    class Meta:
        verbose_name = _('Funcionalidade')
        verbose_name_plural = _('Funcionalidades')
        app_label = 'account'

    def __unicode__(self):
        return self.name


class Plan(PolymorphicModel, SluggableModel, DatableModel):
    description = models.TextField(_('Descricao'), max_length=14, unique=True)
    features = models.ManyToManyField(Feature)

    class Meta:
        verbose_name = _('Plano')
        verbose_name_plural = _('Planos')
        app_label = 'account'

    def __unicode__(self):
        return self.name


class Brass(Plan):

    class Meta:
        verbose_name = _('Plano Bronze')
        verbose_name_plural = _('Planos Bronze')
        app_label = 'account'

    def __unicode__(self):
        return self.name


class Silver(Plan):

    class Meta:
        verbose_name = _('Plano Prata')
        verbose_name_plural = _('Planos Prata')
        app_label = 'account'

    def __unicode__(self):
        return self.name


class Gold(Plan):

    class Meta:
        verbose_name = _('Plano Ouro')
        verbose_name_plural = _('Planos Ouro')
        app_label = 'account'

    def __unicode__(self):
        return self.name


class Diamond(Plan):

    class Meta:
        verbose_name = _('Plano Diamante')
        verbose_name_plural = _('Planos Diamante')
        app_label = 'account'

    def __unicode__(self):
        return self.name


class Account(PolymorphicModel, SluggableModel, AuditableModel):

    TYPE_PERSONAL = 'personal'
    TYPE_CORPORATE = 'corporate'

    @cached_property
    def type(self):

        if type(self) == PersonalAccount:
            return Account.TYPE_PERSONAL
        else:
            return Account.TYPE_CORPORATE

    @cached_property
    def corporation(self):

        corporation = None
        if self.type == self.TYPE_CORPORATE:
            corporation = self.corporation

        return corporation

    class Meta:
        verbose_name = _("Conta")
        verbose_name_plural = _("Contas")

    def __unicode__(self):
        return self.name


class PersonalAccount(Account):

    class Meta:
        verbose_name = _("Conta Pessoal")
        verbose_name_plural = _("Contas Pessoais")

    def __str__(self):
        pass

    def __unicode__(self):
        return self.name


class CorporateAccount(Account):

    class Meta:
        verbose_name = _("Conta Empresarial")
        verbose_name_plural = _("Contas Empresariais")

    def __str__(self):
        pass


class Subscription(AuditableModel):
    account = models.OneToOneField(Account, related_name='subscription')
    plan = models.ForeignKey(Plan)

    class Meta:
        verbose_name = _(u'Inscrição')
        verbose_name_plural = _(u'Inscrições')



class User(SystemUser, AuditableModel):
    account = models.ForeignKey(Account, related_name='users')

    class Meta:
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')

    def __unicode__(self):
        return self.username



class Ownership(AuditableModel):
    account = models.OneToOneField(Account, related_name='ownership')
    user = models.ForeignKey(User, related_name='ownerships')

    class Meta:
        verbose_name = _(u'Propriedade de conta')
        verbose_name_plural = _(u'Propriedades de contas')

    def __unicode__(self):
        return self.account.name


class Corporation(SluggableModel, AuditableModel):
    account = models.OneToOneField(CorporateAccount, related_name='corporation')
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    document = models.CharField(max_length=14)

    class Meta:
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')
