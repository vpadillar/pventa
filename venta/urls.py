
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
    #supra
    url(r'^ws/bill/(?P<pk>\d+)/$', views.BillDetailView.as_view()),
    url(r'^ws/form/bill/$', views.BillFormView.as_view()),
    url(r'^ws/groups/$', views.GroupListView.as_view()),
    url(r'^ws/clients/$', views.ClientListView.as_view()),
    url(r'^ws/categorys/$', views.CategoyListView.as_view()),
    url(r'^ws/orders/$', views.OrderListView.as_view()),
    url(r'^ws/itemorders/$', views.ItemOrderListView.as_view()),
    url(r'^ws/order/(?P<pk>\d+)/$', views.OrderDetailView.as_view()),
    url(r'^ws/del/order/(?P<pk>\d+)/$', views.OrderDeleteView.as_view()),
    url(r'^ws/form/orders/$', views.OrderFormView.as_view()),
    url(r'^ws/form/orders/(?P<pk>\d+)/$', views.OrderFormView.as_view()),
    url(r'^ws/products/$', views.ProductListView.as_view()),
    url(r'^ws/login/$', views.Login.as_view()),
    url(r'^ws/login/impresora/$', views.LoginImpresora.as_view()),
]
