from datetime import datetime

from django.forms import ModelForm, RadioSelect
from django.db import models
from django.db.models import permalink
from django.db.models.base import get_absolute_url
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User

from asset.models import GenericAsset

class Quiz(GenericAsset):
    """ Quiz Model: type, subject, date, class, total_marks, total_questions, duration, note """
    
    name = models.CharField(_("Test Name"), max_length=50, default=_("test name"))
    type = models.CharField(_("Test Type"), max_length=50, default=_("test type"))
    note = models.TextField(_("Test Note"), blank=True, default=_("additional notes"),)
    klass = models.CharField(_("Class"), max_length=20, default=_("open test"))
    
    subject = models.CharField(_("Subject"), max_length=30, default=_("select a subject"))
    duration = models.IntegerField(_("Duration Of The Test"), default=0)
    total_marks = models.IntegerField(_("Total Marks"), default=100)
    total_questions = models.IntegerField(_("Total Questions"), default=15)
    
    published = models.BooleanField(_('published'), default=False)
    expiry_date = models.DateTimeField(_("test expiry date"), default=datetime.now)
    generate_report = models.BooleanField(_("generate report after quiz"), default=False)
    
    class Meta:
        ordering = ('-last_updated', '-created',)
    
    @models.permalink
    def get_absolute_url(self):
        return ("quiz_view", [self.pk])
    
    def save(self, *args, **kwargs):
        super(Quiz, self).save(*args, **kwargs)
    
    def addOwner(self, owner):
        self.owner = owner
        return self
    
    def questions(self, orderby=None):
      return self.quiz_questions.all().order_by(orderby)
    
    def __unicode__(self):
        return "#%d, %s" % (self.id, self.name)
    
    
class Question(GenericAsset):
    """ questions, are independent assets; these are the building blocks.
        a, can be associated to a whole bunch of other high-level assets.
        b, it should solve a lot of problems when there are multiple authors
    """
    
    """ @TODO these should not be hardcoded.. """
    QUESTION_TYPE = (
        (u"MultipleChoice", u"Multiple Choice"),
        (u"TrueFalse", u"True False"),
        (u"Essay", u"Essay"),
        (u"FillBlank", u"Fill Up"),
    )
    
    quiz = models.ForeignKey(Quiz, related_name='quiz_questions')
    number = models.IntegerField(_("Question Number"), default=0)
    text = models.TextField(_("Question Text"), default="type in the question here.", blank=False)
    type = models.CharField(_("Question Type"), default="MultipleChoice", max_length=100, choices=QUESTION_TYPE)
    
    class Meta:
        ordering = ('-text', '-last_updated', '-created',)
    
    def __unicode__(self):
        return "#%d, %s" % (self.id, self.text)
    
class Answer(GenericAsset):
    """ answers, are not independent; but tied to a respective question; 
        but yes, these are building blocks too.
    """
    
    """ @todo: needs to fixup the appropriate models schema; i absolutely suck at this."""
    question = models.ForeignKey(Question, related_name='question_answers')
    option = models.CharField(_("answer option"), max_length=500, default="type in the option here.", blank=True)
    correct = models.BooleanField(_("answer correct"), max_length=10,)
    
    class Meta:
        ordering = ('id',)
        
    def __unicode__(self):
      if self.id is not None:
        return "#%d, %s" % (self.id, self.option)
      else:
        return "%s" % (self.option)
