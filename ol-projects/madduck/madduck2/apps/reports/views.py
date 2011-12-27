from django.db.models import Count, Max, Min
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from quizattempt.models import Attempt, AttemptQuestion

""" @todo, this is the reports-index-page.   """
@login_required
def index(request):
  attempts = Attempt.objects.filter(owner=request.user).order_by('-created')
  
  return render_to_response("reports/index.html", {
          "attempts" : attempts,
       }, context_instance=RequestContext(request))

@login_required
def report_quiz(request, quiz_id):
  attempts = Attempt.objects.filter(owner=request.user, quiz=quiz_id)
  
  return render_to_response("reports/report_quiz.html", {
          "attempts" : attempts,
       }, context_instance=RequestContext(request))

@login_required
def report_attempt(request, quiz_id, attempt_id):
  attempt = Attempt.objects.get(owner=request.user, quiz=quiz_id, attempt=attempt_id)
#  attempt_questions = Attempt.objects.get(attempt_question=attempt)
#  attempt_questions = AttemptQuestion.objects.filter(attempt=attempt).select_related()
#  attempt_answers = AttemptAnswer.objects.filter(question__in=attempt_questions)
  
  return render_to_response("reports/report_attempt.html", {
          "attempt" : attempt,
#          "attempt_questions" : attempt_questions,
       }, context_instance=RequestContext(request))
