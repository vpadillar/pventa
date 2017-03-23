from django.contrib import admin
from pventa.admin import admin_site
import models
import forms
from venta import models as venta
from cuser.middleware import CuserMiddleware
# Register your models here.


class PProductoAdmin(admin.ModelAdmin):
    filter_horizontal = ('producto',)
    model = models.PProducto
    form = forms.PProductoFormAdmin
    list_display = ['servicio', 'nombre', 'descripcion', 'inicio', 'fin', 'estado']
    search_fields = ['servicio__name', 'nombre', 'descripcion', 'inicio', 'fin']
    list_editable = ['estado']

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(PProductoAdmin, self).get_queryset(request)
        print user.is_superuser, user.is_staff,len(query)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(servicio__userservice__user = user)
        print user.is_superuser, user.is_staff,len(query)
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
    		service = venta.Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
                obj.save()
    		#end if
    	super(PProductoAdmin, self).save_model(request, obj, form, change)
    #end def
#end class


class PMarcaAdmin(admin.ModelAdmin):
    filter_horizontal = ('marcas',)
    model = models.PMarca
    form = forms.PMarcaFormAdmin
    list_display = ['servicio', 'nombre', 'descripcion', 'inicio', 'fin', 'estado']
    search_fields = ['servicio__name', 'nombre', 'descripcion', 'inicio', 'fin']
    list_editable = ['estado']

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(PMarcaAdmin, self).get_queryset(request)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(servicio__userservice__user = user)
        #end if
    	return query
    # end def

    def save_model(self, request, obj, form, change):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		service = venta.Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
                obj.save()
    		#end if
    	super(PMarcaAdmin, self).save_model(request, obj, form, change)
    #end def

    def get_form(self, request, obj=None, *args, **kwargs):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		kwargs['form'] = forms.PMarcaForm
    	# end if
    	return super(PMarcaAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
#end class


class PCategoriaAdmin(admin.ModelAdmin):
    filter_horizontal = ('categorias',)
    model = models.PMarca
    form = forms.PCategoriaFormAdmin
    list_display = ['servicio', 'nombre', 'descripcion', 'inicio', 'fin', 'estado']
    search_fields = ['servicio__name', 'nombre', 'descripcion', 'inicio', 'fin']
    list_editable = ['estado']

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(PCategoriaAdmin, self).get_queryset(request)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(servicio__userservice__user = user)
        #end if
    	return query
    # end def

    def save_model(self, request, obj, form, change):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		service = venta.Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
                obj.save()
    		#end if
    	super(PCategoriaAdmin, self).save_model(request, obj, form, change)
    #end def

    def get_form(self, request, obj=None, *args, **kwargs):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		kwargs['form'] = forms.PCategoriaForm
    	# end if
    	return super(PCategoriaAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
#end class


class BProductoAdmin(admin.ModelAdmin):
    filter_horizontal = ('producto',)
    model = models.PProducto
    form = forms.BProductoFormAdmin
    list_display = ['servicio', 'nombre', 'descripcion', 'inicio', 'fin', 'estado']
    search_fields = ['servicio__name', 'nombre', 'descripcion', 'inicio', 'fin']
    list_editable = ['estado']

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(BProductoAdmin, self).get_queryset(request)
        print user.is_superuser, user.is_staff,len(query)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(servicio__userservice__user = user)
        print user.is_superuser, user.is_staff,len(query)
    	return query
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		kwargs['form'] = forms.BProductoForm
    	# end if
    	return super(BProductoAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def save_model(self, request, obj, form, change):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		service = venta.Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
    		#end if
        # end if
        obj.tipo=2
        obj.save()
    	super(BProductoAdmin, self).save_model(request, obj, form, change)
    #end def
#end class


class BMarcaAdmin(admin.ModelAdmin):
    filter_horizontal = ('marcas',)
    model = models.BMarca
    form = forms.BMarcaFormAdmin
    list_display = ['servicio', 'nombre', 'descripcion', 'inicio', 'fin', 'estado']
    search_fields = ['servicio__name', 'nombre', 'descripcion', 'inicio', 'fin']
    list_editable = ['estado']

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(BMarcaAdmin, self).get_queryset(request)
        print user.is_superuser, user.is_staff,len(query)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(servicio__userservice__user = user)
        print user.is_superuser, user.is_staff,len(query)
    	return query
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		kwargs['form'] = forms.BMarcaForm
    	# end if
    	return super(BMarcaAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def save_model(self, request, obj, form, change):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		service = venta.Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
    		#end if
        # end if
        obj.tipo=2
        obj.save()
    	super(BMarcaAdmin, self).save_model(request, obj, form, change)
    #end def
#end class


class BCategoriaAdmin(admin.ModelAdmin):
    filter_horizontal = ('categorias',)
    model = models.BCategoria
    form = forms.BCategoriaFormAdmin
    list_display = ['servicio', 'nombre', 'descripcion', 'inicio', 'fin', 'estado']
    search_fields = ['servicio__name', 'nombre', 'descripcion', 'inicio', 'fin']
    list_editable = ['estado']

    def get_queryset(self, request):
    	user = CuserMiddleware.get_user()
    	query = super(BCategoriaAdmin, self).get_queryset(request)
        print user.is_superuser, user.is_staff,len(query)
    	if  not user.is_superuser and user.is_staff:
    		query = query.filter(servicio__userservice__user = user)
        print user.is_superuser, user.is_staff,len(query)
    	return query
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		kwargs['form'] = forms.BCategoriaForm
    	# end if
    	return super(BCategoriaAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def save_model(self, request, obj, form, change):
    	user = CuserMiddleware.get_user()
    	if not user.is_superuser and user.is_staff:
    		service = venta.Service.objects.filter(userservice__user = user).first()
    		if service:
    			obj.servicio = service
    		#end if
        # end if
        obj.tipo=2
        obj.save()
    	super(BCategoriaAdmin, self).save_model(request, obj, form, change)
    #end def
#end class


admin_site.register(models.PProducto, PProductoAdmin)
admin_site.register(models.PMarca, PMarcaAdmin)
admin_site.register(models.PCategoria, PCategoriaAdmin)
admin_site.register(models.BProducto, BProductoAdmin)
admin_site.register(models.BMarca, BMarcaAdmin)
admin_site.register(models.BCategoria, BCategoriaAdmin)