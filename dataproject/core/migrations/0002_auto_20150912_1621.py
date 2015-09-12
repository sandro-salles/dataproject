# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corporation',
            options={'verbose_name': 'Empresa', 'verbose_name_plural': 'Empresas'},
        ),
        migrations.RemoveField(
            model_name='corporation',
            name='description',
        ),
        migrations.AlterField(
            model_name='corporation',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='corporation',
            name='slug',
            field=models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name='Identificador'),
        ),
    ]
