from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^$', 'profile.views.view', name='profile_view'),
  url(r'^update/$', 'profile.views.update', name='profile_update'),
  url(r'^delete/$', 'profile.views.delete', name='profile_delete'),
  
  #@todo: bad-regexp needs to be fixed.
  url(r'^(?P<username>\w+|\w+\@\w+\.\w+)/$', 'profile.views.userprofile', name='user_profile'),
)
