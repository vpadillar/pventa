#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @author: Exile
    @date: 05-07-2016
    @place: Cartagena - Colombia
    @licence: Creative Common
"""
import reports
from import_export import resources, widgets, fields
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from venta.models import Product, Sell
from pventa.admin import admin_site
from django.db.models import Count

class ProductResource(resources.ModelResource):
	ventas = fields.Field(column_name="Ventas", attribute="ventas")
	class Meta:
		model = Product
		fields = ['category', 'presentation', 'name', 'price', 'ventas']
	# end class

	def export(self, queryset=None, *args, **kwargs):
		queryset = queryset.annotate(ventas=Count('buypresentation__buypoduct__sell__count')).order_by('-ventas')
		return super(ProductResource, self).export(queryset, *args, **kwargs)
	# end def
#end class


class VentaResource(resources.ModelResource):
	ventas = fields.Field(column_name="Ventas", attribute="ventas")
	class Meta:
		model = Sell
		fields = ['bought', 'date', 'count', 'ventas']
	# end class

	def export(self, queryset=None, *args, **kwargs):
		queryset = queryset.annotate(ventas=Count('bought__buypresentation__buypoduct__sell__count')).order_by('-ventas')
		return super(VentaResource, self).export(queryset, *args, **kwargs)
	# end def

#end class


class PlatoResource(resources.ModelResource):
	ventas = fields.Field(column_name="Ventas", attribute="ventas")
	class Meta:
		model = Sell
		fields = ['bought', 'date', 'count', 'ventas']
	# end class

	def export(self, queryset=None, *args, **kwargs):
		queryset = queryset.annotate(ventas=Count('bought__buypresentation__buypoduct__sell__count')).order_by('-ventas')
		return super(VentaResource, self).export(queryset, *args, **kwargs)
	# end def

#end class

reports.register_export(Product, ProductResource)
reports.register_export(Sell, VentaResource)
