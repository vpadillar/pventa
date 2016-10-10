from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group

class PVentaAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'Administracion del Punto de Venta'

    # Text to put in each page's <h1>.
    site_header = 'Punto de Venta'

    # Text to put at the top of the admin index page.
    index_title = 'Administra tu Punto de Venta'

    # Path to a custom template that will be used by the admin site app index view.
    #index_template  = 'pventa/base_template.html'
    #app_index_template  = 'dd'
    #base_template = ""
#end def

admin_site = PVentaAdminSite()
admin_site._registry = admin.site._registry
#admin_site.register(User)
#admin_site.register(Group)