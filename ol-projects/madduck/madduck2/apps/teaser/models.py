from datetime import datetime

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Subscribe(models.Model):
    """ stores the email addresses of the people who subscribed to the teaser. """
    
    email = models.EmailField(_(u'Subscribers'), max_length = 100)
    added = models.DateField(_('added'),  default=datetime.now)
    
    class Meta:
        ordering = ('-added',)
    
    def __unicode__(self):
        return "#%d, %s" % (self.id, self.email)

class SubscribeForm(forms.ModelForm):
    """ 
    Subscribe Form : takes the email address for the user who wants to subscribe.
    """
    email = forms.EmailField(initial = _("please drop in your email here."),
                             max_length = 100,
                             error_messages = {
                                 'required': _(u"amigo, you need to put a real email address in there! :D"),
                                 'invalid': _(u"ahh! we'll actually need a valid e-mail address."),
                              })

    def __init__ (self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].required = True
        self.fields['email'].help_text = _(u"we won't spam you!")

    class Meta:
        model = Subscribe
        exclude = ('added',)
