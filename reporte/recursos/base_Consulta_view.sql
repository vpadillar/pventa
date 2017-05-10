CREATE VIEW base_consultas as select categoria.id as categoria_id,categoria.name as categoria_nombre,producto.id as producto_id,
		producto.name as producto_nombre, producto.price as producto_precio, itempro.count as cantidad,
		venta."date" as fecha, venta.canceled as cancelado,venta.paid as pagado,factura."date" as fecha_factura,
		case when mesero.first_name is not null then mesero.first_name||' '||mesero.last_name else '  --- ' end as mesero_,
		case when cajero.first_name is not null then cajero.first_name||' '||cajero.last_name else ' ---  ' end as cajero_
		from venta_category as categoria
	        left join venta_product as producto on (producto.category_id=categoria.id)
		left join venta_itemorder as itempro on (producto.id=itempro.product_id)
		left join venta_order as venta on (venta.id=itempro.order_id)
		left join venta_bill as factura on (factura.id=venta.bill_id)
		left join auth_user as mesero on (mesero.id=venta.waiter_id)
		left join auth_user as cajero on (cajero.id=venta.casher_id)
