from django.urls import path
from .views import CreateCode, SelectCode

urlpatterns = [
    path("create/", CreateCode.as_view(), name="create_code"),
    path("select/", SelectCode.as_view(), name="select_code")
]