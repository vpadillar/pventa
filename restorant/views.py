from supra import views as supra
import models
import forms
from cuser.middleware import CuserMiddleware

class TablesListView(supra.SupraListView):
	model = models.Table
	list_filter = ['aviable']
	list_display = ['name', 'aviable', 'id', 'order_id']

	def get_queryset(self):
		queryset = super(TablesListView, self).get_queryset()
		user = CuserMiddleware.get_user()
		queryset=queryset.filter(service__userservice__user = user).extra(select={'order_id': 'select o.id from venta_order as o join restorant_settable as s on s.order_id = o.id and s.table_id = restorant_table.id'})
		return queryset
	# end def
# end class

class SetTableFormView(supra.SupraFormView):
	model = models.SetTable
	form_class = forms.SetTableForm
	body = True
# end class

class SetTableListView(supra.SupraListView):
	model = models.SetTable
	list_filter = ['order']
# end class
