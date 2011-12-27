from django.forms import ModelForm, RadioSelect
from formwidgets import RadioButton
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from quiz.models import Quiz, Question, Answer

class QuizForm(ModelForm):
  """ 
  Quiz Form : form associated to the quiz model
  """
  def __init__ (self, *args, **kwargs):
    super(QuizForm, self).__init__(*args, **kwargs)
  
  class Meta:
    model = Quiz
    exclude = ('owner', 'created', 'last_updated', 'status', 'published', 'expiry_date', 'generate_report',)
    
class QuizSettingsForm(ModelForm):
  """ generates form to create quiz-settings. """
  def __init__(self, *args, **kwargs):
    super(QuizSettingsForm, self).__init__(*args, **kwargs)
    
  class Meta:
    model = Quiz
    fields = ('published', 'expiry_date', 'generate_report',)
      
class QuestionForm(ModelForm):
  """ Question Form : form associated to the question model. """
  def __init__ (self, *args, **kwargs):
    super(QuestionForm, self).__init__(*args, **kwargs)
  
  class Meta:
    model = Question
    fields = ('type', 'text',)
    widgets = {
      'type' : RadioButton,
    }
    
class AnswerForm(ModelForm):
  def __init__ (self, *args, **kwargs):
    super(AnswerForm, self).__init__(*args, **kwargs)
  
  class Meta:
    model = Answer
    fields = ('correct', 'option',)
    
AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, max_num=1)
    