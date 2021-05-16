from django.db import models
from datetime import datetime

class Code(models.Model):
    user_id = models.IntegerField()
    code = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.now())  
    token = models.CharField(max_length=255, blank=True)