from django import http, shortcuts
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery, Query
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import urlfetch
import yimagesapi
import simplejson
import sys
import urllib
import logging
from StringIO import StringIO

def respond(request, user, template, params=None):
    if params is None:
       params = {}
    if user:
       params['current_user'] = user
       params['logout_url'] = users.CreateLogoutURL('/')
    else:
      params['login_url'] = users.create_login_url('/')
    return shortcuts.render_to_response(template, params)

def index(request):
    user = users.GetCurrentUser()
    return respond(request, user, "index.html", {})

def yimages(request):
    user = users.GetCurrentUser()
    response = yimagesapi.fetch_search_results_as_json("penguin")
    return respond(request, user, "yimages.html", {'image_results' : response['ysearchresponse']['resultset_images']})
