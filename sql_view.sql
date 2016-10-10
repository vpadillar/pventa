select * from venta_bill as venta 
                  left join venta_order as orden on (venta.id=orden.bill_id and venta.paid=1)
		  left join venta_order_products as pro_orden on (pro_orden.order_id=orden.id)
		  left join venta_itemorder as item on (item.id=pro_orden.itemorder_id)
		  left join venta_product as producto on (producto.id=item.product_id) group by venta.id, producto.name
		  
select strftime('%m',`"date"`) from venta_bill as venta
select date(date)` from venta_bill as venta
select *  from venta_bill as venta
 SELECT strftime('%s','now');