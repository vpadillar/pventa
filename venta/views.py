from django.shortcuts import render
from django.http import HttpResponse
from cuser.middleware import CuserMiddleware
from django.middleware.csrf import get_token
from django.views.generic.base import TemplateView
import models
import json


class PvTemplateView(TemplateView):

	def get_context_data(self, **kwargs):
		user = CuserMiddleware.get_user()
		context = super(PvTemplateView, self).get_context_data(**kwargs)
		if user.is_authenticated():
			service = models.Service.objects.filter(userservice__user = user).first()
			context['service'] = service
			context['user'] = user
			context['groups'] = user.groups.all()
		#end if
		return context
	#end def
#end class

def nocount(request):
	order = models.Order.objects.last()
	if order:
		no = order.id + 1
	else:
		no = 0
	#end if
	return HttpResponse(str(no))
#end def

def token(request):
	sjson = {
		'token': get_token(request)
	}
	return HttpResponse(json.dumps(sjson), content_type="application/json")
#end def

def config(request):
	config, create = models.Config.objects.get_or_create()
	sjson = {
		'ipoconsumo': config.ipoconsumo,
		'propina': config.propina,
		'iva': config.iva
	}
	return HttpResponse(json.dumps(sjson), content_type="application/json")
#end def


def service(request):
	user = CuserMiddleware.get_user()
	service = models.Service.objects.filter(userservice__user = user).first()
	sjson = {
		'name':service.name,
		'code':service.code,
		'printer':service.printer,
		'moviles':service.moviles,
	}
	return HttpResponse(json.dumps(sjson), content_type="application/json")
#end def