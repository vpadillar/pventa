# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0049_provider_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buypoduct',
            name='current_count',
            field=models.IntegerField(verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='sell',
            name='count',
            field=models.IntegerField(verbose_name='Cantidad'),
        ),
    ]
