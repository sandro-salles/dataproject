# -*- coding: utf-8 -*-
from django.db import models
from core.models import DatableModel, SlugModel
from django.contrib.auth.models import AbstractUser


class Corporation(SlugModel, DatableModel):
    owner = models.ForeignKey('User', related_name='owned_corporation')
    document = models.CharField('CNPJ', max_length=14, unique=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        app_label = 'account'

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    corporation = models.ForeignKey(Corporation)

    class Meta:
        verbose_name = u'Usuário'
        verbose_name_plural = u'Usuários'
        app_label = 'account'

    def __unicode__(self):
        return self.username
