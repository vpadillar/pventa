from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import models
from datetime import date
from cuser.middleware import CuserMiddleware
from venta import models as venta

class PProductoForm(forms.ModelForm):
    class Meta:
        model = models.PProducto
        exclude = ['servicio','estado']
        fields = ['codigo', 'tipo', 'nombre', 'descripcion','inicio', 'fin']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
    # end class
# end class


class PProductoFormAdmin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
		super(PProductoFormAdmin, self).__init__(*args, **kwargs)
		user = CuserMiddleware.get_user()
		self.fields["producto"].queryset = venta.Product.objects.filter(service__userservice__user = user)
	#end def

    class Meta:
        model = models.PProducto
        exclude = ['estado']
        fields = ['servicio', 'tipo','codigo', 'nombre', 'descripcion','inicio', 'fin','producto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'nombre': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
    # end class

    def clean(self):
        data = super(PProductoAdmin, self).clean()
        if data.get('inicio') < date.today():
            self.add_error('inicio', 'La fecha de inicio debe ser mayor o igual a hoy.')
        # end def
        if data.get('inicio') > data.get('fin'):
            self.add_error('inicio', 'La fecha de inicio debe ser mayor a la de finalizacion de la promocion.')
        # end def
        if data.get('tipo') == 1 :
            if data.get('valor') < 0 or data.get('valor') > 100 :
                self.add_error('valor','El valor debe encontrase entre 0 y 100.')
             # end if
        # en dif
        if data.get('tipo'):
            if data.get('valor') < 0 :
                self.add_error('valor','El valor debe encontrase mayor a 0.')
             # end if
        # en dif
    # end def
# end class
