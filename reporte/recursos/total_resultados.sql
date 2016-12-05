create view informes_total as select * from (select * from years cross join
						(select mes.id as id_mes,mes.nombre as nom_mes,dia.id as dia_mes
							       from mes cross join dia order by mes.id asc, dia.id asc) as fer
										   order by years.year_ asc,fer.id_mes asc,fer.dia_mes asc) as fecha
                 cross join venta_product as pro
		 left join base_consultas as b on
	         (pro.id=b.producto_id and b.fecha is not null and b.cancelado=0 and b.pagado=1 and b.fecha_factura is not null
		     and cast(strftime('%m',b.fecha) as int)=fecha.id_mes and cast(strftime('%Y',b.fecha) as int)=fecha.year_ and cast(strftime('%d',b.fecha) as int)=fecha.dia_mes)
