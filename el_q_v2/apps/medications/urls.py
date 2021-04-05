from django.urls import re_path, path
from .views import ShowAll, ShowByMedRecord, DeleteById
urlpatterns = [
    path("showAll/", ShowAll.as_view(), name="show"),
    path("showByMedrecord/", ShowByMedRecord.as_view(), name="show_by_medrecord"),
    path("deleteById/<int:id>", DeleteById.as_view(), name="delete_by_id")
]
