# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from cuser.middleware import CuserMiddleware
from django.db import models
import humanize
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Sum


class Config(models.Model):
	name = models.CharField(max_length=45)
	ipoconsumo = models.FloatField(default=0)
	iva = models.FloatField(default=0)
	propina = models.FloatField(default=0)
	impresora = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Configuracion"
		verbose_name_plural = "Tu configuracion"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class Service(models.Model):
	name = models.CharField(max_length=45, unique=True, verbose_name="Nombre")
	code = models.CharField(max_length=45, unique=True, db_index=True, verbose_name="Codigo")
	printer = models.CharField(max_length=100)
	moviles = models.TextField()
	configuracion = models.ForeignKey(Config)

	class Meta:
		verbose_name = "Servicio"
		verbose_name_plural = "Servicios"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class UserService(models.Model):
	user = models.OneToOneField(User, verbose_name="Usuario")
	service = models.ForeignKey(Service, verbose_name="Servicio")

	class Meta:
		verbose_name = "Usuario a Servicio"
		verbose_name_plural = "Usuarios a Servicio"
	#end class

	def __unicode__(self):
		return "%s pertenece a %s" % (str(self.user), str(self.service))
	#end def
#end class

class Image(models.Model):
	service = models.ForeignKey(Service, verbose_name="Servicio")
	name = models.CharField(max_length=45, verbose_name="Nombre")
	url = models.ImageField(upload_to="category_images/", verbose_name="Ruta de la imagen")

	class Meta:
		verbose_name = "Imagen"
		verbose_name_plural = "Imagenes"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class Category(models.Model):
	name = models.CharField(max_length=45, verbose_name="Nombre")
	service = models.ForeignKey(Service, verbose_name="Servicio")
	image = models.ForeignKey(Image, null=True, blank=True, verbose_name="Imagen")

	class Meta:
		verbose_name = "Categoria"
		verbose_name_plural = "Categorias"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class Presentation(models.Model):
	name = models.CharField(max_length=45, verbose_name="Nombre")
	service = models.ForeignKey(Service, verbose_name="Servicio")

	def save(self):
		user = CuserMiddleware.get_user()
		service = Service.objects.filter(userservice__user = user).first()
		if service:
			self.service = service
		#end if
		return super(Presentation, self).save()
	#end def

	class Meta:
		verbose_name = "Presentación"
		verbose_name_plural = "Presentaciones"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class Cellar(models.Model):
	name = models.CharField(max_length=45, verbose_name="Nombre")
	service = models.ForeignKey(Service, verbose_name="Servicio")

	class Meta:
		verbose_name = "Bodega"
		verbose_name_plural = "Bodegas"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class Provider(models.Model):
	name = models.CharField(max_length=45, unique=True, verbose_name="Nombre")
	service = models.ForeignKey(Service, verbose_name="Servicio")

	class Meta:
		verbose_name = "Proveedor"
		verbose_name_plural = "Proveedores"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class


class Brand(models.Model):
	service = models.ForeignKey(Service)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=800)
	state = models.BooleanField(default=True)

	def  __unicode__(self):
		return u'%s'%self.name
	# end class

	def  __str__(self):
		return u'%s'%self.name
	# end class

	class Meta:
		verbose_name = "Marca"
		verbose_name_plural = "Marcas"
	# end class

# en class

class Product(models.Model):
	METHODS = (
		(True, 'PEPS'),
		(False, 'UEPS')
	)
	category = models.ForeignKey(Category, verbose_name="Categoría")
	brand = models.ForeignKey(Brand, verbose_name="Marca")
	presentation = models.ForeignKey(Presentation, null=True, verbose_name="Presentación")
	name = models.CharField(max_length=45, verbose_name="Nombre")
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
	method = models.BooleanField(choices=METHODS, verbose_name="Método", default=True)

	def total(self):
		total = BuyPoduct.objects.filter(buypresentation__product = self).aggregate(total = Sum('current_count'))['total']
		return total or 0
	#end def

	class Meta:
		verbose_name = "Producto"
		verbose_name_plural = "Productos"
	#end class

	def get_buy_product(self):
		if self.method: #PEPS
			return BuyPoduct.objects.filter(buypresentation__product = self, current_count__gt = 0).last()
		else:#UEPS
			return BuyPoduct.objects.filter(buypresentation__product = self, current_count__gt = 0).first()
		#end if
	#end def

	def __unicode__(self):
		return self.name
	#end def

	def sell(self, count):
		print "sell", count, self.name, hasattr(self, 'dish')
		if not hasattr(self, 'dish'):
			bought = BuyPoduct.objects.filter(buypresentation__product = self, current_count__gt = 0).first()
			if bought:
				Sell(bought=bought, count=count).save()
			else:
				return False
			# end if
		# end if
		return True
	#end def
#end class

class BuyPresentation(models.Model):
	name = models.CharField(max_length=45, verbose_name="Nombre")
	product = models.ForeignKey(Product, verbose_name="Producto")
	count = models.IntegerField(verbose_name="Cantidad")
	cellar = models.ForeignKey(Cellar, verbose_name="Bodega")
	provider = models.ForeignKey(Provider, verbose_name="Proveedor")

	class Meta:
		verbose_name = "Presentación de Compra"
		verbose_name_plural = "Presentaciones de Compra"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class BuyPoduct(models.Model):
	code = models.CharField(max_length=45, verbose_name="Código")
	buypresentation = models.ForeignKey(BuyPresentation, verbose_name="Producto")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
	current_count = models.IntegerField(verbose_name="Cantidad")

	class Meta:
		verbose_name = "Compra de Producto"
		verbose_name_plural = "Compras de Productos"
	#end class

	def __unicode__(self):
		return "%s x%s (%s %s)" % (str(self.code), str(self.current_count), self.date.strftime("%d/%m/%Y"), str(self.buypresentation))
	#end def
#end class

class Sell(models.Model):
	bought = models.ForeignKey(BuyPoduct, verbose_name="Producto")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
	count = models.IntegerField(verbose_name="Cantidad")

	class Meta:
		verbose_name = "Venta"
		verbose_name_plural = "Ventas"
	#end class

	def __unicode__(self)	:
		return "%s -%s" % (str(self.bought), str(self.count))
	#end def
#end class

class Client(models.Model):
	service = models.ForeignKey(Service, verbose_name="Servicio")
	cc = models.IntegerField(verbose_name="Numero de cédula")
	name = models.CharField(max_length=45, verbose_name="Nombre")
	email = models.EmailField(default="", verbose_name="Correo")
	tel = models.CharField(max_length=20, verbose_name="Teléfono")

	class Meta:
		verbose_name = "Cliente"
		verbose_name_plural = "Clientes"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class

class Bill(models.Model):
	service = models.ForeignKey(Service, verbose_name="Servicio")
	products = models.TextField(verbose_name="Productos")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
	cash = models.CharField(max_length=45, verbose_name="Efectivo")
	check = models.CharField(max_length=45, default="0", verbose_name="Cheque")
	card = models.CharField(max_length=45, default="0", verbose_name="Tarjeta")
	disscount = models.CharField(max_length=45, default="0", verbose_name="Descuento")
	paid = models.BooleanField(default=True, verbose_name="Pagado")
	cc = models.CharField(max_length=45, default="", verbose_name="Numero de cédula")
	name = models.CharField(max_length=45, default="", verbose_name="Nombre")
	tel = models.CharField(max_length=45, default="", verbose_name="Teléfono")
	subtotal  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sub Total")
	iva  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IVA")
	ipoconsumo  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IpoConsumo")
	total  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
	casher = models.CharField(max_length=45, verbose_name="Cajero")
	waiter = models.CharField(max_length=45, verbose_name="Mesero")
	tip = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Propina")
	totaltip = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total + Propina")
	class Meta:
		verbose_name = "Factura"
		verbose_name_plural = "Facturas"
	#end class

	def __unicode__(self):
		return self.name
	#end def
#end class


class Order(models.Model):
	service = models.ForeignKey(Service, verbose_name="Servicio")
	client = models.ForeignKey(Client, null=True, blank=True, verbose_name="Cliente")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
	bill = models.OneToOneField(Bill, null=True, blank=True, verbose_name="Factura")
	canceled = models.BooleanField(default=False, verbose_name="Cancelado")
	paid = models.BooleanField(default=False, verbose_name="Pagado")
	casher = models.ForeignKey(User, verbose_name="Cajero", related_name="casher", null=True, blank=True)
	waiter = models.ForeignKey(User, verbose_name="Mesero", related_name="waiter")

	class Meta:
		verbose_name = "Orden"
		verbose_name_plural = "Ordenes"
	#end class

	def __unicode__(self):
		return u"Orden del cliente: %s" % (str(self.client),)
	#end def

	def total(self):
		total = 0
		for p in self.products.all():
			total = total + p.product.price * p.count
		#end for
		return total
	#end def

	def frienly_date(self):
		months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
		if self.date.day <= 9:
			cero = "0"
		else:
			cero = ""
		#end if
		return "%s%s-%s-%s" % (cero, str(self.date.day), (months[self.date.month]), str(self.date.year))
	#end def

	def save(self):
		obj = super(Order, self).save()
		items = ItemOrder.objects.filter(order=self)
		print items
		for item in items:
			if hasattr(item.product, 'dish'):
				item.product.dish.consume(self, item.count)
			# end if
		# end for
		return obj
	# end def
#end class


class ItemOrder(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product, verbose_name="Producto")
	count = models.IntegerField(verbose_name="Cantidad")

	class Meta:
		verbose_name = "Item de Orden"
		verbose_name_plural = "Items de Orden"
	#end class

	def __unicode__(self):
		return "%s x%s" % (str(self.product), str(self.count))
	#end def
#end class

class ProductRequest(models.Model):
	service = models.ForeignKey(Service, verbose_name="Servicio")
	date = models.DateTimeField(auto_now_add = True)
	class Meta:
		verbose_name = "Pedido de producto"
		verbose_name_plural = "Pedidos de productos"
	#end class

	def __unicode__(self):
		items = ItemRequest.objects.filter(productrequest=self)
		message = str(items.first())
		count = items.count()
		if count > 1:
			message = message + " y " + str(count - 1) + " pedido(s) más"
		#end if
		return "%s %s" % (str(self.date.strftime("%d/%m/%Y")), message)
	#end def
#end class

class ItemRequest(models.Model):
	productrequest = models.ForeignKey(ProductRequest, verbose_name="Petición de producto")
	product = models.ForeignKey(BuyPresentation, verbose_name="Producto")
	count = models.IntegerField(verbose_name="Cantidad")

	class Meta:
		verbose_name = "Item de pedido"
		verbose_name_plural = "Items del pedido"
	#end class

	def __unicode__(self):
		return "%s x%s" % (str(self.product), str(self.count))
	#end def
#end class

class Cashier(User):

	service = models.ForeignKey(Service, verbose_name="Servicio")

	class Meta:
		verbose_name = "Cajero"
		verbose_name_plural = "Cajeros"
	#end class

	def __unicode__(self):
		return self.name
	#end def

#end class
