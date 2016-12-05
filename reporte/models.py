from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ReporteProducto(models.Model):
    nombre = models.CharField(null=True, blank=True, max_length=100)
    inicio = models.DateField()
    fin = models.DateField()
    tipo = models.IntegerField(
        choices=[(1, 'Diaria'), (2, 'Semana'), (3, 'Mensual'), (4, 'Anual')])

    def __unicode__(self):
        i = 0
        men = ''
        while i < 10 - len(str(self.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, self.pk)
    # end def

    def __str__(self):
        i = 0
        men = ''
        while i < 10 - len(str(self.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, self.pk)
    # end def

    class Meta:
        verbose_name = "Reporte Producto"
        verbose_name_plural = "Reporte Productos"
    # end class
# end class
