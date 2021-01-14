from django.urls import re_path, path
from .views import ShowALL, ShowByID, ShowByPatient, ShowByDoctor, ShowByToken
urlpatterns = [
    re_path(r'^showAll/?$', ShowALL.as_view(), name="show"),
    path('showBy/', ShowByID.as_view(), name="show_by_id"),
    path('showByPatient/<int:patient>/', ShowByPatient.as_view(), name="show_by_patient"),
    path('showByDoctor/<int:doctor>/', ShowByDoctor.as_view(), name="show_by_doctor"),
    re_path(r'^showByToken/?$', ShowByToken.as_view(), name="show_by_token")

]