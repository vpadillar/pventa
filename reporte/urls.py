from django.conf.urls import url
import views


urlpatterns = [
    url(r'^get/reporte/$', views.Reporte.as_view(), name='reporte_producto'),
    url(r'^get/reporte/mensual/$', views.ReporteMensual.as_view(), name='reporte_producto_mensual'),
    url(r'^get/reporte/meses/$', views.ExcelMensual.as_view(), name='reporte_producto_mes'),
    url(r'^get/reporte/dia/$', views.ExcelReporteDia.as_view(), name='reporte_producto_dia'),
]
