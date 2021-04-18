from django.contrib.postgres.fields import ArrayField
from django.db import models
from account.models import User


"""
    Модель медицинской карты
    Она доступна для врача, и только тому пациенту,
    кому она была выписана.
"""

class MedRecord(models.Model):
    patient = models.IntegerField("ID пациента", default=0)
    doctor = models.IntegerField("ID врача", default=0)
    diagnosis = models.CharField("Диагноз", default="Не определён", max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    medications = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    training_list = ArrayField(models.IntegerField(), blank=True)

    # Для того что-бы, если мед. карта была кинута в "архив", понять что она не действительна(=0).
    active_id = models.IntegerField("ID актуального врача", default=1)

    def getPatient(self):
        return User.objects.get(id=self.patient).first_name+" "+User.objects.get(id=self.patient).last_name

    def getDoctor(self):
        return User.objects.get(id=self.doctor).first_name+" "+User.objects.get(id=self.doctor).last_name
