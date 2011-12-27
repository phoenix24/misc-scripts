from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.utils.functional import update_wrapper, wraps  # Python 2.3, 2.4 fallback.
from django.utils.decorators import available_attrs
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

from quiz.models import Quiz, Question, Answer

#def anonymous_required( view_function, redirect_to = None ):
#    return AnonymousRequired( view_function, redirect_to )
#
#class AnonymousRequired( object ):
#  def __init__( self, view_function, redirect_to ):
#    if redirect_to is None:
#        redirect_to = "home.views.index"
#    self.view_function = view_function
#    self.redirect_to = redirect_to
#    
#  def __call__( self, request, *args, **kwargs ):
#    if request.user is not None and request.user.is_authenticated():
#        return HttpResponseRedirect( self.redirect_to ) 
#    return self.view_function( request, *args, **kwargs )
    
def anonymous_required(viewname):
  def decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
      if request.user is not None and request.user.is_authenticated():
        return HttpResponseRedirect(reverse(viewname))
      return view_func(request, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
  return decorator

def quiz_not_published(view_func):
  """ this decorator allows to perform the action, only if the given quiz is not published. """
  def _wrapped_view(request, *args, **kwargs):
    quiz_id = kwargs['quiz_id']
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user,)
    if quiz.published:
      request.user.message_set.create(message="the quiz is already published, un-publish to edit it.")
      return HttpResponseRedirect(reverse("quiz.views.quiz_view", args=[quiz_id]))
    return view_func(request, *args, **kwargs)
  return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)

def quiz_not_attempted(view_func):
  """ this decorator allows to perform the action, only if the given quiz is not published. """
  def _wrapped_view(request, *args, **kwargs):
    quiz_id = kwargs['quiz_id']
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user,)
    if quiz.attempt_set.all(): #quiz.attempt_set.count() or 0
      request.user.message_set.create(message="quiz is already attempted dude!, cant delete it peee-poooo-peee-poooo-peee-poooo :P.")
      return HttpResponseRedirect(reverse("quiz.views.quiz_view", args=[quiz_id]))
    return view_func(request, *args, **kwargs)
  return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
