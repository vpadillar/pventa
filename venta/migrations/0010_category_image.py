# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-06 04:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0009_auto_20160206_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.Image'),
        ),
    ]
