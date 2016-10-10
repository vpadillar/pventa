
from django.conf.urls import url, include
import views 

urlpatterns = [
    url(r'^$', views.PvTemplateView.as_view(template_name="venta/index.html")),
    url(r'^ws/nocount/$', views.nocount),
    url(r'^ws/token/$', views.token),
    url(r'^ws/config/$', views.config),
    url(r'^ws/service/$', views.service),
    url(r'^dashboard.html', views.PvTemplateView.as_view(template_name="venta/dashboard.html")),
    url(r'^order_add.html', views.PvTemplateView.as_view(template_name="venta/order_add.html")),
    url(r'^order_list.html', views.PvTemplateView.as_view(template_name="venta/order_list.html")),
    url(r'^pay_list.html', views.PvTemplateView.as_view(template_name="venta/pay_list.html")),
    url(r'^confirm.html', views.PvTemplateView.as_view(template_name="venta/confirm.html")),
    url(r'^category_list.html', views.PvTemplateView.as_view(template_name="venta/category_list.html")),
    url(r'^category_add.html', views.PvTemplateView.as_view(template_name="venta/category_add.html")),
    url(r'^product_list.html', views.PvTemplateView.as_view(template_name="venta/product_list.html")),
    url(r'^product_add.html', views.PvTemplateView.as_view(template_name="venta/product_add.html")),
    url(r'^login/', views.PvTemplateView.as_view(template_name="venta/login.html")),
]
