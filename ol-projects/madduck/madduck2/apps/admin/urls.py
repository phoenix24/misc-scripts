from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    url(r'^admin/$', 'admin.views.index', name='admin-index'),
#    url(r'^admin/tests/$', 'admin.views.tests', name='admin-tests-index'),
#    url(r'^admin/reports/$', 'admin.views.reports', name='admin-reports-index'),
#    url(r'^admin/groups/$', 'admin.views.groups', name='admin-groups-index'),
    #@fixme: regexp needs to be fixed to accept "this is a group name" as one entity
    #@fixme: or maybe fix the url tagname for treat "this is a group name" as one entity
#    url(r'^admin/groups/(?P<group>\w+)/$', 'admin.views.group_view', name='admin-group-view'),
    
    #@fixme: regexp needs to be fixed to accept "this is a group name" as one entity
    #@fixme: or maybe fix the url tagname for treat "this is a group name" as one entity
#    url(r'^admin/users/$', 'admin.views.users', name='admin-users-index'),
#    url(r'^admin/users/(?P<group>\w+)/$', 'admin.views.users_groups', name='admin-users-groups'),
)
