from __future__ import unicode_literals

from django.db import models

# Create your models here.


class InformeCategoria(models.Model):
    nombre = models.CharField(null=True, blank=True, max_length=100)
    descripcion = models.CharField(null=True, blank=True, max_length=2000)
    inicio = models.DateField()
    fin = models.DateField()

    def __unicode__(self):
        return '%s'%(self.nombre if self.nombre else 'Informe %d'%self.pk)
    # end def

    def __str__(self):
        return '%s'%(self.nombre if self.nombre else 'Informe %d'%self.pk)
    # end def
