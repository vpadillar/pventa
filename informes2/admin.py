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
from django.db import models
from django.contrib import admin
from pventa.admin import admin_site
import models


class InformeCategoriaResource(resources.ModelResource):
    inicio = fields.Field(column_name="inicio", attribute="inicio")
    fin = fields.Field(column_name="fin", attribute="fin")

    class Meta:
        model = models.InformeCategoria
        fields = ['inicio', 'fin']
    # end class

    def export(self, queryset=None, *args, **kwargs):
        return super(ProductResource, self).export(queryset, *args, **kwargs)
    # end def
# end class


class InformeCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'inicio']
    list_filter = ['nombre', 'inicio']
    search_fields = list_filter
# end class


admin_site.register(models.InformeCategoria, InformeCategoriaAdmin)
reports.register_export(models.InformeCategoria, InformeCategoriaResource)
