from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from asset.models import GenericAsset
from quiz.models import Quiz, Question, Answer

class Attempt(GenericAsset):
  quiz = models.ForeignKey(Quiz)
  attempt = models.IntegerField(_("attempt number"), null=False, default=0)
  duration = models.TimeField(_("attempt duration"), auto_now=True)
  
  class Meta:
    ordering = ('-last_updated', '-created',)
  
  def save(self, *args, **kwargs):
    super(Attempt, self).save(*args, **kwargs)
  
  def addOwner(self, owner):
    self.owner = owner
    return self
  
  def addQuiz(self, quiz):
    self.quiz = quiz
    return self
  
  def addAttempt(self, attemptid):
    self.attempt = attemptid
    return self
  
  def __unicode__(self):
    return "attempt #%d, %s, %s" % (self.id, self.owner, self.quiz)
  
class AttemptQuestion(models.Model):
  attempt = models.ForeignKey(Attempt, related_name='attempt_questions')
  question = models.ForeignKey(Question,)
  answer = models.CharField(_("answer"), max_length=500, blank=True)
  correct = models.BooleanField(_("correct"), default=False)
  duration = models.IntegerField(_("milliseconds"), default= 3 * 60 * 100)
  
  def __unicode__(self):
    return "attempted record %d, for question %d" % (self.attempt.id, self.question.id)
  
#class AttemptAnswer(models.Model):
#  question = models.ForeignKey(AttemptQuestion, related_name='attempt_answers')
#  correct = models.BooleanField(_("correct"), default=False)
#  answer = models.CharField(_("answer"), max_length=500, blank=True)
#  
#  def __unicode__(self):
#    if self.id is None:
#      return "attempted answers None, %s" % (self.answer)
#    else:
#      return "attempted answers %d, %s" % (self.id, self.answer)
    
