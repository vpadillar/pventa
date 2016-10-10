from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
import models
import json

def aviable_tables(request, order):
	tables = models.Table.objects.exclude(Q(settable__order__paid=False, settable__order__canceled=False) & ~Q(settable__order=order))
	jtabls = json.dumps(list(tables.values()))
	return HttpResponse(jtabls, content_type="application/json")
#end def
