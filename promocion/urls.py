from django.conf.urls import include, url
import views

urlpatterns = [
	url(r'^ws/pproducto/$', views.PProductoListView.as_view()),
	url(r'^ws/pmarca/$', views.PMarcaListView.as_view()),
	url(r'^ws/pcategoria/$', views.PCategoriaListView.as_view()),
	url(r'^ws/bproducto/$', views.BProductoListView.as_view()),
	url(r'^ws/bmarca/$', views.BMarcaListView.as_view()),
	url(r'^ws/bcategoria/$', views.BCategoriaListView.as_view()),
]