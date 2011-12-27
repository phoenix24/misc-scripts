from django.template import RequestContext
from django.core.urlresolvers import reverse 
from django.core.paginator import EmptyPage, InvalidPage, Paginator

from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404

from django.db.models import Max, Min
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from quiz.models import Quiz, Question, Answer
from quiz.forms import QuizForm, QuestionForm, AnswerForm, AnswerFormSet

from quizattempt.models import Attempt, AttemptQuestion
from quizattempt.forms import AttemptForm, AttemptQuestionForm

@login_required
def index(request):
  """ returns a list of all the published quiz's, that can be attempted. """
  quiz_list = Quiz.objects.filter(published=True)
  
  for quiz in quiz_list:
    if quiz.attempt_set.filter(owner=request.user).all():
      quiz.attempted = True
  
  return render_to_response('quizattempt/index.html', {
                "quiz_list" : quiz_list,
                "pagetitle" : "Available Tests",
          }, context_instance=RequestContext(request))
  
@login_required
def attempt_quiz(request, quiz_id):
  quiz = get_object_or_404(Quiz, id=quiz_id, published=True)
  attempt_form = AttemptForm()
  
  if request.method == 'POST':
   attempt_form = AttemptForm(request.POST)
   if attempt_form.is_valid():
     startattempt = attempt_form.save(commit=False)
     
     #DIRTY HACK needs to be fixed.
     first_question = Question.objects.filter(quiz=quiz_id).aggregate(Min('number'))['number__min']
     attempt = (Attempt.objects.filter(owner=request.user, quiz=quiz_id).aggregate(Max('attempt'))['attempt__max'] or 0) + 1
     startattempt.addOwner(request.user).addQuiz(quiz).addAttempt(attempt).save()
     return HttpResponseRedirect(reverse("quizattempt.views.attempt_question", args=[quiz.id, startattempt.attempt, first_question]))
  
  return render_to_response('quizattempt/attempt_quiz.html', {
                "quizobj" : quiz,
                "pagetitle" : "Attempt Test",
                "attempt_form" : attempt_form,
          }, context_instance=RequestContext(request))
  
@login_required
def attempt_question(request, quiz_id, attempt_id, question_id):
  """ opens the selected question in the quiz-attempt mode. """
  quiz = get_object_or_404(Quiz, id=quiz_id, published=True)
  questions = quiz.quiz_questions.order_by('number')
  questions_prev_next = Paginator(questions, 1).page(question_id)
  
  """ @todo, this is buggy and needs to be fixed. """
  question = get_object_or_404(Question, quiz=quiz_id, number=question_id)
  answers = Answer.objects.filter(question=question)
  attempt_question_form = AttemptQuestionForm(instance=question)
  
  if request.method == "POST":
    attempt = Attempt.objects.get(owner=request.user, quiz=quiz_id, attempt=attempt_id)
    attempt_question, created = AttemptQuestion.objects.get_or_create(attempt=attempt, question=question)
    attempt_question_form = AttemptQuestionForm(request.POST, instance=attempt_question)
    
    if attempt_question_form.is_valid():
      answer_form = attempt_question_form.save(commit=False)
      answer_form.save()
      
      if questions_prev_next.has_next():
        return HttpResponseRedirect(reverse("quizattempt.views.attempt_question", args=[quiz_id, attempt.attempt, questions_prev_next.next_page_number()]))
      else:
        attempt.status = "complete"
        attempt.save()
        return HttpResponseRedirect(reverse("reports.views.report_attempt", args=[quiz_id, attempt.attempt]))
        
  return render_to_response("quizattempt/attempt_question.html", {
              "quiz_id" : quiz_id,
              "attempt_id" : attempt_id,
              "selected_question": question,
              "questions_prev_next" : questions_prev_next,
              "questions" : questions,
              "answers": answers,
              "attemptanswer_form" : attempt_question_form,
              "pagetitle" : "Attempt Question",
          }, context_instance=RequestContext(request))
