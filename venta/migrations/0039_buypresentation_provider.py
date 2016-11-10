# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0038_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='buypresentation',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='venta.Provider', verbose_name='Proveedor'),
            preserve_default=False,
        ),
    ]
