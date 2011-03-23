from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from talkcode.managers import *
    
    

class CodeOperation(models.Model):
	user = models.ForeignKey(User)
	code = models.CharField("Code Operation", max_length=99999999)
	
	def __unicode__(self):
		return u'%s' % self.code