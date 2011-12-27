from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test

from decorators import anonymous_required

""" @todo, should probably use the authentication form here.   """
@anonymous_required(viewname='home.views.index')
def login(request):
    """ returns custom madduck2.login page. """
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            
            # Redirect to a success page.
            return HttpResponseRedirect(reverse("home.views.index"))
    
    return render_to_response("auth/login.html", {
         }, context_instance=RequestContext(request))

def logout(request):
    """ returns custom madduck2.logout page. """
    
    auth.logout(request)
    
    return render_to_response("auth/logout.html", {
        }, context_instance=RequestContext(request))

""" @todo, add support for connecting via facebook. """
@anonymous_required(viewname='home.views.index')
def signup(request):
    """ returns custom madduck2.signup page. """
    
    user_form = UserCreationForm()
    
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            """ new user account is created here"""
            """ @fixme: this is a buggy peice of code; cannot do commit=False; because a M-M relation cannot be attached to a non-existing object. """
            new_user = user_form.save()
            
            """ @fixme: group is added after the account is created/commited to the DB; this is kinda bad; required two DB calls."""
#            new_user.groups.add(Group.objects.get(name='student'))
            return HttpResponseRedirect(reverse("home.views.index"))
    
    return render_to_response("auth/signup.html", {
        'form' : user_form
        }, context_instance=RequestContext(request))
    