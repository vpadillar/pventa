from django import forms
from cuser.middleware import CuserMiddleware
import models
from restorant.models import Table
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

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
		model = models.Cellar
		exclude = ["service"]
	#end class

	def save(self, commit = True):
		bodega = super(CellarForm, self).save(commit)
		usuario = CuserMiddleware.get_user()
		bodega.service = models.Service.objects.filter(userservice__user = usuario).first()
		bodega.save()
		return bodega
	#end def

#end class

class CategoryForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CategoryForm, self).__init__(*args, **kwargs)
		usuario = CuserMiddleware.get_user()
		service = models.Service.objects.filter(userservice__user = usuario).first()
		self.fields['image'] = forms.ModelChoiceField(label='Imagen', queryset=models.Image.objects.filter(service = service), required=False)
	# end def

	class Meta:
		model = models.Category
		exclude = []
	#end class

	def save2(self, commit = True):
		categry = super(CategoryForm, self).save(commit=False)
		usuario = CuserMiddleware.get_user()
		categry.service = models.Service.objects.filter(userservice__user = usuario).first()
		categry.save()
		return categry
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

class ProductRequestForm(forms.ModelForm):

	class Meta:
		exclude = ["service"]
		model = models.ProductRequest
	#end class

	def save(self, commit = True):
		pedido = super(ProductRequestForm, self).save(commit=False)
		usuario = CuserMiddleware.get_user()
		pedido.service = models.Service.objects.filter(userservice__user = usuario).first()
		pedido.waiter = usuario
		pedido.save()
		return pedido
	#end def
#end class

class CashierForm(UserCreationForm):

	class Meta:
		fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
		model = models.Cashier
	#end class

	def save(self, commit = True):
		cashier = super(CashierForm, self).save(commit=False)
		user = CuserMiddleware.get_user()
		cashier.service = models.Service.objects.filter(userservice__user = user).first()
		cashier.save()
		groupCashier, created = Group.objects.get_or_create(name = "cashier")
		cashier.groups.add(groupCashier)
		return cashier
	#end def
#end class


class BrandForm(forms.ModelForm):
	class Meta:
		model = models.Brand
		fields = ['name','description']
		exclude = ['state', 'service']
		widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
	# end class
# end class


class BrandForm(forms.ModelForm):
	class Meta:
		model = models.Brand
		fields = ['name','description']
		exclude = ['state', 'service']
		widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
	# end class
# end class


class BrandFormAdmin(forms.ModelForm):
	class Meta:
		model = models.Brand
		fields = ['service','name','description']
		exclude = ['state']
		widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
	# end class
# end class
