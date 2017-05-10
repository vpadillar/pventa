create view informes as select * from venta_category as categoria
	        left join venta_product as producto on (producto.category_id=categoria.id)
		left join venta_itemorder as item_orden on (item_orden.product_id=producto.id)
		left join venta_order_products as orden_producto on (orden_producto.itemorder_id=item_orden.id)
		left join venta_order as orden on(orden.id=orden_producto.order_id)
		left join venta_bill as factura on (factura.id = orden.bill_id)
