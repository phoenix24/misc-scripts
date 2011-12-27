from django.template import RequestContext
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

def exception_404(request, template='404.html'):
	return render_to_response(template, {}, 
					context_instance=RequestContext(request))
	
def exception_500(request, template='500.html'):
	return render_to_response(template, {}, 
					context_instance=RequestContext(request))
	
