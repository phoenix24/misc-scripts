from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("",
  url(r"^$", "quizattempt.views.index", name="attempt_index"),
  url(r"^(?P<quiz_id>\d+)/$", "quizattempt.views.attempt_quiz", name="attempt_quiz"),
  url(r"^(?P<quiz_id>\d+)/(?P<attempt_id>\d+)/question/(?P<question_id>\d+)$", "quizattempt.views.attempt_question", name="attempt_question"),
)
