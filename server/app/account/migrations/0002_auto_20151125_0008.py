# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Conta', 'verbose_name_plural': 'Contas'},
        ),
        migrations.AlterModelOptions(
            name='corporateaccount',
            options={'verbose_name': 'Conta Empresarial', 'verbose_name_plural': 'Contas Empresariais'},
        ),
        migrations.AlterModelOptions(
            name='corporation',
            options={'verbose_name': 'Empresa', 'verbose_name_plural': 'Empresas'},
        ),
        migrations.AlterModelOptions(
            name='ownership',
            options={'verbose_name': 'Propriedade de conta', 'verbose_name_plural': 'Propriedades de contas'},
        ),
        migrations.AlterModelOptions(
            name='personalaccount',
            options={'verbose_name': 'Conta Pessoal', 'verbose_name_plural': 'Contas Pessoais'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Inscri\xe7\xe3o', 'verbose_name_plural': 'Inscri\xe7\xf5es'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Usu\xe1rio', 'verbose_name_plural': 'Usu\xe1rios'},
        ),
    ]
