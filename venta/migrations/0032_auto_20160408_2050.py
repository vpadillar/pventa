# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0031_buypresentation_cellar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buypoduct',
            name='current_count',
            field=models.IntegerField(verbose_name='Cantidad actual'),
        ),
    ]
