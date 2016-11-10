
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^ws/tables/$', views.TablesListView.as_view()),
    url(r'^ws/form/settable/$', views.SetTableFormView.as_view()),
    url(r'^ws/form/settable/(?P<pk>\d+)/$', views.SetTableFormView.as_view()),
    url(r'^ws/settable/$', views.SetTableListView.as_view()),
]
