from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #@todo: I need to refactor these.
    url(r'^$', 'static_pages.views.welcome', name="welcome"),
#    url(r'^$', direct_to_template, {'template': 'static_pages/welcome.html'}, name='welcome'),
    url(r'^tour/$', 'static_pages.views.tour', name="tour"),
    url(r'^aboutus/$', 'static_pages.views.aboutus', name="aboutus"),
    url(r'^pricing/$', 'static_pages.views.pricing', name="pricing"),
    url(r'^features/$', 'static_pages.views.features', name="features"),
    url(r'^contactus/$', 'static_pages.views.contactus', name="contactus"),
    url(r'^privacypolicy/$', 'static_pages.views.privacypolicy', name="privacypolicy"),
    url(r'^termsofservice/$', 'static_pages.views.termsofservice', name="termsofservice"),
)
