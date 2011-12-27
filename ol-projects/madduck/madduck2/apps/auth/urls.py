from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^login/$', 'auth.views.login', name='login'),
  url(r'^logout/$', 'auth.views.logout', name='logout'),
  url(r'^signup/$', 'auth.views.signup', name='signup'),
)
