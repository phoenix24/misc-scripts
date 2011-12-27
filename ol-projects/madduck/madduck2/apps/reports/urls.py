from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^$', 'reports.views.index', name='reports_index'),
  url(r'^(?P<quiz_id>\d+)/$', 'reports.views.report_quiz', name='report_quiz'),
  url(r'^(?P<quiz_id>\d+)/(?P<attempt_id>\d+)/$', 'reports.views.report_attempt', name='report_attempt'),
)
