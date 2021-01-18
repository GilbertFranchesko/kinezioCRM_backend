from .models import Record

def check_date():
    all_objects = Record.objects.all()
    print("\n\n","ok ",all_objects.dateEvent,"\n\n")
    return True
