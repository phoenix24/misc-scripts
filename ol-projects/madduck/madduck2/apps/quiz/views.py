from django.template import RequestContext
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

from django.db.models import Max, Min

from quiz.models import Quiz, Question, Answer
from quiz.forms import QuizForm, QuizSettingsForm, QuestionForm, AnswerForm, AnswerFormSet

from decorators import anonymous_required, quiz_not_published, quiz_not_attempted

@login_required
def index(request, template='quiz/index.html'):
    """ returns a list of quiz's created by user, else a welcome page. """
    quiz_list = Quiz.objects.filter(owner=request.user).order_by('-created')
    
    if quiz_list:
      template = 'quiz/quiz_view_all.html'
      
      
    """ @todo: this is kinda freaky, and i must do something about it. """
    for quiz in quiz_list:
      attempts = quiz.attempt_set
      if attempts.all():
        quiz.attempted = attempts.count() or 0
        
    return render_to_response(template, {
            "quiz_list" : quiz_list,
            "pagetitle" : "All Tests",
         }, context_instance=RequestContext(request))
    
""" @notice: 
    it would be great to have a common handler for create/update;
    but, create handler is expected to grow in complexity, permissions and features,
    thence is best for the time being to let them live theie own lives.
"""
@login_required
def quiz_create(request, quiz_id=None, template='quiz/quiz_form.html'):
    """ returns a template to create a new quiz. """
    quiz_form = QuizForm()
    
    if request.method == "POST":
       quiz_form = QuizForm(request.POST)
       if quiz_form.is_valid():
           quiz = quiz_form.save(commit=False)
           quiz.addOwner(request.user).save()
           
           request.user.message_set.create(message="the quiz is successfully created. yeppie! add questions now :D")
           return HttpResponseRedirect(reverse('quiz.views.question_create', args=[quiz.id]))
         
    return render_to_response(template, {
                "quiz_form" : quiz_form,
                "selected_button" : "details",
                "pagetitle" : "Make Test",
            }, context_instance=RequestContext(request))
    
@login_required
def quiz_view(request, quiz_id=None, template='quiz/quiz_view.html'):
    """ returns the details of the quiz, given quiz-id."""
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    
    return render_to_response(template, {
              "quizobj" : quiz,
              "questions" : quiz.quiz_questions.all().order_by('number'),
              "selected_button" : "details",
              "pagetitle" : "Test Details",
            }, context_instance=RequestContext(request))
    
@login_required
@quiz_not_published
def quiz_update(request, quiz_id=None, template='quiz/quiz_form.html'):
    """ update the quiz, given its quiz-id; and the owner. if quiz is not found, throws 404. """
    """ @todo: 
        done: you can update only a test which you can actually own.
        todo : admin should also be able to edit any piece of data. 
    """
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user,)
    quiz_form = QuizForm(instance=quiz)
    
    if request.method == "POST":
      quiz_form = QuizForm(request.POST, instance=quiz)
      if quiz_form.is_valid():
        quiz_form.save()
        request.user.message_set.create(message="the quiz succesfully updated. yeah! edited.")
        return HttpResponseRedirect(reverse("quiz.views.quiz_update", args=[quiz_id]))
        
    return render_to_response(template, {
                "quizobj": quiz,
                # @todo: must be overridden in the manager.
                "questions" : quiz.quiz_questions.all().order_by('number'),
                "quiz_form": quiz_form,
                "pagetitle" : "Update Test",
                "selected_button" : "details",
            }, context_instance=RequestContext(request))
    
@login_required
@quiz_not_attempted
@quiz_not_published
def quiz_delete(request, quiz_id=None):
    """ handles the delete for a given quiz. """
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    quiz.delete()
    
    request.user.message_set.create(message="the quiz was deleted successfully. :(")
    return HttpResponseRedirect(reverse("quiz.views.index"))
    
@login_required
def quiz_settings(request, quiz_id):
    """ create/edit/update quiz-settings. """
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    quiz_settings_form = QuizSettingsForm(instance=quiz)
      
    if request.method == "POST":
        quiz_settings_form = QuizSettingsForm(request.POST, instance=quiz)
        if quiz_settings_form.is_valid():
            quiz_settings = quiz_settings_form.save(commit=False)
            quiz_settings.quiz = quiz
            quiz_settings.save()
            request.user.message_set.create(message="the quiz settings successfully saved :D ")
            
    return render_to_response("quiz/quiz_settings.html", {
              "quizobj" : quiz,
              "questions" : quiz.quiz_questions.all().order_by('number'),
              "quiz_settings_form" : quiz_settings_form,
              "selected_button" : "settings",
              "pagetitle" : "Test Settings",
          }, context_instance=RequestContext(request))
        
""" all helper methods related to question creation start from here."""
@login_required
@quiz_not_published
def question_create(request, quiz_id, question_id=None):
    """ returns a template to create a new quiz. """
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    iscomplete = True
    
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)
       
        if question_form.is_valid() and answer_formset.is_valid():
            """ @todo : this must be moved to the quiz-manager """
            new_question = question_form.save(commit=False)
            new_question.number = (quiz.quiz_questions.aggregate(Max('number'))['number__max'] or 0) +1
            new_question.owner = request.user
            new_question.quiz = quiz
            new_question.save()
            
            for answer_form in answer_formset.forms:
                new_answer = answer_form.save(commit=False)
                new_answer.owner = request.user
                new_answer.question = new_question
                new_answer.save()
                
                ##status updation is ugly, must be fixed.
                iscomplete = iscomplete and not (new_answer.option == '')
                
            ##status updation is ugly, must be fixed.
            iscomplete = iscomplete and not (new_question.text == '')
            if iscomplete:
              new_question.status = "complete"
              new_question.save()
              if len(quiz.quiz_questions.filter(status="incomplete")) == 0:
                quiz.status = "complete"
            else:
              quiz.status = "incomplete"
              
            quiz.save()
            
            request.user.message_set.create(message="the question was created successfully. yeppie! add another")
            return HttpResponseRedirect(reverse("quiz.views.question_create", args=[quiz_id]))
    #GET Request
    else:
            question_form = QuestionForm()
            answer_formset = AnswerFormSet(queryset=Answer.objects.none())
            
    return render_to_response('quiz/question_form.html', {
                "question_form" : question_form,
                "answer_formset" : answer_formset,
                "questions" : quiz.quiz_questions.all().order_by('number'),
                "quizobj" : quiz,
                "selected_button" : "create",
                "current_question" : (quiz.quiz_questions.aggregate(Max('number'))['number__max'] or 0) +1,
                "pagetitle" : "Create Question",
           }, context_instance=RequestContext(request))
    
@login_required
def question_view(request, quiz_id, question_id):
    """ opens the selected question in the preview mode. """
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    question = get_object_or_404(Question, quiz=quiz, number=question_id)
    answers = Answer.objects.filter(question=question)
    
    question_form = QuestionForm(instance=question)
    answer_formset = AnswerFormSet(queryset=Answer.objects.filter(question=question))
    
    return render_to_response("quiz/question_form.html", {
                "quizobj" : quiz,
                "questions" : quiz.quiz_questions.all().order_by('number'),
                "question_form" : question_form,
                "answer_formset" : answer_formset,
                "selected_question": question,
                "pagetitle" : "Update Question",
            }, context_instance=RequestContext(request))

@login_required
@quiz_not_published
def question_update(request, quiz_id, question_id):
    """ opens the selected question in the preview mode. """
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    question = get_object_or_404(Question, quiz=quiz, number=question_id)
    answers = Answer.objects.filter(question=question)
    iscomplete = True
    
    if request.method == "POST":
        question_form = QuestionForm(request.POST, instance=question)
        answer_formset = AnswerFormSet(request.POST)
        
        if question_form.is_valid() and answer_formset.is_valid():
            answers.delete()
            
            new_question = question_form.save()
            for answer_form in answer_formset.forms:
                answer_form = answer_form.save(commit=False)
                answer_form.owner = request.user
                answer_form.question = question
                answer_form.save()
                ##status updation is ugly, must be fixed.
                iscomplete = iscomplete and not (answer_form.option == '')
                
            ##status updation is ugly, must be fixed.
            iscomplete = iscomplete and not (new_question.text == '')
            if iscomplete:
              new_question.status = "complete"
            else:
              new_question.status = "incomplete"
            new_question.save()
              
            if len(quiz.quiz_questions.filter(status="incomplete")) == 0:
              quiz.status = "complete"
            else:
              quiz.status = "incomplete"
            quiz.save()
            
            request.user.message_set.create(message="the question was updated successfully :D ")
            return HttpResponseRedirect(reverse("quiz.views.question_view", args=[quiz_id, question_id]))
    #GET Request
    else:
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerFormSet(queryset=Answer.objects.filter(question=question))
    
    return render_to_response("quiz/question_form.html", {
                "quizobj" : quiz,
                "questions" : quiz.quiz_questions.all().order_by('number'),
                "question_form" : question_form,
                "answer_formset" : answer_formset,
                "selected_question": question,
                "pagetitle" : "Update Question",
            }, context_instance=RequestContext(request))
    
@login_required
@quiz_not_published
def question_delete(request, quiz_id, question_id):
    """ deletes the question, given the quiz_id and question_id. """
    question = get_object_or_404(Question, quiz=quiz_id, number=question_id, owner=request.user)
    qnum = question.number
    question.delete()
    
    """ re-number the reminder of questions to fill the void created by deleted question. """
    i = 0
    for ques in Question.objects.filter(quiz=quiz_id).filter(number__gt=qnum):
      ques.number = qnum + i
      ques.save()
      i = i + 1
      
    request.user.message_set.create(message="the question was deleted successfully. :( ")
    return HttpResponseRedirect(reverse("quiz.views.quiz_view", args=[quiz_id]))

@login_required
@quiz_not_published
def question_moveup(request, quiz_id, question_id):
    """ moves the given question one-up, re-number the question - 1 """
    question1 = get_object_or_404(Question, quiz=quiz_id, number=question_id, owner=request.user)
    question2 = get_object_or_404(Question, quiz=quiz_id, number=int(question_id)-1, owner=request.user)
    
    question1.number = question1.number - 1
    question2.number = question2.number + 1
    
    question1.save()
    question2.save()
    
    request.user.message_set.create(message="question moved up. :D ")
    return HttpResponseRedirect(reverse("quiz.views.quiz_view", args=[quiz_id]))

@login_required
@quiz_not_published
def question_movedown(request, quiz_id, question_id):
    """ moves the given question one-down, re-number the question + 1 """
    question1 = get_object_or_404(Question, quiz=quiz_id, number=question_id, owner=request.user)
    question2 = get_object_or_404(Question, quiz=quiz_id, number=int(question_id)+1, owner=request.user)
    
    question1.number = question1.number + 1
    question2.number = question2.number - 1
    
    question1.save()
    question2.save()
    
    request.user.message_set.create(message="question moved down. :D ")
    return HttpResponseRedirect(reverse("quiz.views.quiz_view", args=[quiz_id]))
