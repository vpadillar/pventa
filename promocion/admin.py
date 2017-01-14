from django.contrib import admin
from pventa.admin import admin_site
import models
import forms
from cuser.middleware import CuserMiddleware
# Register your models here.


class PProductoAdmin(admin.ModelAdmin):
    filter_horizontal = ('producto',)
    model = models.PProducto
    form = forms.PProductoFormAdmin

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(PProductoAdmin, self).get_queryset(request)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(service__userservice__user = user)
    	return query
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		kwargs['form'] = forms.PProductoForm
    	# end if
    	return super(PProductoAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def save_model(self, request, obj, form, change):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		service = Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
    		#end if
    	super(PProductoAdmin, self).save_model(request, obj, form, change)
    #end def
#end class


class PMarcaAdmin(admin.ModelAdmin):
    filter_horizontal = ('marcas',)
#end class


class PCategoriaAdmin(admin.ModelAdmin):
    filter_horizontal = ('categorias',)
#end class


class BProductoAdmin(admin.ModelAdmin):
    filter_horizontal = ('producto',)
#end class


class BMarcaAdmin(admin.ModelAdmin):
    filter_horizontal = ('marcas',)
#end class


class BCategoriaAdmin(admin.ModelAdmin):
    filter_horizontal = ('categorias',)
#end class


admin_site.register(models.PProducto, PProductoAdmin)
admin_site.register(models.PMarca, PMarcaAdmin)
admin_site.register(models.PCategoria)
admin_site.register(models.BProducto, BProductoAdmin)
admin_site.register(models.BMarca, BMarcaAdmin)
admin_site.register(models.BCategoria, BCategoriaAdmin)
