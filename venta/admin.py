from django.contrib import admin
from pventa.admin import admin_site
from cuser.middleware import CuserMiddleware
from models import Service
from django.core.exceptions import ValidationError
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
import models
from django.db.models import Count, Sum
from forms import ProductoForm, CellarForm, ProviderForm

class BuyProductStacked(NestedStackedInline):
	model = models.BuyPoduct
	extra = 0
	readonly_fields = ('current_count',)

	def has_add_permission(self, obj):
		return False
	#end def

	def has_delete_permission(self, *obj):
		return False
	#end def

	def get_queryset(self, request):
		queryset = super(BuyProductStacked, self).get_queryset(request)
		queryset = queryset.filter(current_count__gt = 0)
		return queryset
	#end def
#end class

class BuyPresentationStack(NestedStackedInline):
	model = models.BuyPresentation
	inlines = [BuyProductStacked]
	extra = 0

	def has_add_permission(self, obj):
		return False
	#end def

	def has_delete_permission(self, *obj):
		return False
	#end def
#end class

class CellarAdmin(NestedModelAdmin):
	model = models.Cellar
	inlines = [BuyPresentationStack]
	form = CellarForm
#end class

class ProviderAdmin(NestedModelAdmin):
	model = models.Provider
	form = ProviderForm
#end class


class CategoryAdmin(admin.ModelAdmin):
	model = models.Category
	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(CategoryAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

	def get_fields(self, request, obj):
		fields = super(CategoryAdmin, self).get_fields(request, obj)
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			fields.remove('service')
		return fields
	#end def

	def save_model(self, request, obj, form, change):
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			obj.service = service
		#end if
		super(CategoryAdmin, self).save_model(request, obj, form, change)
	#end def
#end class

class ProductAdmin(NestedModelAdmin):
	model = models.Product
	inlines = [BuyPresentationStack]
	list_display = ['name', 'total', 'ventas']
	search_fields = ['name']

	form = ProductoForm


	def ventas(self, obj):
		return models.Sell.objects.filter(bought__buypresentation__product = obj).aggregate(total = Sum('count'))['total']
	# end def

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(ProductAdmin, self).get_queryset(request)
		queryset = queryset.filter(category__service__userservice__user = user)
		return queryset
	#end def

	def get_fields2(self, request, obj):
		fields = super(ProductAdmin, self).get_fields(request, obj)
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			fields.remove('service')
		return fields
	#end def

	def save_model(self, request, obj, form, change):
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			obj.service = service
		#end if
		super(ProductAdmin, self).save_model(request, obj, form, change)
	#end def#end class

class ClientAdmin(admin.ModelAdmin):
	model = models.Client
	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(ClientAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

	def get_fields(self, request, obj):
		fields = super(ClientAdmin, self).get_fields(request, obj)
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			fields.remove('service')
		return fields
	#end def

	def save_model(self, request, obj, form, change):
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			obj.service = service
		#end if
		super(ClientAdmin, self).save_model(request, obj, form, change)
	#end def
#end class

class BillAdmin(admin.ModelAdmin):
	model = models.Bill
	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(BillAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

	def get_fields(self, request, obj):
		fields = super(BillAdmin, self).get_fields(request, obj)
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			fields.remove('service')
		return fields
	#end def

	def save_model(self, request, obj, form, change):
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			obj.service = service
		#end if
		super(BillAdmin, self).save_model(request, obj, form, change)
	#end def
#end class

class ItemOrderAdmin(admin.StackedInline):
	model = models.ItemOrder
	def has_add_permission(self, request, obj=None):
		return False
	#end def

	def has_delete_permission(self, request, obj=None):
		return False
	#end def
#end def

class OrderAdmin(admin.ModelAdmin):
	model = models.Order
	list_display = ['client', 'date']
	inlines = [ItemOrderAdmin]
	exclude = []

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(OrderAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

	def get_fields(self, request, obj):
		fields = super(OrderAdmin, self).get_fields(request, obj)
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			fields.remove('service')
		return fields
	#end def

	def save_model(self, request, obj, form, change):
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			obj.service = service
		#end if
		super(OrderAdmin, self).save_model(request, obj, form, change)
	#end def
#end class

class PresentationAdmin(admin.ModelAdmin):
	model = models.Presentation
	exclude = ['service']
#end def

class SellAdmin(admin.ModelAdmin):
	model = models.Sell

	def save_model(self, request, obj, form, change):
		if not change:
			obj.bought.current_count = obj.bought.current_count - obj.count
			obj.bought.save()
		#end if
		super(SellAdmin, self).save_model(request, obj, form, change)
	#end def
#end class

class ItemRequestInline(admin.StackedInline):
	model = models.ItemRequest
#end def


class ProductRequestAdmin(admin.ModelAdmin):
	model = models.ProductRequest
	inlines = [ItemRequestInline]
#end class


admin_site.register(models.ProductRequest, ProductRequestAdmin)
admin_site.register(models.Cellar, CellarAdmin)
admin_site.register(models.BuyPresentation)
admin_site.register(models.Provider, ProviderAdmin)
admin_site.register(models.BuyPoduct)
admin_site.register(models.Sell, SellAdmin)
admin_site.register(models.Category, CategoryAdmin)
admin_site.register(models.Product, ProductAdmin)
admin_site.register(models.Client, ClientAdmin)
admin_site.register(models.Bill, BillAdmin)
admin_site.register(models.Order, OrderAdmin)
admin_site.register(models.Service)
admin_site.register(models.UserService)
admin_site.register(models.Image)
admin_site.register(models.Config)
admin_site.register(models.Presentation, PresentationAdmin)
admin_site.register(models.Prueba)
