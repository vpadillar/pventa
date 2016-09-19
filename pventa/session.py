from django.shortcuts import redirect
from django.http import HttpResponse
"""
Session py
this middleware manage the access control
"""

class Session(object):

	def process_request(self, request):
		#if self.check_staff(request.user) and request.path in ('/', ):
		#	return redirect('/admin/')
		#end def
		if request.path in ('/login/', '/auth/login/') or self.check_access(request) or request.path.startswith('/rest/') or request.path.startswith('/ws/'):
			return None
		#end if
		return self.no_access(request.path)
	#end def

	def check_access(self, request):
		if request.path in ('/',) or request.path.startswith('/static/') or request.path.startswith('/media/'):
			return self.check_login(request.user)
		if request.path.startswith('/admin/'):
			return self.check_staff(request.user)
		else:
			return self.check_group(request)
		return False
	#end def

	def check_staff(self, user):
		return user is not None and user.is_staff
	#end def

	def check_group(self, request):
		if request.user is not None:
			if request.user.is_staff:
				if request.path in ('/dashboard.html',):
					return True
				#end if
			if request.user.groups.filter(name='mesero').count() > 0:
				if request.path in ('/dashboard.html', '/order_list.html', '/order_add.html'):
					return True
				#end if
			#end def
			if request.user.groups.filter(name='cajero').count() > 0:
				if request.path in ('/dashboard.html', '/pay_list.html', '/confirm.html', '/product_add.html', '/product_list.html', '/category_add.html', '/category_list.html', ):
					return True
				#end if
			#end def
		#end if
		return False
	#end def

	def check_login(self, user):
		return user is not None and user.is_active and user.is_authenticated()
	#end def

	def no_access(self, path):
		if path.startswith('/rest/'):
			return HttpResponse(status=400)
		#end if
		return redirect('/login/')
	#end if
#end class