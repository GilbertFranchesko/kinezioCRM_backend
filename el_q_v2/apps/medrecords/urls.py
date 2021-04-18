from django.urls import re_path, path
from .views import ShowALL, ShowByID, ShowByPatient, ShowByDoctor, ShowByToken, UpdateMedRecords, AddMedication, DeleteMedication
urlpatterns = [
    re_path(r'^showAll/?$', ShowALL.as_view(), name="show"),
    path('showBy/', ShowByID.as_view(), name="show_by_id"),
    path('showByPatient/<int:patient>/', ShowByPatient.as_view(), name="show_by_patient"),
    path('showByDoctor/<int:doctor>/', ShowByDoctor.as_view(), name="show_by_doctor"),
    re_path(r'^showByToken/?$', ShowByToken.as_view(), name="show_by_token"),
    path('update/<int:id>/', UpdateMedRecords.as_view(), name="update_medrecord"),

    path('addMedication/', AddMedication.as_view(), name="add_medication"),
    path('deleteMedication/', DeleteMedication.as_view(), name="delete_medication")

]
