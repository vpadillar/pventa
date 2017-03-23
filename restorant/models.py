#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from cuser.middleware import CuserMiddleware
from venta import models as venta

class Supply(models.Model):
	METHODS = (
		(True, 'PEPS'),
		(False, 'UEPS')
	)
	service = models.ForeignKey(venta.Service, verbose_name="Servicio")
	name = models.CharField(max_length=45, verbose_name="Nombre")
	stock = models.FloatField(null=True, blank=True)
	minimun_stock = models.FloatField(verbose_name="stock mínimo", null=True, blank=True)
	stock_refill = models.FloatField(verbose_name="stock de relleno", null=True, blank=True)
	unidad = models.CharField(max_length=10)
	method = models.BooleanField(choices=METHODS, verbose_name="Método", default=True)

	class Meta:
		verbose_name = "Suministro"
		verbose_name_plural = "Suministros"
	#end def

	def get_buy_supply(self):
		if self.method: #PEPS
			return BuySupply.objects.filter(supply = self, current_count__gt = 0).last()
		else:#UEPS
			return BuySupply.objects.filter(supply = self, current_count__gt = 0).first()
		#end if
	#end def

	def __unicode__(self):
		return u"%s" % self.name
	#end def
#end class

class BillBuySupply(models.Model):
	date = models.DateTimeField(auto_now_add = True)
	code = models.CharField(max_length=45, verbose_name="Codigo")

	class Meta:
		verbose_name = "Factura de Compra"
		verbose_name_plural = "Facturas de Compras"
	#end def

	def __unicode__(self):
		return u"%s" % str(self.code)
	#end def

#end class

class BuySupply(models.Model):
	bill = models.ForeignKey(BillBuySupply,verbose_name="codigo Factura")
	supply = models.ForeignKey(Supply, verbose_name="Suministro")
	buy_count = models.IntegerField(verbose_name="Cantidad")
	current_count = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Actual")
	date = models.DateTimeField(auto_now_add = True)

	class Meta:
		verbose_name = "Compra de Suministro"
		verbose_name_plural = "Compra de Suministros"
	#end def

	def __unicode__(self):
		return u"%s" % str(self.supply)
	#end def
#end class


class Consumption(models.Model):
	product = models.ForeignKey(venta.Product, verbose_name="producto")
	supply = models.ForeignKey(BuySupply, verbose_name="suministro")
	consumption = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="consumo")
	order = models.ForeignKey(venta.Order, verbose_name="Orden")
	date = models.DateTimeField(auto_now_add=True, verbose_name="fecha")
	canceled = models.BooleanField(default=False, verbose_name="Cancelado")

	class Meta:
		verbose_name = "Consumo"
		verbose_name_plural = "Consumos"
	#end def

	def save(self):
		obj = super(Consumption, self).save()
		self.supply.current_count = self.supply.current_count - self.consumption
		self.supply.save()
		return obj
	# end def

#end class

class Dish(venta.Product):
	code = models.CharField(max_length=45, verbose_name="Código")
	photo = models.ImageField(upload_to="plates/", verbose_name="Foto")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

	def thumbnail(self, ):
		return u'<img width="100" src="%s" />' % (self.photo.url)
	#end def

	thumbnail.short_description = 'Thumbnail'
	thumbnail.allow_tags = True
	class Meta:
		verbose_name = "Plato"
		verbose_name_plural = "Platos"
	#end def

	def consume(self, order, count):
		cds = ConsumptionDish.objects.filter(dish=self)
		for cd in cds:
			bysupply = BuySupply.objects.filter(supply=cd.supply, current_count__gt = 0).order_by('date')
			if cd.supply.method:#PEPS
				bysupply = bysupply.first()
			else:#UEPS
				bysupply = bysupply.last()
			#edn if
			Consumption(product=self, supply=bysupply, consumption=cd.consumption*count, order=order).save()
		# end for
	# end def

	def __unicode__(self):
		return u"%s" % (self.name, )
	#end def
#end def

class ConsumptionDish(models.Model):
	dish = models.ForeignKey(Dish)
	supply = models.ForeignKey(Supply, verbose_name="suministro")
	consumption = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="consumo")
#end def

class Table(models.Model):
	name = models.CharField(max_length=45, verbose_name="Nombre")
	service = models.ForeignKey(venta.Service, verbose_name="Servicio")
	aviable = models.BooleanField(default=True)
	class Meta:
		verbose_name = "Mesa"
		verbose_name_plural = "Mesas"
	#end def

	def save(self):
		user = CuserMiddleware.get_user()
		service = venta.Service.objects.filter(userservice__user = user).first()
		if service:
			self.service = service
		#end if
		return super(Table, self).save()
	#end def

	def order(self):
		return venta.Order.objects.filter(settable__table=self).first()
	#end def

	def __unicode__(self):
		return u"%s" % self.name
	#end def
#end class

class SetTable(models.Model):
	table = models.ForeignKey(Table, verbose_name="Mesa")
	order = models.OneToOneField(venta.Order, verbose_name="Orden")
	date = models.DateTimeField(auto_now_add=True, verbose_name="fecha")
	class Meta:
		verbose_name = "Asignacion de Mesa"
		verbose_name_plural = "Asignaciones de Mesa"
	#end class

	def __unicode__(self):
		return "La orden %s es para la mesa %s" % (str(self.order), str(self.table))
	#end def
#end class


class SupplyRequest(models.Model):
	date = models.DateTimeField(auto_now_add = True)
	service = models.ForeignKey(venta.Service, verbose_name="Servicio")
	class Meta:
		verbose_name = "Pedido de Suministro"
		verbose_name_plural = "Pedidos de Suministros"
	#end class

	def __unicode__(self):
		items = ItemRequest.objects.filter(supplyrequest=self)
		message = str(items.first())
		count = items.count()
		if count > 1:
			message = message + " y " + str(count - 1) + " pedido(s)"
		#end if
		return "%s %s" % (str(self.date.strftime("%d/%m/%Y")), message)
	#end def
#end class


class ItemRequest(models.Model):
	supplyrequest = models.ForeignKey(SupplyRequest, verbose_name="Petición de suministro")
	supply = models.ForeignKey(Supply, verbose_name="suministro")
	count = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")

	class Meta:
		verbose_name = "Item de pedido"
		verbose_name_plural = "Items del pedido"
	#end class

	def __unicode__(self):
		return "%s x%s" % (str(self.supply), str(self.count))
	#end def
#end class
