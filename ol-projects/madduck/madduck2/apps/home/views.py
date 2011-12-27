# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

""" @todo, this is the homepage where user is redirected after successful-login.   """
@login_required
def index(request):
    
    return render_to_response("home/index.html", {
         }, context_instance=RequestContext(request))

