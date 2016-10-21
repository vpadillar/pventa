from django.shortcuts import render
from django.http import HttpResponse
from cuser.middleware import CuserMiddleware
from django.middleware.csrf import get_token
from django.views.generic.base import TemplateView
from supra import views as supra
from django.contrib.auth.models import Group
import models
import forms
import json


class GroupListView(supra.SupraListView):
	model = Group
	def get_queryset(self):
		queryset = super(GroupListView, self).get_queryset()
		user = CuserMiddleware.get_user()
		queryset = queryset.filter(user = user)
		return queryset
	# end def
# end class

class ClientListView(supra.SupraListView):
	model = models.Client
	list_filter = ['cc']
	def get_queryset(self):
		queryset = super(ClientListView, self).get_queryset()
		user = CuserMiddleware.get_user()
		queryset = queryset.filter(service__userservice__user = user)
		return queryset
	# end def
# end class

class Login(supra.SupraSession):
	body = True
# end class

class CategoyListView(supra.SupraListView):
	model = models.Category
	search_fields = ['name']

	def get_queryset(self):
		queryset = super(CategoyListView, self).get_queryset()
		user = CuserMiddleware.get_user()
		queryset=queryset.filter(service__userservice__user = user)
		return queryset
	# end def
# end class

class OrderDetailView(supra.SupraDetailView):
	model = models.Order

# end class
# end class

class OrderDeleteView(supra.SupraDeleteView):
	model = models.Order

# end class

class OrderListView(supra.SupraListView):
	model = models.Order
	search_fields = ['pk']
	list_filter = ['settable__table__aviable']
	list_display = ['id', 'bill', 'canceled', 'casher', 'client', 'date', 'paid', 'pk', 'service', 'waiter', 'bill__id']

	def get_queryset(self):
		queryset = super(OrderListView, self).get_queryset()
		user = CuserMiddleware.get_user()
		queryset=queryset.filter(service__userservice__user = user).extra(select={
			'products': 'select count(i.id) from venta_itemorder as i where i.order_id = venta_order.id',
			'total': 'select sum(p.price*i.count) from venta_itemorder as i join venta_product as p on i.product_id=p.id and i.order_id=venta_order.id'
		})
		return queryset
	# end def
# end class

class ProductListView(supra.SupraListView):
	model = models.Product
	search_fields = ['name']
	list_filter = ['itemorder__order']

	def get_queryset(self):
		queryset = super(ProductListView, self).get_queryset()
		category = self.request.GET.get('category', False)
		if category:
			queryset=queryset.filter(category__pk = category)
		# end if
		return queryset
	# end def
# end class

class IntemOrderInlineFormView(supra.SupraInlineFormView):
	model = models.ItemOrder
	#form_class = forms.ItemOrderForm
	body = True

# end class

class ItemOrderListView(supra.SupraListView):
	model = models.ItemOrder
	list_filter = ['order']
	list_display = ['order_id', 'count', 'id', 'product_id', 'product__name', 'product__price']
# end class

class OrderFormView(supra.SupraFormView):
	model = models.Order
	form_class = forms.OrderForm
	inlines = [IntemOrderInlineFormView]
	body = True
# end class

class BillFormView(supra.SupraFormView):
	model = models.Bill
	form_class = forms.BillForm
	body = True
# end class

class BillDetailView(supra.SupraDetailView):
	model = models.Bill
# end class

class PvTemplateView(TemplateView):

	def get_context_data(self, **kwargs):
		user = CuserMiddleware.get_user()
		context = super(PvTemplateView, self).get_context_data(**kwargs)
		if user.is_authenticated():
			service = models.Service.objects.filter(userservice__user = user).first()
			context['service'] = service
			context['user'] = user
			context['groups'] = user.groups.all()
		#end if
		return context
	#end def
#end class

def nocount(request):
	order = models.Order.objects.last()
	if order:
		no = order.id + 1
	else:
		no = 0
	#end if
	return HttpResponse(str(no))
#end def

def token(request):
	sjson = {
		'token': get_token(request)
	}
	return HttpResponse(json.dumps(sjson), content_type="application/json")
#end def

def config(request):
	config, create = models.Config.objects.get_or_create()
	sjson = {
		'ipoconsumo': config.ipoconsumo,
		'propina': config.propina,
		'iva': config.iva
	}
	return HttpResponse(json.dumps(sjson), content_type="application/json")
#end def


def service(request):
	user = CuserMiddleware.get_user()
	service = models.Service.objects.filter(userservice__user = user).first()
	sjson = {
		'name':service.name,
		'code':service.code,
		'printer':service.printer,
		'moviles':service.moviles,
	}
	return HttpResponse(json.dumps(sjson), content_type="application/json")
#end def
