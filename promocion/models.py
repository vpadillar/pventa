# -*- coding: utf-8 -*-
from django.db import models
from venta import models as venta

# Create your models here.


class Oferta(models.Model):
    servicio = models.ForeignKey(venta.Service)
    codigo = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.IntegerField(choices=((1,'Descuento'),(2,'Monto')))
    descripcion = models.CharField(max_length=400, blank=True, null=True, verbose_name='Descripción')
    inicio = models.DateField()
    fin = models.DateField()
    estado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.pk
    # end def

    def __str__(self):
        return self.pk
    # end def

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
    # end class
# end class

class Promocion(Oferta):
    nombre = models.CharField(max_length=400)
    valor = models.FloatField()

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
    # end class
# end class


class PProducto(Promocion):
    producto = models.ManyToManyField(venta.Product)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Promoción de Producto"
        verbose_name_plural = "Promociones de productos"
    # end class
# end class


class PMarca(Promocion):
    marcas = models.ManyToManyField(venta.Brand)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Promoción de Marca"
        verbose_name_plural = "Promociones de Marcas"
    # end class
# end class


class PCategoria(Promocion):
    categorias = models.ManyToManyField(venta.Category)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Promoción de Categoría"
        verbose_name_plural = "Promocines de Categorias"
    # end class
# end class


class Bono(Oferta):
    valor = models.FloatField()

    def __unicode__(self):
        return self.pk
    # end def

    def __str__(self):
        return self.pk
    # end def

    class Meta:
        verbose_name = "Bono"
        verbose_name_plural = "Bonos"
    # end class
# end class

class BProducto(Promocion):
    producto = models.ManyToManyField(venta.Product)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Bono de Producto"
        verbose_name_plural = "Bonos de Productos"
    # end class
# end class


class BMarca(Promocion):
    marcas = models.ManyToManyField(venta.Brand)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Bono Marca"
        verbose_name_plural = "Bonos de Marcas"
    # end class
# end class


class BCategoria(Promocion):
    categorias = models.ManyToManyField(venta.Category)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Bono Categoria"
        verbose_name_plural = "Bonos Categorias"
    # end class
# end class
