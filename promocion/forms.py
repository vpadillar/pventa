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
        fields = ['codigo', 'tipo', 'nombre', 'descripcion','inicio', 'fin','valor','producto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
    # end class

    def clean(self):
        data = super(PProductoForm, self).clean()
        if data.get('inicio') < date.today():
            self.add_error('inicio', 'La fecha de inicio debe ser mayor o igual a hoy.')
        # end def
        if data.get('fin') < date.today():
            self.add_error('fin', 'La fecha de fin debe ser mayor o igual a hoy.')
        # end def
        print 'info de las fechas ',data.get('inicio'),data.get('fin')
        if data.get('inicio') >= data.get('fin'):
            self.add_error('fin', 'La fecha de fin debe ser mayor a la de finalizacion de la promocion.')
        # end def
        if data.get('tipo') == 1 :
            if data.get('valor') < 0 or data.get('valor') > 100 :
                self.add_error('valor','El valor debe encontrase entre 0 y 100.')
             # end if
        # en dif
        if data.get('tipo') == 2:
            if data.get('valor') < 0 :
                self.add_error('valor','El valor debe encontrase mayor a 0.')
             # end if
        # en dif
    # end def
# end class


class PProductoFormAdmin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
		super(PProductoFormAdmin, self).__init__(*args, **kwargs)
		user = CuserMiddleware.get_user()
                if not user.is_superuser and user.is_staff:
		    self.fields["producto"].queryset = venta.Product.objects.filter(brand__service__userservice__user = user)
                else:
		    self.fields["producto"].queryset = venta.Product.objects.all()
	#end def

    class Meta:
        model = models.PProducto
        exclude = ['estado']
        fields = ['servicio', 'tipo','codigo', 'nombre', 'descripcion','inicio', 'fin','valor','producto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'nombre': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
    # end class

    def clean(self):
        data = super(PProductoFormAdmin, self).clean()
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
        if data.get('tipo') == 2:
            if data.get('valor') < 0 :
                self.add_error('valor','El valor debe encontrase mayor a 0.')
             # end if
        # en dif
    # end def
# end class
