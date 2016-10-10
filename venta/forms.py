from django import forms
from cuser.middleware import CuserMiddleware
import models

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
