from django.contrib import auth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
    
from django import forms
from profile.models import UserProfile
    
def fetch_profile(request, user):
    user.userprofile = user.get_profile()
    return render_to_response("profile/profile.html", {
            'requser' : user
        }, context_instance=RequestContext(request))
    
@login_required
def view(request):
    """ returns the loggedin user's profile. """
    return fetch_profile(request, request.user)
    
@login_required
def update(request):
    """ allows a user to update his profile. """
    return fetch_profile(request, request.user)
    
@login_required
def delete(request):
    """ allows a user to delete his profile. """
    return fetch_profile(request, request.user)
    
def userprofile(request, username):
    """ returns user profile, given the username. """
    return fetch_profile(request, get_object_or_404(User, username=username))
    
