from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='home_index'),
)
