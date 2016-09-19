
from django.conf.urls import url, include
import views 

urlpatterns = [
    url(r'^ws/aviable/tables/(?P<order>\d+)/$', views.aviable_tables),
]
