from django.db import models
from account.models import User
from medrecords.models import MedRecord

"""
    Модель мед. препаратов.
    Они будут выписываться врачём и отображаться в мед. карточке пациента.
    И будут содержать описание препарата, его добавлять будет кто-то из персонала.

"""

class Medication(models.Model):
    medRecord = models.IntegerField("ID мед.карточки", default=0)
    doctor = models.IntegerField("ID доктора", default=0)
    name = models.CharField("Название препарата", max_length=255)
    description = models.TextField("Описание препарата")
    dose = models.CharField("Дозировка препарата", max_length=255, default="")
    date = models.DateField("Дата его назначения", auto_now_add=True)
    time = models.TimeField("Время его назначения", auto_now_add=True)
    finish_date = models.DateField("Дата окончания приёма", auto_now_add=True)
    photo = models.ImageField(upload_to="static/medications", default="0")


    def med_record_object(self):
        return MedRecord.objects.get(id = self.medRecord)

    def get_doctor_name(self):
        return User.objects.get(id = self.doctor).first_name + " " + User.objects.get(id = self.doctor).last_name
