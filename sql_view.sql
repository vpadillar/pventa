select * from venta_bill as venta 
                  left join venta_order as orden on (venta.id=orden.bill_id and venta.paid=1)
		  left join venta_order_products as pro_orden on (pro_orden.order_id=orden.id)
		  left join venta_itemorder as item on (item.id=pro_orden.itemorder_id)
		  left join venta_product as producto on (producto.id=item.product_id) group by venta.id, producto.name
		  
select strftime('%m',`"date"`) from venta_bill as venta
select date(date)` from venta_bill as venta
select *  from venta_bill as venta
 SELECT strftime('%s','now');
 select  when length(__u.first_namecase)==0 or  __u.first_namecase is null  then 'operario' else __u.first_namecase end||' '||__u.last_name,case when length(__u.last_name)==0 or  __u.last_name is null  then 0 else 1 end  from auth_user as __u
 select * from operacion_orden where id=6
 select * from operacion_servicio where orden_id =6
 update operacion_servicio set fin=null,inicio=null,estado=0 where id  != 17
 
 SELECT date('2016-11-10');
 
 (select * from operacion_orden as orden left join operacion_servicio as ser on (orden.id=ser.orden_id)
 select * from operacion_tiposervicio as tip_ser left join operacion_servicio as ser on (tip_ser.id=ser.tipo_id)
 
 select  *  from operacion_orden as orden  cross join operacion_tiposervicio as tip_ser 
		  left join operacion_servicio as ser on (orden.id=ser.orden_id and tip_ser.id=ser.tipo_id and ser.status=1) 

 select  *  from operacion_orden as orden  cross join operacion_tiposervicio as tip_ser 
		  left join operacion_servicio as ser on (orden.id=ser.orden_id and tip_ser.id=ser.tipo_id and ser.status=1)  where orden.id = 4
		  
		  select nombre from operacion_tiposervicio order by id asc;
select nombre from operacion_tiposervicio order by id asc		  
 select  tip_ser.id, tip_ser.nombre,case when ser.estado is null or ser.estado=0 then 0 else 1 end as estado ,case when ser.inicio is null then '----/--/--' else ser.inicio end as inicio,case when ser.fin is null then '----/--/--' else ser.fin end as fin  from operacion_orden as orden  cross join operacion_tiposervicio as tip_ser 
		  left join operacion_servicio as ser on (orden.id=ser.orden_id and tip_ser.id=ser.tipo_id and ser.status=1)  where orden.id != 0 and orden.entrada  between  date('2016-10-01') and  date('2016-10-11')  order by tip_ser.id asc 
2016-10-06 22:47:13.587653

select * from operacion_orden 
select * from operacion_servicio		  
select date('2016-10-08 00:00:00')
		  left join empleados_empleado as emp on(ser.operario_id
		  )where orden.id = 4
select * from 
update auth_user set password='pbkdf2_sha256$30000$HOleig7wSmXQ$E2bOUO1BEGlMZfm0PnO0sqM9jkprAtLi87MClQPonqM=' where id=2
select * from auth_user


select * from venta_category as categoria 
	        left join venta_product as producto on (producto.category_id=categoria.id)
		left join venta_itemorder as item_orden on (item_orden.product_id=producto.id)
		left join venta_order_products as orden_producto on (orden_producto.itemorder_id=item_orden.id)
		left join venta_order as orden on(orden.id=orden_producto.order_id)
		left join venta_bill as factura on (factura.id = orden.bill_id)