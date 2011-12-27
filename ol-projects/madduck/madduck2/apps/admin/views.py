# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group, Permission
from admin.forms import *

""" @todo, this is the global administration page.   """
@login_required
def index(request):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    return render_to_response("admin/index.html", {
         }, context_instance=RequestContext(request))

@login_required
def users(request):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    if request.method == 'POST':
        """ @fixme: extremely unsafe; can lead to unexpected application crashes. """
        """ @fixme: only if the group is found, and the user is found then the user to the group. """
        """ @fixme: i don't like to use the primary key for user identification; maybe we should comeup with another mechanism for user IDs. """
        try:
            group = Group.objects.get(name=request.POST['group'])
            user = User.objects.get(pk=request.POST['userid'])
            user.groups.add(group)
        except:
            return HttpResponseRedirect(reverse("admin.views.users"))
    
    """ @todo: needs to be fixed, too bad. """
    users = User.objects.all()
    for user in users:
        user.userprofile = user.get_profile()
    
    return render_to_response("admin/users.html", {
            'users' : users
         }, context_instance=RequestContext(request))
    
@login_required
def users_groups(request, group):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    users = User.objects.filter(groups__name=group)
    for user in users:
        user.userprofile = user.get_profile()
        
    return render_to_response("admin/users.html", {
            'users' : users
         }, context_instance=RequestContext(request))
    
@login_required
def tests(request):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    return render_to_response("admin/tests.html", {
         }, context_instance=RequestContext(request))
    
@login_required
def reports(request):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    return render_to_response("admin/reports.html", {
         }, context_instance=RequestContext(request))
    
    
    
@login_required
def groups(request):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    if request.method == 'POST':
        form = GroupADD(request.POST)
        if form.is_valid():
            """ @fixme: unsafe; needs to be removed; form.cleaned_data['name'] """
            g = Group(name=form.cleaned_data['name'])
            g.save()
    else:
        form = GroupADD()
    
    groups = Group.objects.all()
    
    return render_to_response("admin/groups.html", {
        'form' : form,
        'groups' : groups
         }, context_instance=RequestContext(request))
         
@login_required
def group_view(request, group):
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home.views.index"))
    
    return render_to_response("admin/groups.html", {
        }, context_instance=RequestContext(request))
    