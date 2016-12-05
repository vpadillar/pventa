from django.contrib import admin
from pventa.admin import admin_site
from cuser.middleware import CuserMiddleware
from models import Service
from django.core.exceptions import ValidationError
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
import models
from django.db.models import Count, Sum
from forms import ProductoForm, CellarForm, ProviderForm, CashierForm, WaiterForm, ProductRequestForm

class BuyProductStacked(NestedStackedInline):
	model = models.BuyPoduct
	extra = 0
	readonly_fields = ('current_count',)

	def has_add_permission(self, obj):
		return True
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

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(CellarAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def	

#end class

class BuyProductAdmin(NestedModelAdmin):
	model = models.BuyPoduct

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(BuyProductAdmin, self).get_queryset(request)
		queryset = queryset.filter(buypresentation__product__category__service__userservice__user = user)
		return queryset
	#end def

#end class

class ProviderAdmin(NestedModelAdmin):
	model = models.Provider
	form = ProviderForm

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(ProviderAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

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

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(PresentationAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

#end def

class ImageAdmin(admin.ModelAdmin):
	model = models.Image

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(ImageAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

#end class

class SellAdmin(admin.ModelAdmin):
	model = models.Sell

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(SellAdmin, self).get_queryset(request)
		queryset = queryset.filter(bought__buypresentation__product__category__service__userservice__user = user)
		return queryset
	#end def

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
	form = ProductRequestForm

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(ProductRequestAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def
#end class

class ServiceAdmin(admin.ModelAdmin):
	model = models.Service
	list_display = ["name", "id"]
#end class

class CashierAdmin(admin.ModelAdmin):
	model = models.Cashier 
	form = CashierForm

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(CashierAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def
#end class

class WaiterAdmin(admin.ModelAdmin):
	model = models.Waiter
	form = WaiterForm

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(CashierAdmin, self).get_queryset(request)
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	#end def

#end class

class BuyPresentationAdmin(admin.ModelAdmin):
	model = models.BuyPresentation

	def get_queryset(self, request):
		user = CuserMiddleware.get_user()
		queryset = super(BuyPresentationAdmin, self).get_queryset(request)
		queryset = queryset.filter(provider__service__userservice__user = user)
		return queryset
	#end def
#end class

admin_site.register(models.ProductRequest, ProductRequestAdmin)
admin_site.register(models.Cellar, CellarAdmin)
admin_site.register(models.BuyPresentation, BuyPresentationAdmin)
admin_site.register(models.Provider, ProviderAdmin)
admin_site.register(models.BuyPoduct, BuyProductAdmin)
admin_site.register(models.Sell, SellAdmin)
admin_site.register(models.Category, CategoryAdmin)
admin_site.register(models.Product, ProductAdmin)
admin_site.register(models.Client, ClientAdmin)
admin_site.register(models.Bill, BillAdmin)
admin_site.register(models.Order, OrderAdmin)
admin_site.register(models.Service, ServiceAdmin)
admin_site.register(models.UserService)
admin_site.register(models.Image, ImageAdmin)
admin_site.register(models.Config)
admin_site.register(models.Presentation, PresentationAdmin)
admin_site.register(models.Cashier, CashierAdmin)
