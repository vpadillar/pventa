#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from datetime import date, timedelta, datetime
from django.views.generic import View
from django.db import connection
import csv
import models
from datetime import date
# Create your views here.


class Reporte(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(Reporte, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', 0)
        orden = models.ReporteProducto.objects.filter(id=id).first()
        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename="Reporte Empleados.csv"'
        writer = csv.writer(response)
        writer.writerow(['Express del norte'.encode('utf-8')])
        lista = list()
        if orden:
            writer.writerow(['Fecha de inicio para el reporte'.encode('utf-8'), str(orden.inicio).encode('utf-8')])
            writer.writerow(['Fecha de fin para el reporte'.encode('utf-8'), str(orden.fin).encode('utf-8')])
            if orden.tipo == 3:
                writer.writerow(['Reporte Mensual'.encode('utf-8')])
                lista.append(u'Año'.encode('utf-8'))
                lista.append(u'Mes'.encode('utf-8'))
                lista.append(u'Producto'.encode('utf-8'))
                lista.append(u'cantidad'.encode('utf-8'))
                lista.append(u'Precio'.encode('utf-8'))
                lista.append(u'Venta'.encode('utf-8'))
                writer.writerow(lista)
                sql = "select * from (select year_,id_mes,nom_mes,name,count(name)  as total,"
                sql = sql + "sum(case when cantidad is null then 0 else cantidad end) as articulos,"
                sql = sql + "sum(case when cantidad is not null and producto_precio is not null then producto_precio*cantidad else 0 end) as venta"
                sql = sql + ",producto_precio from informes_total where date(fecha)>= date('"+str(orden.inicio)+"')  and date(fecha)<= date('"+str(orden.fin)+"')   group by year_,id_mes,nom_mes,name) as t"
                cursor = connection.cursor()
                cursor.execute(sql)
                row = cursor.fetchall()
                r = 0
                while r < len(row):
                    li = list()
                    print row[r]
                    li.append(row[r][0])
                    li.append((row[r][2]).encode('utf-8'))
                    li.append((row[r][3]).encode('utf-8'))
                    li.append(row[r][5])
                    li.append(row[r][7])
                    li.append(row[r][6])
                    writer.writerow(li)
                    r = r + 1
                # end for
                return response
            elif orden.tipo == 4:
                writer.writerow(['Reporte Anual'.encode('utf-8')])
                lista.append(u'Año'.encode('utf-8'))
                lista.append(u'Total articulos'.encode('utf-8'))
                lista.append(u'Cantidad de Productos'.encode('utf-8'))
                lista.append(u'Total Venta'.encode('utf-8'))
                writer.writerow(lista)
                sql = "select * from (select year_,id_mes,nom_mes,name,count(name)  as total,"
                sql = sql + "sum(case when cantidad is null then 0 else cantidad end) as articulos,"
                sql = sql + "sum(case when cantidad is not null and producto_precio is not null then producto_precio*cantidad else 0 end) as venta"
                sql = sql + ",producto_precio from informes_total where date(fecha)>= date('"+str(orden.inicio)+"')  and date(fecha)<= date('"+str(orden.fin)+"')   group by year_) as t"
                cursor = connection.cursor()
                cursor.execute(sql)
                row = cursor.fetchall()
                r = 0
                while r < len(row):
                    li = list()
                    li.append(row[r][0])
                    li.append(row[r][5])
                    li.append(row[r][6])
                    writer.writerow(li)
                    r = r + 1
                # end for
                return response
            elif orden.tipo == 2:
                writer.writerow(['Reporte Semana'.encode('utf-8')])
                lista.append(u'Año'.encode('utf-8'))
                lista.append(u'Mes'.encode('utf-8'))
                lista.append(u'Dia'.encode('utf-8'))
                lista.append(u'Semana'.encode('utf-8'))
                lista.append(u'Producto'.encode('utf-8'))
                lista.append(u'Total articulos'.encode('utf-8'))
                lista.append(u'Valor unitario'.encode('utf-8'))
                lista.append(u'Total Venta'.encode('utf-8'))
                writer.writerow(lista)
                sql = "select * from (select  year_,id_mes,dia_mes,nom_mes,name,count(name)  as total,"
                sql = sql + "sum(case when cantidad is null then 0 else cantidad end) as articulos,"
                sql = sql + "sum(case when cantidad is not null and producto_precio is not null then producto_precio*cantidad else 0 end) as venta,producto_precio,strftime('%W',fecha) as semana,fecha"
                sql = sql + ",producto_precio from informes_total where date(fecha)>= date('"+str(orden.inicio)+"')  and date(fecha)<= date('"+str(orden.fin)+"')   group by year_,id_mes,nom_mes,strftime('%W',fecha)  ,name) as t"
                cursor = connection.cursor()
                cursor.execute(sql)
                row = cursor.fetchall()
                r = 0
                while r < len(row):
                    li = list()
                    li.append(row[r][0])
                    li.append(str(row[r][3]).encode('utf-8'))
                    li.append(row[r][2])
                    li.append(row[r][9])
                    li.append(str(row[r][4]).encode('utf-8'))
                    li.append(row[r][6])
                    li.append(row[r][8])
                    li.append(row[r][7])
                    writer.writerow(li)
                    r = r + 1
                # end for
                return response
            elif orden.tipo == 1:
                writer.writerow(['Reporte Dias'.encode('utf-8')])
                lista.append(u'Año'.encode('utf-8'))
                lista.append(u'Mes'.encode('utf-8'))
                lista.append(u'Dia'.encode('utf-8'))
                lista.append(u'Fecha'.encode('utf-8'))
                lista.append(u'Producto'.encode('utf-8'))
                lista.append(u'Total articulos'.encode('utf-8'))
                lista.append(u'Valor unitario'.encode('utf-8'))
                lista.append(u'Total Venta'.encode('utf-8'))
                writer.writerow(lista)
                sql = "select * from (select  year_,id_mes,dia_mes,nom_mes,name,count(name)  as total,"
                sql = sql + "sum(case when cantidad is null then 0 else cantidad end) as articulos,"
                sql = sql + "sum(case when cantidad is not null and producto_precio is not null then producto_precio*cantidad else 0 end) as venta,producto_precio,strftime('%W',fecha) as semana,date(fecha)"
                sql = sql + ",producto_precio from informes_total where date(fecha)>= date('"+str(orden.inicio)+"')  and date(fecha)<= date('"+str(orden.fin)+"')   group by year_,id_mes,nom_mes,fecha ,name) as t"
                cursor = connection.cursor()
                cursor.execute(sql)
                row = cursor.fetchall()
                r = 0
                while r < len(row):
                    li = list()
                    li.append(row[r][0])
                    li.append(str(row[r][3]).encode('utf-8'))
                    li.append(row[r][2])
                    li.append(row[r][10])
                    li.append(str(row[r][4]).encode('utf-8'))
                    li.append(row[r][6])
                    li.append(row[r][8])
                    li.append(row[r][7])
                    writer.writerow(li)
                    r = r + 1
                # end for
                return response
            # end if
            # end if
        # end for
        return render(request, 'reporte/reporte.html', {})
    # end class
# end class


class ReporteMensual(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(ReporteMensual, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'reporte/reporte.html', {})
    # end class
# end class


class ExcelMensual(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(ExcelMensual, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request):
        print request.GET
        id_emp=request.GET.get('id', '0')
        ini=request.GET.get('ini', '2015-01-01')
        fin=request.GET.get('fin', '%s-%s-%s' %
                              (date.today().year, date.today().month, date.today().day))
        f1=ini.split('-')
        f2=fin.split('-')
        d1='%s-%s-%s' % (f1[2], f1[0], f1[1])
        d2='%s-%s-%s' % (f2[2], f2[0], f2[1])
        estado=request.GET.get('estado', False)
        r=0
        lista=list()
        response=HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition']='attachment; filename="Reporte Empleados.csv"'
        writer=csv.writer(response)
        writer.writerow(['Express del norte'.encode('utf-8')])
        writer.writerow(['Fecha de inicio para el reporte'.encode('utf-8'), d1.encode('utf-8'), ''.encode(
            'utf-8'), ''.encode('utf-8'), 'Fecha de fin para el reporte'.encode('utf-8'), d2.encode('utf-8')])
        lista.append(u'Año'.encode('utf-8'))
        lista.append(u'Mes'.encode('utf-8'))
        lista.append(u'Producto'.encode('utf-8'))
        lista.append(u'Producto'.encode('utf-8'))
        lista.append(u'Vendidos'.encode('utf-8'))
        lista.append(u'Venta'.encode('utf-8'))
        writer.writerow(lista)
        sql='''select * from (select year_,id,nombre,name,count(name)  as total,
            sum(case when cantidad is null then 0 else cantidad end) as articulos,
            sum(case when cantidad is not null and producto_precio is not null then
            producto_precio*cantidad else 0 end) as venta
            from informes_total   group by year_,id,nombre,name) as t
        '''
        cursor=connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        cursor2=connection.cursor()
        r=0
        while r < len(row):
            li=list()
            print row[r]
            li.append(row[r][0])
            li.append((row[r][2]).encode('utf-8'))
            li.append((row[r][3]).encode('utf-8'))
            li.append(row[r][5])
            li.append(row[r][6])
            writer.writerow(li)
            r=r + 1
        # end for
        return response
    # end class
# end class


class ExcelReporteDia(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(ExcelReporteDia, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename="Reporte Empleados.csv"'
        writer = csv.writer(response)
        writer.writerow(['Express del norte'.encode('utf-8')])
        lista = list()
        writer.writerow(['Reporte del Dias'.encode('utf-8')])
        lista.append(u'Año'.encode('utf-8'))
        lista.append(u'Mes'.encode('utf-8'))
        lista.append(u'Dia'.encode('utf-8'))
        lista.append(u'Fecha'.encode('utf-8'))
        lista.append(u'Producto'.encode('utf-8'))
        lista.append(u'Total articulos'.encode('utf-8'))
        lista.append(u'Valor unitario'.encode('utf-8'))
        lista.append(u'Total Venta'.encode('utf-8'))
        writer.writerow(lista)
        d = date.today()
        f = '%d-%d-%d' % (d.year, d.month, d.day)
        sql = "select * from (select  year_,id_mes,dia_mes,nom_mes,name,count(name)  as total,"
        sql = sql + "sum(case when cantidad is null then 0 else cantidad end) as articulos,"
        sql = sql + "sum(case when cantidad is not null and producto_precio is not null then producto_precio*cantidad else 0 end) as venta,producto_precio,strftime('%W',fecha) as semana,date(fecha)"
        sql = sql + ",producto_precio from informes_total where date(fecha)>= date('"+str(f)+"')  and date(fecha)<= date('"+str(f)+"')   group by year_,id_mes,nom_mes,fecha ,name) as t"
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        r = 0
        while r < len(row):
            li = list()
            li.append(row[r][0])
            li.append(str(row[r][3]).encode('utf-8'))
            li.append(row[r][2])
            li.append(row[r][10])
            li.append(str(row[r][4]).encode('utf-8'))
            li.append(row[r][6])
            li.append(row[r][8])
            li.append(row[r][7])
            writer.writerow(li)
            r = r + 1
        # end for
        return response
    # end class
# end class
