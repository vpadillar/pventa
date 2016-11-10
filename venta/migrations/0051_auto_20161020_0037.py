# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-20 05:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0050_auto_20161010_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='itemorder',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='venta.Order'),
            preserve_default=False,
        ),
    ]
