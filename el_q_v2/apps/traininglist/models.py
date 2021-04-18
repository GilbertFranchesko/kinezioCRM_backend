from django.db import models

"""
    Модель тренировки
    Из которой будет формироватся список, относительно
    данных которые отдаст медицинская карта.

"""

class Training(models.Model):
    patient = models.IntegerField("Пациент")
    doctor = models.IntegerField("Пациент")
    medrecord = models.IntegerField("Мед. карточка")
    title = models.CharField("Заголовок тренировки", max_length=100)
    descrption = models.TextField("Описание тренировки")
    finish_date = models.DateField("Дата окончание тренировок")


    def __str__(self):
        return self.title
