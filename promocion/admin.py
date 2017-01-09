from django.contrib import admin
from pventa.admin import admin_site
import models
# Register your models here.


class PProductoAdmin(admin.ModelAdmin):
    filter_horizontal = ('producto',)
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
