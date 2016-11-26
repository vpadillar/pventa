# -*- coding: utf-8 -*-
from django.contrib import admin
from pventa.admin import admin_site
from cuser.middleware import CuserMiddleware
from django.db.models import Count, Sum
import models
import forms

class ConsumptionDishInline(admin.StackedInline):
	model = models.ConsumptionDish
#end class

class DishAdmin(admin.ModelAdmin):
	model = models.Dish
	list_display = ['thumbnail', 'name', 'price']
	inlines = [ConsumptionDishInline]
	search_fields = ['name', 'price']

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(DishAdmin, self).get_queryset(request)
		queryset = queryset.filter(category__service__userservice__user = user)
		return queryset
	#end def

#end class

class TableAdmin(admin.ModelAdmin):
	models = models.Table
	exclude = ['service']
	
	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(TableAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def
#end class

class BuySupplyStacked(admin.StackedInline):
	model = models.BuySupply
	extra = 0
	readonly_fields = ('current_count', 'date')
	form = forms.BuySupplyForm

	def get_queryset(self, request):
		queryset = super(BuySupplyStacked, self).get_queryset(request)
		queryset = queryset.filter(current_count__gt = 0)
		return queryset
	#end def

	def has_add_permission(self, obj):
		return True
	#end def

	def has_delete_permission(self, *obj):
		return False
	#end def
#end class

class SupplyAdmin(admin.ModelAdmin):
	models = models.Supply
	exclude = ['stock', 'stock_refill', 'minimun_stock', 'service']
	inlines = [BuySupplyStacked]
	list_display = ['name', 'unidad']
	search_fields = ['name', 'unidad']

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(SupplyAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def


#end class

class ConsumptionAdmin(admin.ModelAdmin):
	models = models.Supply
	list_display = ['supply', 'consumo', 'product', 'date', 'canceled']
	search_fields = ['supply', 'consumption', 'product']
	list_filter = ['date', 'canceled', 'product']
	readonly_fields = ['product', 'supply', 'consumption', 'date', 'order']

	def consumo(self, obj):
		return "%s %s" % (obj.consumption, obj.supply.supply.unidad)
	#end def

	def has_add_permission(self, obj):
		return False
	#end def

	def has_delete_permission(self, *obj):
		return False
	#end def
#end class

class ConsuptionInline(admin.TabularInline):
	model = models.Consumption
	extra = 0
	readonly_fields = ['product', 'consumption', 'order', 'date', 'canceled']

	def has_add_permission(self, obj):
		return False
	#end def

	def has_delete_permission(self, *obj):
		return False
	#end def
# end class

class BuySupplyAdmin(admin.ModelAdmin):
	inlines = [ConsuptionInline]
	model = models.BuySupply
	readonly_fields = ('current_count',)
	def save_model(self, request, obj, form, change):
		if not change:
			obj.current_count = obj.buy_count
			obj.save()
		#end if
		super(BuySupplyAdmin, self).save_model(request, obj, form, change)
	#end def
#end class

class ItemRequestInline(admin.StackedInline):
	model = models.ItemRequest
#end def


class SupplyRequestAdmin(admin.ModelAdmin):
	model = models.SupplyRequest
	inlines = [ItemRequestInline]
	exclude = ["service"]

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(SupplyRequestAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

#end class

class BillBuySupplyAdmin(admin.ModelAdmin):
	inlines = [BuySupplyStacked]
	model = models.BillBuySupply
#end class

admin_site.register(models.SupplyRequest, SupplyRequestAdmin)
admin_site.register(models.BuySupply, BuySupplyAdmin)
admin_site.register(models.Dish, DishAdmin)
admin_site.register(models.Table, TableAdmin)
admin_site.register(models.Supply, SupplyAdmin)
admin_site.register(models.Consumption, ConsumptionAdmin)
admin_site.register(models.SetTable)
admin_site.register(models.BillBuySupply, BillBuySupplyAdmin)