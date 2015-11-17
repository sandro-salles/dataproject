# -*- coding: utf-8 -*-
from django.db import models
from core.models import DatableModel, SlugModel
from django.contrib.auth.models import AbstractUser
from polymorphic import PolymorphicModel

class User(PolymorphicModel, AbstractUser):

    class Meta:
        verbose_name = u'Usuário interno'
        verbose_name_plural = u'Usuários internos'
        app_label = 'account'

    def __unicode__(self):
        return self.username


class Feature(SlugModel, DatableModel):
    description = models.TextField('Descricao', max_length=14, unique=True)

    class Meta:
        verbose_name = 'Funcionalidade'
        verbose_name_plural = 'Funcionalidades'
        app_label = 'account'

    def __unicode__(self):
        return self.name 

class Plan(SlugModel, DatableModel):
    description = models.TextField('Descricao', max_length=14, unique=True)
    features = models.ManyToManyField(Feature)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        app_label = 'account'
        abstract = True

    def __unicode__(self):
        return self.name    


class TrialPlan(Plan):

    class Meta:
        verbose_name = 'Plano de avaliação'
        verbose_name_plural = 'Planos de avaliação'
        app_label = 'account'

    def __unicode__(self):
        return self.name  


class StandalonePlan(Plan):

    class Meta:
        verbose_name = 'Plano Avulso'
        verbose_name_plural = 'Planos Avulsos'
        app_label = 'account'

    def __unicode__(self):
        return self.name  


class ProPlan(Plan):

    class Meta:
        verbose_name = 'Plano premium'
        verbose_name_plural = 'Planos premium'
        app_label = 'account'

    def __unicode__(self):
        return self.name 


class Account(SlugModel, DatableModel):
    plan = models.ForeignKey(Plan)

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        app_label = 'account'

    def __unicode__(self):
        return self.name    


class Corporation(SlugModel, DatableModel):
    account = models.ForeignKey(Account)
    owner = models.ForeignKey('User', related_name='owned_corporation')
    document = models.CharField('CNPJ', max_length=14, unique=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        app_label = 'account'

    def __unicode__(self):
        return self.name


class AppUser(User):
    corporation = models.ForeignKey(Corporation)

    class Meta:
        verbose_name = u'Usuário'
        verbose_name_plural = u'Usuários'
        app_label = 'account'

    def __unicode__(self):
        return self.username

