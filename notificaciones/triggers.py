#!/usr/bin/env python
# -*- coding: utf-8 -*-
# for AthenticationError:
# https://www.google.com/settings/u/1/security/lesssecureapps
from django import forms
from socketIO_client import SocketIO
from django.core import mail as smtpplugin
from Piscix.settings import EMAIL_HOST_USER, BASE_DIR
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from django.contrib.auth.models import User
from django.contrib import admin
from threading import Thread
import time
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from supra import views as supra
from datetime import datetime
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
import os

SMTP_ROOT_URL = 'http://104.236.33.228:8050'


class TriggerIOPlugin(object):
    name = 'ioplugin'
    host = '127.0.0.1'
    port = 1196
    username = ''
    password = ''
    usertype = 'SERVER'
    event = ''
    message = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
    # end def

    def init(self, request):
        self.request = request
    # end def

    def identify(self):
        def waiter(username, password, usertype, session_key):
            ioplugin = SocketIO(self.host, self.port)

            def on_identify(message):
                if not 'ID' in message:
                    obj = {
                        'username': username, 
                        'password': password,
                        'usertype': usertype, 
                        'django_id': session_key
                    }
                    ioplugin.emit('login', obj)
                else:
                    self.do_event(ioplugin)
                # end if
            # end def

            def on_error_login():
                print "Errror ", username, password, usertype, session_key
            # end def

            def on_success_login():
                print "login-success"
                self.do_event(ioplugin)
            # end def

            ioplugin.on('identify', on_identify)
            ioplugin.on('error-login', on_error_login)
            ioplugin.on('success-login', on_success_login)
            ioplugin.emit('identify', {'django_id': session_key, 'usertype': usertype})
            ioplugin.wait(seconds=1)
        # end def
        print "Message: ", self.message
        Thread(target=waiter, args=(self.username, self.password,self.usertype, self.request.session.session_key)).start()
    # end def

    def do_event(self, ioplugin):
        ioplugin.emit(self.event, self.message)
        ioplugin.wait(seconds=10)
    # end def

    @classmethod
    def start(cls):
        return cls(cls.host, cls.port)
    # end def

    def emit(self, event, message):
        message['django_id'] = self.request.session.session_key
        message['usertype'] = self.usertype
        self.event = event
        self.message = message
        self.identify()
    # end def

# end class


class TriggerSMTPPlugin(object):
    name = 'smtpplugin'
    messages = {'save': 'a model has been created'}
    root_url = SMTP_ROOT_URL


    def init(self, request):
        self.smtpplugin = smtpplugin
        self.sender = EMAIL_HOST_USER
    # end def

    @classmethod
    def start(cls):
        return cls()
    # end def

    def add_header(self, message, header_name, header_value):
        if self.hasnt_ascii(header_value):
            header = Header(header_value, 'utf-8')
            message[header_name] = header
        else:
            message[header_name] = header_value
        return message
    # end def

    def hasnt_ascii(self, str):
        return not all(ord(c) < 128 for c in str)
    # end def

    def emit(self, event, message):
        print "emiting"
        message['root_url'] = self.root_url
        if 'message' in self.messages[event]:
            html = self.messages[event]['message'] % message['data']
        elif 'message_template' in self.messages[event]:
            html = render_to_string(self.messages[event]['message_template'], message)
        # end if
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", event
        subject = self.messages[event]['headers']['Subject'] % message['data']
        to = []
        if 'emails' in message['data']:
            to = message['data']['emails']
        # end if

        if 'include' in self.messages[event] and 'include' in message['data']:
            email_add = self.messages[event]['include'] % message['data']
            if email_add and email_add != '':
                to.append(email_add)
            # end if
        # end if
        if 'exclude' in self.messages[event] and 'exclude' in message['data']:
            value = self.messages[event]['exclude'] % message['data']
            if value in to:
                to.remove(value)
            # end if
        # end if
        with open(os.path.join(BASE_DIR, 'trigger_plugin.log'), 'a+') as log:
            log.write("%s sended to: %s\n" % (datetime.now(), to, ))
            log.close()
        # end with
        if len(to):
            msg = self.smtpplugin.EmailMultiAlternatives(subject, ".", self.sender, to)
            msg.attach_alternative(html, "text/html")
            msg.send()
        # end def 
    # end def

# end class


class Trigger(object):
    model = None

    def __init__(self, *args, **kwargs):
        self.plugins = {}
    # end def

    def init(self, request):
        self.request = request
        for plugin in self.plugins:
            self.plugins[plugin].init(request)
        # end def
    # end def

    def add_plugin(self, plugin):
        self.plugins[plugin.name] = plugin.start()
    # end def

    def has_plugin(self, plugin):
        return plugin in self.plugins
    # end def

    def save(self, instance):
        print "override save"
    # end def

    def create(self, instance):
        print "override create"
    # end def

    def update(self, instance):
        print "override update"
    # end def

    def emit_by(self, event, message, by):
        self.plugins[by].emit(event, message)
    # end def

    def emit(self, event, message):
        for plugin in self.plugins:
            self.emit_by(event, message, plugin)
        # end def
    # end def

# end class


_thread_locals = local()
class triggers(object):
    _registry = []
    times = {}

    @classmethod
    def register(cls, trigger, plugins=[]):
        trg = trigger()
        for plugin in plugins:
            trg.add_plugin(plugin)
        # end for
        cls._registry.append(trg)
        if isinstance(trg.model, list):
            for model in trg.model:
                cls.times[model] = 0
            # end for
        else:
            cls.times[trg.model] = 0
        # end if
    # end def

    @classmethod
    def get_registries(cls, model):
        registries = []
        for registry in cls._registry:
            if isinstance(registry, list):
                if model in registry.model:
                    registries.append(registry)
                # end if
            else:
                if model == registry.model:
                    registries.append(registry)
                # end if
            # end if
        # end for
        return registries
    # end def
# end class


def save_model(sender, instance, **kwargs):
    #print sender, triggers.times
    if sender in triggers.times and triggers.times[sender] == 0:
        print "save model", sender, kwargs['created']
        registries = triggers.get_registries(sender)
        for registry in registries:
            registry.init(_thread_locals.request)
            registry.save(instance)
            if kwargs['created']:
                registry.create(instance)
            else:
                registry.update(instance)
            # end if
        # end for
        triggers.times[sender] = triggers.times[sender] + 1
    # end if
# end def

post_save.connect(save_model, dispatch_uid="save_model_for_all")

class Middleware(object):
    def __init__(self, get_response):
        print "set request init"
        self.get_response = get_response
    # end def

    def __call__(self, request):
        print "set request"
        _thread_locals.request = request
        self.process_view(request)
        response = self.get_response(request)

        return response
    # end def

    def process_view(self, request, *args, **kwargs):
        print "set request"
        for model in triggers.times:
            triggers.times[model] = 0
        # end for
        return None
    # end def
# end class