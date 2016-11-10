# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0045_itemrequest_productrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequest',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.BuyPresentation', verbose_name='Producto'),
        ),
    ]
