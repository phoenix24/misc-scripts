from django.db import models
from django.db.models.signals import post_save

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    user = models.ForeignKey(User, unique=True, verbose_name=_("user"))
    karma = models.IntegerField(_("karma"), default=0)
    school = models.CharField(_("school"), max_length=100, null=False, blank=False)
    
    class Meta:
        verbose_name = _("user-profile")
        verbose_name_plural = _("user-profiles")
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("profile.views.view", kwargs={"username": self.user.username})
    
    @staticmethod
    def create(sender, instance=None, **kwargs):
        if instance is None:
            return
        profile, created = UserProfile.objects.get_or_create(user=instance)
        
    def update(self):
        pass
    
    def delete(self):
        pass
    

post_save.connect(UserProfile.create, sender=User)
