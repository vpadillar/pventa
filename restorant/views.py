from supra import views as supra
import models

class TablesListView(supra.SupraListView):
	model = models.Table
	list_filter = ['aviable']
	list_display = ['name', 'aviable', 'id', 'order_id']

	def get_queryset(self):
		queryset = super(TablesListView, self).get_queryset()
		queryset=queryset.extra(select={'order_id': 'select o.id from venta_order as o join restorant_settable as s on s.order_id = o.id and s.table_id = restorant_table.id'})
		return queryset
	# end def
# end class


class SetTableFormView(supra.SupraFormView):
	model = models.SetTable
	body = True
# end class

class SetTableListView(supra.SupraListView):
	model = models.SetTable
	list_filter = ['order']
# end class
