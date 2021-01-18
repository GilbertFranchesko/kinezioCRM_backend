from django.db import models
from account.models import User

class Record(models.Model):
    patientFirstName = models.CharField(max_length=255)
    patientLastName = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    dateEvent = models.DateField()
    timeEvent = models.TimeField()
    doctor = models.IntegerField()
    patient = models.IntegerField(default=0, null=True)
    status = models.CharField(max_length=255, default="в ожидании")

    def getPatient(self):
        return User.objects.get(id=self.patient).first_name+" "+User.objects.get(id=self.patient).last_name

    def getDoctor(self):
        return User.objects.get(id=self.doctor).first_name+" "+User.objects.get(id=self.doctor).last_name
