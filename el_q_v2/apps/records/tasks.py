# Create your tasks here

from notifications.models import Notification
from celery import shared_task
from .models import Record
from datetime import datetime


@shared_task
def check_date():
    objects = Record.objects.all()
    today_day = datetime.now().date()
    print(f"\n\n\n {today_day} \n\n\n")
    for object in objects:
        if(object.dateEvent == today_day):
            object.status = "сегодня"
            object.save()
            content_txt = "Ваша запись #%i на сегодня!\n Успейте во время в %s" % (object.id, str(object.timeEvent))
            print(f'{Notification.objects.filter(patient=object.patient, type="Напоминание")}')
            if not len(Notification.objects.filter(patient=object.patient, type="Напоминание")) == 0:
                print(f'User {object.patient} was notificated about record.')
            else:
                """ ID: 1 IS ADMIN OR CHANGE IT!"""
                print(f"Send notify about record ID: {object.id} ")
                create_object = Notification(patient=object.patient, doctor=object.doctor, title="Ваша запись сегодня", content=content_txt)
                create_object.save()


