from django.shortcuts import render
from supra import views as supra
import models

class PProductoListView(supra.SupraListView):
	model = models.PProducto
	list_filter = ['pk', 'producto__id']
# end class

class PMarcaListView(supra.SupraListView):
	model = models.PMarca
	list_filter = ['pk', 'marca__id']
# end class

class PCategoriaListView(supra.SupraListView):
	model = models.PCategoria
	list_filter = ['pk', 'categoria__id']
# end class

class BProductoListView(supra.SupraListView):
	model = models.BProducto
	list_filter = ['pk', 'producto__id']
# end class

class BMarcaListView(supra.SupraListView):
	model = models.BMarca
	list_filter = ['pk', 'marca__id']
# end class

class BCategoriaListView(supra.SupraListView):
	model = models.BCategoria
	list_filter = ['pk', 'categoria__id']
# end class
