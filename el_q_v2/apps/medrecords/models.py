from django.db import models
from account.models import User


"""
    Модель медицинской карты
    Она доступна для врача, и только тому пациенту, 
    кому она была выписана.
"""

class MedRecord(models.Model):
    patient = models.IntegerField("ID пациента")
    doctor = models.IntegerField("ID врача")
    diagnosis = models.CharField("Диагноз", default="Не определён", max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    training_list = models.TextField("Списко тренеровок(JSON)")

    def getPatient(self):
        return User.objects.get(id=self.patient)

    def getDoctor(self):
        return User.objects.get(id=self.doctor)