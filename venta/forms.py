from django import forms
from cuser.middleware import CuserMiddleware
import models
from restorant.models import Table

class SellCreateForm(forms.ModelForm):
	class Meta:
		model = models.Sell
		exclude = []
	#end def

	def save(self, commit):
		obj = super(SellCreateForm, self).save(commit)
		obj.bougth.current_count = obj.bougth.current_count - obj.count
		return obj
	#end def
#end class

class ProductoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProductoForm, self).__init__(*args, **kwargs)
		user = CuserMiddleware.get_user()
		print user
		self.fields["category"].queryset = models.Category.objects.filter(service__userservice__user = user)
		self.fields["presentation"].queryset = models.Presentation.objects.filter(service__userservice__user = user)
	#end def
#end class

class CellarForm(forms.ModelForm):

	class Meta:
		exclude = ["service"]
	#end class

	def save(self, commit = True):
		bodega = super(CellarForm, self).save(commit)
		usuario = CuserMiddleware.get_user()
		bodega.service = models.Service.objects.filter(userservice__user = usuario).first()
		return bodega
	#end def

#end class

class ProviderForm(forms.ModelForm):

	class Meta:
		exclude = ["service"]
	#end class

	def save(self, commit = True):
		proveedor = super(ProviderForm, self).save(commit)
		usuario = CuserMiddleware.get_user()
		proveedor.service = models.Service.objects.filter(userservice__user = usuario).first()
		return proveedor
	#end def
#end class

class OrderForm(forms.ModelForm):
	class Meta:
		exclude = ["service", "waiter", "products"]
		model = models.Order
	# end class

	def save(self, commit = True):
		order = super(OrderForm, self).save(commit=False)
		usuario = CuserMiddleware.get_user()
		order.service = models.Service.objects.filter(userservice__user = usuario).first()
		order.waiter = usuario
		order.save()
		if order.paid:
			Table.objects.filter(settable__order = order).update(aviable=True)
		# end if
		return order
	# end def
# end class

class BillForm(forms.ModelForm):
	class Meta:
		exclude = ["service", "waiter", ]
		model = models.Bill
	# end class

	def save(self, commit = True):
		bill = super(BillForm, self).save(commit=False)
		usuario = CuserMiddleware.get_user()
		bill.service = models.Service.objects.filter(userservice__user = usuario).first()
		bill.waiter = usuario
		bill.save()
		return bill
	#end def
# end class

class ItemOrderForm(forms.ModelForm):
	class Meta:
		exclude = []
		model = models.ItemOrder
	# end class

# end class
