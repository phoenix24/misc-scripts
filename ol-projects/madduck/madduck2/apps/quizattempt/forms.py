from django import forms
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from quizattempt.models import Attempt, AttemptQuestion

class AttemptForm(forms.ModelForm):
  """ StartAttempt Form : form associated to the attempt model. """
  def __init__ (self, *args, **kwargs):
      self.is_update = False
      super(AttemptForm, self).__init__(*args, **kwargs)
  
  class Meta:
      model = Attempt
      exclude = ('quiz',  'owner', 'created', 'last_updated', 'published', 'status', 'duration', 'attempt')
  
class AttemptQuestionForm(forms.ModelForm):
  """ AttemptQuestionForm Form : generated the appropriate form for attempting answers. """
  def __init__(self, *args, **kwargs):
    super(AttemptQuestionForm, self).__init__(*args, **kwargs)
    
  class Meta:
    model = AttemptQuestion
    exclude = ('question', 'correct', 'attempt')

AttemptQuestionFormSet = modelformset_factory(AttemptQuestion, form=AttemptQuestionForm, max_num=1)

