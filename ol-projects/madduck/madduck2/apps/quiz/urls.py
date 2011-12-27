from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r"^$", "quiz.views.index", name="quiz_index"),
  
  url(r"^create/$", "quiz.views.quiz_create", name="quiz_create"),
  url(r"^(?P<quiz_id>\d+)/view/$", "quiz.views.quiz_view", name="quiz_view"),
  url(r"^(?P<quiz_id>\d+)/update/$", "quiz.views.quiz_update", name="quiz_update"),
  url(r"^(?P<quiz_id>\d+)/delete/$", "quiz.views.quiz_delete", name="quiz_delete"),
  url(r"^(?P<quiz_id>\d+)/settings/$", "quiz.views.quiz_settings", name="quiz_settings"),
  
  url(r"^(?P<quiz_id>\d+)/question/create/$", "quiz.views.question_create", name="question_create"),
  url(r"^(?P<quiz_id>\d+)/question/(?P<question_id>\d+)/view/$", "quiz.views.question_view", name="question_view"),
  url(r"^(?P<quiz_id>\d+)/question/(?P<question_id>\d+)/update/$", "quiz.views.question_update", name="question_update"),
  url(r"^(?P<quiz_id>\d+)/question/(?P<question_id>\d+)/delete/$", "quiz.views.question_delete", name="question_delete"),
  url(r"^(?P<quiz_id>\d+)/question/(?P<question_id>\d+)/moveup/$", "quiz.views.question_moveup", name="question_moveup"),
  url(r"^(?P<quiz_id>\d+)/question/(?P<question_id>\d+)/movedown/$", "quiz.views.question_movedown", name="question_movedown"),
)
