from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'error.views.exception_404'
handler500 = 'error.views.exception_500'

urlpatterns = patterns('',
    #its not really a good idea to do this.
    url(r'', include('auth.urls')),
    url(r'', include('static_pages.urls')),
    
    url(r'^home/', include('home.urls')),
    url(r'^profile/', include('profile.urls')),
    
    url(r'^tests/editor/', include('quiz.urls')),
    url(r'^tests/attempt/', include('quizattempt.urls')),
    url(r'^tests/reports/', include('reports.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

#while application runs under debug mode, serve static files from here.
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT }),
    )
