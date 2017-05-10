#!/usr/bin/env python
# -*- coding: utf-8 -*-
import triggers
from reportes import models as reportes
from mantenimiento import models as mantenimiento
from actividades import models as actividades
from usuarios import models as usuarios
from gestion_cartera import models as gestion_cartera
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from connections import HOST, IO_PORT
from django.core.signals import request_finished, got_request_exception
import os
from datetime import datetime
from Piscix.settings import BASE_DIR


class DefaultTrigger(triggers.Trigger):
    exlude = []
    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk])
    # end def

    def get_exclude(self, instance):
        return self.exlude
    # end def

    def create(self, instance):
        super(DefaultTrigger, self).create(instance)
        data = self.get_data(instance)
        send_to = []
        for type_ in self.types:
            send_to.append(type_.__name__)
        # end for
        url = self.get_url(instance)

        obj = {
            "data": data,
            "url": url,
            "html": self.message % data,
            "_send_to_": send_to,
            "exclude": self.get_exclude(instance)
        }

        if self.has_plugin('ioplugin'):
            self.emit_by('save', obj, 'ioplugin')
        # end if

        if self.has_plugin('smtpplugin'):
            emails = []
            for type_ in self.types:
                users = type_.objects.all()
                for user in users:
                    if user.email != '' and not user.email in emails:
                        emails.append(user.email)
                    # end if
                # end for
            # end for
            obj['data']['emails'] = emails
            self.emit_by('create', obj, 'smtpplugin')
        # end if
    # end def
# end class


class ResendTrigger(triggers.Trigger):

    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk])
    # end def

    def update(self, instance):
        super(ResendTrigger, self).update(instance)
        data = self.get_data(instance)
        send_to = []
        for type_ in self.types:
            send_to.append(type_.__name__)
        # end for

        obj = {
            "data": data,
            "url": self.get_url(instance),
            "html": self.message % data,
            "_send_to_": send_to
        }

        if self.has_plugin('smtpplugin') and hasattr(instance, 'resend') and instance.resend:
            emails = []
            for type_ in self.types:
                users = type_.objects.all()
                for user in users:
                    if user.email != '' and not user.email in emails:
                        emails.append(user.email)
                    # end if
                # end for
            # end for
            obj['data']['emails'] = emails
            self.emit_by('create', obj, 'smtpplugin')
        # end if
    # end def
# end class


class UserTrigger(triggers.Trigger):

    def get_type(self, instance):
        return self.type
    # end  def

    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk])
    # end def

    def save(self, instance):
        super(UserTrigger, self).save(instance)
        data = self.get_data(instance)
        url = self.get_url(instance)
        obj = {
            "data": data,
            "url": url,
            "html": self.message % data,
            "webuser": self.get_webuser(instance)
        }

        if self.has_plugin('ioplugin'):
            obj["_send_to_"] = self.get_type(instance).__name__
            self.emit_by('user', obj, 'ioplugin')
        # end if

        with open(os.path.join(BASE_DIR, 'io_plugin.log'), 'a+') as log:
            log.write("%s sended to: %s\n" % (datetime.now(), obj, ))
            log.close()
        # end with

        if self.has_plugin('smtpplugin'):
            emails = []
            for type_ in self.types:
                users = type_.objects.all()
                for user in users:
                    if user.email != '' and not user.email in emails:
                        emails.append(user.email)
                    # end if
                # end for
            # end for
            obj['data']['emails'] = emails
            self.emit_by('save', obj, 'smtpplugin')
        # end if
    # end def
# end class


class CronTrigger(triggers.Trigger):

    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk])
    # end def

    def save(self, instance):
        super(CronTrigger, self).save(instance)
        data = self.get_data(instance)
        send_to = []
        for type_ in self.types:
            send_to.append(type_.__name__)
        # end for
        url = self.get_url(instance)
        obj = {
            "data": data,
            "url": url,
            "cron": self.get_cron(instance),
            "html": self.message % data,
            "class": self.__class__.__name__,
            "owner": str(instance.pk),
            "_send_to_": send_to
        }
        if self.has_plugin('ioplugin'):
            self.emit_by('cron', obj, 'ioplugin')
        # end if
    # end def
# end class


class BirdateTrigger(CronTrigger):
    model = [usuarios.Asistente, usuarios.Piscinero]
    types = [usuarios.Gerente]
    message = u"Hoy es el cumpleaños de %(nombre)s"

    def get_cron(self, instance):
        #       s m  h  d m  s
        return "0 6 11 %s %s *" % (instance.fecha_nacimiento.day, instance.fecha_nacimiento.month)
    # end def

    def get_data(self, instance):
        if instance.imagen:
            url = instance.imagen.url
        else:
            url = None
        # end if
        data = {
            "nombre": "%s %s" % (instance.first_name, instance.last_name),
            "fecha_nacimiento": instance.fecha_nacimiento.strftime("%Y-%m-%d %I:%M%p"),
            "imagen": url,
            "usuario": instance.username,
        }
        return data
    # end def
# end class


class HappyPiscineroTrigger(BirdateTrigger):
    model = usuarios.Piscinero
    types = [usuarios.Piscinero]
    message = u"Feliz cumpleaños %(nombre)s"
# end class


class HappyAsistenteTrigger(BirdateTrigger):
    model = usuarios.Asistente
    types = [usuarios.Asistente]
    message = u"Feliz cumpleaños %(nombre)s"
# end class


class ActividadTrigger(CronTrigger):
    model = actividades.Actividad
    types = [usuarios.Gerente]
    message = u"Hoy debe cumplirse la actividad %(nombre)s"

    def get_cron(self, instance):
        cron = ""
        if "dias[" in instance.repetir_cada:  # diario
            cron = "0 0 12 * * %s" % (
                instance.repetir_cada.replace("dias[", "").replace("]", ""), )
        # end if
        if "mes[" in instance.repetir_cada:  # diario
            cron = "0 0 12 %s * *" % (
                instance.repetir_cada.replace("mes[", "").replace("]", ""), )
        # end if
        if instance.unidad_de_repeticion == 3:  # mensual
            cron = "0 0 7 %%(dia)s */%s *" % (instance.repetir_cada, )
        # end if
        if instance.unidad_de_repeticion == 4:  # anual
            cron = "0 0 7 %s %s/%s *" % ('%(dia)s', '%(mes)s', int(instance.repetir_cada) * 12, )
        # end if
        return cron % {
            'dia': instance.fecha_de_ejecucion.day,
            'mes': instance.fecha_de_ejecucion.month,
            'dia_semana': instance.fecha_de_ejecucion.weekday()
        }
    # end def

    def get_data(self, instance):
        data = {
            "nombre": instance.nombre,
            "fecha_de_ejecucion": instance.fecha_de_ejecucion.strftime("%Y-%m-%d %I:%M%p"),
            "piscina": instance.piscina.nombre,
            "tipo": "Actividad"
        }
        return data
    # end def
# end class


class ReporteTrigger(DefaultTrigger):
    model = reportes.Reporte
    types = [usuarios.Gerente, usuarios.Asistente, usuarios.Supervisor]
    message = u"""El usuario %(usuario)s ha realizado un reporte sobre la piscina %(piscina)s"""

    def get_data(self, instance):
        data = {
            "nombre": instance.nombre,
            "descripcion": instance.descripcion,
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "piscina": instance.piscina.nombre,
            "usuario": instance.usuario.username,
            "cliente_id": instance.piscina.casa.cliente.pk,
            "cliente": "%s %s" % (instance.piscina.casa.cliente.first_name, instance.piscina.casa.cliente.last_name),
            "reporte_id": instance.pk,
            'gps': "%s,%s" % (instance.piscina.casa.latitud, instance.piscina.casa.longitud),
            'tipo': 'Reporte',
            "exlude": instance.usuario.email,
            "tipo_n": instance.tipo_de_reporte.nombre,
            "cierre": instance.tipo_de_reporte.tipo_de_cierre,
            "estado": instance.estado
        }
        return data
    # end def
# end class


class ReporteResendTrigger(ResendTrigger):
    model = reportes.Reporte
    types = []
    message = u"""El usuario %(usuario)s ha realizado un reporte"""

    def get_data(self, instance):
        data = {
            "nombre": instance.nombre,
            "descripcion": instance.descripcion,
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "piscina": instance.piscina.nombre,
            "usuario": instance.usuario.username,
            "cliente_id": instance.piscina.casa.cliente.pk,
            "cliente": "%s %s" % (instance.piscina.casa.cliente.first_name, instance.piscina.casa.cliente.last_name),
            "reporte_id": instance.pk,
            'gps': "%s,%s" % (instance.piscina.casa.latitud, instance.piscina.casa.longitud),
            'tipo': 'Reporte',
            "include": instance.piscina.casa.cliente.email
        }
        return data
    # end def
# end class


class RespuestaTrigger(DefaultTrigger):
    model = reportes.Respuesta
    types = [usuarios.Gerente, usuarios.Asistente, usuarios.Supervisor]
    message = u"""El usuario %(usuario)s ha respondido"""

    def get_exclude(self, instance):
        print "exclude:", instance
        return [instance.usuario.username]
    # end def

    def get_data(self, instance):
        data = {
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "usuario": instance.usuario.username,
            "reporte_id": instance.reporte.pk,
            "tipo": "Respuesta",
            "nombre": "Respuesta",
            "include": instance.reporte.usuario.email,
            "exclude": instance.usuario.email,
            "mensaje": instance.mensaje
        }
        return data
    # end def

    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance.reporte._meta.app_label,  instance.reporte._meta.model_name),  args=[instance.reporte.pk])
    # end def
# end class


class RespuestaUTrigger(UserTrigger):
    model = reportes.Respuesta
    type = usuarios.Piscinero
    message = u"""El usuario %(usuario)s ha respondido"""

    def get_webuser(self, instance):
        piscineros = usuarios.Piscinero.objects.filter(asignacionpiscinero__piscina = instance.reporte.piscina)
        lista = []
        for piscinero in piscineros:
            if piscinero.pk != instance.usuario.pk:
                lista.append(piscinero.username)
            # end if
        # end for
        return lista
    # end def

    def get_data(self, instance):
        data = {
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "usuario": instance.usuario.username,
            "reporte_id": instance.reporte.pk,
            "tipo": "Respuesta",
            "nombre": "Respuesta",
            "include": instance.reporte.usuario.email,
            "exclude": instance.usuario.email,
            "mensaje": instance.mensaje
        }
        return data
    # end def

    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance.reporte._meta.app_label,  instance.reporte._meta.model_name),  args=[instance.reporte.pk])
    # end def
# end class


class RecordatorioTrigger(DefaultTrigger):
    model = reportes.Recordatorio
    types = [usuarios.Gerente, usuarios.Asistente]
    message = u"""El usuario %(usuario)s ha recordado un Reporte"""

    def get_data(self, instance):
        data = {
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "usuario": instance.usuario.username,
            "tipo": "Recordatorio",
            "reporte_id": instance.reporte.pk,
            'tipo': 'Recordatorio',
            'nombre': 'Recordatorio',
            'include': instance.reporte.usuario.email,
            'exclude': instance.usuario.email
        }
        return data
    # end def

    def get_url(self, instance):
        return reverse('admin:%s_%s_change' % (instance.reporte._meta.app_label,  instance.reporte._meta.model_name),  args=[instance.reporte.pk])
    # end def
# end class


class SolucionTrigger(DefaultTrigger):
    model = mantenimiento.Solucion
    types = [usuarios.Gerente, usuarios.Asistente, usuarios.Supervisor]
    message = u"""El usuario %(emisor)s ha solucionado un reporte"""

    def get_data(self, instance):
        # end if
        data = {
            "nombre": instance.nombre,
            "descripcion": instance.descripcion,
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "reporte": instance.reporte.nombre,
            "emisor": instance.emisor.username,
            "reporte_id": instance.reporte.id,
            "cliente_id": instance.reporte.piscina.casa.cliente.pk,
            "solucion_id": instance.pk,
            "tipo": "Solucion",
            "exclude": instance.emisor.email,
            "cliente": "%s %s" % (instance.reporte.piscina.casa.cliente.first_name, instance.reporte.piscina.casa.cliente.last_name),
        }
        return data
    # end def
# end class


class SolucionResendTrigger(ResendTrigger):
    model = mantenimiento.Solucion
    types = []
    message = u"""El usuario %(emisor)s ha solucionado de un reporte"""

    def get_data(self, instance):
        data = {
            "nombre": instance.nombre,
            "descripcion": instance.descripcion,
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "reporte": instance.reporte.nombre,
            "emisor": instance.emisor.username,
            "reporte_id": instance.reporte.id,
            "cliente_id": instance.reporte.piscina.casa.cliente.pk,
            "solucion_id": instance.pk,
            "tipo": "Solucion",
            "include": instance.reporte.piscina.casa.cliente.email
        }
        return data
    # end def
# end class


class ReporteInformativoTrigger(DefaultTrigger):
    model = reportes.ReporteInformativo
    types = [usuarios.Gerente, usuarios.Asistente, usuarios.Supervisor]
    message = u"""El usuario %(emisor)s ha realizado un reporte informativo"""

    def get_data(self, instance):
        data = {
            "nombre": instance.nombre,
            "descripcion": instance.descripcion,
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "emisor": instance.usuario.username,
            "nombreU": instance.usuario.first_name,
            "apellidosU": instance.usuario.last_name,
            "tipo": "Reporte informativo",
            "exclude": instance.usuario.email,
            "reporte_id": instance.pk,
            'gps': "%s,%s" % (instance.latitud, instance.longitud),
        }
        return data
    # end def
# end class


class SeguimientoTrigger(DefaultTrigger):
    model = gestion_cartera.Seguimiento
    types = [usuarios.Gerente, usuarios.Asistente, usuarios.Supervisor]
    message = u"""El usuario %(usuario)s ha programado un segimiento"""

    def get_data(self, instance):
        data = {
            "fecha": instance.strftime("%Y-%m-%d %I:%M%p"),
            "usuario": instance.usuario.username,
            "comentario": instance.comentario,
            "fecha_proxima": instance.fecha_proxima.strftime("%Y-%m-%d %I:%M%p"),
            "tipo": "Seguimiento",
        }
        return data
    # end def
# end class

class InicioSeguimientoTrigger(DefaultTrigger):
    model = gestion_cartera.InicioSeguimiento
    types = [usuarios.Gerente, usuarios.Asistente, usuarios.Supervisor]
    message = u"""El usuario %(usuario)s ha iniciado un segimiento"""

    def get_data(self, instance):
        data = {
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "usuario": instance.usuario.username,
            "cliente": instance.cliente.username,
            "comentario": instance.comentario,
            "fecha_proxima": instance.fecha_proxima.strftime("%Y-%m-%d %I:%M%p"),
            "tipo": "Inicio de Seguimiento",
        }
        return data
    # end def
# end class


class AsignacionTrigger(UserTrigger):
    model = usuarios.AsignacionPiscinero
    type = usuarios.Piscinero
    types = [usuarios.Piscinero]
    message = u"""La piscina %(piscina)s se te ha %(asignado)s"""

    def get_webuser(self, instance):
        return [instance.piscinero.username]
    # end def

    def get_data(self, instance):
        if instance.asigna:
            asignado = "asignado"
        else:
            asignado = "des asignado"
        # end if
        data = {
            "nombre": "Asignacion",
            "asignado": asignado,
            "piscinero": instance.piscinero.username,
            "piscina": instance.piscina.nombre,
            "fecha": instance.fecha.strftime("%Y-%m-%d %I:%M%p"),
            "asigna": instance.asigna,
            "orden": instance.orden,
            "piscinero_id": instance.piscinero.pk,
            "tipo": "Asignacion",
            "include": instance.piscinero.email,
            "asignacion_id": instance.pk,
            "usuario": instance.piscinero.username
        }
        return data
    # end def
# edn class


class DefaultSMTPPlugin(triggers.TriggerSMTPPlugin):
    messages = {
        "save": {
            "headers": {
                "Subject": 'El usuario %(usuario)s ha realizado un reporte sobre la piscina %(piscina)s'
            },
            "message_template": "notificaciones/email.html",
            "include": "%(include)s",
            "exclude": "%(exclude)s"
        },
        "create": {
            "headers": {
                "Subject": 'Reporte de prisma service'
            },
            "message_template": "notificaciones/email.html",
            "include": "%(include)s",
            "exclude": "%(exclude)s"
        },
        "update": {
            "headers": {
                "Subject": 'Reporte de prisma service'
            },
            "message_template": "notificaciones/email.html",
            "include": "%(include)s",
            "exclude": "%(exclude)s"
        }
    }
# end class


class E500SMTPPlugin(triggers.TriggerSMTPPlugin):
    messages = {
        "create": {
            "headers": {
                "Subject": """Piscis Error 500"""
            },
            "message_template": "notificaciones/500.html",
            "include": "%(include)s"
        }
    }
# end class


class E500Trigger(UserTrigger):
    types = []
    message = u"""Error 500"""

    def get_webuser(self, request):
        if hasattr(request, 'user'):
            return [request.user]
        # end if
        return "No user"
    # end def

    def get_url(self, request):
        return request.path
    # end def

    def get_data(self, request):
        data = request.__dict__
        data['include'] = 'luismiguel.mopa@gmail.com'
        return data
    # end def
# edn class


class DefaultIOPluing(triggers.TriggerIOPlugin):
    username = 'user2'
    password = '123456'
    host = HOST
    port = IO_PORT
# end class

triggers.triggers.register(SolucionTrigger, [DefaultIOPluing, DefaultSMTPPlugin])
triggers.triggers.register(RecordatorioTrigger, [DefaultIOPluing, DefaultSMTPPlugin])
triggers.triggers.register(RespuestaUTrigger, [DefaultIOPluing, ])
triggers.triggers.register(RespuestaTrigger, [DefaultIOPluing, ])
triggers.triggers.register(ReporteTrigger, [DefaultIOPluing, DefaultSMTPPlugin])
triggers.triggers.register(ReporteInformativoTrigger, [DefaultIOPluing, DefaultSMTPPlugin])
triggers.triggers.register(BirdateTrigger, [DefaultIOPluing, ])
triggers.triggers.register(ActividadTrigger, [DefaultIOPluing, DefaultSMTPPlugin])
triggers.triggers.register(AsignacionTrigger, [DefaultIOPluing, DefaultSMTPPlugin])
triggers.triggers.register(HappyAsistenteTrigger, [DefaultIOPluing, ])
triggers.triggers.register(HappyPiscineroTrigger, [DefaultIOPluing, ])
triggers.triggers.register(SolucionResendTrigger, [DefaultSMTPPlugin, ])
triggers.triggers.register(ReporteResendTrigger, [DefaultSMTPPlugin, ])
triggers.triggers.register(InicioSeguimientoTrigger, [DefaultSMTPPlugin, ])
triggers.triggers.register(SeguimientoTrigger, [DefaultSMTPPlugin, ])


def request_exception(sender, **kwargs):
    trigger = E500Trigger()
    e500 = E500SMTPPlugin()
    e500.init(kwargs['request'])
    trigger.plugins['smtpplugin'] = e500
    trigger.create(kwargs['request'])
# end def

got_request_exception.connect(request_exception)
