from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class GenericAsset(models.Model):
    """ this is a generic super-class from which all other assets inherit. """
    
    owner = models.ForeignKey(User)
#    authors = models.
    
    created = models.DateTimeField(_('asset created'), default=datetime.now)
    last_updated = models.DateTimeField(_('last updated'), default=datetime.now)
#    revisions
    
    status = models.CharField(_("status"), max_length=10, default=_("incomplete"))
    
#    importable
#    exportable
#    backups
    def addowner(self):
        pass
    
    def addauthor(self):
        pass
    
    def is_importable(self):
        return False
    
    def is_exportable(self):
        return False
    
    def is_backupable(self):
        return False
    
    def author_list(self):
        return None
    
    def revision_list(self):
        return None
    
    class Meta:
        abstract = True
    