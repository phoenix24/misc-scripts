from datetime import datetime
from django.db import models

from asset.models import GenericAsset
from quizattempt.models import Attempt

class Report(GenericAsset):
    attempt = models.ForeignKey(Attempt)
    
