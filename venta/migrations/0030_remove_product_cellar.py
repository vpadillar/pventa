# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 15:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0029_product_cellar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cellar',
        ),
    ]
