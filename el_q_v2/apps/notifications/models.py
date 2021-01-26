from django.db import models
from account.models import User

class Notification(models.Model):
    patient = models.IntegerField()
    doctor = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(default="Напоминание", max_length=255)
    date_time = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)


    def getPatient(self):
        return User.objects.get(id=self.patient).first_name+" "+User.objects.get(id=self.patient).last_name

    def getDoctor(self):
        return User.objects.get(id=self.doctor).first_name+" "+User.objects.get(id=self.doctor).last_name
