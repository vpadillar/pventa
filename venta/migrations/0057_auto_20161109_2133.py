# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-10 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0056_auto_20161108_1757'),
    ]

    operations = [
        migrations.DeleteModel(
            name='prueba',
        ),
        migrations.AddField(
            model_name='config',
            name='impresora',
            field=models.BooleanField(default=True),
        ),
    ]
