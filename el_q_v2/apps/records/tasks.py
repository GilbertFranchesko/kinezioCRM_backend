# Create your tasks here

from notifications.models import Notification
from celery import shared_task
from .models import Record
from datetime import datetime


@shared_task
def check_date_records():
    
    today_date_str = str(datetime.now().date()) 
    today_objects = Record.objects.filter(dateEvent = today_date_str)

    if len(today_objects) == 0:
        print("[LOG] Today dont have a record, any doctor.")
    else:
        for today_object in today_objects:
            if today_object.patient != 0:
                pass
            else:
                print("[LOG] Patient dont register in system! SMS")
