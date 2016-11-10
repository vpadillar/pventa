from django.contrib import admin
import models
from django.utils.html import format_html

# Register your models here.


class ReporteProductoAdmin(admin.ModelAdmin):
    list_display = ['id_reporte', 'nombre', 'inicio', 'fin', 'accion_reporte']
    search_fields = ['id    ', 'nombre', 'inicio', 'fin']
    list_display_links = ('id_reporte',)

    def id_reporte(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, obj.pk)
    # end def

    class Media:
        js = ('/static/reporte/js/jquery-3.1.1.js', '/static/reporte/js/reporte.js',)
    # end class

    def accion_reporte(self, obj):
        return format_html("<a href='{0}' class='generar addlink'>Imprimir</a>", obj.id)
    # end def
    id_reporte.allow_tags = True
    id_reporte.short_description = 'Reporte Id'
    accion_reporte.allow_tags = True
    accion_reporte.short_description = 'Generar'
# end class
admin.site.register(models.ReporteProducto, ReporteProductoAdmin)
