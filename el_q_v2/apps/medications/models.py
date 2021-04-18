from django.db import models
from account.models import User
from medrecords.models import MedRecord

"""
    Модель мед. препаратов.
    Они будут выписываться врачём и отображаться в мед. карточке пациента.
    И будут содержать описание препарата, его добавлять будет кто-то из персонала.

"""

class Medication(models.Model):
    doctor = models.IntegerField("Доктор добавил", default=0)
    name = models.CharField("Название препарата", max_length=255)
    description = models.TextField("Описание препарата")

    def get_doctor_name(self):
        return User.objects.get(id = self.doctor).first_name + " " + User.objects.get(id = self.doctor).last_name

    def __str__(self):
        return self.name
